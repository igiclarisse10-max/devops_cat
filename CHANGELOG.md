# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-08

### Added
- Initial release of To-Do List application
- Flask REST API with complete CRUD operations for tasks
- SQLite database with SQLAlchemy ORM
- Responsive HTML5 UI with Bulma CSS framework
- Comprehensive unit tests (16 tests) and integration tests (8 tests)
- GitHub Actions CI/CD pipeline with Python 3.9, 3.10, 3.11 matrix
- Slack notifications for test results
- Docker containerization with docker-compose support
- Test coverage reporting with codecov

### Fixed
- Flask/Werkzeug version compatibility across Python 3.9-3.11 (Flask 2.3.3 + Werkzeug 3.0.1)
- SQLAlchemy session management in test fixtures
- Test database configuration for in-memory SQLite

### Technical Details
- Flask==2.3.3
- Werkzeug==3.0.1
- Flask-SQLAlchemy==3.0.5
- pytest==7.4.3 with pytest-cov, pytest-flask, pytest-html
- Python 3.9, 3.10, 3.11 support verified

## [Unreleased]

### Planned Features
- User authentication and authorization
- Task categories/tags
- Task due dates and priorities
- Dark mode UI toggle
- Export tasks to CSV/JSON
- Task sharing and collaboration
