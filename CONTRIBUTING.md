# Contributing to Stplpy

Thank you for your interest in contributing to Stplpy! This document explains how to contribute to the project.

## Development Environment Setup

### Requirements

- Python 3.12 or higher
- Git

### Setup Steps

1. Fork and clone the repository

```bash
git clone https://github.com/yourusername/Stplpy.git
cd Stplpy
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install development dependencies

```bash
pip install -e ".[dev]"
```

## Development Workflow

### 1. Creating a Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Making Changes

- Review the existing code style before making changes
- Always add type hints
- Add docstrings to document function and class behavior

### 3. Code Style

This project uses the following tools:

#### Black (Code Formatter)

```bash
black stplpy tests
```

#### Flake8 (Linter)

```bash
flake8 stplpy tests
```

#### Mypy (Type Checker)

```bash
mypy stplpy
```

### 4. Running Tests

Always run tests after making changes:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=stplpy --cov-report=html

# Run specific test file
pytest tests/test_user.py
```

### 5. Adding New Tests

When adding new features, always include tests:

- Create corresponding test files in the `tests/` directory
- Create at least one test for each function
- Test edge cases and error cases

Example:

```python
def test_new_feature():
    """Test description."""
    # Arrange
    expected = "expected result"

    # Act
    result = your_function()

    # Assert
    assert result == expected
```

## Commit Messages

Follow this format for commit messages:

```
[emoji] Short description

Detailed description (if necessary)

- Change 1
- Change 2
```

### Emoji Usage:

- 🐛 `:bug:` - Bug fix
- ✨ `:sparkles:` - New feature
- 📝 `:memo:` - Documentation
- 🎨 `:art:` - Code style/structure improvements
- ♻️ `:recycle:` - Refactoring
- ✅ `:white_check_mark:` - Adding/updating tests
- 🔧 `:wrench:` - Configuration file changes
- ⬆️ `:arrow_up:` - Dependency updates
- 🔒 `:lock:` - Security fixes

Example:

```
[✨] Add user statistics feature

Added new feature to retrieve user study statistics

- Implemented get_user_statistics() method
- Calculate total study time and record count
- Added test cases
```

## Pull Requests

### Before Creating a PR

- [ ] Ensure all tests pass
- [ ] Ensure code style checks pass
- [ ] New features include tests
- [ ] Update documentation (if necessary)

### PR Description

Include the following in your PR:

1. **Summary of changes**
2. **Reason for changes**
3. **Related issue number** (if applicable)
4. **Screenshots or logs** (if applicable)

### PR Template

```markdown
## Changes

<!-- Briefly explain what was changed -->

## Reason for Changes

<!-- Why this change is necessary -->

## Related Issue

Closes #issue_number

## Checklist

- [ ] Added/updated tests
- [ ] Updated documentation
- [ ] Code style checks passed
- [ ] All tests passed
```

## Issue Reporting

If you find a bug or want to propose a new feature, please create an issue.

### Bug Reports

```markdown
## Bug Description

<!-- Clear description of the bug -->

## Steps to Reproduce

1.
2.
3.

## Expected Behavior

<!-- What should happen -->

## Actual Behavior

<!-- What actually happened -->

## Environment

- OS:
- Python version:
- Stplpy version:
```

### Feature Requests

```markdown
## Feature Description

<!-- Description of the feature you want to add -->

## Use Case

<!-- Why this feature is needed and usage examples -->

## Implementation Ideas

<!-- Implementation ideas (if any) -->
```

## Code Review

All PRs will be reviewed. Please respond constructively to reviewer feedback.

## Questions

If you have questions, please create an issue or join existing discussions.

## License

Contributed code will be published under the project's license (MIT).

---

Thank you for your contributions! 🎉
