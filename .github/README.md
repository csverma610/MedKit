# MedKit GitHub Actions CI/CD Pipeline

Welcome to the MedKit CI/CD documentation! This directory contains all the configuration files for automated testing, code quality checks, documentation builds, and releases.

## 📁 Directory Structure

```
.github/
├── workflows/                    # GitHub Actions workflow definitions
│   ├── tests.yml                 # Run tests across Python 3.8-3.12
│   ├── code-quality.yml          # Linting, formatting, type-checking
│   ├── docs.yml                  # Build & deploy Sphinx documentation
│   ├── release.yml               # PyPI & Docker Hub publishing
│   └── pull-request.yml          # PR validation and checks
├── CODEOWNERS                     # Code review assignments
├── dependabot.yml                # Automated dependency updates
├── SETUP_INSTRUCTIONS.md         # ⭐ START HERE - Initial setup
├── WORKFLOWS_SUMMARY.md          # Quick reference guide
├── CI_CD_GUIDE.md                # Detailed documentation
└── README.md                      # This file
```

---

## 🚀 Quick Start

### For New Setup

1. **Follow the setup instructions:**
   - Read [`SETUP_INSTRUCTIONS.md`](./SETUP_INSTRUCTIONS.md)
   - Configure secrets in GitHub
   - Enable branch protection rules

2. **Test locally:**
   ```bash
   pip install -e ".[dev]"
   pytest tests/ -v --cov=medkit
   ```

3. **Make a test commit:**
   ```bash
   git add .
   git commit -m "ci: add github actions ci/cd pipeline"
   git push origin main
   ```

4. **Monitor in Actions tab:**
   - Go to repository → **Actions**
   - Watch workflows run automatically

### For Existing Setup

Jump to the relevant section:
- **Quick reference:** [`WORKFLOWS_SUMMARY.md`](./WORKFLOWS_SUMMARY.md)
- **Detailed guide:** [`CI_CD_GUIDE.md`](./CI_CD_GUIDE.md)
- **Troubleshooting:** See SETUP_INSTRUCTIONS.md section

---

## 📋 What's Included

### Workflows

| Workflow | Trigger | What It Does |
|----------|---------|-------------|
| **Tests** | Push/PR | Runs pytest across Python 3.8-3.12 with coverage |
| **Code Quality** | Push/PR | Linting, formatting, type-checking, security scans |
| **Documentation** | Push/PR | Builds Sphinx docs, deploys to GitHub Pages |
| **Release** | Tag push | Publishes to PyPI and Docker Hub |
| **Pull Request** | PR created | Validates commits, checks tests/docs |

### Configuration

| File | Purpose |
|------|---------|
| `CODEOWNERS` | Assigns code reviewers by file/directory |
| `dependabot.yml` | Automated weekly dependency updates |
| `Dockerfile` | Multi-stage container build (optional) |
| `.dockerignore` | Docker build exclusions |

### Documentation

| File | Content |
|------|---------|
| `SETUP_INSTRUCTIONS.md` | Step-by-step setup guide |
| `WORKFLOWS_SUMMARY.md` | Quick reference and checklist |
| `CI_CD_GUIDE.md` | Comprehensive documentation |
| `README.md` | This file |

---

## 🔧 Workflows Overview

### Tests Workflow
- **Runs on:** Push to main/develop, PRs to main/develop
- **Python versions:** 3.8, 3.9, 3.10, 3.11, 3.12
- **Reports:** Coverage to Codecov, HTML artifacts
- **Time:** ~2-3 minutes per version

```bash
# Run locally
pytest tests/ -v --cov=medkit --cov-report=html
```

### Code Quality Workflow
- **Runs on:** Push to main/develop, PRs to main/develop
- **Checks:** Linting, formatting, import sorting, type-checking, security
- **Tools:** flake8, black, isort, mypy, bandit, safety
- **Time:** ~1-2 minutes

```bash
# Run locally
black medkit/ cli/ tests/
isort medkit/ cli/ tests/
flake8 medkit/
mypy medkit/ --ignore-missing-imports
```

### Documentation Workflow
- **Runs on:** Push to main/develop, PRs to main/develop
- **Builds:** Sphinx HTML documentation
- **Deploys:** To GitHub Pages on main branch
- **Time:** ~1 minute

```bash
# Build locally
cd docs && make clean html
```

### Release Workflow
- **Runs on:** Tag push matching `v*` pattern
- **Publishes:** To PyPI and Docker Hub
- **Creates:** GitHub Release with artifacts
- **Time:** ~2-3 minutes

