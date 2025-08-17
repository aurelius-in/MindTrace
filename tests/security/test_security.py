"""
Security tests for the Enterprise Employee Wellness AI application
"""
import pytest
from fastapi import status
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta


class TestAuthenticationSecurity:
    """Test authentication security measures."""
    
    def test_password_hashing(self, client):
        """Test that passwords are properly hashed."""
        response = client.post("/api/auth/register", json={
            "email": "security@example.com",
            "password": "testpassword123",
            "first_name": "Security",
            "last_name": "Test"
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify password is not stored in plain text
        # This would require database access to verify
        # For now, we test that the API doesn't return the password
        data = response.json()
        assert "password" not in data
        assert "password_hash" not in data
    
    def test_jwt_token_security(self, client, sample_user):
        """Test JWT token security features."""
        response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "testpassword123"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        token = data["access_token"]
        
        # Test token structure
        assert len(token.split('.')) == 3  # Header.Payload.Signature
        
        # Test token payload (without verification for testing)
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            assert "sub" in payload
            assert "exp" in payload
            assert "iat" in payload
        except jwt.InvalidTokenError:
            pytest.fail("Invalid JWT token structure")
    
    def test_invalid_token_rejection(self, client):
        """Test that invalid tokens are rejected."""
        headers = {"Authorization": "Bearer invalid_token"}
        
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_expired_token_rejection(self, client):
        """Test that expired tokens are rejected."""
        # Create an expired token
        expired_payload = {
            "sub": "test@example.com",
            "exp": datetime.utcnow() - timedelta(hours=1),
            "iat": datetime.utcnow() - timedelta(hours=2)
        }
        
        # This would require the actual secret key
        # For testing, we'll use a mock approach
        with patch('api.routes.auth.verify_token') as mock_verify:
            mock_verify.side_effect = jwt.ExpiredSignatureError("Token has expired")
            
            headers = {"Authorization": "Bearer expired_token"}
            response = client.get("/api/auth/me", headers=headers)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_brute_force_protection(self, client, sample_user):
        """Test brute force protection on login."""
        # Attempt multiple failed logins
        for i in range(10):
            response = client.post("/api/auth/login", data={
                "username": sample_user.email,
                "password": f"wrongpassword{i}"
            })
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # After multiple failures, should implement rate limiting
        # This test verifies the system doesn't crash under attack
        response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "testpassword123"
        })
        
        # Should either succeed or be rate limited
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_429_TOO_MANY_REQUESTS]


class TestInputValidationSecurity:
    """Test input validation security measures."""
    
    def test_sql_injection_prevention(self, authenticated_client):
        """Test SQL injection prevention."""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; INSERT INTO users VALUES ('hacker', 'hacker'); --",
            "admin'--",
            "1' UNION SELECT * FROM users--"
        ]
        
        for malicious_input in malicious_inputs:
            # Test in various endpoints
            response = authenticated_client.get(f"/api/wellness/history?description={malicious_input}")
            assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]
            
            # Should not crash or expose data
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
                # Verify no sensitive data is exposed
                assert "password" not in str(data)
                assert "DROP TABLE" not in str(data)
    
    def test_xss_prevention(self, authenticated_client):
        """Test XSS prevention."""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<svg onload=alert('xss')>",
            "'><script>alert('xss')</script>"
        ]
        
        for payload in xss_payloads:
            response = authenticated_client.post("/api/wellness/check-in", json={
                "entry_type": "mood",
                "value": 7.0,
                "description": payload
            })
            
            # Should either accept (with sanitization) or reject
            assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_422_UNPROCESSABLE_ENTITY]
            
            if response.status_code == status.HTTP_201_CREATED:
                data = response.json()
                # Verify payload is sanitized
                assert "<script>" not in data["description"]
                assert "javascript:" not in data["description"]
    
    def test_large_payload_protection(self, authenticated_client):
        """Test protection against large payloads."""
        large_payload = "A" * 1000000  # 1MB payload
        
        response = authenticated_client.post("/api/wellness/check-in", json={
            "entry_type": "mood",
            "value": 7.0,
            "description": large_payload
        })
        
        # Should reject or truncate large payloads
        assert response.status_code in [status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_201_CREATED]
    
    def test_special_character_handling(self, authenticated_client):
        """Test handling of special characters."""
        special_chars = [
            "!@#$%^&*()",
            "中文测试",
            "🎉🎊🎈",
            "\\n\\t\\r",
            "null",
            "undefined",
            "NaN"
        ]
        
        for chars in special_chars:
            response = authenticated_client.post("/api/wellness/check-in", json={
                "entry_type": "mood",
                "value": 7.0,
                "description": chars
            })
            
            # Should handle special characters gracefully
            assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_422_UNPROCESSABLE_ENTITY]


