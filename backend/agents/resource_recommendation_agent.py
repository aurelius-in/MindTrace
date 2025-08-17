"""
Resource Recommendation Agent - Matches employee needs to wellness resources
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging
from dataclasses import dataclass

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from .base_agent import BaseAgent, AgentType, AgentContext, AgentResponse
from config.settings import settings


@dataclass
class WellnessResource:
    """Wellness resource data structure"""
    id: str
    title: str
    description: str
    category: str
    resource_type: str  # article, video, exercise, contact, program
    url: Optional[str] = None
    tags: List[str] = None
    target_audience: List[str] = None
    difficulty_level: str = "beginner"  # beginner, intermediate, advanced
    duration_minutes: Optional[int] = None
    cost: str = "free"  # free, low_cost, premium


class ResourceRecommendationAgent(BaseAgent):
    """
    Resource Recommendation Agent matches employee needs to appropriate
    wellness resources, EAP programs, and support materials.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.RESOURCE_RECOMMENDATION, config)
        
        # Resource categories and their descriptions
        self.resource_categories = {
            "stress_management": "Resources for managing work stress and pressure",
            "mental_health": "Mental health support and professional resources",
            "work_life_balance": "Tips and tools for maintaining work-life balance",
            "physical_wellness": "Physical health and exercise resources",
            "social_connection": "Building relationships and team connections",
            "financial_wellness": "Financial planning and stress management",
            "crisis_support": "Immediate support for crisis situations",
            "leadership_development": "Resources for managers and leaders"
        }
    
    def _initialize_agent(self):
        """Initialize the resource recommendation agent"""
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=settings.agents.resource_embedding_model,
            openai_api_key=settings.ai.openai_api_key
        )
        
        # Initialize vector database
        self._initialize_vector_db()
        
        # Load wellness resources
        self._load_wellness_resources()
        
        # Initialize recommendation engine
        self._initialize_recommendation_engine()
    
    def _initialize_vector_db(self):
        """Initialize ChromaDB vector database"""
        try:
            self.chroma_client = chromadb.PersistentClient(
                path="./data/chromadb",
                settings=ChromaSettings(
                    anonymized_telemetry=False
                )
            )
            
            # Create or get collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="wellness_resources",
                metadata={"hnsw:space": "cosine"}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB: {e}")
            # Fallback to in-memory storage
            self.collection = None
    
    def _load_wellness_resources(self):
        """Load wellness resources into the system"""
        self.resources = [
            WellnessResource(
                id="stress-breathing",
                title="5-Minute Breathing Exercise",
                description="A simple breathing technique to reduce stress and anxiety",
                category="stress_management",
                resource_type="exercise",
                duration_minutes=5,
                tags=["breathing", "stress", "quick", "meditation"],
                target_audience=["all_employees"]
            ),
            WellnessResource(
                id="eap-contact",
                title="Employee Assistance Program",
                description="Professional counseling and support services",
                category="mental_health",
                resource_type="contact",
                tags=["counseling", "professional", "confidential"],
                target_audience=["all_employees"]
            ),
            WellnessResource(
                id="work-life-tips",
                title="Work-Life Balance Guide",
                description="Practical tips for maintaining work-life balance",
                category="work_life_balance",
                resource_type="article",
                tags=["balance", "productivity", "wellness"],
                target_audience=["all_employees"]
            ),
            WellnessResource(
                id="crisis-hotline",
                title="Crisis Support Hotline",
                description="24/7 crisis intervention and support",
                category="crisis_support",
                resource_type="contact",
                tags=["crisis", "emergency", "support"],
                target_audience=["all_employees"]
            ),
            WellnessResource(
                id="manager-wellness",
                title="Manager Wellness Toolkit",
                description="Resources for supporting team wellness",
                category="leadership_development",
                resource_type="program",
                tags=["leadership", "management", "team"],
                target_audience=["managers", "leaders"]
            ),
            WellnessResource(
                id="mindfulness-app",
                title="Mindfulness Meditation App",
                description="Guided meditation sessions for stress relief",
                category="stress_management",
                resource_type="program",
                duration_minutes=10,
                tags=["meditation", "mindfulness", "app"],
                target_audience=["all_employees"]
            ),
            WellnessResource(
                id="financial-planning",
                title="Financial Wellness Workshop",
                description="Workshop on financial planning and stress management",
                category="financial_wellness",
                resource_type="program",
                duration_minutes=60,
                tags=["financial", "planning", "workshop"],
                target_audience=["all_employees"]
            ),
            WellnessResource(
                id="team-building",
                title="Team Connection Activities",
                description="Activities to build stronger team relationships",
                category="social_connection",
                resource_type="program",
                tags=["team", "connection", "social"],
                target_audience=["all_employees"]
            )
        ]
        
        # Index resources in vector database
        self._index_resources()
    
    def _index_resources(self):
        """Index wellness resources in the vector database"""
        if not self.collection:
            return
        
        try:
            # Prepare documents for indexing
            documents = []
            metadatas = []
            ids = []
            
            for resource in self.resources:
                # Create document text
                doc_text = f"{resource.title} {resource.description} {' '.join(resource.tags or [])}"
                
                documents.append(doc_text)
                metadatas.append({
                    "id": resource.id,
                    "category": resource.category,
                    "resource_type": resource.resource_type,
                    "difficulty_level": resource.difficulty_level,
                    "duration_minutes": resource.duration_minutes,
                    "cost": resource.cost,
                    "target_audience": ",".join(resource.target_audience or [])
                })
                ids.append(resource.id)
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Indexed {len(self.resources)} wellness resources")
            
        except Exception as e:
            self.logger.error(f"Failed to index resources: {e}")
    
    def _initialize_recommendation_engine(self):
        """Initialize the recommendation engine"""
        # Recommendation strategies
        self.recommendation_strategies = {
            "content_based": self._content_based_recommendation,
            "collaborative": self._collaborative_recommendation,
            "hybrid": self._hybrid_recommendation
        }
    
    async def process_request(self, context: AgentContext, data: Dict[str, Any]) -> AgentResponse:
        """Process a resource recommendation request"""
        
        user_needs = data.get("needs", "")
        user_preferences = data.get("preferences", {})
        risk_level = data.get("risk_level", 0.0)
        user_role = data.get("user_role", "employee")
        
        # Determine recommendation strategy
        strategy = self._select_recommendation_strategy(user_needs, risk_level)
        
        # Get recommendations
        recommendations = await self._get_recommendations(
            user_needs, user_preferences, risk_level, user_role, strategy
        )
        
        # Filter and rank recommendations
        filtered_recommendations = self._filter_recommendations(
            recommendations, user_preferences, user_role
        )
        
        response_data = {
            "recommendations": filtered_recommendations,
            "strategy_used": strategy,
            "total_found": len(filtered_recommendations),
            "categories": self._get_recommendation_categories(filtered_recommendations)
        }
        
        return AgentResponse(
            success=True,
            data=response_data,
            message="Resource recommendations generated successfully",
            risk_level=risk_level
        )
    
    def _select_recommendation_strategy(self, user_needs: str, risk_level: float) -> str:
        """Select the best recommendation strategy based on user needs and risk level"""
        if risk_level > 0.7:
            return "content_based"  # Direct matching for high-risk situations
        elif "stress" in user_needs.lower() or "anxiety" in user_needs.lower():
            return "content_based"
        else:
            return "hybrid"
    
    async def _get_recommendations(
        self, 
        user_needs: str, 
        user_preferences: Dict[str, Any], 
        risk_level: float, 
        user_role: str,
        strategy: str
    ) -> List[Dict[str, Any]]:
        """Get resource recommendations using the specified strategy"""
        
        if strategy == "content_based":
            return await self._content_based_recommendation(user_needs, user_preferences)
        elif strategy == "collaborative":
            return await self._collaborative_recommendation(user_needs, user_role)
        else:
            return await self._hybrid_recommendation(user_needs, user_preferences, user_role)
    
    async def _content_based_recommendation(
        self, 
        user_needs: str, 
        user_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Content-based recommendation using vector similarity"""
        
        if not self.collection:
            return self._fallback_recommendations(user_needs)
        
        try:
            # Query vector database
            results = self.collection.query(
                query_texts=[user_needs],
                n_results=10
            )
            
            recommendations = []
            for i, doc_id in enumerate(results['ids'][0]):
                resource = self._get_resource_by_id(doc_id)
                if resource:
                    recommendations.append({
                        "resource": resource,
                        "similarity_score": results['distances'][0][i],
                        "reason": f"Matches your needs: {user_needs}"
                    })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Content-based recommendation failed: {e}")
            return self._fallback_recommendations(user_needs)
    
    async def _collaborative_recommendation(
        self, 
        user_needs: str, 
        user_role: str
    ) -> List[Dict[str, Any]]:
        """Collaborative recommendation based on similar users"""
        # TODO: Implement collaborative filtering
        # This would require user interaction data and similarity calculations
        
        # For now, return role-based recommendations
        role_based_resources = [
            resource for resource in self.resources
            if user_role in (resource.target_audience or []) or "all_employees" in (resource.target_audience or [])
        ]
        
        return [
            {
                "resource": resource,
                "similarity_score": 0.8,
                "reason": f"Recommended for {user_role}s"
            }
            for resource in role_based_resources[:5]
        ]
    
    async def _hybrid_recommendation(
        self, 
        user_needs: str, 
        user_preferences: Dict[str, Any], 
        user_role: str
    ) -> List[Dict[str, Any]]:
        """Hybrid recommendation combining multiple strategies"""
        
        # Get content-based recommendations
        content_recs = await self._content_based_recommendation(user_needs, user_preferences)
        
        # Get collaborative recommendations
        collab_recs = await self._collaborative_recommendation(user_needs, user_role)
        
        # Combine and rank
        all_recs = content_recs + collab_recs
        
        # Remove duplicates and re-rank
        unique_recs = {}
        for rec in all_recs:
            resource_id = rec["resource"].id
            if resource_id not in unique_recs or rec["similarity_score"] > unique_recs[resource_id]["similarity_score"]:
                unique_recs[resource_id] = rec
        
        return sorted(
            list(unique_recs.values()),
            key=lambda x: x["similarity_score"],
            reverse=True
        )[:10]
    
    def _filter_recommendations(
        self, 
        recommendations: List[Dict[str, Any]], 
        user_preferences: Dict[str, Any], 
        user_role: str
    ) -> List[Dict[str, Any]]:
        """Filter recommendations based on user preferences and role"""
        
        filtered = []
        
        for rec in recommendations:
            resource = rec["resource"]
            
            # Check role compatibility
            if user_role not in (resource.target_audience or []) and "all_employees" not in (resource.target_audience or []):
                continue
            
            # Check duration preference
            if "max_duration" in user_preferences and resource.duration_minutes:
                if resource.duration_minutes > user_preferences["max_duration"]:
                    continue
            
            # Check cost preference
            if "max_cost" in user_preferences:
                if user_preferences["max_cost"] == "free" and resource.cost != "free":
                    continue
            
            filtered.append(rec)
        
        return filtered
    
    def _get_recommendation_categories(self, recommendations: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get category distribution of recommendations"""
        categories = {}
        for rec in recommendations:
            category = rec["resource"].category
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _get_resource_by_id(self, resource_id: str) -> Optional[WellnessResource]:
        """Get resource by ID"""
        for resource in self.resources:
            if resource.id == resource_id:
                return resource
        return None
    
    def _fallback_recommendations(self, user_needs: str) -> List[Dict[str, Any]]:
        """Fallback recommendations when vector search fails"""
        # Return general wellness resources
        general_resources = [
            resource for resource in self.resources
            if resource.category in ["stress_management", "mental_health"]
        ]
        
        return [
            {
                "resource": resource,
                "similarity_score": 0.5,
                "reason": "General wellness recommendation"
            }
            for resource in general_resources[:5]
        ]
    
    async def get_resource_details(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific resource"""
        resource = self._get_resource_by_id(resource_id)
        if not resource:
            return None
        
        return {
            "id": resource.id,
            "title": resource.title,
            "description": resource.description,
            "category": resource.category,
            "resource_type": resource.resource_type,
            "url": resource.url,
            "tags": resource.tags,
            "target_audience": resource.target_audience,
            "difficulty_level": resource.difficulty_level,
            "duration_minutes": resource.duration_minutes,
            "cost": resource.cost,
            "related_resources": self._get_related_resources(resource)
        }
    
    def _get_related_resources(self, resource: WellnessResource) -> List[Dict[str, Any]]:
        """Get related resources based on category and tags"""
        related = []
        
        for other_resource in self.resources:
            if other_resource.id == resource.id:
                continue
            
            # Check category match
            if other_resource.category == resource.category:
                related.append({
                    "id": other_resource.id,
                    "title": other_resource.title,
                    "category": other_resource.category,
                    "similarity": "category_match"
                })
                continue
            
            # Check tag overlap
            if resource.tags and other_resource.tags:
                overlap = set(resource.tags) & set(other_resource.tags)
                if len(overlap) > 0:
                    related.append({
                        "id": other_resource.id,
                        "title": other_resource.title,
                        "category": other_resource.category,
                        "similarity": f"tag_overlap: {', '.join(overlap)}"
                    })
        
        return related[:3]  # Limit to 3 related resources
