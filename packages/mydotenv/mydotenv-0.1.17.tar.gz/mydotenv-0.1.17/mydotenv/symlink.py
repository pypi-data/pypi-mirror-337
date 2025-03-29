import os
import sys
from pathlib import Path
from . import config

def create_symlink():
    """Create a symlink for the custom command name"""
    # Get the mydotenv script location
    scripts_dir = Path(sys.executable).parent / 'bin'
    mydotenv_script = scripts_dir / 'mydotenv'
    
    if not mydotenv_script.exists():
        print("Error: mydotenv script not found")
        return False
    
    # Get the custom command name
    cmd_name = config.get_command_name()
    if cmd_name == 'mydotenv':
        return True
    
    # Create the symlink
    custom_script = scripts_dir / cmd_name
    try:
        if custom_script.exists():
            custom_script.unlink()
        custom_script.symlink_to(mydotenv_script)
        return True
    except Exception as e:
        print(f"Error creating symlink: {e}")
        return False

if __name__ == '__main__':
    create_symlink() 