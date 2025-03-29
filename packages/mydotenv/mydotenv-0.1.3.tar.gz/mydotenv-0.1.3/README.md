# Mike Package

A simple Python package to manage environment variables in your `.env` file with command-line interface.

## Installation

### From PyPI
```bash
pip install mike
```

### From Source
```bash
git clone https://github.com/yourusername/mike-package.git
cd mike-package
pip install -e .
```

## Usage

### In Python Scripts

```python
# Import all variables
from mike import *

# Use variables directly
print(API_KEY)
print(DATABASE_URL)

# Or import specific variables
from mike import API_KEY, DATABASE_URL
```

### Command Line Interface

1. Print a variable's value:
```bash
mike API_KEY
```

2. Add or update a variable:
```bash
mike NEW_KEY=value
mike "KEY_WITH_SPACES=value with spaces"
```

3. Delete a variable:
```bash
mike delete VARIABLE_NAME
```

4. View all variables:
```bash
mike
```

## Features

- Automatically loads variables from `.env` file
- Type hints support with auto-generated `.pyi` stub file
- Command-line interface for managing variables
- Preserves comments and formatting in `.env` file
- Handles values with spaces and special characters
- Works from any directory

## File Structure

- `.env`: Your environment variables file (created in your home directory)
- `mike/__init__.py`: Main package code
- `mike/__init__.pyi`: Auto-generated type stubs

## Dependencies

- python-dotenv

## Notes

- The package creates and uses a `.env` file in your home directory
- Variables are automatically reloaded when modified through the CLI
- Type stubs are automatically updated when variables change
- Perfect for managing API keys, database URLs, and other configuration variables

## License

MIT License - feel free to use this package in your projects! 