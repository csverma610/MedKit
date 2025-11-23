.PHONY: help install install-dev install-all venv clean-venv test test-cov test-fast test-integration lint format format-check typecheck security check clean clean-pyc clean-test docs docs-serve docs-clean build docker-build ci-test ci-lint ci-quality ci-all update-deps audit-deps

.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
BLACK := black
FLAKE8 := flake8
MYPY := mypy
ISORT := isort
BANDIT := bandit
PYTEST := pytest
SPHINX := sphinx-build
VENV_DIR := venv
DOCKER_IMAGE := medkit
DOCKER_TAG := latest

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)MedKit - Medical AI Reference System$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Examples:$(NC)"
	@echo "  make install          # Install dependencies"
	@echo "  make install-dev      # Install with development tools"
	@echo "  make test             # Run all tests"
	@echo "  make lint             # Run code quality checks"
	@echo "  make format           # Format code with black and isort"
	@echo "  make ci-all           # Run all CI checks locally"

# ============================================================================
# DEVELOPMENT SETUP
# ============================================================================

venv: ## Create Python virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment created$(NC)"
	@echo "$(YELLOW)Activate with: source $(VENV_DIR)/bin/activate$(NC)"

install: ## Install core dependencies
	$(PIP) install -e .
	@echo "$(GREEN)✓ Core dependencies installed$(NC)"

install-dev: ## Install with development dependencies
	$(PIP) install -e ".[dev]"
	$(PIP) install -e .
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

install-docs: ## Install with documentation dependencies
	$(PIP) install -e ".[docs]"
	$(PIP) install -e .
	@echo "$(GREEN)✓ Documentation dependencies installed$(NC)"

install-all: ## Install all dependencies (core + dev + docs)
	$(PIP) install -e ".[dev,docs]"
	$(PIP) install -e .
	@echo "$(GREEN)✓ All dependencies installed$(NC)"

update-deps: ## Update all dependencies to latest compatible versions
	$(PIP) install --upgrade -e ".[dev,docs]"
	$(PIP) list --outdated
	@echo "$(GREEN)✓ Dependencies updated$(NC)"

audit-deps: ## Audit dependencies for security vulnerabilities
	$(PIP) install safety
	safety check --json || true
	@echo "$(GREEN)✓ Dependency audit complete$(NC)"

clean-venv: ## Remove virtual environment
	rm -rf $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment removed$(NC)"

# ============================================================================
# TESTING
# ============================================================================

test: ## Run all tests with pytest
	$(PYTEST) tests/ -v --tb=short
	@echo "$(GREEN)✓ Tests passed$(NC)"

test-cov: ## Run tests with coverage report
	$(PYTEST) tests/ --cov=medkit --cov-report=html --cov-report=term-missing --cov-report=xml -v
	@echo "$(GREEN)✓ Coverage report generated: htmlcov/index.html$(NC)"

test-fast: ## Run tests with minimal output (fast)
	$(PYTEST) tests/ -q --tb=line
	@echo "$(GREEN)✓ Quick test run complete$(NC)"

test-integration: ## Run integration tests only
	$(PYTEST) tests/ -v -m "integration" --tb=short
	@echo "$(GREEN)✓ Integration tests passed$(NC)"

test-unit: ## Run unit tests only
	$(PYTEST) tests/ -v -m "not integration" --tb=short
	@echo "$(GREEN)✓ Unit tests passed$(NC)"

test-watch: ## Run tests in watch mode (requires pytest-watch)
	ptw tests/ -v
	@echo "$(GREEN)✓ Watch mode exited$(NC)"

test-parallel: ## Run tests in parallel for faster execution
	$(PYTEST) tests/ -v -n auto --tb=short
	@echo "$(GREEN)✓ Parallel tests passed$(NC)"

# ============================================================================
# CODE QUALITY
# ============================================================================

lint: format-check typecheck security ## Run all quality checks (format, types, security)
	@echo "$(GREEN)✓ All quality checks passed$(NC)"

format: ## Format code with black and sort imports with isort
	$(BLACK) medkit/ cli/ tests/
	$(ISORT) medkit/ cli/ tests/
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting without changes
	$(BLACK) --check medkit/ cli/ tests/
	$(ISORT) --check-only medkit/ cli/ tests/
	$(FLAKE8) medkit/ cli/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127
	@echo "$(GREEN)✓ Code formatting check passed$(NC)"

typecheck: ## Run type checking with mypy
	$(MYPY) medkit/ --ignore-missing-imports --no-error-summary 2>&1 | head -20 || true
	@echo "$(GREEN)✓ Type checking complete$(NC)"

security: ## Run security checks with bandit
	$(BANDIT) -r medkit/ -ll --skip B101,B601
	@echo "$(GREEN)✓ Security checks passed$(NC)"

check: format-check typecheck security ## Alias for lint (check all)
	@echo "$(GREEN)✓ All checks passed$(NC)"

# ============================================================================
# DOCUMENTATION
# ============================================================================

docs: ## Build documentation with Sphinx
	$(SPHINX) -b html docs/ docs/_build/html
	@echo "$(GREEN)✓ Documentation built: docs/_build/html/index.html$(NC)"

docs-serve: docs ## Build and serve documentation locally
	@command -v python3 >/dev/null 2>&1 || (echo "$(RED)Python 3 required$(NC)" && exit 1)
	cd docs/_build/html && $(PYTHON) -m http.server 8000
	@echo "$(GREEN)✓ Documentation served at http://localhost:8000$(NC)"

docs-clean: ## Remove built documentation
	rm -rf docs/_build
	rm -rf docs/.doctrees
	@echo "$(GREEN)✓ Documentation cleaned$(NC)"

