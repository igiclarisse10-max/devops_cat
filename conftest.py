"""
Pytest configuration and shared fixtures
"""

import pytest
from app import app, db, Task


@pytest.fixture(scope='session')
def app_context():
    """Application context for the entire test session"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_context):
    """Test client fixture for making requests"""
    return app_context.test_client()


@pytest.fixture
def runner(app_context):
    """CLI test runner fixture"""
    return app_context.test_cli_runner()


@pytest.fixture
def db_session(app_context):
    """Database session fixture"""
    with app_context.app_context():
        yield db.session
        db.session.rollback()


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
