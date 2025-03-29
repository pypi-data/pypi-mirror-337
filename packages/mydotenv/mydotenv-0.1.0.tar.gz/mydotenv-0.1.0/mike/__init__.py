import os
import argparse
from dotenv import load_dotenv, set_key, unset_key, dotenv_values
from pathlib import Path

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

# Automatically load environment variables when the package is imported
load_env()

# Add all environment variables to the module's namespace
globals().update(get_env_vars())

def main():
    parser = argparse.ArgumentParser(description='Manage environment variables in .env file')
    parser.add_argument('args', nargs='*', help='Variable to read or KEY=VALUE to set')
    args = parser.parse_args()

    if not args.args:
        print("Mike package is installed and working!")
        print("\nCurrent environment variables:")
        env_vars = get_env_vars()
        for key, value in env_vars.items():
            print(f"{key} = {value}")
        return

    arg = args.args[0]
    if '=' in arg:
        # Set variable
        key, value = arg.split('=', 1)
        set_key(ENV_FILE, key, value)
        print(f"Updated {key} in .env file")
        print("\nCurrent environment variables:")
        env_vars = get_env_vars()
        for k, v in env_vars.items():
            print(f"{k} = {v}")
    else:
        # Read variable
        env_vars = get_env_vars()
        value = env_vars.get(arg)
        if value is not None:
            print(value)
        else:
            print(f"Variable {arg} not found in .env file")

if __name__ == '__main__':
    main()