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

# Create the 'env' object that will be imported by users
class EnvAccessor:
    def __getattr__(self, name):
        return os.environ.get(name)

env = EnvAccessor()

# Expose all environment variables
for key, value in os.environ.items():
    globals()[key] = value

def main():
    """Main entry point for the CLI"""
    # Check for new advanced CLI flags first
    if len(sys.argv) > 1 and sys.argv[1].startswith('--'):
        if sys.argv[1] in ['--replace', '--add-empty', '--add']:
            # Import CLI functionality only when needed
            from .cli import handle_cli_flags
            return handle_cli_flags(sys.argv[1:])
        elif sys.argv[1] == '--help' and len(sys.argv) > 2 and sys.argv[2] == 'advanced':
            # Show advanced help when specifically requested
            from .cli import show_advanced_help
            return show_advanced_help()
        elif sys.argv[1] == '--set-command':
            if len(sys.argv) != 3:
                print("Usage: mydotenv --set-command NAME")
                return
            config.set_command_name(sys.argv[2])
            return

    # Original CLI functionality 
    if len(sys.argv) > 1:
        if sys.argv[1] == 'delete':
            if len(sys.argv) != 3:
                print("Usage: mydotenv delete VARIABLE_NAME")
                return
            unset_key(env_path, sys.argv[2])
            print(f"Deleted {sys.argv[2]} from .env file")
        elif sys.argv[1] == '--help':
            _print_help()
            return
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
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        print(f"{key} = {value}")
                    else:
                        # Handle lines without an equals sign
                        print(f"Warning: Skipping invalid line: {line}")
    except Exception as e:
        print(f"Error reading .env file: {e}")

def _print_help():
    """Print help message"""
    print("""
mydotenv - A simple package to manage environment variables

Basic Usage:
  mydotenv                         # Show all variables in .env
  mydotenv VARIABLE_NAME           # Print a variable's value
  mydotenv NEW_KEY=value           # Add or update a variable
  mydotenv delete VARIABLE_NAME    # Delete a variable
  mydotenv --set-command NAME      # Set a custom command name

Advanced Features:
  mydotenv --help advanced         # Show advanced features help
  mydotenv --replace env [<path>]  # Replace .env with newly scanned variables
  mydotenv --add-empty env [<path>] # Add new variables as empty placeholders
  mydotenv --add env [<path>]       # Add new variables preserving existing ones
  mydotenv --add imports [<path>]   # Rewrite import statements
""")

if __name__ == '__main__':
    main()