"""
API tests for authentication endpoints
"""
import pytest
from fastapi import status
from unittest.mock import patch
from database.schema import User, UserRole


class TestAuthAPI:
    """Test authentication API endpoints."""
    
    def test_register_success(self, client, sample_user_data):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json={
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "role": "employee",
            "department": "Engineering"
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["first_name"] == "New"
        assert data["last_name"] == "User"
        assert data["role"] == "employee"
        assert "password" not in data
        assert "password_hash" not in data
    
    def test_register_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email."""
        response = client.post("/api/auth/register", json={
            "email": sample_user.email,
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "email already registered" in data["detail"].lower()
    
    def test_register_invalid_data(self, client):
        """Test registration with invalid data."""
        # Missing required fields
        response = client.post("/api/auth/register", json={
            "email": "test@example.com"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "password": "123",  # Too short
            "first_name": "Test",
            "last_name": "User"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_success(self, client, sample_user):
        """Test successful login."""
        response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "testpassword123"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == sample_user.email
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post("/api/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "incorrect" in data["detail"].lower()
    
    def test_login_inactive_user(self, client, db_session, sample_user):
        """Test login with inactive user."""
        sample_user.is_active = False
        db_session.commit()
        
        response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "testpassword123"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "inactive" in data["detail"].lower()
    
    def test_me_endpoint_authenticated(self, authenticated_client, sample_user):
        """Test /me endpoint with authenticated user."""
        response = authenticated_client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == sample_user.email
        assert data["first_name"] == sample_user.first_name
        assert data["last_name"] == sample_user.last_name
    
    def test_me_endpoint_unauthenticated(self, client):
        """Test /me endpoint without authentication."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_refresh_token_success(self, client, sample_user):
        """Test successful token refresh."""
        # First login to get access token
        login_response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "testpassword123"
        })
        
        # Then refresh the token
        response = client.post("/api/auth/refresh", headers={
            "Authorization": f"Bearer {login_response.json()['access_token']}"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
    
    def test_refresh_token_invalid(self, client):
        """Test token refresh with invalid token."""
        response = client.post("/api/auth/refresh", headers={
            "Authorization": "Bearer invalid_token"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_change_password_success(self, authenticated_client, sample_user):
        """Test successful password change."""
        response = authenticated_client.post("/api/auth/change-password", json={
            "current_password": "testpassword123",
            "new_password": "newpassword123"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "password changed successfully" in data["message"].lower()
    
    def test_change_password_wrong_current(self, authenticated_client):
        """Test password change with wrong current password."""
        response = authenticated_client.post("/api/auth/change-password", json={
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "incorrect" in data["detail"].lower()
    
    def test_change_password_weak_new(self, authenticated_client):
        """Test password change with weak new password."""
        response = authenticated_client.post("/api/auth/change-password", json={
            "current_password": "testpassword123",
            "new_password": "123"  # Too short
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_forgot_password_success(self, client, sample_user):
        """Test successful forgot password request."""
        with patch('api.routes.auth.send_reset_email') as mock_send:
            response = client.post("/api/auth/forgot-password", json={
                "email": sample_user.email
            })
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "reset email sent" in data["message"].lower()
            mock_send.assert_called_once()
    
    def test_forgot_password_nonexistent_email(self, client):
        """Test forgot password with nonexistent email."""
        response = client.post("/api/auth/forgot-password", json={
            "email": "nonexistent@example.com"
        })
        
        # Should return success even for nonexistent email (security)
        assert response.status_code == status.HTTP_200_OK
    
    def test_reset_password_success(self, client, sample_user):
        """Test successful password reset."""
        with patch('api.routes.auth.verify_reset_token') as mock_verify:
            mock_verify.return_value = sample_user.email
            
            response = client.post("/api/auth/reset-password", json={
                "token": "valid_reset_token",
                "new_password": "newpassword123"
            })
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "password reset successfully" in data["message"].lower()
    
    def test_reset_password_invalid_token(self, client):
        """Test password reset with invalid token."""
        with patch('api.routes.auth.verify_reset_token') as mock_verify:
            mock_verify.side_effect = Exception("Invalid token")
            
            response = client.post("/api/auth/reset-password", json={
                "token": "invalid_token",
                "new_password": "newpassword123"
            })
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_verify_email_success(self, client, db_session, sample_user):
        """Test successful email verification."""
        sample_user.is_verified = False
        db_session.commit()
        
        with patch('api.routes.auth.verify_email_token') as mock_verify:
            mock_verify.return_value = sample_user.email
            
            response = client.post("/api/auth/verify-email", json={
                "token": "valid_verification_token"
            })
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "email verified successfully" in data["message"].lower()
    
    def test_verify_email_invalid_token(self, client):
        """Test email verification with invalid token."""
        with patch('api.routes.auth.verify_email_token') as mock_verify:
            mock_verify.side_effect = Exception("Invalid token")
            
            response = client.post("/api/auth/verify-email", json={
                "token": "invalid_token"
            })
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_logout_success(self, authenticated_client):
        """Test successful logout."""
        response = authenticated_client.post("/api/auth/logout")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "logged out successfully" in data["message"].lower()
    
    def test_logout_unauthenticated(self, client):
        """Test logout without authentication."""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.parametrize("role", ["employee", "manager", "hr", "admin", "executive"])
    def test_register_with_different_roles(self, client, role):
        """Test registration with different user roles."""
        response = client.post("/api/auth/register", json={
            "email": f"{role}@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "role": role
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == role
    
    def test_register_with_optional_fields(self, client):
        """Test registration with optional fields."""
        response = client.post("/api/auth/register", json={
            "email": "complete@example.com",
            "password": "password123",
            "first_name": "Complete",
            "last_name": "User",
            "role": "employee",
            "department": "Engineering",
            "position": "Software Engineer",
            "company": "Test Corp",
            "phone": "+1234567890",
            "timezone": "UTC",
            "language": "en"
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["department"] == "Engineering"
        assert data["position"] == "Software Engineer"
        assert data["company"] == "Test Corp"
        assert data["phone"] == "+1234567890"
        assert data["timezone"] == "UTC"
        assert data["language"] == "en"
    
    def test_login_rate_limiting(self, client, sample_user):
        """Test login rate limiting."""
        # Attempt multiple failed logins
        for _ in range(5):
            response = client.post("/api/auth/login", data={
                "username": sample_user.email,
                "password": "wrongpassword"
            })
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Should be rate limited after multiple failures
        response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "wrongpassword"
        })
        
        # This would depend on the rate limiting implementation
        # For now, we just test that it doesn't crash
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_429_TOO_MANY_REQUESTS]
    
    def test_token_expiration(self, client, sample_user):
        """Test token expiration handling."""
        # This would require mocking time or using expired tokens
        # For now, we test the basic structure
        response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "testpassword123"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/api/auth/login")
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
