import os
import subprocess
from importlib.metadata import distribution, PackageNotFoundError
from pathlib import Path
import sys

CONFIG_DIR = Path.home() / '.config' / 'mydotenv'
CONFIG_FILE = CONFIG_DIR / 'config.env'

def ensure_config_dir():
    """Ensure the config directory exists"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.touch()

def get_command_name():
    """Get the configured command name or return default"""
    ensure_config_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                return content
    return 'mydotenv'

def is_package_installed(package_name):
    """Check if a package is installed"""
    try:
        distribution(package_name)
        return True
    except PackageNotFoundError:
        return False

def set_command_name(name=None):
    """Set the command name if it's not already taken"""
    if name is None:
        print("Usage: mydotenv --set-command NAME")
        return False

    # Check if the name is already a command in PATH
    which_result = subprocess.run(['which', name], capture_output=True, text=True)
    if which_result.returncode == 0:
        print(f"Error: Command '{name}' already exists in your system")
        return False
    
    # Check if it's a Python package
    if is_package_installed(name):
        print(f"Error: '{name}' is already installed as a Python package")
        return False
    
    # Get current command name and remove its symlink if it exists
    current_name = get_command_name()
    if current_name != 'mydotenv':
        scripts_dir = Path.home() / '.local' / 'bin'
        current_script = scripts_dir / current_name
        if current_script.exists():
            try:
                current_script.unlink()
            except Exception as e:
                print(f"Warning: Could not remove old command symlink: {e}")
    
    # Save the new command name
    ensure_config_dir()
    with open(CONFIG_FILE, 'w') as f:
        f.write(name)
    
    # Create a symlink for the new command name
    scripts_dir = Path.home() / '.local' / 'bin'
    mydotenv_script = scripts_dir / 'mydotenv'
    custom_script = scripts_dir / name
    
    try:
        if custom_script.exists():
            custom_script.unlink()
        os.symlink(mydotenv_script, custom_script)
        print(f"Command name set to '{name}'")
        print(f"You can now use either 'mydotenv' or '{name}' to run commands")
        return True
    except Exception as e:
        print(f"Warning: Could not create symlink: {e}")
        print(f"Command name is set to '{name}', but you'll need to use 'mydotenv' for now")
        return True 