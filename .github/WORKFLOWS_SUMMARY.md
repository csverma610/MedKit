# MedKit CI/CD Workflows Summary

## Quick Reference

| Workflow | Trigger | Purpose | Status |
|----------|---------|---------|--------|
| **Tests** | Push/PR to main, develop | Run pytest across Python 3.8-3.12 | ✅ Configured |
| **Code Quality** | Push/PR to main, develop | Lint, format, type-check, security scan | ✅ Configured |
| **Documentation** | Push/PR to main, develop | Build and deploy Sphinx docs | ✅ Configured |
| **Release** | Tag push (v*) | Publish to PyPI and Docker Hub | ✅ Configured |
| **Pull Request** | PR to main, develop | Validate commits and encourage tests/docs | ✅ Configured |

---

## Files Created

```
.github/
├── workflows/
│   ├── tests.yml                 # Test suite across Python versions
│   ├── code-quality.yml          # Linting, formatting, type-checking
│   ├── docs.yml                  # Sphinx documentation build & deploy
│   ├── release.yml               # PyPI & Docker Hub publishing
│   └── pull-request.yml          # PR validation checks
├── CODEOWNERS                     # Code review assignments
├── dependabot.yml                # Automated dependency updates
├── CI_CD_GUIDE.md                # Comprehensive CI/CD documentation
└── WORKFLOWS_SUMMARY.md          # This file

Dockerfile                         # Multi-stage container build
.dockerignore                      # Docker build exclusions
```

---

## Setup Checklist

### GitHub Repository Settings

- [ ] Enable GitHub Actions (should be default for public repos)
- [ ] Add required secrets (if needed):
  - `PYPI_API_TOKEN` - for PyPI publishing
  - `DOCKER_USERNAME` - for Docker Hub (optional)
  - `DOCKER_PASSWORD` - for Docker Hub (optional)
  - `GOOGLE_API_KEY` - for integration tests (optional)

### Repository Branch Protection

Recommended settings for `main` branch:
- [ ] Require pull request reviews before merging
- [ ] Require status checks to pass before merging:
  - `test (3.11)` - at minimum
  - `lint` - recommended
  - `type-check` - recommended

### Local Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run pre-commit checks
black medkit/ cli/ tests/
isort medkit/ cli/ tests/
flake8 medkit/
mypy medkit/ --ignore-missing-imports
pytest tests/ -v
```

---

## Common Operations

### Running Tests Locally
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=medkit --cov-report=html

# Specific test file
pytest tests/test_disease_info.py -v
```

### Code Quality Checks
```bash
# Format code
black medkit/ cli/ tests/

# Fix import sorting
isort medkit/ cli/ tests/

# Lint
flake8 medkit/

# Type checking
mypy medkit/ --ignore-missing-imports
```

### Building Documentation
```bash
cd docs
make clean html
# Open: docs/_build/html/index.html
```

### Creating a Release
```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release version 1.2.3"

# Push tag (triggers release workflow)
git push origin v1.2.3

# Workflow will:
# 1. Build distribution packages
# 2. Create GitHub Release
# 3. Publish to PyPI
# 4. Build and push Docker image
```

---

## Workflow Details

### 1. Tests Workflow
- **Runs:** pytest across Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Reports:** Coverage to Codecov, HTML artifacts to GitHub
- **Time:** ~2-3 minutes per Python version
- **On failure:** PR cannot be merged (configure in branch protection)

### 2. Code Quality Workflow
- **Linting:** Checks syntax, style, complexity
- **Formatting:** Validates black formatting
- **Imports:** Checks isort ordering
- **Type hints:** Validates mypy types
- **Security:** Scans with bandit and safety
- **Time:** ~1-2 minutes
- **On failure:** Non-blocking warnings (can be configured as required)

### 3. Documentation Workflow
- **Builds:** Sphinx HTML documentation
- **Artifacts:** Available for PR preview
- **Deploy:** Auto-deploys to GitHub Pages on main branch
- **Time:** ~1 minute
- **Access:** https://csverma610.github.io/medkit/

### 4. Release Workflow
- **Triggers:** When a tag matching `v*` is pushed
- **Builds:** Python wheel and sdist packages
- **Publishes:** To PyPI automatically
- **Docker:** Builds and pushes image to Docker Hub
- **GitHub:** Creates Release with artifacts
- **Time:** ~2-3 minutes

### 5. Pull Request Workflow
- **Validates:** Conventional commit format
- **Checks:** For documentation and test updates
- **Warns:** About missing CHANGELOG.md
- **Time:** ~30 seconds

---

## Environment Variables

### Required
- `GOOGLE_API_KEY` - For integration tests (set in GitHub Secrets)

### Optional
- `PYPI_API_TOKEN` - For PyPI publishing (GitHub Secret)
- `DOCKER_USERNAME` - For Docker Hub (GitHub Secret)
- `DOCKER_PASSWORD` - For Docker Hub (GitHub Secret)

---

## Monitoring

### View Workflow Status
1. Go to repository → **Actions** tab
2. See recent workflow runs
3. Click on a run for detailed logs

### Coverage Reports
- **Codecov:** https://codecov.io/gh/csverma610/medkit
- **Local HTML:** Run `pytest --cov-report=html`, open `htmlcov/index.html`

### Documentation
- **GitHub Pages:** https://csverma610.github.io/medkit/
- **Local build:** Run `cd docs && make html`

---

## Troubleshooting

### Workflow Not Running
- [ ] Check branch name matches trigger (main/develop)
- [ ] Verify workflows are enabled in Actions settings
- [ ] Check if changes match file patterns

### Tests Failing
- [ ] Run locally: `pytest tests/ -v`
- [ ] Check Python version compatibility
- [ ] Review test logs in Actions tab

### Code Quality Warnings
- [ ] Format code: `black medkit/`
- [ ] Sort imports: `isort medkit/`
- [ ] Run linter: `flake8 medkit/`

### Release Not Publishing
- [ ] Verify tag format: `v1.2.3`
- [ ] Check secrets are configured
- [ ] Review release workflow logs

---

## Next Steps

1. **Add status badges to README.md:**
   ```markdown
   [![Tests](https://github.com/csverma610/medkit/actions/workflows/tests.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
   ```

2. **Configure branch protection rules** in GitHub Settings

3. **Set up code review assignments** using CODEOWNERS

4. **Enable Dependabot** for automated dependency updates

5. **Configure Codecov** integration for coverage tracking

6. **Set up issue templates** for consistent bug reports

---

## Support

For detailed information, see [CI_CD_GUIDE.md](./CI_CD_GUIDE.md)

For GitHub Actions documentation: https://docs.github.com/en/actions
