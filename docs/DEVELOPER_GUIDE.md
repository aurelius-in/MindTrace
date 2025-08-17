# Enterprise Employee Wellness AI - Developer Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [Code Quality & Standards](#code-quality--standards)
7. [API Development](#api-development)
8. [Frontend Development](#frontend-development)
9. [Database & Migrations](#database--migrations)
10. [AI Integration](#ai-integration)
11. [Security & Privacy](#security--privacy)
12. [Performance Optimization](#performance-optimization)
13. [Contributing](#contributing)
14. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm/yarn
- **Docker Desktop** 4.0+
- **Git** 2.30+
- **PostgreSQL** 14+ (or Docker)
- **Redis** 6+ (or Docker)

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-org/enterprise-wellness-ai.git
cd enterprise-wellness-ai
```

2. **Set up environment**
```bash
# Copy environment template
cp .env.example .env

# Install dependencies
make install

# Start development services
make dev-up
```

3. **Initialize database**
```bash
make db-init
make db-migrate
make db-seed
```

4. **Start development servers**
```bash
make dev-start
```

## Development Environment Setup

### Backend Setup

1. **Create Python virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. **Configure environment variables**
```bash
# backend/.env
DATABASE_URL=postgresql://wellness_user:wellness_pass@localhost:5432/wellness_db
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

4. **Run backend development server**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Node.js dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment variables**
```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

3. **Start frontend development server**
```bash
npm start
```

### Database Setup

1. **Start PostgreSQL and Redis**
```bash
docker-compose -f docker-compose.dev.yml up -d postgres redis
```

2. **Run database migrations**
```bash
cd backend
alembic upgrade head
```

3. **Seed development data**
```bash
python -m scripts.seed_data
```

## Project Structure

```
enterprise-wellness-ai/
├── backend/                    # FastAPI backend
│   ├── api/                   # API routes
│   │   ├── routes/           # Route handlers
│   │   └── middleware/       # Custom middleware
│   ├── agents/               # AI agent implementations
│   ├── database/             # Database models and connection
│   ├── services/             # Business logic services
│   ├── utils/                # Utility functions
│   ├── config/               # Configuration management
│   ├── tests/                # Backend tests
│   └── main.py              # FastAPI application entry point
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   ├── pages/           # Page components
│   │   ├── store/           # Redux store and slices
│   │   ├── services/        # API service layer
│   │   ├── hooks/           # Custom React hooks
│   │   └── utils/           # Frontend utilities
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── docs/                     # Documentation
├── k8s/                      # Kubernetes manifests
├── helm/                     # Helm charts
├── monitoring/               # Monitoring configuration
├── scripts/                  # Utility scripts
└── docker-compose.dev.yml    # Development environment
```

## Development Workflow

### Git Workflow

1. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make changes and commit**
```bash
git add .
git commit -m "feat: add new wellness check-in feature"
```

3. **Push and create pull request**
```bash
git push origin feature/your-feature-name
# Create PR on GitHub
```

### Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Examples:**
```bash
git commit -m "feat(wellness): add mood tracking functionality"
git commit -m "fix(auth): resolve JWT token expiration issue"
git commit -m "docs(api): update authentication endpoint documentation"
```

### Development Commands

```bash
# Start development environment
make dev-up

# Stop development environment
make dev-down

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Check code quality
make quality

# Build for production
make build

# Deploy to staging
make deploy-staging

# Deploy to production
make deploy-production
```

## Testing

### Backend Testing

1. **Unit Tests**
```bash
cd backend
pytest tests/unit/ -v
```

2. **Integration Tests**
```bash
pytest tests/integration/ -v
```

3. **API Tests**
```bash
pytest tests/api/ -v
```

4. **Coverage Report**
```bash
pytest --cov=app --cov-report=html
```

### Frontend Testing

1. **Unit Tests**
```bash
cd frontend
npm test
```

2. **Integration Tests**
```bash
npm run test:integration
```

3. **E2E Tests**
```bash
npm run test:e2e
```

### Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── test_services.py    # Service layer tests
│   ├── test_models.py      # Database model tests
│   └── test_utils.py       # Utility function tests
├── integration/            # Integration tests
│   ├── test_database.py    # Database integration tests
│   └── test_external.py    # External service tests
├── api/                    # API endpoint tests
│   ├── test_auth.py        # Authentication tests
│   ├── test_wellness.py    # Wellness endpoint tests
│   └── test_analytics.py   # Analytics endpoint tests
└── fixtures/               # Test data and fixtures
    ├── users.json          # User test data
    └── wellness_data.json  # Wellness test data
```

### Writing Tests

#### Backend Test Example
```python
# tests/unit/test_wellness_service.py
import pytest
from unittest.mock import Mock, patch
from backend.services.wellness_service import WellnessService

class TestWellnessService:
    @pytest.fixture
    def wellness_service(self):
        return WellnessService()
    
    @pytest.fixture
    def mock_user(self):
        return {
            "id": "user_123",
            "email": "test@example.com",
            "role": "employee"
        }
    
    def test_create_wellness_checkin(self, wellness_service, mock_user):
        # Arrange
        checkin_data = {
            "mood_score": 7,
            "stress_level": 5,
            "energy_level": 6
        }
        
        # Act
        result = wellness_service.create_wellness_checkin(
            user_id=mock_user["id"],
            data=checkin_data
        )
        
        # Assert
        assert result.user_id == mock_user["id"]
        assert result.mood_score == 7
        assert result.overall_score > 0
```

#### Frontend Test Example
```typescript
// frontend/src/components/WellnessCheckIn.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { store } from '../store';
import WellnessCheckIn from './WellnessCheckIn';

describe('WellnessCheckIn', () => {
  it('should submit wellness check-in form', async () => {
    // Arrange
    render(
      <Provider store={store}>
        <WellnessCheckIn />
      </Provider>
    );
    
    // Act
    fireEvent.change(screen.getByLabelText(/mood score/i), {
      target: { value: '7' }
    });
    fireEvent.click(screen.getByText(/submit/i));
    
    // Assert
    expect(await screen.findByText(/check-in submitted/i)).toBeInTheDocument();
  });
});
```

## Code Quality & Standards

### Python Standards

1. **Code Formatting**
```bash
# Format with black
black backend/

# Sort imports with isort
isort backend/

# Check with flake8
flake8 backend/
```

2. **Type Hints**
```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class WellnessCheckIn(BaseModel):
    mood_score: int
    stress_level: int
    energy_level: int
    notes: Optional[str] = None

def create_checkin(user_id: str, data: WellnessCheckIn) -> Dict[str, Any]:
    """Create a wellness check-in for a user."""
    pass
```

3. **Documentation**
```python
def analyze_wellness_trends(user_id: str, timeframe: str = "30d") -> Dict[str, Any]:
    """
    Analyze wellness trends for a user over a specified timeframe.
    
    Args:
        user_id: The user's unique identifier
        timeframe: Time period for analysis (e.g., "7d", "30d", "90d")
    
    Returns:
        Dictionary containing trend analysis and insights
        
    Raises:
        UserNotFoundError: If user_id doesn't exist
        InvalidTimeframeError: If timeframe is invalid
    """
    pass
```

### JavaScript/TypeScript Standards

1. **Code Formatting**
```bash
# Format with Prettier
npm run format

# Lint with ESLint
npm run lint

# Type checking with TypeScript
npm run type-check
```

2. **TypeScript Interfaces**
```typescript
interface WellnessCheckIn {
  moodScore: number;
  stressLevel: number;
  energyLevel: number;
  notes?: string;
  timestamp: Date;
}

interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

const submitCheckIn = async (data: WellnessCheckIn): Promise<ApiResponse<WellnessCheckIn>> => {
  // Implementation
};
```

3. **Component Documentation**
```typescript
/**
 * WellnessCheckIn component for submitting daily wellness check-ins
 * 
 * @param onSubmit - Callback function called when check-in is submitted
 * @param initialData - Initial data to populate the form
 * @param disabled - Whether the form is disabled
 */
interface WellnessCheckInProps {
  onSubmit: (data: WellnessCheckIn) => void;
  initialData?: Partial<WellnessCheckIn>;
  disabled?: boolean;
}
```

## API Development

### Creating New Endpoints

1. **Define Pydantic models**
```python
# backend/api/models/wellness.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class WellnessCheckInRequest(BaseModel):
    mood_score: int = Field(..., ge=1, le=10, description="Mood score from 1-10")
    stress_level: int = Field(..., ge=1, le=10, description="Stress level from 1-10")
    energy_level: int = Field(..., ge=1, le=10, description="Energy level from 1-10")
    notes: Optional[str] = Field(None, max_length=1000, description="Optional notes")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")

class WellnessCheckInResponse(BaseModel):
    id: str
    user_id: str
    timestamp: datetime
    overall_score: float
    risk_level: str
    recommendations: List[dict]
```

2. **Create route handler**
```python
# backend/api/routes/wellness.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.utils.auth import get_current_user
from backend.services.wellness_service import WellnessService
from backend.api.models.wellness import WellnessCheckInRequest, WellnessCheckInResponse

router = APIRouter(prefix="/wellness", tags=["wellness"])

@router.post("/check-in", response_model=WellnessCheckInResponse)
async def create_wellness_checkin(
    checkin_data: WellnessCheckInRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a comprehensive wellness check-in.
    
    This endpoint allows users to submit their daily wellness check-in
    with mood, stress, and energy levels, along with optional notes.
    """
    try:
        wellness_service = WellnessService()
        result = await wellness_service.create_wellness_checkin(
            user_id=current_user.id,
            data=checkin_data.dict()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

3. **Add to main router**
```python
# backend/main.py
from backend.api.routes import wellness

app.include_router(wellness.router, prefix="/api")
```

### API Testing

```python
# tests/api/test_wellness.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_wellness_checkin():
    # Arrange
    checkin_data = {
        "mood_score": 7,
        "stress_level": 5,
        "energy_level": 6,
        "notes": "Feeling good today"
    }
    
    # Act
    response = client.post(
        "/api/wellness/check-in",
        json=checkin_data,
        headers={"Authorization": "Bearer test-token"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] > 0
    assert data["risk_level"] in ["low", "medium", "high"]
```

## Frontend Development

### Creating New Components

1. **Component Structure**
```typescript
// frontend/src/components/Wellness/WellnessCheckIn.tsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  TextField,
  Slider,
  Alert
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import { submitWellnessCheckIn } from '../../store/slices/wellnessSlice';
import { addNotification } from '../../store/slices/uiSlice';

interface WellnessCheckInProps {
  onSubmit?: () => void;
  initialData?: Partial<WellnessCheckInData>;
}

const WellnessCheckIn: React.FC<WellnessCheckInProps> = ({
  onSubmit,
  initialData
}) => {
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state: RootState) => state.wellness);
  
  const [formData, setFormData] = useState({
    moodScore: initialData?.moodScore || 5,
    stressLevel: initialData?.stressLevel || 5,
    energyLevel: initialData?.energyLevel || 5,
    notes: initialData?.notes || ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await dispatch(submitWellnessCheckIn(formData)).unwrap();
      dispatch(addNotification({
        type: 'success',
        title: 'Check-in Submitted',
        message: 'Your wellness check-in has been recorded.'
      }));
      onSubmit?.();
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Submission Failed',
        message: 'Failed to submit wellness check-in.'
      }));
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Daily Wellness Check-in
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit}>
          <Typography gutterBottom>How are you feeling today?</Typography>
          <Slider
            value={formData.moodScore}
            onChange={(_, value) => setFormData(prev => ({ ...prev, moodScore: value as number }))}
            min={1}
            max={10}
            marks
            valueLabelDisplay="auto"
          />
          
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Additional Notes"
            value={formData.notes}
            onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
            margin="normal"
          />
          
          <Button
            type="submit"
            variant="contained"
            disabled={loading}
            fullWidth
          >
            {loading ? 'Submitting...' : 'Submit Check-in'}
          </Button>
        </Box>
        
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default WellnessCheckIn;
```

2. **Redux Slice**
```typescript
// frontend/src/store/slices/wellnessSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { wellnessApi } from '../../services/api';

export const submitWellnessCheckIn = createAsyncThunk(
  'wellness/submitCheckIn',
  async (data: WellnessCheckInData) => {
    const response = await wellnessApi.submitCheckIn(data);
    return response.data;
  }
);

const wellnessSlice = createSlice({
  name: 'wellness',
  initialState: {
    checkIns: [],
    loading: false,
    error: null
  },
  reducers: {
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(submitWellnessCheckIn.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(submitWellnessCheckIn.fulfilled, (state, action) => {
        state.loading = false;
        state.checkIns.push(action.payload);
      })
      .addCase(submitWellnessCheckIn.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export const { clearError } = wellnessSlice.actions;
export default wellnessSlice.reducer;
```

## Database & Migrations

### Creating Database Models

```python
# backend/database/models/wellness.py
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.base import Base

class WellnessEntry(Base):
    __tablename__ = "wellness_entries"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    mood_score = Column(Integer, nullable=False)
    stress_level = Column(Integer, nullable=False)
    energy_level = Column(Integer, nullable=False)
    sleep_quality = Column(Integer)
    work_life_balance = Column(Integer)
    notes = Column(Text)
    tags = Column(Text)  # JSON string
    overall_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="wellness_entries")
    recommendations = relationship("WellnessRecommendation", back_populates="entry")
```

### Creating Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "Add wellness entries table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Migration Example

```python
# backend/alembic/versions/001_add_wellness_entries.py
"""Add wellness entries table

Revision ID: 001
Revises: 
Create Date: 2024-01-25 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'wellness_entries',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('mood_score', sa.Integer(), nullable=False),
        sa.Column('stress_level', sa.Integer(), nullable=False),
        sa.Column('energy_level', sa.Integer(), nullable=False),
        sa.Column('sleep_quality', sa.Integer(), nullable=True),
        sa.Column('work_life_balance', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', sa.Text(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=False),
        sa.Column('risk_level', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wellness_entries_id'), 'wellness_entries', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_wellness_entries_id'), table_name='wellness_entries')
    op.drop_table('wellness_entries')
```

## AI Integration

### Creating AI Agents

```python
# backend/agents/wellness_companion.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import openai
from backend.config.settings import settings

class WellnessCompanionAgent:
    def __init__(self):
        self.model = "gpt-4"
        self.system_prompt = """
        You are a compassionate AI wellness companion designed to support employees 
        in their mental health and well-being journey. Your role is to:
        
        1. Provide empathetic and supportive responses
        2. Offer practical wellness advice and resources
        3. Identify potential risk factors and escalate when necessary
        4. Maintain professional boundaries while being warm and approachable
        
        Always prioritize user safety and well-being.
        """
    
    async def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a response to user wellness concerns."""
        
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            if context:
                context_prompt = f"Context: {context}"
                messages.insert(1, {"role": "system", "content": context_prompt})
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Analyze sentiment and risk
            risk_analysis = await self._analyze_risk(user_message, ai_response)
            
            return {
                "response": ai_response,
                "sentiment": risk_analysis["sentiment"],
                "risk_level": risk_analysis["risk_level"],
                "suggestions": risk_analysis["suggestions"],
                "escalation_needed": risk_analysis["escalation_needed"]
            }
            
        except Exception as e:
            return {
                "response": "I'm having trouble processing your message right now. Please try again later.",
                "error": str(e),
                "risk_level": "unknown"
            }
    
    async def _analyze_risk(self, user_message: str, ai_response: str) -> Dict[str, Any]:
        """Analyze user message for risk factors."""
        
        risk_keywords = [
            "suicide", "kill myself", "end it all", "no reason to live",
            "self-harm", "cut myself", "hurt myself", "want to die"
        ]
        
        user_message_lower = user_message.lower()
        
        # Check for immediate risk
        for keyword in risk_keywords:
            if keyword in user_message_lower:
                return {
                    "sentiment": "distressed",
                    "risk_level": "critical",
                    "suggestions": ["Please contact a mental health professional immediately"],
                    "escalation_needed": True
                }
        
        # Basic sentiment analysis
        negative_words = ["sad", "depressed", "anxious", "stressed", "overwhelmed", "hopeless"]
        positive_words = ["happy", "good", "great", "excited", "optimistic", "hopeful"]
        
        negative_count = sum(1 for word in negative_words if word in user_message_lower)
        positive_count = sum(1 for word in positive_words if word in user_message_lower)
        
        if negative_count > positive_count:
            return {
                "sentiment": "negative",
                "risk_level": "medium",
                "suggestions": ["Consider talking to a counselor", "Practice self-care activities"],
                "escalation_needed": False
            }
        else:
            return {
                "sentiment": "positive",
                "risk_level": "low",
                "suggestions": ["Keep up the great work!", "Continue your wellness practices"],
                "escalation_needed": False
            }
```

### Using AI Agents in Services

```python
# backend/services/wellness_service.py
from backend.agents.wellness_companion import WellnessCompanionAgent
from backend.utils.privacy import PrivacyManager

class WellnessService:
    def __init__(self):
        self.companion_agent = WellnessCompanionAgent()
        self.privacy_manager = PrivacyManager()
    
    async def send_conversation_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """Send a message to the AI wellness companion."""
        
        # Apply privacy controls
        anonymized_message = self.privacy_manager.anonymize_text(message)
        
        # Get user context
        user_context = await self._get_user_context(user_id)
        
        # Generate AI response
        ai_response = await self.companion_agent.generate_response(
            anonymized_message, 
            context=user_context
        )
        
        # Log conversation (with privacy controls)
        await self._log_conversation(user_id, message, ai_response)
        
        return ai_response
```

## Security & Privacy

### Privacy Controls

```python
# backend/utils/privacy.py
import re
import hashlib
from typing import Dict, Any

class PrivacyManager:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        self.name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    
    def anonymize_text(self, text: str) -> str:
        """Anonymize sensitive information in text."""
        
        # Anonymize emails
        text = re.sub(self.email_pattern, '[EMAIL]', text)
        
        # Anonymize phone numbers
        text = re.sub(self.phone_pattern, '[PHONE]', text)
        
        # Anonymize names (basic)
        text = re.sub(self.name_pattern, '[NAME]', text)
        
        return text
    
    def hash_identifier(self, identifier: str) -> str:
        """Hash identifiers for privacy."""
        return hashlib.sha256(identifier.encode()).hexdigest()
    
    def apply_privacy_controls(self, data: Dict[str, Any], user_consent: Dict[str, bool]) -> Dict[str, Any]:
        """Apply privacy controls based on user consent."""
        
        if not user_consent.get('data_collection', False):
            return {'error': 'Data collection not consented'}
        
        if not user_consent.get('analytics', False):
            # Remove analytics-related fields
            data.pop('analytics_data', None)
            data.pop('usage_patterns', None)
        
        return data
```

### Authentication & Authorization

```python
# backend/utils/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

security = HTTPBearer()

class AuthManager:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 15
    
    def create_access_token(self, data: dict) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
    auth_manager = AuthManager()
    payload = auth_manager.verify_token(credentials.credentials)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"id": user_id, "role": payload.get("role", "employee")}
```

## Performance Optimization

### Database Optimization

```python
# backend/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# Optimized database connection
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Connection pooling for async operations
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Caching Strategy

```python
# backend/utils/cache.py
import redis
import json
from typing import Any, Optional
from functools import wraps

class CacheManager:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.default_ttl = 3600  # 1 hour
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache."""
        try:
            ttl = ttl or self.default_ttl
            return self.redis_client.setex(key, ttl, json.dumps(value))
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            return bool(self.redis_client.delete(key))
        except Exception:
            return False

def cache_result(ttl: int = 3600):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_manager = CacheManager()
            
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
```

## Contributing

### Development Process

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Write tests**
5. **Update documentation**
6. **Submit a pull request**

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Security considerations addressed
- [ ] Performance impact considered
- [ ] Privacy controls implemented

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database status
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Reset database
docker-compose down
docker volume rm mindtrace_postgres_data
docker-compose up -d postgres
```

#### Redis Connection Issues
```bash
# Check Redis status
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

#### Frontend Build Issues
```bash
# Clear node modules and reinstall
rm -rf frontend/node_modules
cd frontend && npm install

# Clear build cache
npm run build -- --reset-cache
```

#### Backend Import Issues
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start with debug logging
uvicorn main:app --reload --log-level debug
```

### Performance Profiling

```python
# Backend profiling
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    return result
```

### Support

For development support:
- **Documentation**: [docs.enterprise-wellness.ai](https://docs.enterprise-wellness.ai)
- **GitHub Issues**: [github.com/your-org/enterprise-wellness-ai/issues](https://github.com/your-org/enterprise-wellness-ai/issues)
- **Developer Chat**: [discord.gg/wellness-dev](https://discord.gg/wellness-dev)
- **Email**: dev-support@enterprise-wellness.ai
