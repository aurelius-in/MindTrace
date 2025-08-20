"""
Unit tests for integrations
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from backend.integrations.slack import SlackIntegration
from backend.integrations.teams import TeamsIntegration
from backend.integrations.email import EmailIntegration
from backend.integrations.hris import HRISIntegration
from backend.integrations.workday import WorkdayIntegration
from backend.integrations.bamboohr import BambooHRIntegration


class TestSlackIntegration:
    """Test Slack integration functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.slack = SlackIntegration()
        self.mock_user = Mock()
        self.mock_user.id = "test_user_123"
        self.mock_user.name = "Test User"
    
    def test_initialization(self):
        """Test Slack integration initialization"""
        assert self.slack.client is not None
        assert self.slack.channel_id is not None
    
    def test_send_message(self):
        """Test sending Slack message"""
        with patch.object(self.slack.client, 'chat_postMessage') as mock_post:
            mock_post.return_value = {"ok": True}
            
            result = self.slack.send_message("test_channel", "Hello World!")
            assert result is True
            mock_post.assert_called_once()
    
    def test_send_wellness_check(self):
        """Test sending wellness check"""
        with patch.object(self.slack, 'send_message') as mock_send:
            mock_send.return_value = True
            
            result = self.slack.send_wellness_check(self.mock_user)
            assert result is True
            mock_send.assert_called_once()
    
    def test_handle_high_risk_situation(self):
        """Test handling high risk situation"""
        with patch.object(self.slack, '_escalate_to_hr') as mock_escalate:
            mock_escalate.return_value = True
            
            result = self.slack.handle_high_risk_situation(
                user_id="test_user",
                risk_level="high",
                details="User showing signs of crisis"
            )
            assert result is True
            mock_escalate.assert_called_once()
    
    def test_escalate_to_hr(self):
        """Test HR escalation"""
        with patch('backend.integrations.slack.analytics_repo') as mock_analytics:
            with patch('backend.integrations.slack.email_utility') as mock_email:
                mock_analytics.create_escalation_record.return_value = True
                mock_email.send_notification.return_value = True
                
                result = self.slack._escalate_to_hr(
                    user_id="test_user",
                    reason="High stress detected",
                    urgency="high"
                )
                assert result is True
                mock_analytics.create_escalation_record.assert_called_once()
                mock_email.send_notification.assert_called_once()


class TestTeamsIntegration:
    """Test Microsoft Teams integration functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.teams = TeamsIntegration()
        self.mock_user = Mock()
        self.mock_user.id = "test_user_123"
        self.mock_user.name = "Test User"
    
    def test_initialization(self):
        """Test Teams integration initialization"""
        assert self.teams.client is not None
        assert self.teams.team_id is not None
    
    def test_send_message(self):
        """Test sending Teams message"""
        with patch.object(self.teams.client, 'send_message') as mock_send:
            mock_send.return_value = {"id": "msg_123"}
            
            result = self.teams.send_message("test_channel", "Hello World!")
            assert result is True
            mock_send.assert_called_once()
    
    def test_send_wellness_check(self):
        """Test sending wellness check"""
        with patch.object(self.teams, 'send_message') as mock_send:
            mock_send.return_value = True
            
            result = self.teams.send_wellness_check(self.mock_user)
            assert result is True
            mock_send.assert_called_once()
    
    def test_handle_high_risk_situation(self):
        """Test handling high risk situation"""
        with patch.object(self.teams, '_escalate_to_hr') as mock_escalate:
            mock_escalate.return_value = True
            
            result = self.teams.handle_high_risk_situation(
                user_id="test_user",
                risk_level="high",
                details="User showing signs of crisis"
            )
            assert result is True
            mock_escalate.assert_called_once()
    
    def test_escalate_to_hr(self):
        """Test HR escalation"""
        with patch('backend.integrations.teams.analytics_repo') as mock_analytics:
            with patch('backend.integrations.teams.email_utility') as mock_email:
                mock_analytics.create_escalation_record.return_value = True
                mock_email.send_notification.return_value = True
                
                result = self.teams._escalate_to_hr(
                    user_id="test_user",
                    reason="High stress detected",
                    urgency="high"
                )
                assert result is True
                mock_analytics.create_escalation_record.assert_called_once()
                mock_email.send_notification.assert_called_once()


class TestEmailIntegration:
    """Test email integration functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.email = EmailIntegration()
    
    def test_initialization(self):
        """Test email integration initialization"""
        assert self.email.smtp_server is not None
        assert self.email.smtp_port is not None
    
    def test_send_email(self):
        """Test sending email"""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value = mock_server
            
            result = self.email.send_email(
                to_email="test@example.com",
                subject="Test Subject",
                body="Test Body"
            )
            assert result is True
            mock_server.send_message.assert_called_once()
    
    def test_send_wellness_report(self):
        """Test sending wellness report"""
        with patch.object(self.email, 'send_email') as mock_send:
            mock_send.return_value = True
            
            report_data = {
                "user_id": "test_user",
                "wellness_score": 7.5,
                "recommendations": ["Take a break", "Practice mindfulness"]
            }
            
            result = self.email.send_wellness_report("test@example.com", report_data)
            assert result is True
            mock_send.assert_called_once()
    
    def test_send_escalation_notification(self):
        """Test sending escalation notification"""
        with patch.object(self.email, 'send_email') as mock_send:
            mock_send.return_value = True
            
            result = self.email.send_escalation_notification(
                user_id="test_user",
                reason="High stress detected",
                urgency="high"
            )
            assert result is True
            mock_send.assert_called_once()


