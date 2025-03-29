import os
import sys
from pathlib import Path
from dotenv import load_dotenv, set_key, unset_key, find_dotenv
from . import config

# Load environment variables
env_path = find_dotenv()
if not env_path:
    env_path = Path.cwd() / '.env'
    env_path.touch()
load_dotenv(env_path)

# Expose all environment variables
globals().update(os.environ)

def main():
    """Main entry point for the CLI"""
    if len(sys.argv) > 1 and sys.argv[1] == '--set-command':
        if len(sys.argv) != 3:
            print("Usage: mydotenv --set-command NAME")
            return
        config.set_command_name(sys.argv[2])
        return

    # Handle commands
    if len(sys.argv) > 1:
        if sys.argv[1] == 'delete':
            if len(sys.argv) != 3:
                print("Usage: mydotenv delete VARIABLE_NAME")
                return
            unset_key(env_path, sys.argv[2])
            print(f"Deleted {sys.argv[2]} from .env file")
        else:
            # Check if it's a variable assignment
            if '=' in sys.argv[1]:
                key, value = sys.argv[1].split('=', 1)
                set_key(env_path, key, value)
                print(f"Updated {key} in .env file")
            else:
                # Print variable value
                value = os.getenv(sys.argv[1])
                if value is None:
                    print(f"Variable {sys.argv[1]} not found in .env file")
                else:
                    print(value)
                return

    # Print all variables
    print("\nCurrent environment variables:")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                print(f"{key} = {value}")

if __name__ == '__main__':
    main()