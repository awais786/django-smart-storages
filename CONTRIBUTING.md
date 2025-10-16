# Contributing to django-smart-storages

Thank you for your interest in contributing to django-smart-storages! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/django-smart-storages.git
   cd django-smart-storages
   ```
3. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. Install the package in development mode:
   ```bash
   pip install -e .
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run the test suite using:
```bash
python runtests.py
```

All tests must pass before submitting a pull request.

## Code Style

- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and concise

## Making Changes

1. **Write tests first**: Add tests for any new functionality
2. **Make minimal changes**: Keep changes focused on a single issue
3. **Update documentation**: Update README.md and docstrings as needed
4. **Add examples**: If adding new features, add examples to the `example/` directory

## Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Update documentation as needed
- Add yourself to the contributors list if desired

## Reporting Issues

When reporting issues, please include:
- Django version
- Python version
- django-storages version
- boto3 version
- A minimal code example that reproduces the issue
- Full error traceback if applicable

## Feature Requests

Feature requests are welcome! Please:
- Check if the feature already exists
- Provide a clear use case
- Describe the expected behavior
- Consider submitting a PR if possible

## Questions

If you have questions about using django-smart-storages:
- Check the README.md for documentation
- Look at examples in the `example/` directory
- Open an issue with the "question" label

## Code of Conduct

Be respectful and considerate of others. We aim to maintain a welcoming and inclusive community.

## License

By contributing to django-smart-storages, you agree that your contributions will be licensed under the MIT License.
