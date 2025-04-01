# python.text2doc.com


        
```bash
# Clean up any previous build artifacts
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m pip install --upgrade pip build
python -m build

# Publish to PyPI (if needed)
python -m pip install --upgrade twine
python -m twine upload dist/*

```

Clean up the build artifacts and rebuild
```bash
rm -rf build/ dist/ src/text2doc.egg-info/
python -m pip install -e .
python -m build

```




`text2doc` implements a virtual file system in memory. This module provides an interface compatible with the `os` module and provides operations on files and directories stored in RAM rather than on disk.

## Installation

```bash
pip install text2doc
```

## Usage

```python
from text2doc import text2doc

# Example usage
texts = ["This is a sample text.", "Another text to tokenize."]
tokenizer = YourTokenizer()  # Replace with your tokenizer instance
docs = text2doc(texts, tokenizer)
print(docs)
```

## Development

### Clean up any previous build artifacts

```bash
rm -rf build/ dist/ *.egg-info/
```

### Build the package

```bash
python -m pip install --upgrade pip build
python -m build
```

### Publish to PyPI (if needed)

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
```

