import os
import argparse
from dotenv import load_dotenv, set_key, unset_key, dotenv_values
from pathlib import Path
from . import config

# Get the package directory
PACKAGE_DIR = Path(__file__).parent
ENV_FILE = PACKAGE_DIR / '.env'

def load_env():
    """Load environment variables from .env file"""
    if not ENV_FILE.exists():
        ENV_FILE.touch()
    load_dotenv(ENV_FILE)

def get_env_vars():
    """Get only the variables from .env file"""
    if not ENV_FILE.exists():
        return {}
    return dotenv_values(ENV_FILE)

def delete_env_var(key):
    """Delete a variable from the .env file"""
    if not ENV_FILE.exists():
        return False
    
    # Read all lines from .env
    with open(ENV_FILE, 'r') as f:
        lines = f.readlines()
    
    # Write back lines that don't start with the key
    with open(ENV_FILE, 'w') as f:
        for line in lines:
            if not line.strip() or line.strip().startswith('#'):
                f.write(line)
                continue
            parts = line.split('=', 1)
            if len(parts) == 2 and parts[0].strip() == key:
                continue
            f.write(line)
    
    return True

# Automatically load environment variables when the package is imported
load_env()

# Add all environment variables to the module's namespace
globals().update(get_env_vars())

def main():
    parser = argparse.ArgumentParser(description='Manage environment variables in .env file')
    parser.add_argument('args', nargs='*', help='Variable to read or KEY=VALUE to set')
    parser.add_argument('--set-command', help='Set a custom command name for the CLI')
    args = parser.parse_args()

    # Handle command name configuration
    if args.set_command:
        config.set_command_name(args.set_command)
        return

    if not args.args:
        cmd_name = config.get_command_name()
        print(f"{cmd_name} package is installed and working!")
        print("\nCurrent environment variables:")
        env_vars = get_env_vars()
        for key, value in env_vars.items():
            print(f"{key} = {value}")
        return

    arg = args.args[0]
    if len(args.args) > 1 and args.args[0] == 'delete':
        # Handle delete command
        key = args.args[1]
        if delete_env_var(key):
            print(f"Deleted {key} from .env file")
        else:
            print(f"Variable {key} not found in .env file")
    elif '=' in arg:
        # Set variable
        key, value = arg.split('=', 1)
        set_key(ENV_FILE, key, value)
        print(f"Updated {key} in .env file")
    else:
        # Read variable
        env_vars = get_env_vars()
        value = env_vars.get(arg)
        if value is not None:
            print(value)
        else:
            print(f"Variable {arg} not found in .env file")

    # Show current variables after any operation
    print("\nCurrent environment variables:")
    env_vars = get_env_vars()
    for key, value in env_vars.items():
        print(f"{key} = {value}")

if __name__ == '__main__':
    main()