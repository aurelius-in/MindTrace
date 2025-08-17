"""
Sentiment & Risk Detection Agent - Analyzes text for burnout risk and stress patterns
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import logging
import re
from dataclasses import dataclass

import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from .base_agent import BaseAgent, AgentType, AgentContext, AgentResponse
from config.settings import settings


@dataclass
class RiskIndicator:
    """Risk indicator data structure"""
    type: str  # burnout, stress_spike, toxic_pattern, crisis
    confidence: float
    severity: str  # low, medium, high, critical
    keywords: List[str]
    context: str
    timestamp: datetime


@dataclass
class SentimentAnalysis:
    """Sentiment analysis results"""
    compound_score: float
    positive_score: float
    negative_score: float
    neutral_score: float
    subjectivity: float
    emotion_labels: List[str]
    risk_factors: List[str]


class SentimentRiskDetectionAgent(BaseAgent):
    """
    Sentiment & Risk Detection Agent analyzes text for:
    - Burnout indicators
    - Stress patterns
    - Toxic workplace patterns
    - Crisis situations
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.SENTIMENT_RISK_DETECTION, config)
        
        # Initialize sentiment analyzers
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Risk detection patterns
        self._load_risk_patterns()
        
        # Historical data for trend analysis
        self.sentiment_history = {}
        self.risk_history = {}
    
    def _initialize_agent(self):
        """Initialize the sentiment and risk detection agent"""
        # Initialize anomaly detection
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        
        # Initialize scaler for normalization
        self.scaler = StandardScaler()
        
        # Load risk detection models
        self._load_risk_models()
    
    def _load_risk_patterns(self):
        """Load risk detection patterns and keywords"""
        self.risk_patterns = {
            "burnout": {
                "keywords": [
                    "exhausted", "burned out", "overwhelmed", "can't take it anymore",
                    "breaking point", "no energy", "mentally drained", "physically tired",
                    "work-life imbalance", "always working", "no time for myself"
                ],
                "phrases": [
                    "I'm so tired of", "I can't keep up", "I'm at my limit",
                    "work is consuming me", "I have no life outside work"
                ],
                "threshold": 0.6
            },
            "stress_spike": {
                "keywords": [
                    "stressed", "anxious", "worried", "panicked", "overwhelmed",
                    "pressure", "deadline", "urgent", "crisis", "emergency"
                ],
                "phrases": [
                    "I'm so stressed", "I can't handle this", "too much pressure",
                    "everything is urgent", "I'm losing it"
                ],
                "threshold": 0.7
            },
            "toxic_pattern": {
                "keywords": [
                    "toxic", "hostile", "bullying", "harassment", "discrimination",
                    "unfair", "favoritism", "gossip", "backstabbing", "micromanagement"
                ],
                "phrases": [
                    "toxic environment", "hostile workplace", "being bullied",
                    "unfair treatment", "favoritism", "micromanaged"
                ],
                "threshold": 0.8
            },
            "crisis": {
                "keywords": [
                    "suicide", "kill myself", "end it all", "no reason to live",
                    "self-harm", "hurt myself", "want to die", "better off dead",
                    "can't go on", "life is meaningless"
                ],
                "phrases": [
                    "I want to end my life", "I can't take it anymore",
                    "I'm thinking of hurting myself", "life isn't worth living"
                ],
                "threshold": 0.9
            }
        }
    
    def _load_risk_models(self):
        """Load machine learning models for risk detection"""
        # TODO: Load pre-trained models for specific risk detection
        # This could include:
        # - Burnout prediction models
        # - Stress pattern recognition
        # - Toxic behavior detection
        pass
    
    async def process_request(self, context: AgentContext, data: Dict[str, Any]) -> AgentResponse:
        """Process text for sentiment analysis and risk detection"""
        
        text_content = data.get("text", "")
        text_type = data.get("type", "conversation")  # conversation, journal, feedback
        user_id = context.user_id
        
        # Perform sentiment analysis
        sentiment_result = self._analyze_sentiment(text_content)
        
        # Detect risk indicators
        risk_indicators = self._detect_risk_indicators(text_content, sentiment_result)
        
        # Analyze trends
        trend_analysis = self._analyze_trends(user_id, sentiment_result, risk_indicators)
        
        # Calculate overall risk level
        overall_risk = self._calculate_overall_risk(risk_indicators, trend_analysis)
        
        # Update historical data
        self._update_history(user_id, sentiment_result, risk_indicators)
        
        response_data = {
            "sentiment": {
                "compound_score": sentiment_result.compound_score,
                "positive_score": sentiment_result.positive_score,
                "negative_score": sentiment_result.negative_score,
                "neutral_score": sentiment_result.neutral_score,
                "subjectivity": sentiment_result.subjectivity,
                "emotion_labels": sentiment_result.emotion_labels
            },
            "risk_indicators": [
                {
                    "type": indicator.type,
                    "confidence": indicator.confidence,
                    "severity": indicator.severity,
                    "keywords": indicator.keywords,
                    "context": indicator.context
                }
                for indicator in risk_indicators
            ],
            "trend_analysis": trend_analysis,
            "overall_risk_level": overall_risk,
            "recommendations": self._generate_risk_recommendations(risk_indicators, overall_risk)
        }
        
        return AgentResponse(
            success=True,
            data=response_data,
            message="Sentiment and risk analysis completed",
            risk_level=overall_risk,
            requires_escalation=overall_risk > 0.8
        )
    
    def _analyze_sentiment(self, text: str) -> SentimentAnalysis:
        """Perform comprehensive sentiment analysis"""
        
        # VADER sentiment analysis
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # TextBlob sentiment analysis
        blob = TextBlob(text)
        subjectivity = blob.sentiment.subjectivity
        
        # Emotion detection (simplified)
        emotion_labels = self._detect_emotions(text)
        
        # Risk factors
        risk_factors = self._identify_risk_factors(text)
        
        return SentimentAnalysis(
            compound_score=vader_scores['compound'],
            positive_score=vader_scores['pos'],
            negative_score=vader_scores['neg'],
            neutral_score=vader_scores['neu'],
            subjectivity=subjectivity,
            emotion_labels=emotion_labels,
            risk_factors=risk_factors
        )
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Detect emotions in text"""
        emotions = []
        text_lower = text.lower()
        
        # Simple emotion keyword matching
        emotion_keywords = {
            "anger": ["angry", "furious", "mad", "irritated", "frustrated"],
            "sadness": ["sad", "depressed", "melancholy", "gloomy", "hopeless"],
            "fear": ["afraid", "scared", "terrified", "anxious", "worried"],
            "joy": ["happy", "excited", "thrilled", "elated", "content"],
            "surprise": ["surprised", "shocked", "amazed", "astonished"],
            "disgust": ["disgusted", "repulsed", "appalled", "revolted"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                emotions.append(emotion)
        
        return emotions
    
    def _identify_risk_factors(self, text: str) -> List[str]:
        """Identify risk factors in text"""
        risk_factors = []
        text_lower = text.lower()
        
        # Check for various risk factors
        if any(word in text_lower for word in ["work", "job", "career"]):
            risk_factors.append("work_related")
        
        if any(word in text_lower for word in ["relationship", "colleague", "boss", "team"]):
            risk_factors.append("interpersonal")
        
        if any(word in text_lower for word in ["health", "physical", "mental"]):
            risk_factors.append("health_related")
        
        if any(word in text_lower for word in ["money", "financial", "salary", "debt"]):
            risk_factors.append("financial")
        
        return risk_factors
    
    def _detect_risk_indicators(self, text: str, sentiment: SentimentAnalysis) -> List[RiskIndicator]:
        """Detect specific risk indicators in text"""
        indicators = []
        text_lower = text.lower()
        
        for risk_type, pattern in self.risk_patterns.items():
            # Check keywords
            found_keywords = [
                keyword for keyword in pattern["keywords"]
                if keyword in text_lower
            ]
            
            # Check phrases
            found_phrases = [
                phrase for phrase in pattern["phrases"]
                if phrase in text_lower
            ]
            
            if found_keywords or found_phrases:
                # Calculate confidence based on matches and sentiment
                keyword_confidence = len(found_keywords) / len(pattern["keywords"])
                phrase_confidence = len(found_phrases) / len(pattern["phrases"])
                sentiment_factor = abs(sentiment.compound_score) if sentiment.compound_score < 0 else 0
                
                confidence = (keyword_confidence * 0.4 + phrase_confidence * 0.6 + sentiment_factor * 0.3) / 1.3
                
                if confidence >= pattern["threshold"]:
                    # Determine severity
                    severity = self._determine_severity(confidence, risk_type)
                    
                    indicators.append(RiskIndicator(
                        type=risk_type,
                        confidence=confidence,
                        severity=severity,
                        keywords=found_keywords + found_phrases,
                        context=self._extract_context(text, found_keywords + found_phrases),
                        timestamp=datetime.now()
                    ))
        
        return indicators
    
    def _determine_severity(self, confidence: float, risk_type: str) -> str:
        """Determine severity level based on confidence and risk type"""
        if risk_type == "crisis":
            if confidence > 0.9:
                return "critical"
            elif confidence > 0.7:
                return "high"
            else:
                return "medium"
        else:
            if confidence > 0.8:
                return "high"
            elif confidence > 0.6:
                return "medium"
            else:
                return "low"
    
    def _extract_context(self, text: str, keywords: List[str]) -> str:
        """Extract context around detected keywords"""
        if not keywords:
            return ""
        
        # Find the first keyword and extract surrounding context
        for keyword in keywords:
            if keyword in text.lower():
                start = max(0, text.lower().find(keyword) - 50)
                end = min(len(text), text.lower().find(keyword) + len(keyword) + 50)
                return text[start:end].strip()
        
        return ""
    
    def _analyze_trends(self, user_id: str, sentiment: SentimentAnalysis, indicators: List[RiskIndicator]) -> Dict[str, Any]:
        """Analyze trends in user's sentiment and risk patterns"""
        
        if user_id not in self.sentiment_history:
            return {"trend": "insufficient_data", "change_rate": 0.0}
        
        history = self.sentiment_history[user_id]
        
        if len(history) < 3:
            return {"trend": "insufficient_data", "change_rate": 0.0}
        
        # Calculate trend in sentiment scores
        recent_scores = [entry["compound_score"] for entry in history[-5:]]
        trend_slope = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
        
        # Determine trend direction
        if trend_slope > 0.05:
            trend = "improving"
        elif trend_slope < -0.05:
            trend = "declining"
        else:
            trend = "stable"
        
        # Calculate change rate
        if len(recent_scores) >= 2:
            change_rate = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
        else:
            change_rate = 0.0
        
        return {
            "trend": trend,
            "change_rate": change_rate,
            "data_points": len(history),
            "volatility": np.std(recent_scores)
        }
    
    def _calculate_overall_risk(self, indicators: List[RiskIndicator], trends: Dict[str, Any]) -> float:
        """Calculate overall risk level"""
        
        if not indicators:
            return 0.0
        
        # Base risk from indicators
        max_confidence = max(ind.confidence for ind in indicators)
        
        # Severity multiplier
        severity_multipliers = {"low": 1.0, "medium": 1.5, "high": 2.0, "critical": 3.0}
        severity_multiplier = max(
            severity_multipliers.get(ind.severity, 1.0) for ind in indicators
        )
        
        # Trend adjustment
        trend_adjustment = 0.0
        if trends.get("trend") == "declining":
            trend_adjustment = 0.2
        elif trends.get("trend") == "improving":
            trend_adjustment = -0.1
        
        # Calculate overall risk
        overall_risk = max_confidence * severity_multiplier + trend_adjustment
        
        return min(overall_risk, 1.0)
    
    def _update_history(self, user_id: str, sentiment: SentimentAnalysis, indicators: List[RiskIndicator]):
        """Update historical data for trend analysis"""
        
        if user_id not in self.sentiment_history:
            self.sentiment_history[user_id] = []
        
        # Add sentiment data
        self.sentiment_history[user_id].append({
            "timestamp": datetime.now(),
            "compound_score": sentiment.compound_score,
            "positive_score": sentiment.positive_score,
            "negative_score": sentiment.negative_score,
            "neutral_score": sentiment.neutral_score,
            "subjectivity": sentiment.subjectivity
        })
        
        # Keep only last 30 entries
        if len(self.sentiment_history[user_id]) > 30:
            self.sentiment_history[user_id] = self.sentiment_history[user_id][-30:]
        
        # Update risk history
        if user_id not in self.risk_history:
            self.risk_history[user_id] = []
        
        for indicator in indicators:
            self.risk_history[user_id].append({
                "timestamp": indicator.timestamp,
                "type": indicator.type,
                "confidence": indicator.confidence,
                "severity": indicator.severity
            })
        
        # Keep only last 50 risk entries
        if len(self.risk_history[user_id]) > 50:
            self.risk_history[user_id] = self.risk_history[user_id][-50:]
    
    def _generate_risk_recommendations(self, indicators: List[RiskIndicator], overall_risk: float) -> List[str]:
        """Generate recommendations based on detected risks"""
        recommendations = []
        
        if overall_risk > 0.8:
            recommendations.append("Immediate intervention recommended - consider escalating to HR or EAP")
        
        for indicator in indicators:
            if indicator.type == "burnout":
                recommendations.append("Consider taking time off and setting work boundaries")
            elif indicator.type == "stress_spike":
                recommendations.append("Try stress management techniques like deep breathing or meditation")
            elif indicator.type == "toxic_pattern":
                recommendations.append("Document incidents and consider speaking with HR about workplace concerns")
            elif indicator.type == "crisis":
                recommendations.append("CRITICAL: Contact crisis support immediately")
        
        return recommendations[:3]  # Limit to 3 recommendations
    
    async def analyze_batch(self, texts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze a batch of texts for sentiment and risk"""
        results = []
        
        for text_data in texts:
            context = AgentContext(
                user_id=text_data.get("user_id", "anonymous"),
                session_id=text_data.get("session_id", "batch"),
                timestamp=datetime.now(),
                metadata={"batch_analysis": True}
            )
            
            result = await self.process_request(context, text_data)
            results.append(result.data)
        
        return results
    
    def get_user_risk_profile(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive risk profile for a user"""
        
        if user_id not in self.sentiment_history:
            return {"error": "No data available for user"}
        
        sentiment_data = self.sentiment_history[user_id]
        risk_data = self.risk_history.get(user_id, [])
        
        # Calculate statistics
        avg_sentiment = np.mean([entry["compound_score"] for entry in sentiment_data])
        sentiment_volatility = np.std([entry["compound_score"] for entry in sentiment_data])
        
        # Risk frequency
        risk_counts = {}
        for entry in risk_data:
            risk_type = entry["type"]
            risk_counts[risk_type] = risk_counts.get(risk_type, 0) + 1
        
        return {
            "user_id": user_id,
            "data_points": len(sentiment_data),
            "average_sentiment": avg_sentiment,
            "sentiment_volatility": sentiment_volatility,
            "risk_frequency": risk_counts,
            "highest_risk_type": max(risk_counts.items(), key=lambda x: x[1])[0] if risk_counts else None,
            "last_analysis": sentiment_data[-1]["timestamp"] if sentiment_data else None
        }
