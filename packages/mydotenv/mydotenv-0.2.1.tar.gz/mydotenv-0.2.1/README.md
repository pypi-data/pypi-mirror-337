# mydotenv

A simple Python package to manage environment variables in your `.env` file with command-line interface.

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

### Custom Command Name

You can set a custom command name to use instead of `mydotenv`:

```bash
mydotenv --set-command dotman
```

Now you can use either `mydotenv` or `dotman` to run commands:
```bash
dotman NEW_KEY=value
dotman delete NEW_KEY
```

When you set a new command name, it replaces any previous custom command name.

## Features

- Manage environment variables from the command line
- Set custom command names for easier use
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