```bash
# Trigger release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Pull Request Workflow
- **Runs on:** PR to main/develop
- **Validates:** Conventional commits, encourages tests/docs
- **Time:** ~30 seconds

---

## 🔐 Secrets Configuration

### Required (if using PyPI)
- `PYPI_API_TOKEN` - Get from https://pypi.org/account/

### Optional
- `GOOGLE_API_KEY` - For integration tests with Gemini API
- `DOCKER_USERNAME` - Docker Hub username (for Docker publishing)
- `DOCKER_PASSWORD` - Docker Hub password/token (for Docker publishing)

**How to add:**
1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Enter Name and Value
4. Click "Add secret"

---

## ✅ Setup Checklist

- [ ] Read [`SETUP_INSTRUCTIONS.md`](./SETUP_INSTRUCTIONS.md)
- [ ] Add required secrets (if applicable)
- [ ] Configure branch protection rules for `main`
- [ ] Enable GitHub Pages (optional)
- [ ] Enable Dependabot (optional)
- [ ] Add status badges to README
- [ ] Run workflows locally to test
- [ ] Make test commit to trigger workflows
- [ ] Review workflow logs

---

## 📊 Monitoring & Visibility

### View Workflow Runs
1. Go to repository → **Actions**
2. Click on workflow name
3. Select a run to see details

### Add Status Badges
```markdown
[![Tests](https://github.com/csverma610/medkit/actions/workflows/tests.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
[![Code Quality](https://github.com/csverma610/medkit/actions/workflows/code-quality.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
[![Documentation](https://github.com/csverma610/medkit/actions/workflows/docs.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
```

### Coverage Reports
- **Codecov:** https://codecov.io/gh/csverma610/medkit
- **Local:** `pytest --cov-report=html` then open `htmlcov/index.html`

### Documentation
- **GitHub Pages:** https://csverma610.github.io/medkit/
- **Local:** `cd docs && make html`

---

## 🔨 Local Development Workflow

```bash
# 1. Make changes
# ... edit files ...

# 2. Run tests locally
pytest tests/ -v --cov=medkit

# 3. Format code
black medkit/ cli/ tests/
isort medkit/ cli/ tests/

# 4. Check code quality
flake8 medkit/
mypy medkit/ --ignore-missing-imports

# 5. Commit with conventional message
git commit -m "feat: describe your changes"

# 6. Push to feature branch
git push origin feature-branch

# 7. Create pull request on GitHub
# ... workflow checks run automatically ...

# 8. After merge, create release (optional)
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

---

## 📚 Documentation Files

### [`SETUP_INSTRUCTIONS.md`](./SETUP_INSTRUCTIONS.md)
Complete step-by-step setup guide:
- Configuring secrets
- Setting up branch protection
- Enabling GitHub Pages
- Configuring Dependabot
- Adding status badges
- Troubleshooting

### [`WORKFLOWS_SUMMARY.md`](./WORKFLOWS_SUMMARY.md)
Quick reference guide:
- Workflow table
- Common operations
- Checklist
- Environment variables
- Troubleshooting tips

### [`CI_CD_GUIDE.md`](./CI_CD_GUIDE.md)
Comprehensive detailed guide:
- Full workflow descriptions
- Configuration file explanations
- Secrets and authentication
- Status badges
- Advanced customization
- Best practices

---

## 🐛 Troubleshooting

### Workflows not running
- [ ] Verify branch name (main/develop)
- [ ] Check Actions are enabled in Settings
- [ ] Wait a few minutes for GitHub to register

### Tests failing
- [ ] Run locally: `pytest tests/ -v`
- [ ] Check Python version compatibility
- [ ] Review detailed logs in Actions tab

### Secrets not working
- [ ] Verify secret name matches exactly
- [ ] Secrets are case-sensitive
- [ ] Wait a few minutes after adding

### Documentation not deploying
- [ ] Verify GitHub Pages is enabled
- [ ] Check branch is set to `gh-pages`
- [ ] View docs build logs in Actions tab

See [`SETUP_INSTRUCTIONS.md`](./SETUP_INSTRUCTIONS.md) for more troubleshooting.

---

## 🚢 Making a Release

```bash
# Tag and push (triggers Release workflow)
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

The Release workflow will:
- Build distribution packages
- Create GitHub Release with artifacts
- Publish to PyPI (if token configured)
- Push Docker image (if credentials configured)

---

## 📖 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)

---

## 🎯 Next Steps

1. **Read:** [`SETUP_INSTRUCTIONS.md`](./SETUP_INSTRUCTIONS.md)
2. **Configure:** GitHub secrets and branch protection
3. **Test:** Run workflows locally and on GitHub
4. **Monitor:** Watch Actions tab as you develop
5. **Iterate:** Workflows run on every push and PR

---

## ❓ Questions?

1. Check relevant documentation above
2. Review workflow logs in Actions tab
3. Consult GitHub Actions documentation
4. Open an issue on GitHub with details

---

**Happy coding! 🚀**

Last updated: 2025-11-08
