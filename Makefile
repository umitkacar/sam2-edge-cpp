.PHONY: help install install-dev test test-cov lint format clean build docs pre-commit cpp-build

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)EdgeSAM Development Makefile$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# ===== INSTALLATION =====

install: ## Install package for production
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e ".[dev]"
	pre-commit install

install-all: ## Install package with all optional dependencies
	pip install -e ".[all]"
	pre-commit install

# ===== TESTING =====

test: ## Run tests
	hatch run test:test

test-cov: ## Run tests with coverage
	hatch run test:test-cov

test-all: ## Run tests on all Python versions
	hatch run test:test

benchmark: ## Run benchmark tests
	pytest tests/ -m benchmark --benchmark-only

# ===== LINTING & FORMATTING =====

lint: ## Run all linters
	hatch run lint:all

lint-fix: ## Run linters with auto-fix
	hatch run lint:fmt

format: lint-fix ## Format code (alias for lint-fix)

ruff: ## Run ruff linter
	ruff check .

ruff-fix: ## Run ruff with auto-fix
	ruff check --fix .

black: ## Run black formatter
	black .

mypy: ## Run mypy type checker
	hatch run lint:typing

# ===== BUILDING =====

build: ## Build Python package
	hatch build

build-cpp: ## Build C++ project
	chmod +x build.sh
	./build.sh

clean: ## Clean build artifacts
	rm -rf build dist *.egg-info
	rm -rf .hatch .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# ===== DOCUMENTATION =====

docs: ## Build documentation
	cd docs && mkdocs build

docs-serve: ## Serve documentation locally
	cd docs && mkdocs serve

# ===== PRE-COMMIT =====

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	pre-commit autoupdate

# ===== COVERAGE =====

coverage: test-cov ## Generate coverage report
	hatch run cov-report

coverage-html: test-cov ## Generate HTML coverage report
	coverage html
	@echo "$(GREEN)Coverage report generated at htmlcov/index.html$(NC)"

# ===== SECURITY =====

security: ## Run security checks
	bandit -r edgesam_py -c pyproject.toml
	safety check

# ===== DEVELOPMENT =====

dev: install-dev pre-commit ## Setup development environment
	@echo "$(GREEN)Development environment ready!$(NC)"

shell: ## Start hatch shell
	hatch shell

version: ## Show version
	@python -c "from edgesam_py import __version__; print(__version__)"

# ===== CI/CD =====

ci: lint test build ## Run CI checks locally
	@echo "$(GREEN)All CI checks passed!$(NC)"

publish-test: build ## Publish to TestPyPI
	hatch publish -r test

publish: build ## Publish to PyPI
	hatch publish

# ===== DOCKER =====

docker-build: ## Build Docker image
	docker build -t edgesam:latest .

docker-run: ## Run Docker container
	docker run -it --rm edgesam:latest

# ===== UTILITIES =====

tree: ## Show project structure
	@tree -I '__pycache__|*.pyc|*.egg-info|.git|.hatch|.pytest_cache|.mypy_cache|.ruff_cache|htmlcov|dist|build'

check: ## Quick check (lint + test)
	@echo "$(BLUE)Running quick checks...$(NC)"
	@make lint
	@make test
	@echo "$(GREEN)All checks passed!$(NC)"

all: clean install-dev lint test build ## Run all development tasks
	@echo "$(GREEN)All tasks completed successfully!$(NC)"
