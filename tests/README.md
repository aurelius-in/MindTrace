# Enterprise Employee Wellness AI - Test Suite

This directory contains a comprehensive test suite for the Enterprise Employee Wellness AI application, covering unit tests, API tests, integration tests, security tests, and performance tests.

## 📁 Directory Structure

```
tests/
├── __init__.py                 # Package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── run_tests.py               # Test runner script
├── README.md                  # This documentation
├── unit/                      # Unit tests
│   ├── __init__.py
│   └── test_database_models.py
├── api/                       # API tests
│   ├── __init__.py
│   ├── test_auth_api.py
│   └── test_wellness_api.py
├── integration/               # Integration tests
│   ├── __init__.py
│   └── test_integration.py
├── security/                  # Security tests
│   ├── __init__.py
│   └── test_security.py
└── performance/               # Performance tests
    ├── __init__.py
    └── test_performance.py
```

## 🚀 Quick Start

### Prerequisites

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Install additional test packages:
```bash
pip install pytest pytest-cov pytest-asyncio pytest-mock pytest-html pytest-xdist pytest-timeout pytest-env
```

### Running Tests

#### Using the Test Runner Script

```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
python tests/run_tests.py --unit
python tests/run_tests.py --api
python tests/run_tests.py --integration
python tests/run_tests.py --security
python tests/run_tests.py --performance

# Run with coverage
python tests/run_tests.py --all --coverage

# Run with verbose output
python tests/run_tests.py --all -v

# Run specific test file
python tests/run_tests.py --test tests/unit/test_database_models.py

# Run tests with specific markers
python tests/run_tests.py --markers "unit and not slow"

# Generate comprehensive report
python tests/run_tests.py --report
```

#### Using Pytest Directly

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/
pytest tests/api/
pytest tests/integration/
pytest tests/security/
pytest tests/performance/

# Run with markers
pytest -m unit
pytest -m api
pytest -m integration
pytest -m security
pytest -m performance

# Run with coverage
pytest --cov=backend --cov-report=html

# Run in parallel
pytest -n auto

# Run specific test
pytest tests/unit/test_database_models.py::TestUserModel::test_user_creation
```

## 📋 Test Categories

### 1. Unit Tests (`tests/unit/`)

Unit tests focus on testing individual components in isolation.

**Coverage:**
- Database models and their methods
- Business logic functions
- Utility functions
- Data validation
- Serialization methods

**Example:**
```python
def test_user_creation(self, db_session):
    """Test basic user creation."""
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
```

### 2. API Tests (`tests/api/`)

API tests verify the HTTP endpoints and their responses.

**Coverage:**
- Authentication endpoints
- Wellness endpoints
- Resource endpoints
- Analytics endpoints
- Error handling
- Response formats
- Status codes

**Example:**
```python
def test_login_success(self, client, sample_user):
    """Test successful login."""
    response = client.post("/api/auth/login", data={
        "username": sample_user.email,
        "password": "testpassword123"
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
```

### 3. Integration Tests (`tests/integration/`)

Integration tests verify that different components work together correctly.

**Coverage:**
- Complete user workflows
- End-to-end scenarios
- Cross-component interactions
- Data flow between services
- System behavior under normal conditions

**Example:**
```python
def test_complete_user_journey(self, client, db_session):
    """Test complete user journey from registration to wellness tracking."""
    # 1. User Registration
    # 2. User Login
    # 3. Create Wellness Check-in
    # 4. Get Analytics
    # 5. Logout
```

### 4. Security Tests (`tests/security/`)

Security tests ensure the application is secure against common vulnerabilities.

**Coverage:**
- Authentication security
- Input validation
- SQL injection prevention
- XSS prevention
- Authorization checks
- Data protection
- Token security

**Example:**
```python
def test_sql_injection_prevention(self, authenticated_client):
    """Test SQL injection prevention."""
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "' OR '1'='1"
    ]
    
    for malicious_input in malicious_inputs:
        response = authenticated_client.get(f"/api/wellness/history?description={malicious_input}")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]
```

### 5. Performance Tests (`tests/performance/`)

Performance tests verify the application performs well under load.

**Coverage:**
- Database performance
- API response times
- Concurrent user handling
- Memory usage
- CPU usage
- Scalability
- Load testing

**Example:**
```python
def test_bulk_wellness_entry_creation(self, authenticated_client, sample_user):
    """Test bulk creation of wellness entries."""
    start_time = time.time()
    
    # Create 100 wellness entries
    for i in range(100):
        response = authenticated_client.post("/api/wellness/check-in", json={
            "entry_type": "mood",
            "value": 7.0,
            "description": f"Bulk test entry {i}"
        })
    
    duration = time.time() - start_time
    assert duration < 30.0  # Should complete within 30 seconds
