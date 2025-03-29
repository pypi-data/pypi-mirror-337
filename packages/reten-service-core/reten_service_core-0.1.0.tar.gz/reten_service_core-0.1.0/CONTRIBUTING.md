# Contributing to reten-service-core

Thank you for your interest in contributing to reten-service-core! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Contributing to reten-service-core](#contributing-to-reten-service-core)
  - [Table of Contents](#table-of-contents)
  - [Development Environment Setup](#development-environment-setup)
    - [Prerequisites](#prerequisites)
    - [Setting up your development environment](#setting-up-your-development-environment)
  - [Code Style Guidelines](#code-style-guidelines)
  - [Pull Request Process](#pull-request-process)
  - [Testing Guidelines](#testing-guidelines)
  - [Commit Conventions](#commit-conventions)
    - [Tips for Good Commits](#tips-for-good-commits)
  - [Questions or Problems?](#questions-or-problems)

## Development Environment Setup

### Prerequisites
- Python 3.9 or higher
- pip
- virtualenv or your preferred virtual environment tool

### Setting up your development environment

1. Clone the repository:
```bash
git clone https://github.com/your-org/reten-service-core.git
cd reten-service-core
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Code Style Guidelines

We use [ruff](https://github.com/astral-sh/ruff) as our all-in-one Python toolchain for:
- Code formatting
- Import sorting
- Linting and static analysis

Our code style follows these principles:

1. Use descriptive variable names
2. Write docstrings for all public functions and classes (Google style)
3. Keep functions focused and single-purpose
4. Maximum line length is 100 characters (configured in ruff)
5. Use type hints for function arguments and return values

The project has pre-configured ruff with the following rules:
- Code formatting with `ruff format`
- Import sorting (using isort rules)
- Multiple linting rules including: pyflakes, pycodestyle, isort, mccabe, and more
- Google-style docstring convention

Example of well-formatted code:

```python
from typing import List, Optional

def process_data(input_data: List[str], max_length: Optional[int] = None) -> dict:
    """Process the input data and return results.

    Args:
        input_data: List of strings to process
        max_length: Optional maximum length for processing

    Returns:
        dict: Processed data results
    """
    result = {}
    # Implementation
    return result
```

## Pull Request Process

1. **Branch Naming**:
   - Feature: `feature/description`
   - Bug fix: `fix/description`
   - Documentation: `docs/description`

2. **Before Submitting**:
   - Ensure all tests pass
   - Update documentation if needed
   - Add tests for new features
   - Run pre-commit hooks
   - Update CHANGELOG.md if applicable

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Other (please specify)

   ## Testing
   Describe testing done

   ## Checklist
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] Pre-commit hooks passed
   ```

## Testing Guidelines

1. **Test Structure**:
   - Place tests in the `tests/` directory
   - Mirror the package structure in tests
   - Use descriptive test names: `test_should_do_something_when_condition`

2. **Test Requirements**:
   - All new features must include tests
   - Maintain or improve code coverage
   - Use pytest fixtures for common setup
   - Mock external services

3. **Running Tests**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=reten_service_core

# Run specific test file
pytest tests/test_specific.py
```

## Commit Conventions

We follow the Conventional Commits specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc)
- `refactor:` Code refactoring
- `test:` Adding or modifying tests
- `chore:` Maintenance tasks

Example commit messages:
```
feat: add support for custom logging formats
fix: correct BigQuery client authentication
docs: update installation instructions
```

### Tips for Good Commits
- Keep commits focused and atomic
- Write clear, descriptive commit messages
- Reference issues in commit messages when applicable

## Questions or Problems?

If you have questions or run into problems, please:
1. Check existing issues
2. Create a new issue with a clear description
3. Reach out to the maintainers

Thank you for contributing to reten-service-core!
