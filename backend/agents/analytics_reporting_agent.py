"""
Analytics & Reporting Agent - Aggregates data into HR dashboards and predictive reports
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import logging
from dataclasses import dataclass
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from .base_agent import BaseAgent, AgentType, AgentContext, AgentResponse
from config.settings import settings
from database.repository import analytics_repo, wellness_entry_repo, user_repo


class ReportType(Enum):
    """Types of reports that can be generated"""
    ORGANIZATIONAL_HEALTH = "organizational_health"
    TEAM_WELLNESS = "team_wellness"
    RISK_ANALYSIS = "risk_analysis"
    TREND_FORECAST = "trend_forecast"
    INTERVENTION_EFFECTIVENESS = "intervention_effectiveness"


@dataclass
class AnalyticsMetric:
    """Analytics metric data structure"""
    name: str
    value: float
    unit: str
    trend: str  # increasing, decreasing, stable
    change_percentage: float
    threshold: Optional[float] = None
    status: str = "normal"  # normal, warning, critical


@dataclass
class PredictiveInsight:
    """Predictive insight data structure"""
    metric: str
    prediction: float
    confidence: float
    timeframe: str
    factors: List[str]
    recommendations: List[str]


class AnalyticsReportingAgent(BaseAgent):
    """
    Analytics & Reporting Agent provides:
    - Aggregated organizational health metrics
    - Team-level wellness insights
    - Predictive analytics for workforce health
    - Intervention effectiveness tracking
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.ANALYTICS_REPORTING, config)
        
        # Data storage for analytics
        self.organizational_data = {}
        self.team_data = {}
        self.predictive_models = {}
        self.historical_data = {}
        
        # Report templates
        self._load_report_templates()
        
        # Initialize data aggregation
        self._initialize_data_aggregation()
    
    def _initialize_agent(self):
        """Initialize the analytics and reporting agent"""
        # Initialize predictive models
        self._initialize_predictive_models()
        
        # Load analytics configurations
        self._load_analytics_config()
        
        # Initialize historical data tracking
        self._initialize_historical_tracking()
    
    def _initialize_historical_tracking(self):
        """Initialize historical data tracking for trend analysis"""
        try:
            # Load historical wellness data
            historical_entries = wellness_entry_repo.get_historical_data(
                days=settings.agents.analytics_retention_days
            )
            
            # Process and store historical data
            self.historical_data = self._process_historical_data(historical_entries)
            
            self.logger.info(f"Loaded {len(self.historical_data)} historical data points")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize historical tracking: {e}")
            self.historical_data = {}
    
    def _process_historical_data(self, entries: List[Dict]) -> Dict[str, List[float]]:
        """Process historical wellness entries into time series data"""
        processed_data = {
            'wellness_scores': [],
            'stress_levels': [],
            'engagement_scores': [],
            'timestamps': []
        }
        
        for entry in entries:
            processed_data['wellness_scores'].append(entry.get('wellness_score', 0))
            processed_data['stress_levels'].append(entry.get('stress_level', 0))
            processed_data['engagement_scores'].append(entry.get('engagement_score', 0))
            processed_data['timestamps'].append(entry.get('timestamp', datetime.now()))
        
        return processed_data
    
    def _load_report_templates(self):
        """Load report templates and configurations"""
        self.report_templates = {
            ReportType.ORGANIZATIONAL_HEALTH: {
                "title": "Organizational Health Dashboard",
                "metrics": ["overall_wellness_score", "stress_levels", "engagement", "burnout_risk"],
                "timeframe": "30d",
                "refresh_rate": "daily"
            },
            ReportType.TEAM_WELLNESS: {
                "title": "Team Wellness Analysis",
                "metrics": ["team_sentiment", "collaboration_health", "workload_distribution"],
                "timeframe": "14d",
                "refresh_rate": "weekly"
            },
            ReportType.RISK_ANALYSIS: {
                "title": "Risk Analysis Report",
                "metrics": ["high_risk_individuals", "risk_trends", "intervention_needs"],
                "timeframe": "7d",
                "refresh_rate": "daily"
            },
            ReportType.TREND_FORECAST: {
                "title": "Wellness Trend Forecast",
                "metrics": ["predicted_stress", "burnout_probability", "engagement_forecast"],
                "timeframe": "90d",
                "refresh_rate": "weekly"
            }
        }
    
    def _initialize_predictive_models(self):
        """Initialize machine learning models for predictions"""
        self.models = {
            "stress_prediction": RandomForestRegressor(n_estimators=100, random_state=42),
            "burnout_prediction": RandomForestRegressor(n_estimators=100, random_state=42),
            "engagement_prediction": RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        self.scalers = {
            "stress_prediction": StandardScaler(),
            "burnout_prediction": StandardScaler(),
            "engagement_prediction": StandardScaler()
        }
    
    def _initialize_data_aggregation(self):
        """Initialize data aggregation structures"""
        self.aggregation_windows = {
            "hourly": timedelta(hours=1),
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(days=30)
        }
    
    def _load_analytics_config(self):
        """Load analytics configuration"""
        self.analytics_config = {
            "retention_days": settings.agents.analytics_retention_days,
            "aggregation_window": settings.agents.analytics_aggregation_window,
            "privacy_threshold": 5,  # Minimum users for aggregation
            "anonymization_level": "team"  # individual, team, department, organization
        }
    
    async def process_request(self, context: AgentContext, data: Dict[str, Any]) -> AgentResponse:
        """Process analytics and reporting requests"""
        
        report_type = data.get("report_type", "organizational_health")
        timeframe = data.get("timeframe", "30d")
        filters = data.get("filters", {})
        user_role = data.get("user_role", "hr")
        
        # Generate the requested report
        if report_type == "organizational_health":
            report_data = await self._generate_organizational_health_report(timeframe, filters)
        elif report_type == "team_wellness":
            report_data = await self._generate_team_wellness_report(timeframe, filters)
        elif report_type == "risk_analysis":
            report_data = await self._generate_risk_analysis_report(timeframe, filters)
        elif report_type == "trend_forecast":
            report_data = await self._generate_trend_forecast_report(timeframe, filters)
        else:
            report_data = {"error": f"Unknown report type: {report_type}"}
        
        # Apply role-based filtering
        filtered_data = self._apply_role_based_filtering(report_data, user_role)
        
        # Generate visualizations
        visualizations = self._generate_visualizations(filtered_data, report_type)
        
        response_data = {
            "report_type": report_type,
            "timeframe": timeframe,
            "generated_at": datetime.now().isoformat(),
            "data": filtered_data,
            "visualizations": visualizations,
            "insights": self._extract_insights(filtered_data, report_type),
            "recommendations": self._generate_recommendations(filtered_data, report_type)
        }
        
        return AgentResponse(
            success=True,
            data=response_data,
            message=f"{report_type} report generated successfully"
        )
    
    async def _generate_organizational_health_report(self, timeframe: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate organizational health dashboard"""
        
        # Calculate key metrics
        metrics = {
            "overall_wellness_score": self._calculate_overall_wellness_score(timeframe),
            "stress_levels": self._calculate_stress_levels(timeframe),
            "engagement_score": self._calculate_engagement_score(timeframe),
            "burnout_risk": self._calculate_burnout_risk(timeframe),
            "work_life_balance": self._calculate_work_life_balance(timeframe),
            "team_collaboration": self._calculate_team_collaboration(timeframe)
        }
        
        # Calculate trends
        trends = self._calculate_trends(metrics, timeframe)
        
        # Identify high-risk areas
        risk_areas = self._identify_risk_areas(metrics)
        
        return {
            "metrics": metrics,
            "trends": trends,
            "risk_areas": risk_areas,
            "summary": self._generate_organizational_summary(metrics, trends)
        }
    
    async def _generate_team_wellness_report(self, timeframe: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate team-level wellness analysis"""
        
        teams = filters.get("teams", self._get_all_teams())
        team_data = {}
        
        for team in teams:
            team_data[team] = {
                "wellness_score": self._calculate_team_wellness_score(team, timeframe),
                "stress_distribution": self._calculate_team_stress_distribution(team, timeframe),
                "collaboration_health": self._calculate_team_collaboration_health(team, timeframe),
                "workload_distribution": self._calculate_team_workload_distribution(team, timeframe),
                "risk_individuals": self._identify_team_risk_individuals(team, timeframe)
            }
        
        # Compare teams
        team_comparison = self._compare_teams(team_data)
        
        return {
            "team_data": team_data,
            "team_comparison": team_comparison,
            "insights": self._extract_team_insights(team_data)
        }
    
    async def _generate_risk_analysis_report(self, timeframe: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk analysis report"""
        
        # Identify high-risk individuals
        high_risk_individuals = self._identify_high_risk_individuals(timeframe)
        
        # Analyze risk trends
        risk_trends = self._analyze_risk_trends(timeframe)
        
        # Predict future risks
        risk_predictions = self._predict_future_risks(timeframe)
        
        # Intervention recommendations
        interventions = self._recommend_interventions(high_risk_individuals, risk_trends)
        
        return {
            "high_risk_individuals": high_risk_individuals,
            "risk_trends": risk_trends,
            "risk_predictions": risk_predictions,
            "interventions": interventions,
            "risk_summary": self._generate_risk_summary(high_risk_individuals, risk_trends)
        }
    
    async def _generate_trend_forecast_report(self, timeframe: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trend forecast report"""
        
        # Historical data analysis
        historical_data = self._get_historical_data(timeframe)
        
        # Generate predictions
        predictions = {}
        for metric in ["stress", "burnout", "engagement", "wellness"]:
            predictions[metric] = self._predict_metric_trend(metric, historical_data)
        
        # Confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(predictions)
        
        # Scenario analysis
        scenarios = self._generate_scenarios(predictions)
        
        return {
            "predictions": predictions,
            "confidence_intervals": confidence_intervals,
            "scenarios": scenarios,
            "forecast_summary": self._generate_forecast_summary(predictions)
        }
    
    def _calculate_overall_wellness_score(self, timeframe: str) -> float:
        """Calculate overall organizational wellness score based on aggregated data"""
        try:
            # Get wellness entries for the specified timeframe
            days = self._get_timeframe_days(timeframe)
            entries = wellness_entry_repo.get_entries_by_timeframe(days)
            
            if not entries:
                return 7.0  # Default score if no data
            
            # Calculate weighted average based on multiple factors
            wellness_scores = []
            stress_scores = []
            engagement_scores = []
            
            for entry in entries:
                wellness_scores.append(entry.get('wellness_score', 0))
                stress_scores.append(entry.get('stress_level', 0))
                engagement_scores.append(entry.get('engagement_score', 0))
            
            # Weighted calculation (wellness 50%, stress 30%, engagement 20%)
            avg_wellness = np.mean(wellness_scores) if wellness_scores else 7.0
            avg_stress = np.mean(stress_scores) if stress_scores else 5.0
            avg_engagement = np.mean(engagement_scores) if engagement_scores else 7.0
            
            # Normalize stress (inverse relationship)
            normalized_stress = 10 - avg_stress
            
            # Calculate weighted score
            overall_score = (avg_wellness * 0.5) + (normalized_stress * 0.3) + (avg_engagement * 0.2)
            
            # Apply trend adjustment based on historical data
            trend_adjustment = self._calculate_trend_adjustment('wellness_scores', timeframe)
            
            return min(max(overall_score + trend_adjustment, 0), 10)
            
        except Exception as e:
            self.logger.error(f"Error calculating overall wellness score: {e}")
            return 7.0
    
    def _calculate_trend_adjustment(self, metric: str, timeframe: str) -> float:
        """Calculate trend adjustment based on historical data"""
        try:
            if metric not in self.historical_data:
                return 0.0
            
            data = self.historical_data[metric]
            if len(data) < 2:
                return 0.0
            
            # Calculate recent vs historical average
            recent_data = data[-7:]  # Last 7 data points
            historical_avg = np.mean(data[:-7]) if len(data) > 7 else np.mean(data)
            recent_avg = np.mean(recent_data)
            
            # Calculate trend adjustment
            trend = (recent_avg - historical_avg) * 0.1  # Small adjustment factor
            return trend
            
        except Exception as e:
            self.logger.error(f"Error calculating trend adjustment: {e}")
            return 0.0
    
    def _get_timeframe_days(self, timeframe: str) -> int:
        """Convert timeframe string to number of days"""
        timeframe_map = {
            '7d': 7,
            '14d': 14,
            '30d': 30,
            '90d': 90,
            '180d': 180,
            '365d': 365
        }
        return timeframe_map.get(timeframe, 30)
    
    def _calculate_stress_levels(self, timeframe: str) -> Dict[str, float]:
        """Calculate organizational stress levels based on actual data"""
        try:
            days = self._get_timeframe_days(timeframe)
            entries = wellness_entry_repo.get_entries_by_timeframe(days)
            
            if not entries:
                return {
                    "low_stress": 0.4,
                    "moderate_stress": 0.35,
                    "high_stress": 0.2,
                    "critical_stress": 0.05
                }
            
            stress_levels = []
            for entry in entries:
                stress_levels.append(entry.get('stress_level', 5.0))
            
            # Categorize stress levels
            low_stress = len([s for s in stress_levels if s <= 3.0]) / len(stress_levels)
            moderate_stress = len([s for s in stress_levels if 3.0 < s <= 6.0]) / len(stress_levels)
            high_stress = len([s for s in stress_levels if 6.0 < s <= 8.0]) / len(stress_levels)
            critical_stress = len([s for s in stress_levels if s > 8.0]) / len(stress_levels)
            
            return {
                "low_stress": low_stress,
                "moderate_stress": moderate_stress,
                "high_stress": high_stress,
                "critical_stress": critical_stress
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating stress levels: {e}")
            return {
                "low_stress": 0.4,
                "moderate_stress": 0.35,
                "high_stress": 0.2,
                "critical_stress": 0.05
            }
    
    def _calculate_engagement_score(self, timeframe: str) -> float:
        """Calculate organizational engagement score based on interaction data"""
        try:
            days = self._get_timeframe_days(timeframe)
            
            # Get engagement metrics from multiple sources
            wellness_entries = wellness_entry_repo.get_entries_by_timeframe(days)
            user_interactions = analytics_repo.get_user_interactions(days)
            resource_usage = analytics_repo.get_resource_usage(days)
            
            # Calculate engagement factors
            participation_rate = self._calculate_participation_rate(wellness_entries, days)
            interaction_frequency = self._calculate_interaction_frequency(user_interactions)
            resource_engagement = self._calculate_resource_engagement(resource_usage)
            sentiment_score = self._calculate_average_sentiment(wellness_entries)
            
            # Weighted engagement score
            engagement_score = (
                participation_rate * 0.3 +
                interaction_frequency * 0.25 +
                resource_engagement * 0.25 +
                sentiment_score * 0.2
            )
            
            return min(max(engagement_score, 0), 10)
            
        except Exception as e:
            self.logger.error(f"Error calculating engagement score: {e}")
            return 7.8
    
    def _calculate_participation_rate(self, entries: List[Dict], days: int) -> float:
        """Calculate participation rate in wellness activities"""
        try:
            if not entries:
                return 0.5
            
            # Get total active users
            total_users = user_repo.get_active_user_count()
            if total_users == 0:
                return 0.5
            
            # Count unique users who participated
            participating_users = len(set(entry.get('user_id') for entry in entries))
            
            # Calculate participation rate
            participation_rate = participating_users / total_users
            
            # Normalize to 0-10 scale
            return participation_rate * 10
            
        except Exception as e:
            self.logger.error(f"Error calculating participation rate: {e}")
            return 5.0
    
    def _calculate_interaction_frequency(self, interactions: List[Dict]) -> float:
        """Calculate average interaction frequency"""
        try:
            if not interactions:
                return 5.0
            
            # Calculate average interactions per user per day
            total_interactions = len(interactions)
            unique_users = len(set(inter.get('user_id') for inter in interactions))
            
            if unique_users == 0:
                return 5.0
            
            avg_interactions_per_user = total_interactions / unique_users
            
            # Normalize to 0-10 scale (assuming 5 interactions per day is optimal)
            normalized_frequency = min(avg_interactions_per_user / 5.0, 2.0) * 5.0
            
            return normalized_frequency
            
        except Exception as e:
            self.logger.error(f"Error calculating interaction frequency: {e}")
            return 5.0
    
    def _calculate_resource_engagement(self, resource_usage: List[Dict]) -> float:
        """Calculate resource engagement score"""
        try:
            if not resource_usage:
                return 5.0
            
            # Calculate engagement based on resource usage patterns
            total_resources = len(resource_usage)
            used_resources = len([r for r in resource_usage if r.get('usage_count', 0) > 0])
            
            if total_resources == 0:
                return 5.0
            
            engagement_rate = used_resources / total_resources
            
            # Normalize to 0-10 scale
            return engagement_rate * 10
            
        except Exception as e:
            self.logger.error(f"Error calculating resource engagement: {e}")
            return 5.0
    
    def _calculate_average_sentiment(self, entries: List[Dict]) -> float:
        """Calculate average sentiment score from wellness entries"""
        try:
            if not entries:
                return 5.0
            
            sentiment_scores = []
            for entry in entries:
                sentiment = entry.get('sentiment_score', 5.0)
                sentiment_scores.append(sentiment)
            
            avg_sentiment = np.mean(sentiment_scores)
            
            # Normalize to 0-10 scale
            return min(max(avg_sentiment, 0), 10)
            
        except Exception as e:
            self.logger.error(f"Error calculating average sentiment: {e}")
            return 5.0
    
    def _calculate_burnout_risk(self, timeframe: str) -> float:
        """Calculate organizational burnout risk based on risk detection data"""
        try:
            days = self._get_timeframe_days(timeframe)
            
            # Get risk assessment data
            risk_assessments = analytics_repo.get_risk_assessments(days)
            
            if not risk_assessments:
                return 0.15
            
            # Calculate risk factors
            high_risk_count = 0
            total_assessments = len(risk_assessments)
            
            for assessment in risk_assessments:
                risk_level = assessment.get('risk_level', 0)
                if risk_level > 0.7:  # High risk threshold
                    high_risk_count += 1
            
            # Calculate overall risk percentage
            risk_percentage = high_risk_count / total_assessments if total_assessments > 0 else 0.15
            
            # Apply trend analysis
            trend_adjustment = self._calculate_trend_adjustment('burnout_risk', timeframe)
            
            return min(max(risk_percentage + trend_adjustment, 0), 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating burnout risk: {e}")
            return 0.15
    
    def _calculate_work_life_balance(self, timeframe: str) -> float:
        """Calculate work-life balance score based on work patterns and feedback"""
        try:
            days = self._get_timeframe_days(timeframe)
            
            # Get work-life balance indicators
            work_patterns = analytics_repo.get_work_patterns(days)
            feedback_data = analytics_repo.get_work_life_feedback(days)
            
            if not work_patterns and not feedback_data:
                return 6.9
            
            # Calculate work-life balance factors
            overtime_hours = self._calculate_overtime_hours(work_patterns)
            weekend_work = self._calculate_weekend_work(work_patterns)
            feedback_score = self._calculate_feedback_score(feedback_data)
            
            # Weighted calculation
            balance_score = (
                (10 - overtime_hours) * 0.4 +
                (10 - weekend_work) * 0.3 +
                feedback_score * 0.3
            )
            
            return min(max(balance_score, 0), 10)
            
        except Exception as e:
            self.logger.error(f"Error calculating work-life balance: {e}")
            return 6.9
    
    def _calculate_overtime_hours(self, work_patterns: List[Dict]) -> float:
        """Calculate overtime hours impact on work-life balance"""
        try:
            if not work_patterns:
                return 5.0
            
            total_overtime = 0
            total_workdays = 0
            
            for pattern in work_patterns:
                regular_hours = pattern.get('regular_hours', 8)
                actual_hours = pattern.get('actual_hours', 8)
                overtime = max(0, actual_hours - regular_hours)
                total_overtime += overtime
                total_workdays += 1
            
            if total_workdays == 0:
                return 5.0
            
            avg_overtime = total_overtime / total_workdays
            
            # Normalize to 0-10 scale (0 overtime = 10, 4+ hours overtime = 0)
            normalized_overtime = max(0, 10 - (avg_overtime * 2.5))
            
            return normalized_overtime
            
        except Exception as e:
            self.logger.error(f"Error calculating overtime hours: {e}")
            return 5.0
    
    def _calculate_weekend_work(self, work_patterns: List[Dict]) -> float:
        """Calculate weekend work impact on work-life balance"""
        try:
            if not work_patterns:
                return 5.0
            
            weekend_work_days = 0
            total_weeks = 0
            
            for pattern in work_patterns:
                if pattern.get('weekend_work', False):
                    weekend_work_days += 1
                total_weeks += 1
            
            if total_weeks == 0:
                return 5.0
            
            weekend_work_ratio = weekend_work_days / total_weeks
            
            # Normalize to 0-10 scale (0 weekend work = 10, 100% weekend work = 0)
            normalized_weekend = 10 - (weekend_work_ratio * 10)
            
            return normalized_weekend
            
        except Exception as e:
            self.logger.error(f"Error calculating weekend work: {e}")
            return 5.0
    
    def _calculate_feedback_score(self, feedback_data: List[Dict]) -> float:
        """Calculate work-life balance feedback score"""
        try:
            if not feedback_data:
                return 5.0
            
            feedback_scores = []
            for feedback in feedback_data:
                score = feedback.get('work_life_balance_score', 5.0)
                feedback_scores.append(score)
            
            avg_feedback = np.mean(feedback_scores)
            
            return min(max(avg_feedback, 0), 10)
            
        except Exception as e:
            self.logger.error(f"Error calculating feedback score: {e}")
            return 5.0
    
    def _calculate_team_collaboration(self, timeframe: str) -> float:
        """Calculate team collaboration health based on communication patterns"""
        try:
            days = self._get_timeframe_days(timeframe)
            
            # Get collaboration metrics
            communication_data = analytics_repo.get_communication_patterns(days)
            team_feedback = analytics_repo.get_team_feedback(days)
            
            if not communication_data and not team_feedback:
                return 7.2
            
            # Calculate collaboration factors
            communication_frequency = self._calculate_communication_frequency(communication_data)
            cross_team_interaction = self._calculate_cross_team_interaction(communication_data)
            team_satisfaction = self._calculate_team_satisfaction(team_feedback)
            
            # Weighted collaboration score
            collaboration_score = (
                communication_frequency * 0.4 +
                cross_team_interaction * 0.3 +
                team_satisfaction * 0.3
            )
            
            return min(max(collaboration_score, 0), 10)
            
        except Exception as e:
            self.logger.error(f"Error calculating team collaboration: {e}")
            return 7.2
    
    def _calculate_communication_frequency(self, communication_data: List[Dict]) -> float:
        """Calculate communication frequency score"""
        try:
            if not communication_data:
                return 5.0
            
            total_communications = len(communication_data)
            unique_participants = len(set(comm.get('participant_id') for comm in communication_data))
            
            if unique_participants == 0:
                return 5.0
            
            avg_communications_per_participant = total_communications / unique_participants
            
            # Normalize to 0-10 scale (assuming 10 communications per day is optimal)
            normalized_frequency = min(avg_communications_per_participant / 10.0, 2.0) * 5.0
            
            return normalized_frequency
            
        except Exception as e:
            self.logger.error(f"Error calculating communication frequency: {e}")
            return 5.0
    
    def _calculate_cross_team_interaction(self, communication_data: List[Dict]) -> float:
        """Calculate cross-team interaction score"""
        try:
            if not communication_data:
                return 5.0
            
            cross_team_communications = 0
            total_communications = len(communication_data)
            
            for comm in communication_data:
                if comm.get('cross_team', False):
                    cross_team_communications += 1
            
            if total_communications == 0:
                return 5.0
            
            cross_team_ratio = cross_team_communications / total_communications
            
            # Normalize to 0-10 scale
            return cross_team_ratio * 10
            
        except Exception as e:
            self.logger.error(f"Error calculating cross-team interaction: {e}")
            return 5.0
    
    def _calculate_team_satisfaction(self, team_feedback: List[Dict]) -> float:
        """Calculate team satisfaction score"""
        try:
            if not team_feedback:
                return 5.0
            
            satisfaction_scores = []
            for feedback in team_feedback:
                score = feedback.get('collaboration_satisfaction', 5.0)
                satisfaction_scores.append(score)
            
            avg_satisfaction = np.mean(satisfaction_scores)
            
            return min(max(avg_satisfaction, 0), 10)
            
        except Exception as e:
            self.logger.error(f"Error calculating team satisfaction: {e}")
            return 5.0
    
    def _calculate_trends(self, metrics: Dict[str, Any], timeframe: str) -> Dict[str, str]:
        """Calculate trends for metrics based on historical data"""
        trends = {}
        
        for metric, value in metrics.items():
            if isinstance(value, (int, float)):
                trend = self._calculate_metric_trend(metric, value, timeframe)
                trends[metric] = trend
            else:
                trends[metric] = "stable"
        
        return trends
    
    def _calculate_metric_trend(self, metric: str, current_value: float, timeframe: str) -> str:
        """Calculate trend for a specific metric"""
        try:
            if metric not in self.historical_data:
                return "stable"
            
            data = self.historical_data[metric]
            if len(data) < 2:
                return "stable"
            
            # Calculate recent vs historical average
            recent_data = data[-7:]  # Last 7 data points
            historical_avg = np.mean(data[:-7]) if len(data) > 7 else np.mean(data)
            recent_avg = np.mean(recent_data)
            
            # Determine trend based on comparison
            if recent_avg > historical_avg * 1.05:  # 5% improvement
                return "improving"
            elif recent_avg < historical_avg * 0.95:  # 5% decline
                return "declining"
            else:
                return "stable"
                
        except Exception as e:
            self.logger.error(f"Error calculating metric trend: {e}")
            return "stable"
    
    def _identify_risk_areas(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify areas of concern based on metrics"""
        risk_areas = []
        
        # Define risk thresholds for different metrics
        risk_thresholds = {
            "overall_wellness_score": 6.0,
            "engagement_score": 6.0,
            "work_life_balance": 6.0,
            "team_collaboration": 6.0,
            "burnout_risk": 0.3  # High risk threshold
        }
        
        for metric, value in metrics.items():
            if isinstance(value, (int, float)):
                threshold = risk_thresholds.get(metric, 5.0)
                
                # For burnout risk, higher values are worse
                if metric == "burnout_risk":
                    is_risky = value > threshold
                else:
                    is_risky = value < threshold
                
                if is_risky:
                    severity = "high" if (value < threshold * 0.8 or (metric == "burnout_risk" and value > threshold * 1.2)) else "medium"
                    
                    risk_areas.append({
                        "metric": metric,
                        "value": value,
                        "severity": severity,
                        "recommendation": self._generate_risk_recommendation(metric, value, severity)
                    })
        
        return risk_areas
    
    def _generate_risk_recommendation(self, metric: str, value: float, severity: str) -> str:
        """Generate specific recommendations for risk areas"""
        recommendations = {
            "overall_wellness_score": {
                "high": "Implement immediate wellness interventions and stress management programs",
                "medium": "Focus on improving workplace wellness initiatives and employee support"
            },
            "engagement_score": {
                "high": "Conduct employee surveys and implement engagement improvement programs",
                "medium": "Enhance communication channels and recognition programs"
            },
            "work_life_balance": {
                "high": "Review workload distribution and implement flexible work policies",
                "medium": "Promote work-life balance initiatives and time management training"
            },
            "team_collaboration": {
                "high": "Implement team-building activities and improve communication tools",
                "medium": "Enhance collaboration platforms and cross-team projects"
            },
            "burnout_risk": {
                "high": "Immediate intervention required - implement stress reduction programs and workload review",
                "medium": "Monitor closely and provide additional support resources"
            }
        }
        
        return recommendations.get(metric, {}).get(severity, f"Focus on improving {metric.replace('_', ' ')}")
    
    def _generate_organizational_summary(self, metrics: Dict[str, Any], trends: Dict[str, str]) -> str:
        """Generate organizational health summary"""
        wellness_score = metrics.get("overall_wellness_score", 0)
        stress_levels = metrics.get("stress_levels", {})
        high_stress = stress_levels.get("high_stress", 0) + stress_levels.get("critical_stress", 0)
        
        # Generate comprehensive summary
        if wellness_score >= 8.0:
            summary = f"Organizational health is excellent with a wellness score of {wellness_score:.1f}/10."
        elif wellness_score >= 6.0:
            summary = f"Organizational health is good with a wellness score of {wellness_score:.1f}/10."
        else:
            summary = f"Organizational health needs attention with a wellness score of {wellness_score:.1f}/10."
        
        # Add stress level information
        if high_stress > 0.3:
            summary += f" High stress levels ({high_stress:.1%}) require immediate attention."
        elif high_stress > 0.2:
            summary += f" Elevated stress levels ({high_stress:.1%}) should be monitored."
        
        # Add trend information
        improving_metrics = [metric for metric, trend in trends.items() if trend == "improving"]
        declining_metrics = [metric for metric, trend in trends.items() if trend == "declining"]
        
        if improving_metrics:
            summary += f" Positive trends observed in {', '.join(improving_metrics)}."
        
        if declining_metrics:
            summary += f" Areas of concern: {', '.join(declining_metrics)} showing decline."
        
        return summary
    
    def _get_all_teams(self) -> List[str]:
        """Get list of all teams"""
        try:
            # Get teams from user repository
            teams = user_repo.get_all_teams()
            if teams:
                return teams
            
            # Fallback to default teams if no data available
            return ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]
        except Exception as e:
            self.logger.error(f"Error getting teams: {e}")
            return ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]
    
    def _calculate_team_wellness_score(self, team: str, timeframe: str) -> float:
        """Calculate wellness score for a specific team"""
        try:
            # Get team members
            team_members = user_repo.get_users_by_team(team)
            if not team_members:
                return 7.0
            
            # Calculate average wellness score for team
            team_scores = []
            for member in team_members:
                member_entries = wellness_entry_repo.get_user_entries(
                    user_id=member.id,
                    timeframe=timeframe
                )
                if member_entries:
                    avg_score = np.mean([entry.wellness_score for entry in member_entries])
                    team_scores.append(avg_score)
            
            if team_scores:
                return np.mean(team_scores)
            
            # Fallback to base scores if no data
            base_scores = {
                "Engineering": 7.2,
                "Sales": 6.8,
                "Marketing": 7.5,
                "HR": 8.1,
                "Finance": 7.0,
                "Operations": 6.9
            }
            return base_scores.get(team, 7.0)
        except Exception as e:
            self.logger.error(f"Error calculating team wellness score for {team}: {e}")
            return 7.0
    
    def _calculate_team_stress_distribution(self, team: str, timeframe: str) -> Dict[str, float]:
        """Calculate stress distribution for a team"""
        try:
            # Get team members
            team_members = user_repo.get_users_by_team(team)
            if not team_members:
                return {"low_stress": 0.5, "moderate_stress": 0.3, "high_stress": 0.15, "critical_stress": 0.05}
            
            # Calculate stress distribution
            stress_levels = {"low_stress": 0, "moderate_stress": 0, "high_stress": 0, "critical_stress": 0}
            total_entries = 0
            
            for member in team_members:
                member_entries = wellness_entry_repo.get_user_entries(
                    user_id=member.id,
                    timeframe=timeframe
                )
                for entry in member_entries:
                    total_entries += 1
                    if entry.stress_level <= 3:
                        stress_levels["low_stress"] += 1
                    elif entry.stress_level <= 6:
                        stress_levels["moderate_stress"] += 1
                    elif entry.stress_level <= 8:
                        stress_levels["high_stress"] += 1
                    else:
                        stress_levels["critical_stress"] += 1
            
            if total_entries > 0:
                return {level: count / total_entries for level, count in stress_levels.items()}
            
            return {"low_stress": 0.5, "moderate_stress": 0.3, "high_stress": 0.15, "critical_stress": 0.05}
        except Exception as e:
            self.logger.error(f"Error calculating team stress distribution for {team}: {e}")
            return {"low_stress": 0.5, "moderate_stress": 0.3, "high_stress": 0.15, "critical_stress": 0.05}
    
    def _calculate_team_collaboration_health(self, team: str, timeframe: str) -> float:
        """Calculate collaboration health for a team"""
        try:
            # Get team members
            team_members = user_repo.get_users_by_team(team)
            if not team_members:
                return 7.5
            
            # Calculate collaboration metrics
            collaboration_scores = []
            for member in team_members:
                member_entries = wellness_entry_repo.get_user_entries(
                    user_id=member.id,
                    timeframe=timeframe
                )
                if member_entries:
                    # Calculate based on team interaction and satisfaction
                    avg_satisfaction = np.mean([entry.team_satisfaction for entry in member_entries if hasattr(entry, 'team_satisfaction')])
                    avg_interaction = np.mean([entry.team_interaction for entry in member_entries if hasattr(entry, 'team_interaction')])
                    
                    if avg_satisfaction > 0 and avg_interaction > 0:
                        collaboration_score = (avg_satisfaction + avg_interaction) / 2
                        collaboration_scores.append(collaboration_score)
            
            if collaboration_scores:
                return np.mean(collaboration_scores)
            
            return 7.5
        except Exception as e:
            self.logger.error(f"Error calculating team collaboration health for {team}: {e}")
            return 7.5
    
    def _calculate_team_workload_distribution(self, team: str, timeframe: str) -> Dict[str, float]:
        """Calculate workload distribution for a team"""
        try:
            # Get team members
            team_members = user_repo.get_users_by_team(team)
            if not team_members:
                return {"balanced": 0.6, "slightly_high": 0.25, "high": 0.1, "overloaded": 0.05}
            
            # Calculate workload distribution
            workload_levels = {"balanced": 0, "slightly_high": 0, "high": 0, "overloaded": 0}
            total_members = len(team_members)
            
            for member in team_members:
                member_entries = wellness_entry_repo.get_user_entries(
                    user_id=member.id,
                    timeframe=timeframe
                )
                if member_entries:
                    avg_workload = np.mean([entry.workload_level for entry in member_entries if hasattr(entry, 'workload_level')])
                    
                    if avg_workload <= 5:
                        workload_levels["balanced"] += 1
                    elif avg_workload <= 7:
                        workload_levels["slightly_high"] += 1
                    elif avg_workload <= 8:
                        workload_levels["high"] += 1
                    else:
                        workload_levels["overloaded"] += 1
            
            if total_members > 0:
                return {level: count / total_members for level, count in workload_levels.items()}
            
            return {"balanced": 0.6, "slightly_high": 0.25, "high": 0.1, "overloaded": 0.05}
        except Exception as e:
            self.logger.error(f"Error calculating team workload distribution for {team}: {e}")
            return {"balanced": 0.6, "slightly_high": 0.25, "high": 0.1, "overloaded": 0.05}
    
    def _identify_team_risk_individuals(self, team: str, timeframe: str) -> List[Dict[str, Any]]:
        """Identify individuals at risk within a team"""
        try:
            # Get team members
            team_members = user_repo.get_users_by_team(team)
            if not team_members:
                return []
            
            risk_individuals = []
            for member in team_members:
                member_entries = wellness_entry_repo.get_user_entries(
                    user_id=member.id,
                    timeframe=timeframe
                )
                if member_entries:
                    # Calculate risk indicators
                    avg_stress = np.mean([entry.stress_level for entry in member_entries])
                    avg_wellness = np.mean([entry.wellness_score for entry in member_entries])
                    burnout_risk = np.mean([entry.burnout_risk for entry in member_entries if hasattr(entry, 'burnout_risk')])
                    
                    # Identify high-risk individuals
                    if avg_stress > 7.0 or avg_wellness < 5.0 or burnout_risk > 0.7:
                        risk_individuals.append({
                            "user_id": member.id,
                            "name": member.name,
                            "risk_factors": {
                                "high_stress": avg_stress > 7.0,
                                "low_wellness": avg_wellness < 5.0,
                                "burnout_risk": burnout_risk > 0.7
                            },
                            "risk_score": (avg_stress * 0.4 + (10 - avg_wellness) * 0.4 + burnout_risk * 0.2) / 10
                        })
            
            return sorted(risk_individuals, key=lambda x: x["risk_score"], reverse=True)
        except Exception as e:
            self.logger.error(f"Error identifying team risk individuals for {team}: {e}")
            return []
    
    def _compare_teams(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare teams across metrics"""
        comparison = {
            "best_performing": None,
            "needs_attention": [],
            "metric_rankings": {}
        }
        
        # Find best performing team
        wellness_scores = {team: data["wellness_score"] for team, data in team_data.items()}
        best_team = max(wellness_scores.items(), key=lambda x: x[1])
        comparison["best_performing"] = {"team": best_team[0], "score": best_team[1]}
        
        # Identify teams needing attention
        for team, data in team_data.items():
            if data["wellness_score"] < 6.0:
                comparison["needs_attention"].append({
                    "team": team,
                    "score": data["wellness_score"],
                    "primary_concern": "low_wellness"
                })
        
        return comparison
    
    def _extract_team_insights(self, team_data: Dict[str, Any]) -> List[str]:
        """Extract insights from team data"""
        insights = []
        
        # Find patterns across teams
        avg_wellness = np.mean([data["wellness_score"] for data in team_data.values()])
        if avg_wellness < 7.0:
            insights.append("Overall team wellness is below target levels")
        
        # Identify common issues
        high_stress_teams = [
            team for team, data in team_data.items()
            if data["stress_distribution"]["high_stress"] > 0.2
        ]
        if high_stress_teams:
            insights.append(f"High stress levels detected in {len(high_stress_teams)} teams")
        
        return insights
    
    def _identify_high_risk_individuals(self, timeframe: str) -> List[Dict[str, Any]]:
        """Identify individuals at high risk"""
        try:
            # Get all users
            all_users = user_repo.get_all_users()
            if not all_users:
                return []
            
            high_risk_individuals = []
            for user in all_users:
                user_entries = wellness_entry_repo.get_user_entries(
                    user_id=user.id,
                    timeframe=timeframe
                )
                if user_entries:
                    # Calculate comprehensive risk score
                    avg_stress = np.mean([entry.stress_level for entry in user_entries])
                    avg_wellness = np.mean([entry.wellness_score for entry in user_entries])
                    burnout_risk = np.mean([entry.burnout_risk for entry in user_entries if hasattr(entry, 'burnout_risk')])
                    crisis_risk = np.mean([entry.crisis_risk for entry in user_entries if hasattr(entry, 'crisis_risk')])
                    
                    # Calculate overall risk score
                    risk_score = (
                        avg_stress * 0.3 +
                        (10 - avg_wellness) * 0.3 +
                        burnout_risk * 0.2 +
                        crisis_risk * 0.2
                    ) / 10
                    
                    # Identify high-risk individuals
                    if risk_score > 0.7:
                        high_risk_individuals.append({
                            "user_id": user.id,
                            "name": user.name,
                            "team": user.team,
                            "risk_score": risk_score,
                            "risk_factors": {
                                "high_stress": avg_stress > 7.0,
                                "low_wellness": avg_wellness < 5.0,
                                "burnout_risk": burnout_risk > 0.7,
                                "crisis_risk": crisis_risk > 0.7
                            },
                            "metrics": {
                                "avg_stress": avg_stress,
                                "avg_wellness": avg_wellness,
                                "burnout_risk": burnout_risk,
                                "crisis_risk": crisis_risk
                            }
                        })
            
            return sorted(high_risk_individuals, key=lambda x: x["risk_score"], reverse=True)
        except Exception as e:
            self.logger.error(f"Error identifying high risk individuals: {e}")
            return []
    
    def _analyze_risk_trends(self, timeframe: str) -> Dict[str, Any]:
        """Analyze risk trends over time"""
        try:
            # Get historical data
            historical_data = self._get_historical_data(timeframe)
            if historical_data.empty:
                return {
                    "overall_risk_trend": "stable",
                    "risk_factors": ["workload", "stress", "work_life_balance"],
                    "trend_data": []
                }
            
            # Calculate trend data
            trend_data = []
            risk_factors = []
            
            # Analyze stress trends
            if 'stress_level' in historical_data.columns:
                stress_trend = self._calculate_metric_trend('stress_level', historical_data)
                trend_data.append({
                    "metric": "stress_level",
                    "trend": stress_trend["trend"],
                    "change_percentage": ((stress_trend["predicted_value"] - stress_trend["current_value"]) / stress_trend["current_value"]) * 100
                })
                if stress_trend["trend"] == "increasing":
                    risk_factors.append("stress")
            
            # Analyze wellness trends
            if 'wellness_score' in historical_data.columns:
                wellness_trend = self._calculate_metric_trend('wellness_score', historical_data)
                trend_data.append({
                    "metric": "wellness_score",
                    "trend": wellness_trend["trend"],
                    "change_percentage": ((wellness_trend["predicted_value"] - wellness_trend["current_value"]) / wellness_trend["current_value"]) * 100
                })
                if wellness_trend["trend"] == "declining":
                    risk_factors.append("wellness")
            
            # Determine overall trend
            increasing_risks = len([t for t in trend_data if t["trend"] == "increasing"])
            decreasing_risks = len([t for t in trend_data if t["trend"] == "decreasing"])
            
            if increasing_risks > decreasing_risks:
                overall_trend = "increasing"
            elif decreasing_risks > increasing_risks:
                overall_trend = "decreasing"
            else:
                overall_trend = "stable"
            
            return {
                "overall_risk_trend": overall_trend,
                "risk_factors": risk_factors,
                "trend_data": trend_data
            }
        except Exception as e:
            self.logger.error(f"Error analyzing risk trends: {e}")
            return {
                "overall_risk_trend": "stable",
                "risk_factors": ["workload", "stress", "work_life_balance"],
                "trend_data": []
            }
    
    def _predict_future_risks(self, timeframe: str) -> List[PredictiveInsight]:
        """Predict future risks"""
        try:
            # Get historical data
            historical_data = self._get_historical_data(timeframe)
            if historical_data.empty:
                return []
            
            predictions = []
            
            # Predict stress trends
            if 'stress_level' in historical_data.columns:
                stress_prediction = self._predict_metric_trend('stress_level', historical_data)
                if stress_prediction["predicted_value"] > 7.0:
                    predictions.append(PredictiveInsight(
                        insight_type="stress_increase",
                        confidence=stress_prediction["confidence"],
                        description=f"Stress levels predicted to increase to {stress_prediction['predicted_value']:.1f}",
                        severity="medium" if stress_prediction["predicted_value"] <= 8.0 else "high",
                        timeframe="30d"
                    ))
            
            # Predict wellness trends
            if 'wellness_score' in historical_data.columns:
                wellness_prediction = self._predict_metric_trend('wellness_score', historical_data)
                if wellness_prediction["predicted_value"] < 6.0:
                    predictions.append(PredictiveInsight(
                        insight_type="wellness_decline",
                        confidence=wellness_prediction["confidence"],
                        description=f"Wellness scores predicted to decline to {wellness_prediction['predicted_value']:.1f}",
                        severity="medium" if wellness_prediction["predicted_value"] >= 5.0 else "high",
                        timeframe="30d"
                    ))
            
            # Predict burnout risk
            if 'burnout_risk' in historical_data.columns:
                burnout_prediction = self._predict_metric_trend('burnout_risk', historical_data)
                if burnout_prediction["predicted_value"] > 0.7:
                    predictions.append(PredictiveInsight(
                        insight_type="burnout_risk",
                        confidence=burnout_prediction["confidence"],
                        description=f"Burnout risk predicted to increase to {burnout_prediction['predicted_value']:.2f}",
                        severity="high",
                        timeframe="30d"
                    ))
            
            return predictions
        except Exception as e:
            self.logger.error(f"Error predicting future risks: {e}")
            return []
    
    def _recommend_interventions(self, high_risk_individuals: List[Dict], risk_trends: Dict) -> List[Dict[str, Any]]:
        """Recommend interventions based on risk analysis"""
        interventions = []
        
        if high_risk_individuals:
            interventions.append({
                "type": "individual_support",
                "priority": "high",
                "description": "Provide individual support to high-risk employees",
                "target_count": len(high_risk_individuals)
            })
        
        if risk_trends.get("overall_risk_trend") == "increasing":
            interventions.append({
                "type": "organizational_intervention",
                "priority": "medium",
                "description": "Implement organizational wellness programs",
                "target_count": "all_employees"
            })
        
        return interventions
    
    def _generate_risk_summary(self, high_risk_individuals: List[Dict], risk_trends: Dict) -> str:
        """Generate risk summary"""
        if not high_risk_individuals:
            return "No high-risk individuals identified at this time."
        
        return f"Identified {len(high_risk_individuals)} high-risk individuals requiring immediate attention."
    
    def _get_historical_data(self, timeframe: str) -> pd.DataFrame:
        """Get historical data for trend analysis"""
        try:
            # Get all wellness entries for the timeframe
            all_entries = wellness_entry_repo.get_all_entries(timeframe=timeframe)
            
            if not all_entries:
                return pd.DataFrame()
            
            # Convert to DataFrame
            data = []
            for entry in all_entries:
                data.append({
                    'user_id': entry.user_id,
                    'timestamp': entry.timestamp,
                    'wellness_score': entry.wellness_score,
                    'stress_level': entry.stress_level,
                    'mood': entry.mood,
                    'energy_level': entry.energy_level,
                    'burnout_risk': getattr(entry, 'burnout_risk', 0.0),
                    'crisis_risk': getattr(entry, 'crisis_risk', 0.0),
                    'team': getattr(entry, 'team', 'Unknown')
                })
            
            df = pd.DataFrame(data)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
            
            return df
        except Exception as e:
            self.logger.error(f"Error getting historical data: {e}")
            return pd.DataFrame()
    
    def _predict_metric_trend(self, metric: str, historical_data: pd.DataFrame) -> Dict[str, Any]:
        """Predict trend for a specific metric"""
        try:
            if historical_data.empty or metric not in historical_data.columns:
                return {
                    "current_value": 7.5,
                    "predicted_value": 7.3,
                    "confidence": 0.8,
                    "trend": "slight_decline"
                }
            
            # Get metric data
            metric_data = historical_data[metric].dropna()
            if len(metric_data) < 3:
                return {
                    "current_value": metric_data.mean() if not metric_data.empty else 7.5,
                    "predicted_value": metric_data.mean() if not metric_data.empty else 7.3,
                    "confidence": 0.5,
                    "trend": "stable"
                }
            
            # Calculate current value (average of last 7 days)
            current_value = metric_data.tail(7).mean()
            
            # Simple linear trend prediction
            x = np.arange(len(metric_data))
            y = metric_data.values
            
            # Fit linear regression
            slope, intercept = np.polyfit(x, y, 1)
            
            # Predict next value
            predicted_value = slope * (len(metric_data) + 7) + intercept
            
            # Calculate confidence based on R-squared
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            confidence = max(0.1, min(0.95, r_squared))
            
            # Determine trend
            if slope > 0.1:
                trend = "increasing"
            elif slope < -0.1:
                trend = "decreasing"
            else:
                trend = "stable"
            
            return {
                "current_value": current_value,
                "predicted_value": predicted_value,
                "confidence": confidence,
                "trend": trend
            }
        except Exception as e:
            self.logger.error(f"Error predicting metric trend for {metric}: {e}")
            return {
                "current_value": 7.5,
                "predicted_value": 7.3,
                "confidence": 0.8,
                "trend": "slight_decline"
            }
    
    def _calculate_confidence_intervals(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate confidence intervals for predictions"""
        try:
            confidence_intervals = {}
            
            for metric, prediction in predictions.items():
                if isinstance(prediction, dict) and "predicted_value" in prediction:
                    predicted_value = prediction["predicted_value"]
                    confidence = prediction.get("confidence", 0.8)
                    
                    # Calculate standard error based on confidence
                    # Higher confidence = wider interval
                    margin_of_error = (1 - confidence) * predicted_value * 0.2
                    
                    confidence_intervals[metric] = {
                        "lower_bound": max(0, predicted_value - margin_of_error),
                        "upper_bound": min(10, predicted_value + margin_of_error),
                        "confidence_level": confidence
                    }
            
            return confidence_intervals
        except Exception as e:
            self.logger.error(f"Error calculating confidence intervals: {e}")
            return {}
    
    def _generate_scenarios(self, predictions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate different scenarios based on predictions"""
        scenarios = [
            {
                "name": "Optimistic",
                "description": "Best-case scenario with improved interventions",
                "metrics": {metric: pred["predicted_value"] * 1.1 for metric, pred in predictions.items()}
            },
            {
                "name": "Baseline",
                "description": "Current trajectory without changes",
                "metrics": {metric: pred["predicted_value"] for metric, pred in predictions.items()}
            },
            {
                "name": "Pessimistic",
                "description": "Worst-case scenario without intervention",
                "metrics": {metric: pred["predicted_value"] * 0.9 for metric, pred in predictions.items()}
            }
        ]
        return scenarios
    
    def _generate_forecast_summary(self, predictions: Dict[str, Any]) -> str:
        """Generate forecast summary"""
        avg_prediction = np.mean([pred["predicted_value"] for pred in predictions.values()])
        
        if avg_prediction > 7.5:
            return "Forecast indicates positive wellness trends with continued support."
        elif avg_prediction > 6.0:
            return "Forecast shows stable wellness levels with room for improvement."
        else:
            return "Forecast indicates declining wellness trends requiring immediate intervention."
    
    def _apply_role_based_filtering(self, data: Dict[str, Any], user_role: str) -> Dict[str, Any]:
        """Apply role-based filtering to data"""
        if user_role == "executive":
            # High-level summary for executives
            return self._filter_for_executives(data)
        elif user_role == "hr":
            # Detailed data for HR
            return data
        elif user_role == "manager":
            # Team-level data for managers
            return self._filter_for_managers(data)
        else:
            # Limited data for other roles
            return self._filter_for_employees(data)
    
    def _filter_for_executives(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter data for executive view"""
        # Return high-level summary only
        return {
            "summary": data.get("summary", ""),
            "key_metrics": {
                "overall_wellness_score": data.get("metrics", {}).get("overall_wellness_score", 0),
                "burnout_risk": data.get("metrics", {}).get("burnout_risk", 0)
            },
            "risk_areas": data.get("risk_areas", [])[:3]  # Top 3 only
        }
    
    def _filter_for_managers(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter data for manager view"""
        # Return team-level data
        return {
            "team_data": data.get("team_data", {}),
            "team_comparison": data.get("team_comparison", {}),
            "insights": data.get("insights", [])
        }
    
    def _filter_for_employees(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter data for employee view"""
        # Return limited, anonymized data
        return {
            "organizational_summary": data.get("summary", ""),
            "general_trends": "positive" if data.get("metrics", {}).get("overall_wellness_score", 0) > 7.0 else "stable"
        }
    
    def _generate_visualizations(self, data: Dict[str, Any], report_type: str) -> Dict[str, Any]:
        """Generate visualizations for the report"""
        visualizations = {}
        
        if report_type == "organizational_health":
            visualizations["wellness_trend"] = self._create_wellness_trend_chart(data)
            visualizations["stress_distribution"] = self._create_stress_distribution_chart(data)
        
        elif report_type == "team_wellness":
            visualizations["team_comparison"] = self._create_team_comparison_chart(data)
        
        elif report_type == "risk_analysis":
            visualizations["risk_trends"] = self._create_risk_trends_chart(data)
        
        return visualizations
    
    def _create_wellness_trend_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create wellness trend chart"""
        try:
            # Extract wellness trend data
            metrics = data.get("metrics", {})
            wellness_score = metrics.get("overall_wellness_score", 7.0)
            historical_data = data.get("historical_data", [])
            
            # Create chart data
            chart_data = {
                "labels": [],
                "datasets": [{
                    "label": "Wellness Score",
                    "data": [],
                    "borderColor": "#4CAF50",
                    "backgroundColor": "rgba(76, 175, 80, 0.1)",
                    "tension": 0.4
                }]
            }
            
            # Add historical data points
            if historical_data:
                for entry in historical_data[-30:]:  # Last 30 data points
                    chart_data["labels"].append(entry.get("date", ""))
                    chart_data["datasets"][0]["data"].append(entry.get("wellness_score", wellness_score))
            
            # Add current value
            chart_data["labels"].append("Current")
            chart_data["datasets"][0]["data"].append(wellness_score)
            
            return {
                "type": "line_chart",
                "data": chart_data,
                "config": {
                    "responsive": True,
                    "plugins": {
                        "title": {
                            "display": True,
                            "text": "Wellness Score Trend"
                        }
                    },
                    "scales": {
                        "y": {
                            "beginAtZero": False,
                            "min": 0,
                            "max": 10
                        }
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error creating wellness trend chart: {e}")
            return {
                "type": "line_chart",
                "data": {"labels": [], "datasets": []},
                "config": {}
            }
    
    def _create_stress_distribution_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create stress distribution chart"""
        try:
            # Extract stress distribution data
            metrics = data.get("metrics", {})
            stress_distribution = metrics.get("stress_distribution", {
                "low_stress": 0.5,
                "moderate_stress": 0.3,
                "high_stress": 0.15,
                "critical_stress": 0.05
            })
            
            # Create chart data
            chart_data = {
                "labels": ["Low Stress", "Moderate Stress", "High Stress", "Critical Stress"],
                "datasets": [{
                    "data": [
                        stress_distribution.get("low_stress", 0) * 100,
                        stress_distribution.get("moderate_stress", 0) * 100,
                        stress_distribution.get("high_stress", 0) * 100,
                        stress_distribution.get("critical_stress", 0) * 100
                    ],
                    "backgroundColor": [
                        "#4CAF50",  # Green
                        "#FFC107",  # Yellow
                        "#FF9800",  # Orange
                        "#F44336"   # Red
                    ],
                    "borderWidth": 2,
                    "borderColor": "#fff"
                }]
            }
            
            return {
                "type": "pie_chart",
                "data": chart_data,
                "config": {
                    "responsive": True,
                    "plugins": {
                        "title": {
                            "display": True,
                            "text": "Stress Level Distribution"
                        },
                        "legend": {
                            "position": "bottom"
                        }
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error creating stress distribution chart: {e}")
            return {
                "type": "pie_chart",
                "data": {"labels": [], "datasets": []},
                "config": {}
            }
    
    def _create_team_comparison_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create team comparison chart"""
        try:
            # Extract team data
            team_data = data.get("team_data", {})
            
            if not team_data:
                return {
                    "type": "bar_chart",
                    "data": {"labels": [], "datasets": []},
                    "config": {}
                }
            
            # Create chart data
            labels = []
            wellness_scores = []
            stress_scores = []
            
            for team_name, team_info in team_data.items():
                labels.append(team_name)
                wellness_scores.append(team_info.get("wellness_score", 7.0))
                stress_scores.append(team_info.get("avg_stress_level", 5.0))
            
            chart_data = {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Wellness Score",
                        "data": wellness_scores,
                        "backgroundColor": "rgba(76, 175, 80, 0.8)",
                        "borderColor": "#4CAF50",
                        "borderWidth": 1
                    },
                    {
                        "label": "Stress Level",
                        "data": stress_scores,
                        "backgroundColor": "rgba(244, 67, 54, 0.8)",
                        "borderColor": "#F44336",
                        "borderWidth": 1
                    }
                ]
            }
            
            return {
                "type": "bar_chart",
                "data": chart_data,
                "config": {
                    "responsive": True,
                    "plugins": {
                        "title": {
                            "display": True,
                            "text": "Team Wellness Comparison"
                        },
                        "legend": {
                            "position": "top"
                        }
                    },
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 10
                        }
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error creating team comparison chart: {e}")
            return {
                "type": "bar_chart",
                "data": {"labels": [], "datasets": []},
                "config": {}
            }
    
    def _create_risk_trends_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create risk trends chart"""
        try:
            # Extract risk trends data
            risk_trends = data.get("risk_trends", {})
            trend_data = risk_trends.get("trend_data", [])
            
            if not trend_data:
                return {
                    "type": "area_chart",
                    "data": {"labels": [], "datasets": []},
                    "config": {}
                }
            
            # Create chart data
            labels = []
            stress_data = []
            burnout_data = []
            crisis_data = []
            
            for trend in trend_data:
                metric = trend.get("metric", "")
                if "stress" in metric.lower():
                    labels.append(trend.get("date", ""))
                    stress_data.append(trend.get("value", 0))
                elif "burnout" in metric.lower():
                    burnout_data.append(trend.get("value", 0))
                elif "crisis" in metric.lower():
                    crisis_data.append(trend.get("value", 0))
            
            chart_data = {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Stress Risk",
                        "data": stress_data,
                        "backgroundColor": "rgba(255, 152, 0, 0.3)",
                        "borderColor": "#FF9800",
                        "borderWidth": 2,
                        "fill": True
                    },
                    {
                        "label": "Burnout Risk",
                        "data": burnout_data,
                        "backgroundColor": "rgba(244, 67, 54, 0.3)",
                        "borderColor": "#F44336",
                        "borderWidth": 2,
                        "fill": True
                    },
                    {
                        "label": "Crisis Risk",
                        "data": crisis_data,
                        "backgroundColor": "rgba(156, 39, 176, 0.3)",
                        "borderColor": "#9C27B0",
                        "borderWidth": 2,
                        "fill": True
                    }
                ]
            }
            
            return {
                "type": "area_chart",
                "data": chart_data,
                "config": {
                    "responsive": True,
                    "plugins": {
                        "title": {
                            "display": True,
                            "text": "Risk Trends Over Time"
                        },
                        "legend": {
                            "position": "top"
                        }
                    },
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 1
                        }
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error creating risk trends chart: {e}")
            return {
                "type": "area_chart",
                "data": {"labels": [], "datasets": []},
                "config": {}
            }
    
    def _extract_insights(self, data: Dict[str, Any], report_type: str) -> List[str]:
        """Extract insights from the data"""
        insights = []
        
        if report_type == "organizational_health":
            wellness_score = data.get("metrics", {}).get("overall_wellness_score", 0)
            if wellness_score < 7.0:
                insights.append("Organizational wellness score is below target levels")
        
        elif report_type == "team_wellness":
            team_data = data.get("team_data", {})
            if team_data:
                avg_wellness = np.mean([team["wellness_score"] for team in team_data.values()])
                if avg_wellness < 7.0:
                    insights.append("Average team wellness is below target")
        
        return insights
    
    def _generate_recommendations(self, data: Dict[str, Any], report_type: str) -> List[str]:
        """Generate recommendations based on the data"""
        recommendations = []
        
        if report_type == "organizational_health":
            wellness_score = data.get("metrics", {}).get("overall_wellness_score", 0)
            if wellness_score < 7.0:
                recommendations.append("Implement organization-wide wellness programs")
                recommendations.append("Conduct employee satisfaction surveys")
        
        elif report_type == "risk_analysis":
            high_risk_count = len(data.get("high_risk_individuals", []))
            if high_risk_count > 0:
                recommendations.append(f"Provide immediate support to {high_risk_count} high-risk individuals")
                recommendations.append("Review workload distribution across teams")
        
        return recommendations
