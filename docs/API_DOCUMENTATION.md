# Enterprise Employee Wellness AI - API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Endpoints](#endpoints)
   - [Authentication](#authentication-endpoints)
   - [Wellness](#wellness-endpoints)
   - [Resources](#resources-endpoints)
   - [Analytics](#analytics-endpoints)
   - [Users](#users-endpoints)
   - [Notifications](#notifications-endpoints)
   - [Compliance](#compliance-endpoints)
   - [Team Management](#team-management-endpoints)
   - [System Administration](#system-administration-endpoints)

## Overview

The Enterprise Employee Wellness AI API provides comprehensive endpoints for managing employee wellness, organizational health analytics, and administrative functions. The API follows RESTful principles and uses JSON for data exchange.

### API Version
- Current Version: `v1`
- Base URL: `https://api.enterprise-wellness.ai/v1`

### Content Type
All requests and responses use `application/json` content type.

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Token Types
- **Access Token**: Short-lived (15 minutes) for API requests
- **Refresh Token**: Long-lived (7 days) for token renewal

## Base URL

### Development
```
http://localhost:8000/api
```

### Production
```
https://api.enterprise-wellness.ai/api
```

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error details"
    },
    "timestamp": "2024-01-25T10:30:00Z"
  }
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Internal Server Error

## Rate Limiting

- **Standard Users**: 100 requests per minute
- **Premium Users**: 500 requests per minute
- **Admin Users**: 1000 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1643107200
```

## Endpoints

### Authentication Endpoints

#### POST /auth/login
Authenticate user and receive access token.

**Request Body:**
```json
{
  "email": "user@company.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "user_123",
    "email": "user@company.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "employee",
    "department": "Engineering",
    "team_id": "team_456"
  }
}
```

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "newuser@company.com",
  "password": "securepassword",
  "first_name": "Jane",
  "last_name": "Smith",
  "company": "Acme Corp",
  "phone": "+1234567890",
  "department": "Marketing",
  "position": "Marketing Manager"
}
```

#### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### POST /auth/change-password
Change user password.

**Request Body:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newsecurepassword"
}
```

#### GET /auth/me
Get current user information.

**Response:**
```json
{
  "id": "user_123",
  "email": "user@company.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "employee",
  "department": "Engineering",
  "team_id": "team_456",
  "preferences": {
    "check_in_frequency": "daily",
    "notification_settings": {
      "email": true,
      "push": true,
      "slack": false
    }
  }
}
```

### Wellness Endpoints

#### POST /wellness/check-in
Submit a comprehensive wellness check-in.

**Request Body:**
```json
{
  "mood_score": 7,
  "stress_level": 5,
  "energy_level": 6,
  "sleep_quality": 8,
  "work_life_balance": 6,
  "notes": "Feeling productive today, but a bit tired from late meeting",
  "tags": ["productive", "tired", "meeting"]
}
```

**Response:**
```json
{
  "id": "checkin_789",
  "user_id": "user_123",
  "timestamp": "2024-01-25T10:30:00Z",
  "overall_score": 6.4,
  "risk_level": "low",
  "recommendations": [
    {
      "type": "resource",
      "title": "Power Nap Techniques",
      "description": "Learn effective power nap strategies",
      "url": "/resources/power-nap-techniques"
    }
  ],
  "ai_insights": {
    "sentiment": "positive",
    "stress_indicators": ["fatigue"],
    "suggestions": ["Consider taking short breaks", "Practice deep breathing"]
  }
}
```

#### POST /wellness/mood
Quick mood tracking.

**Request Body:**
```json
{
  "mood": "happy",
  "intensity": 8
}
```

#### GET /wellness/history
Get user's wellness history.

**Query Parameters:**
- `start_date` (optional): Start date filter (YYYY-MM-DD)
- `end_date` (optional): End date filter (YYYY-MM-DD)
- `limit` (optional): Number of records to return (default: 50)
- `offset` (optional): Number of records to skip (default: 0)

**Response:**
```json
{
  "entries": [
    {
      "id": "checkin_789",
      "timestamp": "2024-01-25T10:30:00Z",
      "mood_score": 7,
      "stress_level": 5,
      "overall_score": 6.4,
      "risk_level": "low"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

#### GET /wellness/analytics
Get comprehensive wellness analytics.

**Query Parameters:**
- `timeframe` (optional): Time period for analytics (week, month, quarter, year)
- `metrics` (optional): Comma-separated list of metrics to include

**Response:**
```json
{
  "overview": {
    "average_mood": 6.8,
    "average_stress": 4.2,
    "wellness_trend": "improving",
    "risk_level": "low"
  },
  "trends": {
    "mood_trend": [6.5, 6.7, 6.8, 7.0, 6.9, 6.8, 7.1],
    "stress_trend": [4.5, 4.3, 4.2, 4.1, 4.3, 4.2, 4.0]
  },
  "insights": [
    {
      "type": "pattern",
      "title": "Mood improves on Wednesdays",
      "description": "Your mood tends to be 15% better on Wednesdays",
      "confidence": 0.85
    }
  ]
}
```

#### POST /wellness/conversation
Send message to AI wellness companion.

**Request Body:**
```json
{
  "message": "I'm feeling overwhelmed with my workload",
  "context": {
    "current_task": "Project deadline",
    "time_of_day": "afternoon"
  }
}
```

**Response:**
```json
{
  "response": "I understand that feeling overwhelmed can be really challenging. Let's break this down together. What specific aspects of your workload are causing the most stress?",
  "sentiment": "concerned",
  "risk_level": "medium",
  "suggestions": [
    "Take a 5-minute breathing break",
    "Prioritize your tasks",
    "Consider talking to your manager about workload"
  ],
  "follow_up_questions": [
    "What's the most urgent deadline you're facing?",
    "Have you tried breaking down your tasks into smaller chunks?"
  ]
}
```

### Resources Endpoints

#### GET /resources
Get wellness resources.

**Query Parameters:**
- `category` (optional): Filter by category
- `difficulty` (optional): Filter by difficulty level
- `duration` (optional): Filter by duration (in minutes)
- `search` (optional): Search in title and description
- `limit` (optional): Number of resources to return
- `offset` (optional): Number of resources to skip

**Response:**
```json
{
  "resources": [
    {
      "id": "resource_123",
      "title": "Mindfulness Meditation for Beginners",
      "description": "A comprehensive guide to mindfulness meditation",
      "category": "mindfulness",
      "difficulty_level": "beginner",
      "duration_minutes": 15,
      "tags": ["meditation", "stress-relief", "beginner-friendly"],
      "rating": 4.7,
      "review_count": 124,
      "completion_rate": 78,
      "author": "Dr. Sarah Johnson",
      "media_type": "video",
      "thumbnail_url": "https://example.com/thumbnail.jpg"
    }
  ],
  "pagination": {
    "total": 250,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

#### GET /resources/{resource_id}
Get specific resource details.

**Response:**
```json
{
  "id": "resource_123",
  "title": "Mindfulness Meditation for Beginners",
  "description": "A comprehensive guide to mindfulness meditation",
  "content": {
    "overview": "This resource provides step-by-step guidance...",
    "instructions": ["Find a quiet space", "Sit comfortably", "Focus on your breath"],
    "benefits": ["Reduces stress", "Improves focus", "Enhances well-being"],
    "tips": ["Start with 5 minutes", "Be patient with yourself"]
  },
  "category": "mindfulness",
  "difficulty_level": "beginner",
  "duration_minutes": 15,
  "tags": ["meditation", "stress-relief"],
  "rating": 4.7,
  "review_count": 124,
  "completion_rate": 78,
  "author": {
    "name": "Dr. Sarah Johnson",
    "credentials": "Licensed Clinical Psychologist",
    "bio": "Dr. Johnson has over 15 years of experience..."
  },
  "media": {
    "type": "video",
    "url": "https://example.com/video.mp4",
    "thumbnail": "https://example.com/thumbnail.jpg",
    "transcript": "Welcome to mindfulness meditation..."
  },
  "accessibility": {
    "has_subtitles": true,
    "has_transcript": true,
    "keyboard_navigable": true
  },
  "related_resources": [
    {
      "id": "resource_456",
      "title": "Breathing Exercises",
      "category": "stress-management"
    }
  ]
}
```

#### POST /resources/{resource_id}/interact
Record user interaction with resource.

**Request Body:**
```json
{
  "interaction_type": "view",
  "duration_seconds": 300,
  "progress_percentage": 75,
  "rating": 5,
  "feedback": "Very helpful resource!"
}
```

### Analytics Endpoints

#### GET /analytics/organizational-health
Get organizational health analytics (HR/Admin only).

**Query Parameters:**
- `timeframe` (optional): Time period for analytics
- `department` (optional): Filter by department
- `team` (optional): Filter by team

**Response:**
```json
{
  "overview": {
    "total_employees": 1250,
    "active_users": 1180,
    "average_wellness_score": 7.2,
    "risk_distribution": {
      "low_risk": 65,
      "medium_risk": 25,
      "high_risk": 10
    }
  },
  "trends": {
    "wellness_trend": [7.0, 7.1, 7.2, 7.3, 7.2, 7.1, 7.2],
    "engagement_trend": [75, 76, 77, 78, 77, 76, 77],
    "stress_trend": [4.2, 4.1, 4.0, 3.9, 4.0, 4.1, 4.0]
  },
  "department_insights": [
    {
      "department": "Engineering",
      "wellness_score": 7.5,
      "risk_level": "low",
      "engagement_rate": 85,
      "trend": "improving"
    }
  ],
  "risk_factors": [
    {
      "factor": "High Workload",
      "affected_employees": 45,
      "risk_level": "medium",
      "trend": "stable"
    }
  ]
}
```

#### GET /analytics/team/{team_id}
Get team-specific analytics.

**Response:**
```json
{
  "team_info": {
    "id": "team_456",
    "name": "Product Development",
    "manager": "Jane Smith",
    "member_count": 12
  },
  "wellness_metrics": {
    "average_score": 7.3,
    "risk_level": "low",
    "engagement_rate": 88,
    "participation_rate": 92
  },
  "individual_insights": [
    {
      "user_id": "user_123",
      "name": "John Doe",
      "wellness_score": 7.5,
      "risk_level": "low",
      "trend": "improving",
      "last_checkin": "2024-01-25T10:30:00Z"
    }
  ],
  "recommendations": [
    {
      "type": "team_activity",
      "title": "Team Wellness Challenge",
      "description": "Consider implementing a team wellness challenge",
      "impact": "high"
    }
  ]
}
```

#### GET /analytics/risk-assessment
Get risk assessment analytics.

**Response:**
```json
{
  "overall_risk": {
    "level": "medium",
    "score": 65,
    "trend": "stable"
  },
  "risk_factors": [
    {
      "factor": "High Workload",
      "risk_level": "high",
      "score": 85,
      "trend": "increasing",
      "affected_employees": 23,
      "recommendations": [
        "Workload redistribution",
        "Time management training"
      ]
    }
  ],
  "interventions": [
    {
      "id": "intervention_123",
      "type": "immediate",
      "title": "Workload Assessment",
      "priority": "high",
      "status": "pending",
      "assigned_to": "Manager",
      "due_date": "2024-02-01"
    }
  ]
}
```

### Users Endpoints

#### GET /users
Get users list (Admin only).

**Query Parameters:**
- `department` (optional): Filter by department
- `role` (optional): Filter by role
- `status` (optional): Filter by status (active, inactive)
- `limit` (optional): Number of users to return
- `offset` (optional): Number of users to skip

**Response:**
```json
{
  "users": [
    {
      "id": "user_123",
      "email": "user@company.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "employee",
      "department": "Engineering",
      "team_id": "team_456",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z",
      "last_login": "2024-01-25T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 1250,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

#### PUT /users/profile
Update user profile.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "department": "Engineering",
  "position": "Senior Developer",
  "preferences": {
    "check_in_frequency": "daily",
    "notification_settings": {
      "email": true,
      "push": true,
      "slack": false
    }
  }
}
```

### Notifications Endpoints

#### GET /notifications
Get user notifications.

**Query Parameters:**
- `status` (optional): Filter by status (read, unread)
- `type` (optional): Filter by type
- `limit` (optional): Number of notifications to return

**Response:**
```json
{
  "notifications": [
    {
      "id": "notification_123",
      "type": "wellness_reminder",
      "title": "Time for your daily check-in",
      "message": "Take a moment to reflect on your wellness",
      "status": "unread",
      "created_at": "2024-01-25T10:00:00Z",
      "action_url": "/wellness/check-in"
    }
  ]
}
```

#### POST /notifications/{notification_id}/mark-read
Mark notification as read.

### Compliance Endpoints

#### GET /compliance/audit-trail
Get audit trail (Admin only).

**Query Parameters:**
- `start_date` (optional): Start date filter
- `end_date` (optional): End date filter
- `action_type` (optional): Filter by action type
- `user_id` (optional): Filter by user

**Response:**
```json
{
  "audit_entries": [
    {
      "id": "audit_123",
      "timestamp": "2024-01-25T10:30:00Z",
      "user_id": "user_123",
      "action": "wellness_checkin",
      "resource": "wellness_entries",
      "details": {
        "entry_id": "checkin_789",
        "risk_level": "low"
      },
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0..."
    }
  ]
}
```

#### GET /compliance/privacy-consent
Get user privacy consent status.

**Response:**
```json
{
  "consent_status": {
    "data_collection": true,
    "analytics": true,
    "third_party_sharing": false,
    "last_updated": "2024-01-01T00:00:00Z"
  },
  "data_rights": {
    "data_export": true,
    "data_deletion": true,
    "data_correction": true
  }
}
```

### Team Management Endpoints

#### GET /teams
Get teams list.

**Response:**
```json
{
  "teams": [
    {
      "id": "team_456",
      "name": "Product Development",
      "manager_id": "user_789",
      "member_count": 12,
      "department": "Engineering",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### GET /teams/{team_id}
Get team details.

**Response:**
```json
{
  "id": "team_456",
  "name": "Product Development",
  "manager": {
    "id": "user_789",
    "name": "Jane Smith",
    "email": "jane@company.com"
  },
  "members": [
    {
      "id": "user_123",
      "name": "John Doe",
      "email": "john@company.com",
      "role": "employee",
      "joined_at": "2024-01-01T00:00:00Z"
    }
  ],
  "wellness_metrics": {
    "average_score": 7.3,
    "risk_level": "low",
    "engagement_rate": 88
  }
}
```

### System Administration Endpoints

#### GET /admin/metrics
Get system metrics (Admin only).

**Response:**
```json
{
  "system_health": {
    "status": "healthy",
    "uptime": 99.9,
    "response_time": 150
  },
  "user_metrics": {
    "total_users": 1250,
    "active_users": 1180,
    "new_users_this_month": 45
  },
  "wellness_metrics": {
    "total_checkins": 15420,
    "average_score": 7.2,
    "risk_detections": 23
  },
  "ai_metrics": {
    "conversations_processed": 8920,
    "average_response_time": 2.3,
    "accuracy_rate": 94.5
  }
}
```

#### GET /admin/health-check
System health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-25T10:30:00Z",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "ai_services": "healthy",
    "external_integrations": "healthy"
  },
  "performance": {
    "response_time": 150,
    "memory_usage": 65,
    "cpu_usage": 45
  }
}
```

## SDKs and Libraries

### Python SDK
```python
from wellness_ai import WellnessAIClient

client = WellnessAIClient(api_key="your-api-key")

# Submit wellness check-in
checkin = client.wellness.check_in(
    mood_score=7,
    stress_level=5,
    energy_level=6
)

# Get analytics
analytics = client.analytics.get_organizational_health()
```

### JavaScript SDK
```javascript
import { WellnessAI } from '@enterprise-wellness/sdk';

const client = new WellnessAI({ apiKey: 'your-api-key' });

// Submit wellness check-in
const checkin = await client.wellness.checkIn({
  moodScore: 7,
  stressLevel: 5,
  energyLevel: 6
});

// Get analytics
const analytics = await client.analytics.getOrganizationalHealth();
```

## Webhooks

### Supported Events
- `wellness.checkin.created`
- `wellness.risk.detected`
- `user.registered`
- `team.created`
- `intervention.assigned`

### Webhook Configuration
```json
{
  "url": "https://your-app.com/webhooks/wellness",
  "events": ["wellness.checkin.created", "wellness.risk.detected"],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload Example
```json
{
  "event": "wellness.checkin.created",
  "timestamp": "2024-01-25T10:30:00Z",
  "data": {
    "user_id": "user_123",
    "checkin_id": "checkin_789",
    "risk_level": "medium",
    "overall_score": 6.4
  }
}
```

## Rate Limits and Quotas

### Free Tier
- 1,000 API calls per month
- 100 users
- Basic analytics

### Professional Tier
- 50,000 API calls per month
- 1,000 users
- Advanced analytics
- Priority support

### Enterprise Tier
- Unlimited API calls
- Unlimited users
- Custom integrations
- Dedicated support

## Support

For API support and questions:
- **Documentation**: [docs.enterprise-wellness.ai](https://docs.enterprise-wellness.ai)
- **API Status**: [status.enterprise-wellness.ai](https://status.enterprise-wellness.ai)
- **Support Email**: api-support@enterprise-wellness.ai
- **Developer Community**: [community.enterprise-wellness.ai](https://community.enterprise-wellness.ai)