class TestHRISIntegration:
    """Test HRIS integration functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.hris = HRISIntegration()
    
    def test_initialization(self):
        """Test HRIS integration initialization"""
        assert self.hris.api_key is not None
        assert self.hris.base_url is not None
    
    def test_get_employee_data(self):
        """Test getting employee data"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "employee_id": "emp_123",
                "name": "John Doe",
                "department": "Engineering",
                "manager": "Jane Smith"
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            employee_data = self.hris.get_employee_data("emp_123")
            assert employee_data is not None
            assert "employee_id" in employee_data
            assert "name" in employee_data
    
    def test_get_team_data(self):
        """Test getting team data"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "team_id": "team_123",
                "name": "Engineering",
                "members": ["emp_123", "emp_124"]
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            team_data = self.hris.get_team_data("team_123")
            assert team_data is not None
            assert "team_id" in team_data
            assert "members" in team_data
    
    def test_sync_employee_data(self):
        """Test syncing employee data"""
        with patch.object(self.hris, 'get_employee_data') as mock_get:
            mock_get.return_value = {
                "employee_id": "emp_123",
                "name": "John Doe",
                "department": "Engineering"
            }
            
            with patch('backend.integrations.hris.user_repo') as mock_repo:
                mock_repo.update_user.return_value = True
                
                result = self.hris.sync_employee_data("emp_123")
                assert result is True
                mock_repo.update_user.assert_called_once()


class TestWorkdayIntegration:
    """Test Workday integration functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.workday = WorkdayIntegration()
    
    def test_initialization(self):
        """Test Workday integration initialization"""
        assert self.workday.client_id is not None
        assert self.workday.client_secret is not None
    
    def test_authenticate(self):
        """Test Workday authentication"""
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "token_123",
                "expires_in": 3600
            }
            mock_response.status_code = 200
            mock_post.return_value = mock_response
            
            token = self.workday.authenticate()
            assert token is not None
            assert token == "token_123"
    
    def test_get_employee_info(self):
        """Test getting employee information"""
        with patch.object(self.workday, 'authenticate') as mock_auth:
            mock_auth.return_value = "token_123"
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.json.return_value = {
                    "employee": {
                        "id": "emp_123",
                        "name": "John Doe",
                        "position": "Software Engineer",
                        "department": "Engineering"
                    }
                }
                mock_response.status_code = 200
                mock_get.return_value = mock_response
                
                employee_info = self.workday.get_employee_info("emp_123")
                assert employee_info is not None
                assert "employee" in employee_info
    
    def test_get_organization_structure(self):
        """Test getting organization structure"""
        with patch.object(self.workday, 'authenticate') as mock_auth:
            mock_auth.return_value = "token_123"
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.json.return_value = {
                    "departments": [
                        {"id": "dept_1", "name": "Engineering"},
                        {"id": "dept_2", "name": "Sales"}
                    ]
                }
                mock_response.status_code = 200
                mock_get.return_value = mock_response
                
                org_structure = self.workday.get_organization_structure()
                assert org_structure is not None
                assert "departments" in org_structure


class TestBambooHRIntegration:
    """Test BambooHR integration functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.bamboohr = BambooHRIntegration()
    
    def test_initialization(self):
        """Test BambooHR integration initialization"""
        assert self.bamboohr.api_key is not None
        assert self.bamboohr.subdomain is not None
    
    def test_get_employee(self):
        """Test getting employee data"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "id": "emp_123",
                "firstName": "John",
                "lastName": "Doe",
                "jobTitle": "Software Engineer",
                "department": "Engineering"
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            employee = self.bamboohr.get_employee("emp_123")
            assert employee is not None
            assert "id" in employee
            assert "firstName" in employee
    
    def test_get_employees(self):
        """Test getting all employees"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "employees": [
                    {"id": "emp_123", "firstName": "John", "lastName": "Doe"},
                    {"id": "emp_124", "firstName": "Jane", "lastName": "Smith"}
                ]
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            employees = self.bamboohr.get_employees()
            assert employees is not None
            assert "employees" in employees
            assert len(employees["employees"]) == 2
    
    def test_get_company_structure(self):
        """Test getting company structure"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "departments": [
                    {"id": 1, "name": "Engineering"},
                    {"id": 2, "name": "Sales"}
                ]
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            structure = self.bamboohr.get_company_structure()
            assert structure is not None
            assert "departments" in structure
    
    def test_update_employee(self):
        """Test updating employee data"""
        with patch('requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            update_data = {"jobTitle": "Senior Software Engineer"}
            result = self.bamboohr.update_employee("emp_123", update_data)
            assert result is True
            mock_put.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
