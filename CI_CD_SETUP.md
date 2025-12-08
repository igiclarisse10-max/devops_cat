# CI/CD Setup Guide for To-Do App

This document explains how to set up and configure the CI/CD pipeline with testing and notifications for the To-Do App.

## Overview

The setup includes:
- **Unit Tests**: Backend API tests using pytest
- **Integration Tests**: Full API workflow tests
- **Frontend Tests**: JavaScript tests (can be run with Jest)
- **CI/CD Pipeline**: Automated testing on GitHub Actions
- **Notifications**: Slack and Email notifications for test results

## Prerequisites

- GitHub repository
- GitHub Actions enabled (default for public repos)
- Slack workspace (optional, for Slack notifications)
- Email SMTP server (optional, for email notifications)

## Setup Steps

### 1. Install Testing Dependencies

```bash
pip install -r requirements.txt
```

This includes:
- pytest: Testing framework
- pytest-cov: Coverage reports
- requests: HTTP client for integration tests
- slack-sdk: Slack notifications

### 2. Run Local Tests

#### Run Unit Tests
```bash
pytest tests/test_unit.py -v
```

#### Run Integration Tests
First, start the app in another terminal:
```bash
python app.py
```

Then run integration tests:
```bash
pytest tests/test_integration.py -v
```

#### Run All Tests with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

This generates a coverage report in `htmlcov/index.html`

### 3. Configure GitHub Actions

The CI/CD pipeline is defined in `.github/workflows/ci.yml` and runs:
- Unit tests on Python 3.9, 3.10, 3.11
- Coverage report generation
- Docker image build
- Integration tests

#### Set Up Slack Notifications

1. **Create a Slack App**:
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Name it "To-Do App CI/CD"
   - Select your workspace

2. **Enable Incoming Webhooks**:
   - In the app settings, go to "Incoming Webhooks"
   - Click "Add New Webhook to Workspace"
   - Select the channel where notifications should go
   - Copy the Webhook URL

3. **Add to GitHub Secrets**:
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `SLACK_WEBHOOK_URL`
   - Value: Paste the Webhook URL
   - Click "Add secret"

#### Set Up Email Notifications (Optional)

1. **Prepare Email Credentials**:
   - Use Gmail: Enable 2FA and create an App Password
   - Or use your own SMTP server

2. **Add to GitHub Secrets**:
   - `EMAIL_FROM`: Your email address
   - `EMAIL_PASSWORD`: Your app password or SMTP password
   - `SMTP_SERVER`: SMTP server address (default: smtp.gmail.com)
   - `SMTP_PORT`: SMTP port (default: 587)

3. **Update Environment Variables** in `.github/workflows/ci.yml`:
   ```yaml
   - name: Send Email Notification
     env:
       EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
       EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
   ```

### 4. Test Local Notifications (Optional)

```python
from notifications import NotificationService

service = NotificationService()
service.send_slack_notification("Test message", "info")
```

Environment variables needed:
- `SLACK_BOT_TOKEN`: Your Slack bot token
- `SLACK_CHANNEL`: Target channel (e.g., #ci-cd-notifications)
- `EMAIL_ENABLED`: "true" or "false"
- `EMAIL_FROM`: Your email address
- `EMAIL_PASSWORD`: Your email password

## CI/CD Workflow

### When Code is Pushed

1. **Unit Tests Run** (multiple Python versions)
   - Tests run on Python 3.9, 3.10, 3.11
   - Coverage report is generated
   - Slack notification sent

2. **Docker Build** (if tests pass)
   - Docker image is built
   - Slack notification sent

3. **Integration Tests** (if Docker build succeeds)
   - Full API tests run
   - Slack notification sent

4. **Notifications**
   - Success: Green ✅ message
   - Failure: Red ❌ message
   - Includes repository, branch, commit, and author info

## File Structure

```
TO_DO_LIST_APP/
├── app.py                          # Main Flask app
├── requirements.txt                # Python dependencies
├── tests/
│   ├── __init__.py
│   ├── test_unit.py               # Backend unit tests
│   ├── test_integration.py        # Integration tests
│   └── test_frontend.js           # Frontend tests
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions workflow
├── conftest.py                     # pytest configuration
├── pytest.ini                      # pytest settings
├── notifications.py                # Notification service
└── README.md                       # This file
```

## Test Coverage

### Unit Tests (test_unit.py)
- Task model creation
- GET /api/tasks (empty and with items)
- POST /api/tasks (create task)
- PATCH /api/tasks/<id> (update task)
- DELETE /api/tasks/<id> (delete task)
- Error handling for invalid requests

### Integration Tests (test_integration.py)
- Full API workflow tests
- End-to-end task operations
- Multiple task management

### Frontend Tests (test_frontend.js)
- Task loading from API
- Task addition
- Task completion toggle
- Task deletion
- Empty state handling

## Troubleshooting

### Tests fail locally but pass in CI
- Check Python version matches (use 3.11)
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Delete `.db` files and try again

### Slack notifications not sending
- Verify webhook URL in GitHub Secrets
- Check webhook URL starts with `https://hooks.slack.com/`
- Ensure bot has permission to post in the channel

### Integration tests fail
- Ensure app starts successfully: `python app.py`
- Check if port 5000 is available
- Check logs for database issues

## Monitoring

Check CI/CD status:
1. Go to GitHub repo → Actions
2. Select the latest workflow run
3. View logs for each job
4. Check Slack for notifications

## Best Practices

1. **Run tests locally** before pushing:
   ```bash
   pytest tests/ -v
   ```

2. **Check coverage** regularly:
   ```bash
   pytest --cov=app --cov-report=html
   ```

3. **Write tests for new features** before implementing them

4. **Keep dependencies updated**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

5. **Monitor CI/CD runs** and fix failures promptly

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Slack API Documentation](https://api.slack.com/messaging/webhooks)
- [Flask Testing Guide](https://flask.palletsprojects.com/en/latest/testing/)

## Support

For issues or questions:
1. Check the CI/CD logs on GitHub Actions
2. Run tests locally: `pytest -v`
3. Review error messages and stack traces
4. Check notifications for details