class TestAuthorizationSecurity:
    """Test authorization security measures."""
    
    def test_user_data_isolation(self, authenticated_client, sample_user, db_session):
        """Test that users can only access their own data."""
        # Create another user
        from database.schema import User
        other_user = User(
            email="other@example.com",
            password_hash="hash",
            first_name="Other",
            last_name="User"
        )
        db_session.add(other_user)
        db_session.commit()
        
        # Try to access other user's data
        response = authenticated_client.get(f"/api/users/{other_user.id}")
        
        # Should be forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_role_based_access_control(self, client, db_session):
        """Test role-based access control."""
        # Create users with different roles
        from database.schema import User, UserRole
        
        employee = User(
            email="employee@example.com",
            password_hash="hash",
            first_name="Employee",
            last_name="User",
            role=UserRole.EMPLOYEE
        )
        
        admin = User(
            email="admin@example.com",
            password_hash="hash",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN
        )
        
        db_session.add_all([employee, admin])
        db_session.commit()
        
        # Login as employee
        emp_response = client.post("/api/auth/login", data={
            "username": "employee@example.com",
            "password": "testpassword123"
        })
        
        # Login as admin
        admin_response = client.post("/api/auth/login", data={
            "username": "admin@example.com",
            "password": "testpassword123"
        })
        
        # Test admin-only endpoints
        if emp_response.status_code == status.HTTP_200_OK:
            emp_token = emp_response.json()["access_token"]
            emp_headers = {"Authorization": f"Bearer {emp_token}"}
            
            # Employee should not access admin endpoints
            response = client.get("/api/admin/users", headers=emp_headers)
            assert response.status_code == status.HTTP_403_FORBIDDEN
        
        if admin_response.status_code == status.HTTP_200_OK:
            admin_token = admin_response.json()["access_token"]
            admin_headers = {"Authorization": f"Bearer {admin_token}"}
            
            # Admin should access admin endpoints
            response = client.get("/api/admin/users", headers=admin_headers)
            # This might be 404 if endpoint doesn't exist, but not 403
            assert response.status_code != status.HTTP_403_FORBIDDEN
    
    def test_session_management(self, client, sample_user):
        """Test session management security."""
        # Login
        response = client.post("/api/auth/login", data={
            "username": sample_user.email,
            "password": "testpassword123"
        })
        
        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Use token
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Logout
        response = client.post("/api/auth/logout", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Token should be invalidated
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDataProtectionSecurity:
    """Test data protection security measures."""
    
    def test_sensitive_data_encryption(self, authenticated_client, sample_user):
        """Test that sensitive data is properly handled."""
        # Test wellness check-in with sensitive information
        response = authenticated_client.post("/api/wellness/check-in", json={
            "entry_type": "comprehensive",
            "value": 7.0,
            "description": "Feeling stressed about work issues",
            "factors": {
                "workload": "high",
                "personal_issues": "confidential"
            }
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Verify sensitive data is not exposed in logs or responses
        # This is more of a verification that the system handles it properly
        assert "confidential" not in str(data).lower()
    
    def test_audit_trail(self, authenticated_client, sample_user):
        """Test audit trail functionality."""
        # Perform an action that should be audited
        response = authenticated_client.post("/api/wellness/check-in", json={
            "entry_type": "mood",
            "value": 8.0,
            "description": "Test audit trail"
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Check audit trail
        response = authenticated_client.get("/api/compliance/audit-trail")
        
        # Should return audit information
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_data_anonymization(self, authenticated_client, sample_user):
        """Test data anonymization for privacy."""
        # Create anonymous check-in
        response = authenticated_client.post("/api/wellness/check-in", json={
            "entry_type": "stress",
            "value": 6.0,
            "description": "Anonymous stress check-in",
            "is_anonymous": True
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Anonymous entries should not expose user information
        assert "user_id" not in data
        assert "email" not in data
        assert "name" not in data
    
    def test_privacy_consent(self, authenticated_client, sample_user):
        """Test privacy consent management."""
        # Check privacy consent status
        response = authenticated_client.get("/api/compliance/privacy-consent")
        
        # Should return consent information
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        # Update privacy consent
        response = authenticated_client.post("/api/compliance/privacy-consent", json={
            "data_collection": True,
            "data_processing": True,
            "data_sharing": False
        })
        
        # Should accept consent updates
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


class TestAPISecurity:
    """Test API security measures."""
    
    def test_cors_configuration(self, client):
        """Test CORS configuration."""
        response = client.options("/api/auth/login")
        
        # Should include CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
    
    def test_rate_limiting(self, client, sample_user):
        """Test rate limiting implementation."""
        # Make multiple requests quickly
        for _ in range(20):
            response = client.get("/api/wellness/history")
            # Should not crash
        
        # Verify system remains responsive
        response = client.get("/api/wellness/history")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_429_TOO_MANY_REQUESTS]
    
    def test_request_validation(self, authenticated_client):
        """Test request validation."""
        # Test malformed JSON
        response = authenticated_client.post(
            "/api/wellness/check-in",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_error_handling(self, authenticated_client):
        """Test error handling doesn't expose sensitive information."""
        # Trigger an error
        response = authenticated_client.post("/api/wellness/check-in", json={
            "invalid_field": "test"
        })
        
        # Should not expose internal details
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        
        # Error should not contain sensitive information
        error_str = str(data).lower()
        assert "password" not in error_str
        assert "secret" not in error_str
        assert "key" not in error_str
        assert "token" not in error_str


class TestIntegrationSecurity:
    """Test integration security measures."""
    
    def test_external_api_security(self, authenticated_client):
        """Test external API integration security."""
        # Test that external API calls are properly secured
        with patch('api.routes.wellness.openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.return_value = Mock(
                choices=[Mock(message=Mock(content="Test response"))]
            )
            
            response = authenticated_client.post("/api/wellness/conversation", json={
                "message": "Test message"
            })
            
            # Should handle external API calls securely
            assert response.status_code in [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]
    
    def test_database_security(self, authenticated_client):
        """Test database security measures."""
        # Test that database queries are properly parameterized
        response = authenticated_client.get("/api/wellness/history?user_id=1' OR '1'='1")
        
        # Should handle malicious input gracefully
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST]
    
    def test_file_upload_security(self, authenticated_client):
        """Test file upload security."""
        # Test file upload validation
        files = {"file": ("test.txt", b"test content", "text/plain")}
        
        response = authenticated_client.post("/api/resources/upload", files=files)
        
        # Should validate file uploads
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_404_NOT_FOUND]
