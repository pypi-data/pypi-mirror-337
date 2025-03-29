import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv, set_key, unset_key, find_dotenv
from . import config

# Load environment variables
env_path = find_dotenv()
if not env_path:
    env_path = Path.cwd() / '.env'
    env_path.touch()
load_dotenv(env_path)

# Auto-generate .pyi file for IDE autocompletion
def generate_pyi_file():
    """Generate a .pyi file with type hints for all environment variables"""
    pyi_path = Path(__file__).parent / "__init__.pyi"
    env_vars = {}
    
    # First collect variables from .env file
    if env_path and Path(env_path).exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        key, _ = line.split('=', 1)
                        env_vars[key.strip()] = True
                    except ValueError:
                        pass
    
    # Generate the .pyi file content
    content = "# Auto-generated type stubs for environment variables\n\n"
    for var in sorted(env_vars.keys()):
        if var.isidentifier():  # Only include valid Python identifiers
            content += f"{var}: str\n"
    
    # Write the .pyi file
    with open(pyi_path, 'w') as f:
        f.write(content)

# Generate the .pyi file on import
generate_pyi_file()

# This is the key part that makes variables accessible without the mydotenv prefix
# We need to modify the builtins module to inject our variables
if env_path and Path(env_path).exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                        value = value[1:-1]
                    # Add to builtins module
                    setattr(sys.modules['builtins'], key, value)
                    # Also make it available at module level for those who import mydotenv
                    globals()[key] = value
                except ValueError:
                    pass

def open_env_file():
    """Open the .env file in the default text editor"""
    if not env_path:
        print("Error: .env file not found")
        return False
    
    # Determine the editor to use
    editor = os.environ.get('EDITOR', 'nano')  # Default to nano if EDITOR is not set
    
    try:
        subprocess.run([editor, env_path], check=True)
        print(f"Opened {env_path} with {editor}")
        
        # Regenerate .pyi file after editing
        generate_pyi_file()
        
        # Reload environment variables
        load_dotenv(env_path, override=True)
        
        # Update builtins with new variables
        if env_path and Path(env_path).exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # Remove quotes if present
                            if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                                value = value[1:-1]
                            # Update builtins
                            setattr(sys.modules['builtins'], key, value)
                            # Also update module level
                            globals()[key] = value
                        except ValueError:
                            pass
        
        return True
    except Exception as e:
        print(f"Error opening .env file: {e}")
        return False

def main():
    """Main entry point for the CLI"""
    if len(sys.argv) > 1:
        # Handle open command
        if sys.argv[1] == 'open':
            open_env_file()
            return
            
        # Handle set-command
        if sys.argv[1] == '--set-command':
            if len(sys.argv) != 3:
                print("Usage: mydotenv --set-command NAME")
                return
            config.set_command_name(sys.argv[2])
            return

        # Handle delete command
        if sys.argv[1] == 'delete':
            if len(sys.argv) != 3:
                print("Usage: mydotenv delete VARIABLE_NAME")
                return
            unset_key(env_path, sys.argv[2])
            print(f"Deleted {sys.argv[2]} from .env file")
            # Regenerate .pyi file after deletion
            generate_pyi_file()
            return
            
        # Check if it's a variable assignment
        if '=' in sys.argv[1]:
            key, value = sys.argv[1].split('=', 1)
            set_key(env_path, key, value)
            print(f"Updated {key} in .env file")
            # Regenerate .pyi file after update
            generate_pyi_file()
            return
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
