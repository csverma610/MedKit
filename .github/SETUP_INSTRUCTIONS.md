# GitHub Actions CI/CD Setup Instructions

Follow these steps to complete the setup of the CI/CD pipeline for MedKit.

## Prerequisites

- Administrator access to the MedKit GitHub repository
- Accounts for optional services (PyPI, Docker Hub, Codecov)

---

## Step 1: Enable GitHub Actions

GitHub Actions should be enabled by default for public repositories.

**To verify:**
1. Go to repository → **Settings**
2. Click **Actions** in the left sidebar
3. Ensure **Allow all actions and reusable workflows** is selected

---

## Step 2: Configure Required Secrets

### Only if using PyPI publishing:

1. Go to repository → **Settings** → **Secrets and variables** → **Actions**

2. Click **New repository secret**

3. Add secret:
   - **Name:** `PYPI_API_TOKEN`
   - **Value:** Your PyPI token (get from https://pypi.org/account/)

### Optional: Add Docker Hub credentials

1. Click **New repository secret**

2. Add secrets:
   - **Name:** `DOCKER_USERNAME`
   - **Value:** Your Docker Hub username

3. Add another:
   - **Name:** `DOCKER_PASSWORD`
   - **Value:** Your Docker Hub password or access token

### Optional: Add Google API Key for integration tests

1. Click **New repository secret**

2. Add secret:
   - **Name:** `GOOGLE_API_KEY`
   - **Value:** Your Gemini API key

---

## Step 3: Configure Branch Protection Rules

Recommended for the `main` branch:

1. Go to repository → **Settings** → **Branches**

2. Click **Add rule** under "Branch protection rules"

3. Configure for branch name: `main`

4. Enable:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**

5. Select required status checks:
   - `test (3.11)` - Python 3.11 tests (minimum)
   - `lint` - Code quality checks (recommended)
   - `type-check` - Type validation (recommended)

6. Click **Create**

---

## Step 4: Configure Code Owners

The `.github/CODEOWNERS` file is already created. To enable code owner reviews:

1. Go to repository → **Settings** → **Branches**

2. For `main` branch protection rule, enable:
   - ✅ **Require code owner reviews**

---

## Step 5: Set Up GitHub Pages (Optional)

To enable automatic documentation deployment:

1. Go to repository → **Settings** → **Pages**

2. Under "Source", select:
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`

3. Click **Save**

4. Documentation will be available at: `https://csverma610.github.io/medkit/`

---

## Step 6: Configure Dependabot (Optional)

Dependabot is configured via `.github/dependabot.yml`. To enable:

1. Go to repository → **Settings** → **Code security and analysis**

2. Enable **Dependabot alerts** (if not already enabled)

3. Enable **Dependabot security updates** (if not already enabled)

4. Dependabot will automatically create PRs for dependency updates

---

## Step 7: Configure Code Scanning (Optional)

For additional security scanning:

1. Go to repository → **Settings** → **Code security and analysis**

2. Enable **CodeQL analysis** (recommended for production)

3. This will add additional security scanning to your workflows

---

## Step 8: Add Status Badges to README

Add these badges to your README.md to show CI/CD status:

```markdown
## CI/CD Status

[![Tests](https://github.com/csverma610/medkit/actions/workflows/tests.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
[![Code Quality](https://github.com/csverma610/medkit/actions/workflows/code-quality.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
[![Documentation](https://github.com/csverma610/medkit/actions/workflows/docs.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
```

---

## Verification

### Test the setup locally first:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=medkit

# Check code quality
black --check medkit/ cli/ tests/
flake8 medkit/
mypy medkit/ --ignore-missing-imports

# Build documentation
cd docs && make clean html
```

### Trigger workflows manually:

1. Go to repository → **Actions**
2. Select a workflow
3. Click **Run workflow** (if available)

---

## First Release

When ready to make the first release:

```bash
# Create version tag
git tag -a v1.0.0 -m "Initial release"

# Push tag (triggers Release workflow)
git push origin v1.0.0
```

The Release workflow will:
- Build distribution packages
- Create GitHub Release with artifacts
- Publish to PyPI (if PYPI_API_TOKEN is configured)
- Build Docker image (if Docker credentials are configured)

---

## Troubleshooting

### Workflows not showing

**Problem:** Workflows don't appear in Actions tab

**Solution:**
- Verify workflows are in `.github/workflows/`
- Check workflow YAML syntax (validate at https://editor.swagger.io/)
- Wait a few minutes for GitHub to register new workflows

### Tests failing

**Problem:** Tests fail in CI but pass locally

**Solution:**
- Check Python version compatibility
- Verify environment variables are set
- Review detailed logs in Actions tab
- Run tests locally: `pytest tests/ -v`

### Secrets not working

**Problem:** Build fails with "secret not found"

**Solution:**
- Verify secret name matches exactly in workflow
- Secrets are case-sensitive
- Re-create secret if recently changed
- Wait a few minutes after adding secret

### Documentation not deploying

**Problem:** Documentation not updating on GitHub Pages

**Solution:**
- Verify GitHub Pages is configured (Settings → Pages)
- Check branch is set to `gh-pages`
- Verify docs build successfully in workflow logs
- May take a few minutes to appear

### Docker push failing

**Problem:** Docker image fails to push

**Solution:**
- Verify Docker Hub credentials are correct
- Check Docker Hub account is not rate-limited
- Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets

---

## Monitoring Workflows

### View workflow runs:
1. Go to repository → **Actions**
2. Click on a workflow name
3. See all runs for that workflow

### View detailed logs:
1. Click on a specific run
2. Click on a job (e.g., "test (3.11)")
3. Expand step logs to see details

### Set up notifications:
1. Go to https://github.com/settings/notifications
2. Configure workflow notification preferences

---

## Next Steps

1. ✅ Complete all setup steps above
2. Make a test commit to verify workflows run
3. Create a test release with tag `v0.1.0-rc1`
4. Review workflow logs and fix any issues
5. Set up branch protection rules
6. Begin development with confidence!

---

## Workflow Files Reference

| File | Purpose |
|------|---------|
| `.github/workflows/tests.yml` | Run pytest across Python versions |
| `.github/workflows/code-quality.yml` | Code linting, formatting, type-checking |
| `.github/workflows/docs.yml` | Build and deploy documentation |
| `.github/workflows/release.yml` | PyPI & Docker publishing |
| `.github/workflows/pull-request.yml` | PR validation checks |
| `.github/CODEOWNERS` | Code review assignments |
| `.github/dependabot.yml` | Automated dependency updates |
| `Dockerfile` | Container image definition |
| `.dockerignore` | Docker build exclusions |

---

## Documentation

- **Quick Reference:** See [WORKFLOWS_SUMMARY.md](./WORKFLOWS_SUMMARY.md)
- **Detailed Guide:** See [CI_CD_GUIDE.md](./CI_CD_GUIDE.md)
- **GitHub Actions Docs:** https://docs.github.com/en/actions

---

## Questions?

For help:
1. Review the detailed [CI_CD_GUIDE.md](./CI_CD_GUIDE.md)
2. Check workflow logs in Actions tab for error details
3. Consult GitHub Actions documentation
4. Open an issue on GitHub with logs and description

Good luck with your CI/CD setup! 🚀
