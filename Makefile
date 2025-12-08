.PHONY: help install test test-unit test-integration test-all coverage clean dev lint format

help:
	@echo "To-Do App Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install dependencies"
	@echo "  make dev              Start app in development mode"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-watch       Run tests in watch mode"
	@echo "  make coverage         Run tests with coverage report"
	@echo ""
	@echo "Quality:"
	@echo "  make lint             Run code linting"
	@echo "  make format           Format code"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean            Remove test artifacts and cache"
	@echo "  make run              Start production app"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-run       Run app in Docker"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	npm install 2>/dev/null || true

run:
	python app.py

dev:
	FLASK_ENV=development flask run --debug

test:
	pytest tests/ -v

test-unit:
	pytest tests/test_unit.py -v

test-integration:
	pytest tests/test_integration.py -v

test-watch:
	pytest tests/ -v --tb=short --looponfail

coverage:
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	@command -v pylint >/dev/null 2>&1 || pip install pylint
	pylint app.py tests/ || true

format:
	@command -v black >/dev/null 2>&1 || pip install black
	black app.py tests/ conftest.py notifications.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name 'tasks.db' -delete
	@echo "Cleaned up cache and test artifacts"

docker-build:
	docker build -t to-do-list-app:latest .

docker-run: docker-build
	docker run -p 5000:5000 to-do-list-app:latest

docker-compose-build:
	docker compose build

docker-compose-up:
	docker compose up

docker-compose-down:
	docker compose down

docker-clean:
	docker system prune -f

ci-local:
	@echo "Running local CI pipeline..."
	make clean
	make install
	make lint || true
	make test-unit
	make coverage

.DEFAULT_GOAL := help
