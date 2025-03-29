# mydotenv

A simple Python package to manage environment variables in your `.env` file with command-line interface and direct variable access in Python code.

## Installation

### Using pipx (Recommended)
```bash
pipx install mydotenv
```

### Using pip
```bash
pip install mydotenv
```

### From Source
```bash
git clone https://github.com/banddude/mydotenv.git
cd mydotenv
pip install -e .
```

## Usage

### Python Usage

To access environment variables directly in your code without prefixes:

```python
# Import this way for direct variable access
from mydotenv import *

# Now you can use environment variables directly
print(HI)  # Prints the value of HI from your .env file
```

The package also provides IDE autocompletion support through type hints, so your IDE won't show errors for environment variables.

### Command Line Interface

1. Print a variable's value:
```bash
mydotenv API_KEY
```

2. Add or update a variable:
```bash
mydotenv NEW_KEY=value
mydotenv "KEY_WITH_SPACES=value with spaces"
```

3. Delete a variable:
```bash
mydotenv delete VARIABLE_NAME
```

4. View all variables:
```bash
mydotenv
```

5. Open the .env file in your default editor:
```bash
mydotenv open
```

### Custom Command Name

You can set a custom command name to use instead of `mydotenv`:

```bash
mydotenv --set-command dotman
```

Now you can use either `mydotenv` or `dotman` to run commands:
```bash
dotman NEW_KEY=value
dotman delete NEW_KEY
dotman open  # Opens the .env file in your editor
```

When you set a new command name, it replaces any previous custom command name.

## Features

- Manage environment variables from the command line
- Access environment variables directly in Python code without prefixes
- IDE autocompletion support through auto-generated type hints
- Set custom command names for easier use
- Open and edit your .env file with a simple command
- Preserves comments and formatting in `.env` file
- Handles values with spaces and special characters
- Works from any directory
- Creates and manages `.env` file in your current directory

## Dependencies

- python-dotenv >= 1.0.0

## Configuration

- The package stores its configuration in `~/.config/mydotenv/config.env`
- Custom command names are managed through symlinks in `~/.local/bin`

## License

MIT License - feel free to use this package in your projects!
