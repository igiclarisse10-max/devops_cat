# CI/CD Configuration and Testing Guide

## Overview

This To-Do List application includes comprehensive testing and CI/CD automation:

- **Unit Tests**: Individual component testing using pytest
- **Integration Tests**: End-to-end workflow testing
- **CI Pipeline**: Automated testing on push/PR using GitHub Actions
- **Notifications**: Slack and Email notifications for test results

## Setting Up Tests Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Unit Tests

```bash
pytest test_app.py -v
```

### Run Integration Tests

```bash
pytest test_integration.py -v
```

### Run All Tests with Coverage

```bash
pytest test_app.py test_integration.py -v --cov=app --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`

### Run Specific Test Class or Function

```bash
# Run a specific test class
pytest test_app.py::TestGetTasksAPI -v

# Run a specific test function
pytest test_app.py::TestGetTasksAPI::test_get_tasks_empty_list -v
```

## GitHub Actions CI Pipeline

The CI pipeline automatically runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### Pipeline Stages

1. **Test Stage**
   - Tests against Python 3.9, 3.10, and 3.11
   - Runs unit tests with coverage
   - Runs integration tests
   - Uploads coverage to Codecov
   - Generates test reports

2. **Lint Stage**
   - Runs flake8 for code style
   - Runs pylint for code quality

### Pipeline Files

- `.github/workflows/tests.yml` - Main CI pipeline definition

## Setting Up Notifications

### Slack Notifications

1. **Create a Slack App**
   - Go to https://api.slack.com/apps
   - Create a new app
   - Enable Incoming Webhooks

2. **Get the Webhook URL**
   - In Incoming Webhooks, click "Add New Webhook to Workspace"
   - Select your channel and authorize
   - Copy the Webhook URL

3. **Add to GitHub Secrets**
   ```
   Repository Settings → Secrets and variables → Actions
   New repository secret:
   Name: SLACK_WEBHOOK_URL
   Value: [Your webhook URL]
   ```

### Email Notifications

1. **Prepare Email Credentials**
   - For Gmail: Create an [App Password](https://support.google.com/accounts/answer/185833)
   - For other providers: Use your SMTP credentials

2. **Add to GitHub Secrets**
   ```
   Repository Settings → Secrets and variables → Actions
   
   New secrets:
   - EMAIL_FROM: your-email@gmail.com
   - EMAIL_PASSWORD: your-app-password
   - EMAIL_TO: recipient@example.com
   - SMTP_SERVER: smtp.gmail.com (default)
   - SMTP_PORT: 587 (default)
   ```

## Test Structure

### Unit Tests (`test_app.py`)

Tests individual components:
- **TestHomeRoute**: Home page loading
- **TestGetTasksAPI**: Task retrieval
- **TestCreateTaskAPI**: Task creation
- **TestUpdateTaskAPI**: Task updates
- **TestDeleteTaskAPI**: Task deletion
- **TestTaskModel**: Database model

### Integration Tests (`test_integration.py`)

Tests complete workflows:
- **TestCompleteUserWorkflow**: CRUD operations
- **TestMultipleTasksWorkflow**: Managing multiple tasks
- **TestDataPersistence**: Data persistence across requests
- **TestErrorHandling**: Error scenarios
- **TestAPIResponseFormat**: Response consistency
- **TestUIIntegration**: UI page loading

## Test Coverage

Run coverage analysis:

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

View HTML report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Debugging Failed Tests

1. **Run with verbose output**
   ```bash
   pytest -vv test_app.py
   ```

2. **Run with print statements**
   ```bash
   pytest -s test_app.py
   ```

3. **Run with pdb on failure**
   ```bash
   pytest --pdb test_app.py
   ```

4. **Run specific test**
   ```bash
   pytest test_app.py::TestCreateTaskAPI::test_create_task_success -v
   ```

## Adding New Tests

1. Create test functions in `test_app.py` (unit) or `test_integration.py` (integration)
2. Follow naming convention: `test_<feature>_<scenario>`
3. Use fixtures for setup/teardown
4. Use assertions for validation

Example:
```python
def test_new_feature(client):
    """Test description"""
    response = client.post('/api/endpoint', data={...})
    assert response.status_code == 200
```

## CI Pipeline Status Badge

Add this to your README.md:

```markdown
![CI Pipeline](https://github.com/YOUR_USERNAME/TO_DO_LIST_APP/workflows/CI%20Pipeline/badge.svg)
```

## Troubleshooting

### Tests Pass Locally but Fail in CI

- Check Python version compatibility
- Verify all dependencies are in requirements.txt
- Check for environment-specific issues

### Slack Notifications Not Working

- Verify SLACK_WEBHOOK_URL is set correctly
- Check Slack app permissions
- Review GitHub Actions logs for errors

### Email Notifications Not Working

- Verify email credentials are correct
- For Gmail, ensure App Password is used (not regular password)
- Check SMTP settings for your provider
- Review GitHub Actions logs for errors

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Slack API Reference](https://api.slack.com/)
- [Python email Documentation](https://docs.python.org/3/library/email.html)
