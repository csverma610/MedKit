# Quick Start: GitHub Actions CI/CD for MedKit

Get your CI/CD pipeline running in 5 minutes!

---

## 🚀 5-Minute Setup

### Step 1: Enable GitHub Actions (1 minute)
1. Go to your GitHub repository
2. Click **Settings** → **Actions** → **General**
3. Verify **Allow all actions and reusable workflows** is selected
4. ✅ Done

### Step 2: Add Secrets (2 minutes) - *Only if publishing*

**Skip this if not publishing to PyPI or Docker Hub**

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token from https://pypi.org/account/
4. Click **Add secret**
5. ✅ Done

### Step 3: Configure Branch Protection (2 minutes)

1. Go to **Settings** → **Branches**
2. Click **Add rule**
3. Branch name pattern: `main`
4. Check:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
5. Select status checks:
   - `test (3.11)`
   - `lint` (recommended)
6. Click **Create**
7. ✅ Done

---

## 🧪 Test Locally (3 minutes)

Before pushing, test your setup:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=medkit

# Format code
black medkit/ cli/ tests/

# Check quality
flake8 medkit/

# Type check
mypy medkit/ --ignore-missing-imports
```

---

## 📤 First Commit (2 minutes)

Push to trigger the workflows:

```bash
# Stage changes
git add .

# Commit
git commit -m "ci: add github actions ci/cd pipeline"

# Push
git push origin main
```

---

## 👀 Monitor Workflows (1 minute)

1. Go to your repository
2. Click **Actions** tab
3. Watch workflows run
4. Click on a workflow to see details

---

## 📊 Workflows Running

You should see:
- ✅ **Tests** - Running pytest
- ✅ **Code Quality** - Linting and formatting
- ✅ **Documentation** - Building docs
- ✅ **Pull Request** - Only on PRs

---

## 🚢 Create a Release (2 minutes)

When ready to release:

```bash
# Create tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Push tag (triggers Release workflow)
git push origin v1.0.0
```

The Release workflow will:
- Build distribution packages
- Create GitHub Release
- Publish to PyPI (if configured)

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Workflows appear in Actions tab
- [ ] Workflows run on push
- [ ] Tests pass
- [ ] Code quality checks pass
- [ ] Documentation builds
- [ ] Status badge appears (refresh Actions tab)

---

## 📚 Need More Information?

| Task | Document |
|------|----------|
| Quick reference | `WORKFLOWS_SUMMARY.md` |
| Detailed setup | `SETUP_INSTRUCTIONS.md` |
| Troubleshooting | `CI_CD_GUIDE.md` |
| Overview | `README.md` |
| Implementation | `IMPLEMENTATION_SUMMARY.md` |

---

## 🆘 Common Issues

### Workflows not showing
- Wait 5 minutes for GitHub to register
- Refresh page
- Check Actions settings

### Tests failing
- Run locally: `pytest tests/ -v`
- Check Python version compatibility
- Review action logs for details

### Status checks not running
- Verify branch name is `main` or `develop`
- Check Actions are enabled
- Review branch protection settings

---

## 🎯 What's Running

### On Every Push
```
✓ Tests across Python 3.8-3.12
✓ Code linting with flake8
✓ Format check with black
✓ Type checking with mypy
✓ Security scanning with bandit
✓ Documentation building with Sphinx
```

### On Pull Requests
```
✓ All of the above
✓ PR validation checks
✓ Conventional commit validation
✓ Documentation/test warnings
```

### On Tag Push (v*)
```
✓ Build distribution packages
✓ Create GitHub Release
✓ Publish to PyPI (if configured)
```

---

## 💡 Pro Tips

1. **Format before pushing:**
   ```bash
   black medkit/ cli/ tests/
   isort medkit/ cli/ tests/
   ```

2. **Use conventional commits:**
   ```
   feat: add new feature
   fix: fix a bug
   docs: update documentation
   chore: maintenance tasks
   ```

3. **View workflow logs:**
   - Go to Actions tab
   - Click on a workflow run
   - Click on a job for details

4. **Monitor coverage:**
   - Coverage reports uploaded to Codecov
   - HTML reports available in artifacts
   - Track trends over time

5. **Add status badges:**
   ```markdown
   [![Tests](https://github.com/csverma610/medkit/actions/workflows/tests.yml/badge.svg)](https://github.com/csverma610/medkit/actions)
   ```

---

## 🎉 You're All Set!

Your CI/CD pipeline is ready to use. Now:

1. **Develop** with confidence
2. **Test** automatically on every push
3. **Deploy** with one git command
4. **Release** production-ready code

Happy coding! 🚀

---

## 📖 Full Documentation

For comprehensive information, see:
- `.github/SETUP_INSTRUCTIONS.md` - Detailed setup
- `.github/CI_CD_GUIDE.md` - Complete reference
- `.github/README.md` - Overview

---

**Last Updated:** 2025-11-08
