# Publishing Magapy to PyPI

This guide walks you through the process of publishing Magapy to the Python Package Index (PyPI).

## Prerequisites

1. Create an account on [PyPI](https://pypi.org/account/register/)
2. Install required tools:
   ```bash
   pip install --upgrade pip
   pip install --upgrade setuptools wheel twine
   ```

## Publishing Process

### 1. Update Version Number

Edit `__init__.py` to increment the version number:

```python
__version__ = '0.1.0'  # Change to '0.1.1', '0.2.0', etc.
```

### 2. Build the Package

Clean up any previous builds:
```bash
rm -rf build/ dist/ *.egg-info/
```

Build the package:
```bash
python setup.py sdist bdist_wheel
```

### 3. Check the Package

Verify the package structure:
```bash
twine check dist/*
```

### 4. Test on TestPyPI (Optional but Recommended)

Upload to TestPyPI:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Install from TestPyPI to verify:
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps magapy
```

### 5. Upload to PyPI

Upload to the real PyPI:
```bash
twine upload dist/*
```

### 6. Verify Installation

Uninstall any development version:
```bash
pip uninstall -y magapy
```

Install from PyPI:
```bash
pip install magapy
```

Test the installation:
```bash
magapy --help
```

## Troubleshooting

1. If you encounter a name conflict, choose a more unique package name
2. For permission errors, make sure you're using the correct PyPI credentials
3. For build errors, check your package structure and dependencies
