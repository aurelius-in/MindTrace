"""
Analytics Utilities - Wellness data analysis and insights generation
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class WellnessAnalytics:
    """Analytics engine for wellness data analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_user_analytics(self, entries: List[Dict[str, Any]], timeframe: str) -> Dict[str, Any]:
        """
        Generate comprehensive analytics for a user's wellness data
        """
        try:
            if not entries:
                return self._empty_analytics()
            
            # Parse entries and extract metrics
            parsed_entries = self._parse_entries(entries)
            
            # Generate different types of analytics
            analytics = {
                "summary": self._generate_summary_analytics(parsed_entries),
                "trends": self._generate_trend_analytics(parsed_entries, timeframe),
                "patterns": self._generate_pattern_analytics(parsed_entries),
                "insights": self._generate_insights(parsed_entries),
                "recommendations": self._generate_recommendations(parsed_entries),
                "risk_assessment": self._generate_risk_assessment(parsed_entries)
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Failed to generate analytics: {e}")
            return self._empty_analytics()
    
    def _parse_entries(self, entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Parse and organize entries by type"""
        parsed = defaultdict(list)
        
        for entry in entries:
            entry_type = entry.get("entry_type", "unknown")
            parsed[entry_type].append(entry)
        
        return dict(parsed)
    
    def _generate_summary_analytics(self, parsed_entries: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate summary statistics"""
        summary = {
            "total_entries": sum(len(entries) for entries in parsed_entries.values()),
            "entry_types": {},
            "overall_average": 0,
            "consistency_score": 0
        }
        
        total_value = 0
        total_count = 0
        
        for entry_type, entries in parsed_entries.items():
            if entries:
                values = [entry.get("value", 0) for entry in entries]
                avg_value = np.mean(values)
                
                summary["entry_types"][entry_type] = {
                    "count": len(entries),
                    "average": round(avg_value, 2),
                    "min": min(values),
                    "max": max(values),
                    "std_dev": round(np.std(values), 2)
                }
                
                total_value += sum(values)
                total_count += len(values)
        
        if total_count > 0:
            summary["overall_average"] = round(total_value / total_count, 2)
        
        # Calculate consistency score (percentage of days with entries)
        summary["consistency_score"] = self._calculate_consistency_score(parsed_entries)
        
        return summary
    
    def _generate_trend_analytics(self, parsed_entries: Dict[str, List[Dict[str, Any]]], timeframe: str) -> Dict[str, Any]:
        """Generate trend analysis"""
        trends = {
            "overall_trend": "stable",
            "trend_direction": "neutral",
            "trend_strength": 0,
            "periodic_patterns": {},
            "seasonal_effects": {}
        }
        
        # Analyze trends for each entry type
        for entry_type, entries in parsed_entries.items():
            if len(entries) >= 3:  # Need at least 3 entries for trend analysis
                values = [entry.get("value", 0) for entry in entries]
                dates = [datetime.fromisoformat(entry.get("created_at", "").replace("Z", "+00:00")) for entry in entries]
                
                # Sort by date
                sorted_data = sorted(zip(dates, values), key=lambda x: x[0])
                dates, values = zip(*sorted_data)
                
                # Calculate trend
                trend_info = self._calculate_trend(values)
                trends["periodic_patterns"][entry_type] = trend_info
        
        # Calculate overall trend
        if parsed_entries:
            all_values = []
            for entries in parsed_entries.values():
                all_values.extend([entry.get("value", 0) for entry in entries])
            
            if len(all_values) >= 3:
                overall_trend = self._calculate_trend(all_values)
                trends["overall_trend"] = overall_trend["trend"]
                trends["trend_direction"] = overall_trend["direction"]
                trends["trend_strength"] = overall_trend["strength"]
        
        return trends
    
    def _generate_pattern_analytics(self, parsed_entries: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate pattern analysis"""
        patterns = {
            "daily_patterns": {},
            "weekly_patterns": {},
            "correlations": {},
            "anomalies": []
        }
        
        # Analyze daily patterns
        daily_data = defaultdict(list)
        for entry_type, entries in parsed_entries.items():
            for entry in entries:
                date = datetime.fromisoformat(entry.get("created_at", "").replace("Z", "+00:00"))
                hour = date.hour
                daily_data[hour].append(entry.get("value", 0))
        
        for hour, values in daily_data.items():
            patterns["daily_patterns"][hour] = {
                "average": round(np.mean(values), 2),
                "count": len(values)
            }
        
        # Analyze weekly patterns
        weekly_data = defaultdict(list)
        for entry_type, entries in parsed_entries.items():
            for entry in entries:
                date = datetime.fromisoformat(entry.get("created_at", "").replace("Z", "+00:00"))
                weekday = date.weekday()
                weekly_data[weekday].append(entry.get("value", 0))
        
        for weekday, values in weekly_data.items():
            patterns["weekly_patterns"][weekday] = {
                "average": round(np.mean(values), 2),
                "count": len(values)
            }
        
        # Detect anomalies
        patterns["anomalies"] = self._detect_anomalies(parsed_entries)
        
        return patterns
    
    def _generate_insights(self, parsed_entries: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Generate insights from the data"""
        insights = []
        
        if not parsed_entries:
            insights.append("No wellness data available yet. Start tracking to get insights.")
            return insights
        
        # Analyze consistency
        consistency_score = self._calculate_consistency_score(parsed_entries)
        if consistency_score < 50:
            insights.append("Your wellness tracking consistency is low. Consider setting reminders.")
        elif consistency_score > 80:
            insights.append("Great job maintaining consistent wellness tracking!")
        
        # Analyze trends
        for entry_type, entries in parsed_entries.items():
            if len(entries) >= 3:
                values = [entry.get("value", 0) for entry in entries]
                recent_avg = np.mean(values[-3:])  # Last 3 entries
                overall_avg = np.mean(values)
                
                if recent_avg > overall_avg + 1:
                    insights.append(f"Your {entry_type.replace('_', ' ')} has been improving recently.")
                elif recent_avg < overall_avg - 1:
                    insights.append(f"Your {entry_type.replace('_', ' ')} has been declining recently.")
        
        # Analyze patterns
        if len(insights) < 3:
            insights.append("Consider tracking at consistent times for better pattern analysis.")
        
        return insights[:5]  # Limit to 5 insights
    
    def _generate_recommendations(self, parsed_entries: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Generate recommendations based on data"""
        recommendations = []
        
        if not parsed_entries:
            recommendations.append("Start with daily wellness check-ins to build a baseline.")
            return recommendations
        
        # Analyze each metric type
        for entry_type, entries in parsed_entries.items():
            if entries:
                values = [entry.get("value", 0) for entry in entries]
                avg_value = np.mean(values)
                
                if entry_type == "stress" and avg_value > 7:
                    recommendations.append("Consider stress management techniques like meditation or deep breathing.")
                elif entry_type == "energy" and avg_value < 4:
                    recommendations.append("Focus on improving sleep quality and regular exercise.")
                elif entry_type == "sleep_quality" and avg_value < 4:
                    recommendations.append("Establish a consistent bedtime routine and limit screen time before bed.")
                elif entry_type == "work_life_balance" and avg_value < 4:
                    recommendations.append("Set clear boundaries between work and personal time.")
        
        # Add general recommendations
        if len(recommendations) < 3:
            recommendations.append("Maintain regular wellness check-ins to track your progress.")
            recommendations.append("Consider using the AI chat for personalized wellness support.")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _generate_risk_assessment(self, parsed_entries: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate risk assessment"""
        risk_assessment = {
            "overall_risk": "low",
            "risk_factors": [],
            "risk_score": 0,
            "alerts": []
        }
        
        if not parsed_entries:
            return risk_assessment
        
        risk_score = 0
        risk_factors = []
        
        # Analyze each metric for risk factors
        for entry_type, entries in parsed_entries.items():
            if entries:
                values = [entry.get("value", 0) for entry in entries]
                recent_values = values[-3:] if len(values) >= 3 else values
                recent_avg = np.mean(recent_values)
                
                if entry_type == "stress" and recent_avg > 8:
                    risk_score += 30
                    risk_factors.append("High stress levels")
                    risk_assessment["alerts"].append("Consistently high stress levels detected")
                
                elif entry_type == "mood" and recent_avg < 3:
                    risk_score += 25
                    risk_factors.append("Low mood")
                    risk_assessment["alerts"].append("Persistently low mood detected")
                
                elif entry_type == "energy" and recent_avg < 3:
                    risk_score += 20
                    risk_factors.append("Low energy")
                
                elif entry_type == "sleep_quality" and recent_avg < 3:
                    risk_score += 15
                    risk_factors.append("Poor sleep quality")
        
        # Determine overall risk level
        if risk_score >= 50:
            risk_assessment["overall_risk"] = "high"
        elif risk_score >= 25:
            risk_assessment["overall_risk"] = "medium"
        else:
            risk_assessment["overall_risk"] = "low"
        
        risk_assessment["risk_score"] = min(risk_score, 100)
        risk_assessment["risk_factors"] = risk_factors
        
        return risk_assessment
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend direction and strength"""
        if len(values) < 2:
            return {"trend": "stable", "direction": "neutral", "strength": 0}
        
        # Simple linear trend calculation
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        # Determine trend direction
        if slope > 0.1:
            direction = "increasing"
            trend = "improving"
        elif slope < -0.1:
            direction = "decreasing"
            trend = "declining"
        else:
            direction = "stable"
            trend = "stable"
        
        # Calculate trend strength (0-1)
        strength = min(abs(slope) * 10, 1.0)
        
        return {
            "trend": trend,
            "direction": direction,
            "strength": round(strength, 2),
            "slope": round(slope, 3)
        }
    
    def _calculate_consistency_score(self, parsed_entries: Dict[str, List[Dict[str, Any]]]) -> float:
        """Calculate consistency score based on tracking frequency"""
        if not parsed_entries:
            return 0
        
        # Count unique days with entries
        unique_days = set()
        for entries in parsed_entries.values():
            for entry in entries:
                date_str = entry.get("created_at", "")[:10]  # Get date part only
                unique_days.add(date_str)
        
        # Calculate consistency as percentage of days with entries
        # Assuming 30 days for calculation
        consistency_score = (len(unique_days) / 30) * 100
        return min(consistency_score, 100)
    
    def _detect_anomalies(self, parsed_entries: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Detect anomalies in the data"""
        anomalies = []
        
        for entry_type, entries in parsed_entries.items():
            if len(entries) >= 5:  # Need enough data for anomaly detection
                values = [entry.get("value", 0) for entry in entries]
                mean = np.mean(values)
                std = np.std(values)
                
                for i, entry in enumerate(entries):
                    value = entry.get("value", 0)
                    z_score = abs((value - mean) / std) if std > 0 else 0
                    
                    if z_score > 2:  # More than 2 standard deviations
                        anomalies.append({
                            "entry_type": entry_type,
                            "entry_id": entry.get("id"),
                            "value": value,
                            "expected_range": f"{mean - 2*std:.1f} - {mean + 2*std:.1f}",
                            "z_score": round(z_score, 2),
                            "created_at": entry.get("created_at")
                        })
        
        return anomalies
    
    def _empty_analytics(self) -> Dict[str, Any]:
        """Return empty analytics structure"""
        return {
            "summary": {
                "total_entries": 0,
                "entry_types": {},
                "overall_average": 0,
                "consistency_score": 0
            },
            "trends": {
                "overall_trend": "stable",
                "trend_direction": "neutral",
                "trend_strength": 0,
                "periodic_patterns": {},
                "seasonal_effects": {}
            },
            "patterns": {
                "daily_patterns": {},
                "weekly_patterns": {},
                "correlations": {},
                "anomalies": []
            },
            "insights": ["No wellness data available yet. Start tracking to get insights."],
            "recommendations": ["Begin with daily wellness check-ins to build a baseline."],
            "risk_assessment": {
                "overall_risk": "low",
                "risk_factors": [],
                "risk_score": 0,
                "alerts": []
            }
        }
