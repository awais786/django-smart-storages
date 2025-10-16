# Publishing Guide for django-smart-storages

This guide explains how to publish the django-smart-storages package to PyPI.

## Prerequisites

1. Install required tools:
```bash
pip install build twine
```

2. Create accounts on:
   - PyPI: https://pypi.org/
   - TestPyPI (for testing): https://test.pypi.org/

## Build the Package

1. Clean previous builds:
```bash
rm -rf dist/ build/ *.egg-info
```

2. Build the package:
```bash
python -m build
```

This will create two files in the `dist/` directory:
- A source distribution (`.tar.gz`)
- A wheel distribution (`.whl`)

## Test on TestPyPI (Recommended)

1. Upload to TestPyPI:
```bash
python -m twine upload --repository testpypi dist/*
```

2. Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ django-smart-storages
```

3. Verify the package works:
```bash
python -c "import smart_storages; print(smart_storages.__version__)"
```

## Publish to PyPI

1. Upload to PyPI:
```bash
python -m twine upload dist/*
```

2. Verify on PyPI:
   - Visit https://pypi.org/project/django-smart-storages/
   - Check that the README renders correctly
   - Verify the version and metadata

3. Test installation:
```bash
pip install django-smart-storages
```

## Version Management

Update the version in:
- `setup.py` (version field)
- `smart_storages/__init__.py` (__version__ variable)

Follow semantic versioning:
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality
- PATCH version for backwards-compatible bug fixes

## Release Checklist

Before publishing a new version:

- [ ] Update version numbers in setup.py and __init__.py
- [ ] Update CHANGELOG.md (if exists)
- [ ] Run all tests: `python runtests.py`
- [ ] Build the package: `python -m build`
- [ ] Check the package contents: `tar -tzf dist/*.tar.gz`
- [ ] Test on TestPyPI first
- [ ] Create a git tag: `git tag v0.1.0`
- [ ] Push the tag: `git push origin v0.1.0`
- [ ] Upload to PyPI: `python -m twine upload dist/*`
- [ ] Create a GitHub release with release notes

## Configuration

### PyPI API Token

For secure authentication, use API tokens instead of username/password:

1. Create an API token on PyPI
2. Configure it in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
username = __token__
password = pypi-your-test-api-token-here
```

## Automated Publishing (GitHub Actions)

Consider setting up GitHub Actions to automatically publish releases:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: python -m twine upload dist/*
```

## Troubleshooting

### Common Issues

1. **"File already exists" error**
   - You cannot upload the same version twice
   - Increment the version number

2. **Invalid credentials**
   - Verify your PyPI credentials
   - Use API tokens instead of passwords

3. **README not rendering**
   - Ensure README.md is valid Markdown
   - Check that long_description_content_type is set to "text/markdown" in setup.py

4. **Missing files in package**
   - Check MANIFEST.in
   - Verify files are included when running: `python setup.py sdist`
