# MedKit CI/CD Pipeline Guide

This document describes the GitHub Actions CI/CD pipeline configured for the MedKit project.

## Overview

MedKit uses GitHub Actions to automate testing, code quality checks, documentation building, and releases. The pipeline ensures code quality and reliability with every push and pull request.

## Workflows

### 1. Tests Workflow (`.github/workflows/tests.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**What it does:**
- Tests against Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Installs dependencies from `requirements-dev.txt`
- Runs pytest with coverage reporting
- Uploads coverage reports to Codecov
- Archives HTML coverage reports as artifacts
- (Optional) Runs integration tests with Gemini API on main branch

**Key features:**
- Parallel testing across multiple Python versions
- Dependency caching for faster builds
- Coverage reporting with HTML artifacts
- Codecov integration for tracking coverage over time

**How to run locally:**
```bash
pytest tests/ -v --cov=medkit --cov-report=html
```

---

### 2. Code Quality Workflow (`.github/workflows/code-quality.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**What it does:**
- **Linting:** Checks code with flake8 for syntax errors and style issues
- **Formatting:** Verifies code formatting with black
- **Import sorting:** Checks import order with isort
- **Type checking:** Validates type hints with mypy
- **Security:** Scans for security issues with bandit
- **Dependencies:** Checks for known vulnerabilities with safety

**Key features:**
- Non-blocking checks that report issues without failing the build
- Three separate jobs for efficiency:
  - `lint` - Code style and formatting checks
  - `type-check` - Type annotation validation
  - `security` - Security vulnerability scanning

**How to run locally:**
```bash
# Format code
black medkit/ cli/ tests/
isort medkit/ cli/ tests/

# Lint code
flake8 medkit/

# Type check
mypy medkit/ --ignore-missing-imports

# Security scan
bandit -r medkit/ -ll
safety check
```

---

### 3. Documentation Workflow (`.github/workflows/docs.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**What it does:**
- Builds Sphinx documentation
- Uploads documentation as artifacts
- Deploys documentation to GitHub Pages on main branch pushes

**Key features:**
- Uses Sphinx to build HTML documentation
- Archives documentation artifacts for PR reviews
- Automatic GitHub Pages deployment for main branch
- Supports full API documentation generation

**How to run locally:**
```bash
cd docs
make clean html
# View in browser: docs/_build/html/index.html
```

---

### 4. Release Workflow (`.github/workflows/release.yml`)

**Triggers:**
- Pushes to tags matching `v*` (e.g., `v1.0.0`, `v2.1.3`)

**What it does:**
- Builds Python distribution (wheel and sdist)
- Creates GitHub Release with artifacts
- Publishes package to PyPI
- (Optional) Builds and pushes Docker images

**Key features:**
- Automated PyPI publishing
- GitHub Release creation with build artifacts
- Docker image building and pushing
- Supports semantic versioning

**How to create a release:**
```bash
# Create a tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push the tag
git push origin v1.0.0
```

**Required secrets:**
- `PYPI_API_TOKEN` - PyPI API token for publishing
- `DOCKER_USERNAME` - Docker Hub username (optional)
- `DOCKER_PASSWORD` - Docker Hub password (optional)

---

### 5. Pull Request Checks (`.github/workflows/pull-request.yml`)

**Triggers:**
- Pull requests to `main` or `develop` branches

**What it does:**
- Validates PR title against conventional commits format
- Checks for PR description content
- Warns about missing documentation updates
- Warns about missing test updates
- Checks for CHANGELOG.md

**Key features:**
- Enforces conventional commit messages
- Encourages documentation and test coverage
- Provides helpful warnings for contributors

---

## Configuration Files

### `.github/CODEOWNERS`
Defines who should be notified for pull request reviews. Currently all files are owned by `@csverma610`.

### `.github/dependabot.yml`
Configures automated dependency updates:
- **Python dependencies:** Weekly updates on Mondays at 3 AM UTC
- **GitHub Actions:** Weekly updates on Mondays at 4 AM UTC

Creates automated pull requests for dependency updates, allowing you to review and merge them.

### `Dockerfile` & `.dockerignore`
Provides containerized deployment:
- Multi-stage build for optimal image size
- Non-root user for security
- Health checks for container monitoring
- Python 3.11 slim image for minimal footprint

