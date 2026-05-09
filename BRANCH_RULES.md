# 🌿 Branch Rules & Guidelines

## 📋 Table of Contents
- [Branch Naming Convention](#branch-naming-convention)
- [Branch Types](#branch-types)
- [Workflow](#workflow)
- [Code Review Requirements](#code-review-requirements)
- [Merge Rules](#merge-rules)

---

## 🏷️ Branch Naming Convention

All branches must follow this pattern:
```
<type>/<short-description>
```

**Examples:**
- `feature/system-monitor`
- `bugfix/memory-leak-fix`
- `docs/readme-update`
- `refactor/code-cleanup`
- `test/add-unit-tests`

### Rules:
- Use lowercase letters only
- Use hyphens (`-`) to separate words
- Keep descriptions short and meaningful (max 50 characters)
- No special characters except hyphens and slashes

---

## 📁 Branch Types

| Type | Description | Example |
|------|-------------|---------|
| `feature` | New functionality or enhancements | `feature/disk-analysis` |
| `bugfix` | Fixing bugs in existing code | `bugfix/cpu-usage-error` |
| `hotfix` | Critical fixes for production | `hotfix/security-patch` |
| `docs` | Documentation changes only | `docs/api-reference` |
| `refactor` | Code refactoring without behavior changes | `refactor/module-structure` |
| `test` | Adding or updating tests | `test/integration-tests` |
| `chore` | Maintenance tasks, dependencies | `chore/update-deps` |

---

## 🔄 Workflow

### 1. Create a Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, documented code
- Add tests for new functionality
- Update documentation if needed

### 3. Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Examples:**
- `feat(system_info): add network monitoring`
- `fix(memory): resolve leak in disk analysis`
- `docs(readme): update installation instructions`

### 4. Push and Create PR
```bash
git push origin feature/your-feature-name
```

---

## ✅ Code Review Requirements

Before merging, ensure:
- [ ] All tests pass (`python test_system_info.py`)
- [ ] Code follows project style guidelines
- [ ] Documentation is updated
- [ ] No sensitive data committed
- [ ] At least 1 approval from maintainer
- [ ] All CI checks pass (if configured)

---

## 🔀 Merge Rules

### Protected Branches
- `main` - Production-ready code
- Requires PR review before merging
- Must pass all tests

### Merge Strategy
- **Feature branches → main**: Squash merge preferred
- **Hotfix branches → main**: Regular merge with detailed message
- **Keep history clean**: Rebase before merging if needed

### Before Merging to Main:
1. Update branch from main: `git rebase main`
2. Run all tests locally
3. Ensure PR description explains changes
4. Get required approvals
5. Delete branch after merge

---

## 🚫 Prohibited Practices

- ❌ Direct commits to `main`
- ❌ Long-lived branches (> 2 weeks)
- ❌ Committing secrets or credentials
- ❌ Merging without code review
- ❌ Force pushing to shared branches

---

## 📞 Questions?

Contact maintainers or open an issue for clarification.

**Made with ❤️ by tipichniy340-tech**