```

## 🛠️ Test Fixtures

The test suite uses comprehensive fixtures defined in `conftest.py`:

### Database Fixtures
- `db_session`: Database session for each test
- `test_db`: Test database setup
- `sample_user`: Sample user for testing
- `sample_wellness_entry`: Sample wellness entry
- `sample_resource`: Sample resource
- `sample_team`: Sample team

### API Fixtures
- `client`: Test client without authentication
- `authenticated_client`: Test client with authentication
- `sample_user_data`: Sample user data

### Mock Fixtures
- `mock_agent_orchestrator`: Mock agent orchestrator
- `mock_openai_client`: Mock OpenAI client
- `mock_redis_client`: Mock Redis client
- `mock_prometheus_metrics`: Mock Prometheus metrics

### Utility Fixtures
- `temp_file`: Temporary file for testing
- `temp_dir`: Temporary directory for testing
- `security_test_data`: Data for security testing

## 📊 Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.api`: API tests
- `@pytest.mark.database`: Database tests
- `@pytest.mark.security`: Security tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.slow`: Slow running tests
- `@pytest.mark.smoke`: Smoke tests
- `@pytest.mark.regression`: Regression tests
- `@pytest.mark.e2e`: End-to-end tests

## 🔧 Configuration

### Pytest Configuration (`pytest.ini`)

The pytest configuration includes:
- Test discovery settings
- Markers definition
- Coverage settings
- Parallel execution
- Logging configuration
- Environment variables
- Required plugins

### Environment Variables

Test environment variables are set in `pytest.ini`:
- `TESTING=true`: Indicates test environment
- `DATABASE_URL=sqlite:///:memory:`: In-memory test database
- `REDIS_URL=redis://localhost:6379/1`: Test Redis instance
- `OPENAI_API_KEY=test_key`: Test API key
- `JWT_SECRET_KEY=test_secret_key`: Test JWT secret

## 📈 Coverage Reports

The test suite generates comprehensive coverage reports:

### HTML Coverage Report
```bash
pytest --cov=backend --cov-report=html
# Generates: htmlcov/index.html
```

### XML Coverage Report
```bash
pytest --cov=backend --cov-report=xml
# Generates: coverage.xml
```

### Terminal Coverage Report
```bash
pytest --cov=backend --cov-report=term-missing
```

## 🚨 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio pytest-mock
    
    - name: Run tests
      run: |
        python tests/run_tests.py --all --coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 🐛 Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with maximum verbosity
pytest -vvv

# Run with print statements
pytest -s

# Run specific test with debugger
pytest tests/unit/test_database_models.py::TestUserModel::test_user_creation -s
```

### Common Issues

1. **Database Connection Issues**
   - Ensure test database is properly configured
   - Check database URL in environment variables

2. **Import Errors**
   - Verify Python path includes backend directory
   - Check for missing dependencies

3. **Mock Issues**
   - Ensure mocks are properly configured
   - Check mock paths match actual imports

## 📝 Best Practices

### Writing Tests

1. **Test Naming**
   - Use descriptive test names
   - Follow the pattern: `test_<what>_<when>_<expected_result>`

2. **Test Structure**
   - Arrange: Set up test data
   - Act: Execute the code being tested
   - Assert: Verify the results

3. **Test Isolation**
   - Each test should be independent
   - Use fixtures for common setup
   - Clean up after tests

4. **Test Data**
   - Use realistic test data
   - Avoid hardcoded values
   - Use factories for complex objects

### Test Maintenance

1. **Keep Tests Simple**
   - One assertion per test
   - Focus on one behavior
   - Avoid complex setup

2. **Update Tests with Code Changes**
   - Update tests when changing functionality
   - Maintain test coverage
   - Review test failures

3. **Performance Considerations**
   - Use appropriate test data sizes
   - Mock external dependencies
   - Use efficient database operations

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Cov Documentation](https://pytest-cov.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

## 🤝 Contributing

When adding new tests:

1. Follow the existing test structure
2. Use appropriate markers
3. Add comprehensive docstrings
4. Ensure good coverage
5. Update this documentation if needed

## 📞 Support

For questions about the test suite:
- Check the test documentation
- Review existing test examples
- Consult the pytest documentation
- Open an issue for specific problems