---

## Secrets Required

To fully utilize the CI/CD pipeline, configure these secrets in GitHub:

### Optional Secrets

1. **`GOOGLE_API_KEY`** - Required for integration tests with Gemini API
   - Set in repository settings: Settings → Secrets and variables → Actions
   - Used for testing medical data fetching

2. **`PYPI_API_TOKEN`** - Required for PyPI publishing
   - Get from https://pypi.org/account/
   - Used in Release workflow

3. **`DOCKER_USERNAME`** & **`DOCKER_PASSWORD`** - Required for Docker publishing
   - Docker Hub credentials
   - Used in Release workflow for pushing Docker images

### GitHub Token
- `GITHUB_TOKEN` is automatically provided by GitHub Actions
- Used for creating releases and publishing to GitHub Pages

---

## Status Badges

Add these badges to your README.md to display CI/CD status:

```markdown
![Tests](https://github.com/csverma610/medkit/actions/workflows/tests.yml/badge.svg)
![Code Quality](https://github.com/csverma610/medkit/actions/workflows/code-quality.yml/badge.svg)
![Documentation](https://github.com/csverma610/medkit/actions/workflows/docs.yml/badge.svg)
```

---

## Monitoring and Troubleshooting

### View Workflow Runs
1. Go to repository → Actions tab
2. Select a workflow to see recent runs
3. Click on a run to see detailed logs

### Common Issues

#### Tests failing on multiple Python versions
- Check if code uses version-specific features
- Ensure all dependencies support the target Python versions
- Update `setup.py` to specify supported versions

#### Coverage not being reported
- Ensure `coverage.xml` is generated by pytest
- Check Codecov integration in repository settings

#### Documentation build failures
- Verify Sphinx configuration in `docs/conf.py`
- Check for broken references or missing modules
- Ensure all required Sphinx extensions are in `requirements-dev.txt`

#### Release workflow not triggering
- Verify tag matches `v*` pattern (e.g., `v1.0.0`)
- Check that secrets are properly configured
- Ensure you're pushing tags: `git push origin <tagname>`

---

## Best Practices

1. **Always run tests locally before pushing:**
   ```bash
   pytest tests/ -v --cov=medkit
   ```

2. **Format code before committing:**
   ```bash
   black medkit/ cli/ tests/
   isort medkit/ cli/ tests/
   ```

3. **Create conventional commit messages:**
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for test additions
   - `chore:` for maintenance

4. **Update tests with code changes:**
   - Every feature should have tests
   - Every bug fix should include a regression test

5. **Update documentation with code changes:**
   - Update docstrings
   - Update README if applicable
   - Update API documentation

6. **Use semantic versioning for releases:**
   - `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
   - Bump MAJOR for breaking changes
   - Bump MINOR for new features
   - Bump PATCH for bug fixes

---

## Integration with Development Workflow

### Local Development
```bash
# Clone and setup
git clone https://github.com/csverma610/medkit.git
cd medkit
pip install -e ".[dev]"

# Make changes
# ... edit files ...

# Test locally
pytest tests/ -v

# Format and lint
black medkit/ cli/ tests/
isort medkit/ cli/ tests/
flake8 medkit/

# Commit with conventional format
git commit -m "feat: add new feature description"

# Push
git push origin feature-branch

# Create Pull Request on GitHub
```

### Release Process
```bash
# Update version in setup.py if needed
# Run full test suite locally
pytest tests/

# Create tag
git tag -a v1.2.3 -m "Release v1.2.3"

# Push tag (triggers Release workflow)
git push origin v1.2.3
```

---

## Advanced Customization

### Modifying Test Matrix
Edit `.github/workflows/tests.yml` to change Python versions:
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
```

### Adding Required Status Checks
In GitHub repository settings:
1. Go to Settings → Branches
2. Under "Require status checks to pass before merging"
3. Select which workflows must pass

### Skipping Workflows for Certain Changes
Use skip instructions in commit messages:
```bash
git commit -m "docs: update readme [skip ci]"
```

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)

---

## Questions or Issues?

For questions about the CI/CD setup, please:
1. Check the workflow logs in the Actions tab
2. Review this guide for common solutions
3. Open an issue on GitHub with detailed information
