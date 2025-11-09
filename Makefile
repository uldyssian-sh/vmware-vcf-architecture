# VMware VCF Architecture - Makefile

.PHONY: help install install-dev test lint format security clean build run docker-build docker-run docker-stop

# Default target
help: ## Show this help message
	@echo "VMware VCF Architecture - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

# Testing
test: ## Run tests
	pytest tests/ -v --cov=. --cov-report=term --cov-report=html

test-watch: ## Run tests in watch mode
	pytest-watch tests/ -- -v --cov=.

# Code quality
lint: ## Run linting
	flake8 .
	mypy .
	bandit -r . -f json -o bandit-report.json || true

format: ## Format code
	black .
	isort .

format-check: ## Check code formatting
	black --check .
	isort --check-only .

# Security
security: ## Run security checks
	bandit -r .
	safety check
	pip-audit

# Cleanup
clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ dist/ build/
	rm -f bandit-report.json

# Build and run
build: ## Build the application
	python -m py_compile main.py

run: ## Run the application
	python main.py

run-debug: ## Run the application in debug mode
	python main.py --debug

health-check: ## Perform health check
	python main.py --health-check

# Docker operations
docker-build: ## Build Docker image
	docker build -t vmware-vcf-architecture:latest .

docker-run: ## Run Docker container
	docker run -d --name vmware-vcf-architecture -p 8080:8080 vmware-vcf-architecture:latest

docker-stop: ## Stop Docker container
	docker stop vmware-vcf-architecture || true
	docker rm vmware-vcf-architecture || true

docker-compose-up: ## Start services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	docker-compose down

docker-compose-logs: ## View docker-compose logs
	docker-compose logs -f

# Development workflow
dev-setup: install-dev ## Set up development environment
	cp .env.template .env
	echo "Please edit .env file with your configuration"

validate: format-check lint test security ## Run all validation checks

ci: validate ## Run CI pipeline locally

# Documentation
docs-serve: ## Serve documentation locally
	mkdocs serve

docs-build: ## Build documentation
	mkdocs build

# Release
release-patch: ## Create patch release
	@echo "Creating patch release..."
	@git tag -a v$$(python -c "import main; print(main.VCFArchitecture().version)") -m "Release v$$(python -c "import main; print(main.VCFArchitecture().version)")"

release-minor: ## Create minor release
	@echo "Creating minor release..."
	@echo "Please update version in main.py first"

release-major: ## Create major release
	@echo "Creating major release..."
	@echo "Please update version in main.py first"# Updated 20251109_123823
# Updated Sun Nov  9 12:52:31 CET 2025