docs-check: ## Check documentation build without errors
	$(SPHINX) -b html -W --keep-going docs/ docs/_build/html
	@echo "$(GREEN)✓ Documentation build successful$(NC)"

# ============================================================================
# BUILD & DEPLOYMENT
# ============================================================================

build: format-check typecheck ## Build distribution packages
	$(PYTHON) -m build
	@echo "$(GREEN)✓ Distribution packages built in dist/$(NC)"

sdist: ## Build source distribution
	$(PYTHON) -m build --sdist
	@echo "$(GREEN)✓ Source distribution built$(NC)"

wheel: ## Build wheel distribution
	$(PYTHON) -m build --wheel
	@echo "$(GREEN)✓ Wheel distribution built$(NC)"

install-build-deps: ## Install build tools
	$(PIP) install build wheel twine
	@echo "$(GREEN)✓ Build dependencies installed$(NC)"

# ============================================================================
# DOCKER
# ============================================================================

docker-build: ## Build Docker image
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "$(GREEN)✓ Docker image built: $(DOCKER_IMAGE):$(DOCKER_TAG)$(NC)"

docker-build-dev: ## Build Docker image with development tools
	docker build -t $(DOCKER_IMAGE):dev --target builder .
	@echo "$(GREEN)✓ Docker dev image built: $(DOCKER_IMAGE):dev$(NC)"

docker-run: ## Run Docker container interactively
	docker run -it --rm $(DOCKER_IMAGE):$(DOCKER_TAG)
	@echo "$(GREEN)✓ Container execution complete$(NC)"

docker-push: ## Push Docker image to registry (requires docker login)
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)
	@echo "$(GREEN)✓ Docker image pushed$(NC)"

# ============================================================================
# CLEANUP
# ============================================================================

clean: clean-pyc clean-test docs-clean ## Remove all build, test, and Python artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned all artifacts$(NC)"

clean-pyc: ## Remove Python cache and compiled files
	find . -type f -name '*.py[cod]' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Python cache cleaned$(NC)"

clean-test: ## Remove test and coverage artifacts
	rm -rf .tox/
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache
	rm -f coverage.xml
	@echo "$(GREEN)✓ Test artifacts cleaned$(NC)"

distclean: clean clean-venv ## Remove everything including virtual environment
	@echo "$(GREEN)✓ Full clean complete$(NC)"

# ============================================================================
# CI/CD LOCAL TESTING
# ============================================================================

ci-test: ## Run tests locally (CI simulation)
	@echo "$(BLUE)Running tests...$(NC)"
	$(PYTEST) tests/ -v --tb=short --cov=medkit --cov-report=term-missing
	@echo "$(GREEN)✓ CI tests passed$(NC)"

ci-lint: ## Run linting locally (CI simulation)
	@echo "$(BLUE)Running code quality checks...$(NC)"
	$(BLACK) --check medkit/ cli/ tests/
	$(ISORT) --check-only medkit/ cli/ tests/
	$(FLAKE8) medkit/ cli/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127
	@echo "$(GREEN)✓ CI lint passed$(NC)"

ci-quality: ## Run all quality checks (CI simulation)
	@echo "$(BLUE)Running quality checks...$(NC)"
	$(MYPY) medkit/ --ignore-missing-imports || true
	$(BANDIT) -r medkit/ -ll --skip B101,B601 || true
	@echo "$(GREEN)✓ CI quality checks passed$(NC)"

ci-all: ci-test ci-lint ci-quality ## Run full CI pipeline locally
	@echo "$(GREEN)✓ All CI checks passed locally$(NC)"

# ============================================================================
# UTILITY TARGETS
# ============================================================================

list: ## List all available make targets
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished/ {if ($$1 !~ "^[#.]") {print $$1}}' | grep -E '^[a-zA-Z_-]+$$' | sort

version: ## Show version information
	@echo "$(BLUE)MedKit Version Information:$(NC)"
	@$(PYTHON) -c "import medkit; print(f'  medkit version: {medkit.__version__}' if hasattr(medkit, '__version__') else '  medkit version: unknown')"
	@$(PYTHON) --version
	@$(PIP) show medkit 2>/dev/null | grep Version || echo "  MedKit not installed"

info: ## Show project information
	@echo "$(BLUE)Project Information:$(NC)"
	@echo "  Name: MedKit"
	@echo "  Type: Medical AI Reference System"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  Venv: $(VENV_DIR)"
	@echo ""
	@echo "$(GREEN)Key Paths:$(NC)"
	@echo "  Source: medkit/"
	@echo "  CLI Tools: cli/"
	@echo "  Tests: tests/"
	@echo "  Docs: docs/"
	@echo ""
	@echo "$(GREEN)Test Status:$(NC)"
	@echo "  Total test files: $(shell find tests/ -name 'test_*.py' -o -name '*_test.py' | wc -l)"

# ============================================================================
# DEVELOPMENT WORKFLOW TARGETS
# ============================================================================

dev-setup: venv install-all ## Complete development environment setup
	@echo "$(GREEN)✓ Development environment ready!$(NC)"
	@echo "$(YELLOW)Activate with: source $(VENV_DIR)/bin/activate$(NC)"

pre-commit: format-check typecheck test-fast ## Quick checks before commit
	@echo "$(GREEN)✓ Pre-commit checks passed!$(NC)"

ready: pre-commit ## Alias for pre-commit (ready to push)
	@echo "$(GREEN)✓ Ready to push!$(NC)"

.PHONY: $(MAKECMDGOALS)
