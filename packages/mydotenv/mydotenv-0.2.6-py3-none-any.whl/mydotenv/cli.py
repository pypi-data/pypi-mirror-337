#!/usr/bin/env python3

"""
Expanded CLI for 'mydotenv' that can:
  - Scan for env.* references
  - Replace .env entirely
  - Add empty env vars to .env
  - Rewrite Python imports to 'from mydotenv import env' (naively)

Usage examples:

  # Replaces existing .env with newly scanned environment variables
  mydotenv --replace env [<path>]

  # Merges new environment variables as empty placeholders
  mydotenv --add-empty env [<path>]

  # Merges new environment variables (keeping old ones) 
  # This is basically a 'scan' + 'merge' scenario
  mydotenv --add env [<path>]

  # Naively rewrite import statements to 'from mydotenv import env'
  # (removes "import mydotenv" or "from mydotenv import something_else")
  mydotenv --add imports [<path>]

If <path> is not provided, it scans the current directory ('.') recursively.
"""

import os
import re
import argparse
from typing import List, Set, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

###############################################################################
# SCANNER LOGIC: find env.* references
###############################################################################

def scan_for_env_vars(directory: str, ignore_paths: List[str] = None) -> Set[str]:
    """
    Recursively scans for occurrences of "env.SOMETHING" in .py files,
    skipping any paths that match ignore_paths.

    :param directory: Base directory or file to scan.
    :param ignore_paths: List of path substrings/directories to ignore.
    :return: A set of unique environment variable names found.
    """
    if ignore_paths is None:
        ignore_paths = []

    # Regex to match env.<VAR_NAME> or directly used env vars
    patterns = [
        re.compile(r'\benv\.([A-Za-z_][A-Za-z0-9_]*)\b'),  # matches env.VAR
        re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\b')  # matches any identifier that could be an env var
    ]
    found_vars = set()

    # If the user gave a single file instead of a directory, handle that
    if os.path.isfile(directory) and directory.endswith('.py'):
        _scan_file(directory, patterns, found_vars, ignore_paths)
        return found_vars

    # Otherwise, walk directories
    for root, dirs, files in os.walk(directory):
        # Filter out directories we don't want to descend into
        dirs[:] = [
            d for d in dirs
            if not any(os.path.join(root, d).startswith(os.path.join(directory, ip)) for ip in ignore_paths)
        ]

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if any(ip in file_path for ip in ignore_paths):
                    continue
                _scan_file(file_path, patterns, found_vars, ignore_paths)

    return found_vars

def _scan_file(
    file_path: str,
    patterns: List["re.Pattern"],
    found_vars: Set[str],
    ignore_paths: List[str]
) -> None:
    """Helper function to scan a single .py file."""
    if any(ip in file_path for ip in ignore_paths):
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # First, check for env.VAR matches
        env_var_matches = patterns[0].findall(content)
        if env_var_matches:
            found_vars.update(env_var_matches)
            return  # We found env.VAR patterns, no need to check for direct access
            
        # Then check for any identifiers that might be env vars
        # These are potential direct env var usages
        potential_env_vars = set(patterns[1].findall(content))
        
        # Check if any of these potential vars are in the master env
        master_env = load_master_env()
        for var in potential_env_vars:
            if var in master_env and var.isidentifier() and not var.startswith('_'):
                found_vars.add(var)
                
    except (UnicodeDecodeError, OSError) as e:
        print(f"Warning: Could not read file {file_path}: {e}")

def load_master_env() -> Dict[str, str]:
    """Load environment variables from the master .env file"""
    # Look for .env in the current directory and its parents
    current_dir = Path.cwd()
    for parent in [current_dir, *current_dir.parents]:
        env_path = parent / '.env'
        if env_path.exists():
            return load_existing_env(str(env_path))
    return os.environ  # Fallback to environment variables


###############################################################################
# ENV FILE MERGING/REPLACING
###############################################################################

def load_existing_env(env_file_path: str) -> Dict[str, str]:
    """
    Loads key=value pairs from an existing .env file, ignoring empty lines
    and comment lines (#...).
    """
    env_dict = {}
    if os.path.exists(env_file_path) and os.path.isfile(env_file_path):
        with open(env_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    env_dict[key] = value
    return env_dict

def write_env_file(env_vars: Dict[str, str], output_path: str) -> None:
    """
    Writes environment variables to the specified file path in KEY=VALUE form.
    If VALUE is empty, includes a "# TODO: set value" comment.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for key in sorted(env_vars):
            value = env_vars[key]
            comment = "  # TODO: set value" if not value else ""
            f.write(f"{key}={value}{comment}\n")

def replace_env_file(found_vars: Set[str], env_file_path: str) -> None:
    """
    Overwrites the existing .env with only the newly found variables 
    (all values empty).
    """
    new_dict = {var: "" for var in found_vars}
    write_env_file(new_dict, env_file_path)

def add_empty_env_vars(found_vars: Set[str], env_file_path: str) -> None:
    """
    Loads the existing .env, merges with newly found variables as empty 
    placeholders, writes back to .env.
    """
    existing = load_existing_env(env_file_path)
    updated = dict(existing)  # copy
    for var in found_vars:
        if var not in updated:
            updated[var] = ""
    write_env_file(updated, env_file_path)

def add_env_vars_preserving_values(found_vars: Set[str], env_file_path: str) -> None:
    """
    Similar to add_empty_env_vars, but logically it's the same:
    we load existing, then add new ones if not present, set them to "".
    """
    add_empty_env_vars(found_vars, env_file_path)


###############################################################################
# IMPORTS REWRITING
###############################################################################

def rewrite_imports_in_code(base_path: str, ignore_paths: List[str] = None) -> None:
    """
    Enhanced method that not only rewrites imports but also adds dotenv loading code.
    This will:
    1. Remove any 'import mydotenv' or 'from mydotenv import ...' lines
    2. Add code to load the .env file from the project root
    3. Make environment variables directly accessible in the script
    
    Works on a single file or recursively in a directory.
    
    :param base_path: directory or file to rewrite
    :param ignore_paths: list of paths to ignore
    """
    if ignore_paths is None:
        ignore_paths = []
    
    # Get the master environment variables to check against
    master_env = load_master_env()

    # If it's a single .py file:
    if os.path.isfile(base_path) and base_path.endswith('.py'):
        _rewrite_imports_in_single_file(base_path, master_env)
        return

    # Otherwise, walk the directory
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [
            d for d in dirs
            if not any(os.path.join(root, d).startswith(os.path.join(base_path, ip)) for ip in ignore_paths)
        ]
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if any(ip in file_path for ip in ignore_paths):
                    continue
                _rewrite_imports_in_single_file(file_path, master_env)

def _rewrite_imports_in_single_file(file_path: str, master_env: Dict[str, str]) -> None:
    """
    Enhanced method that not only rewrites imports but also adds dotenv loading code.
    This will:
    1. Remove any 'import mydotenv' or 'from mydotenv import ...' lines
    2. Add code to load the .env file from the project root
    3. Make environment variables directly accessible in the script
    
    :param file_path: Path to the file to rewrite
    :param master_env: Dictionary of environment variables from the master .env
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines)
    except (UnicodeDecodeError, OSError) as e:
        print(f"Warning: Could not read file {file_path}: {e}")
        return

    # Check if file uses any environment variables from the master env
    # or has mydotenv imports
    import_line_regex = re.compile(r'^\s*(import\s+mydotenv|from\s+mydotenv\s+import\s+.*)', re.MULTILINE)
    uses_mydotenv = bool(import_line_regex.search(content))
    
    # Pattern to detect references to env.<something>
    env_usage_regex = re.compile(r'\benv\.([A-Za-z_][A-Za-z0-9_]*)\b')
    env_var_matches = env_usage_regex.findall(content)
    uses_env_object = bool(env_var_matches)
    
    # Pattern to detect direct variable access
    direct_var_regex = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\b')
    all_identifiers = set(direct_var_regex.findall(content))
    
    # Check if any of the identifiers match env vars in the master env
    uses_direct_vars = False
    for var in all_identifiers:
        if var in master_env and var.isidentifier() and not var.startswith('_'):
            uses_direct_vars = True
            break
    
    # Skip if no env vars are used and no mydotenv imports
    if not (uses_mydotenv or uses_env_object or uses_direct_vars):
        return
    
    # We'll store the new lines here
    new_lines = []
    found_mydotenv_import = False
    
    # Skip any mydotenv imports
    import_regex = re.compile(r'^\s*(import\s+mydotenv|from\s+mydotenv\s+import\s+.*)')

    # First, process all lines except the imports we want to replace
    for line in lines:
        if import_regex.match(line):
            # Skip this line to remove old mydotenv imports
            # But we note that we found them
            found_mydotenv_import = True
            continue
        else:
            new_lines.append(line)

    # Find where to insert our new code
    insert_idx = _find_place_after_imports(new_lines)
    
    # Add our new code block that loads the .env file and makes variables accessible
    dotenv_setup_code = [
        "# Auto-added by mydotenv --add imports\n",
        "from pathlib import Path\n",
        "from dotenv import load_dotenv\n",
        "\n",
        "# Find and load the .env file from the project root\n",
        "env_path = Path().absolute() / '.env'\n",
        "if env_path.exists():\n",
        "    load_dotenv(env_path)\n",
        "else:\n",
        "    # Try to find .env file in parent directories\n",
        "    current_dir = Path().absolute()\n",
        "    found = False\n",
        "    for parent in [current_dir, *current_dir.parents]:\n",
        "        potential_env = parent / '.env'\n",
        "        if potential_env.exists():\n",
        "            load_dotenv(potential_env)\n",
        "            found = True\n",
        "            break\n",
        "    if not found:\n",
        "        print(\"Warning: No .env file found in project directory or parents\")\n",
        "\n",
        "# Import os to access environment variables\n",
        "import os\n",
        "\n",
        "# Create env accessor for compatibility with env.VAR syntax\n",
        "class EnvAccessor:\n",
        "    def __getattr__(self, name):\n",
        "        return os.environ.get(name)\n",
        "\n",
        "env = EnvAccessor()\n",
        "\n",
        "# Make all environment variables directly accessible as variables\n",
        "for key, value in os.environ.items():\n",
        "    # Only import valid Python identifiers\n",
        "    if key.isidentifier() and not key.startswith('_'):\n",
        "        globals()[key] = value\n",
        "\n"
    ]
    
    # Insert our setup code
    for i, code_line in enumerate(dotenv_setup_code):
        new_lines.insert(insert_idx + i, code_line)

    # Write back the new content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def _find_place_after_imports(lines: list) -> int:
    """
    Find the index to insert code after all imports but before the main code starts.
    """
    i = 0
    n = len(lines)
    
    # Skip shebang if it exists
    if i < n and lines[i].startswith('#!'):
        i += 1
    
    # Skip blank lines and comments at the top
    while i < n and (not lines[i].strip() or lines[i].strip().startswith('#')):
        i += 1
    
    # Check for docstring
    if i < n and (lines[i].strip().startswith('"""') or lines[i].strip().startswith("'''")):
        # Skip until end of docstring
        doc_start = lines[i].strip()[:3]  # Grab the first 3 chars (''' or """)
        i += 1
        while i < n and doc_start not in lines[i]:
            i += 1
        if i < n:  # Found the end of the docstring
            i += 1
    
    # Skip blank lines after docstring
    while i < n and not lines[i].strip():
        i += 1
    
    # Now look for import statements and skip past them
    in_multiline_import = False
    start_idx = i  # Remember where imports started
    
    while i < n:
        line = lines[i].strip()
        
        # Check for multiline imports with parentheses
        if line.startswith('from ') or line.startswith('import '):
            if '(' in line and ')' not in line:
                in_multiline_import = True
                i += 1
                continue
            elif not in_multiline_import:
                i += 1
                continue
        
        # Check if we're in a multiline import
        if in_multiline_import:
            if ')' in line:
                in_multiline_import = False
                i += 1
                continue
            else:
                i += 1
                continue
                
        # If we've reached a line that's not an import or blank, stop
        if line and not line.startswith('#'):
            break
            
        # Skip blank lines and comments between imports
        i += 1
    
    # Add a blank line if we're not at the end and the next line isn't blank
    if i < n and lines[i].strip():
        return i
        
    return i


###############################################################################
# HELPER FUNCTIONS FOR INTEGRATION WITH MAIN CLI
###############################################################################

def handle_cli_flags(argv):
    """
    Handle the advanced CLI flags when called from the main CLI.
    This is used for integration with the original CLI.
    
    :param argv: List of command-line arguments (excluding the program name)
    """
    # Recreate a parser and process the arguments
    parser = argparse.ArgumentParser(
        description="Advanced CLI for mydotenv with scanning, .env replacement, additions, and import rewriting."
    )

    # Flags/Options
    parser.add_argument("--replace", action="store_true",
                        help="Replace the existing .env file with newly discovered env vars.")
    parser.add_argument("--add-empty", action="store_true",
                        help="Add newly discovered env vars with empty values if not present.")
    parser.add_argument("--add", action="store_true",
                        help="Add newly discovered env vars (placeholder). Or if used with 'imports', rewrite imports.")
    parser.add_argument("what", nargs="?", default=None,
                        help="Specify 'env' or 'imports'. For example: '--replace env', '--add imports' etc.")
    parser.add_argument("path", nargs="?", default=".",
                        help="Optional path to scan or rewrite. Defaults to current directory.")
    parser.add_argument("--ignore", nargs="*", default=[],
                        help="Paths to ignore when scanning or rewriting (e.g. 'tests', 'venv').")
    parser.add_argument("--env-file", default=".env",
                        help="Which .env file to write to or replace (default: .env)")

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        # If argparse tries to exit (e.g., on error), show help and return
        show_advanced_help()
        return

    # Continue with the normal CLI logic
    _process_cli_args(args)

def show_advanced_help():
    """Display help for the advanced CLI options."""
    print("""
mydotenv Advanced CLI Options

Environment Variable Scanning:
  --replace env [<path>]       Replace existing .env with variables found in code
  --add-empty env [<path>]     Add empty variables to existing .env
  --add env [<path>]           Add variables to existing .env (preserving values)

Import Rewriting:
  --add imports [<path>]       Rewrite imports to 'from mydotenv import env'

Options:
  --ignore [PATH...]           Paths to ignore when scanning
  --env-file FILE              Specify a different .env file (default: .env)

Examples:
  mydotenv --replace env .                   # Replace .env with variables from current dir
  mydotenv --add-empty env src/              # Add empty vars from src/ directory
  mydotenv --add imports .                   # Rewrite imports in current dir
  mydotenv --add env . --ignore tests venv   # Scan excluding tests and venv dirs
""")

def _process_cli_args(args):
    """
    Process the parsed CLI arguments - extracted from main() for reusability.
    """
    # Handle the case when --add imports is used without a what/path argument
    if args.add and not args.what and not args.path:
        print("Rewriting imports for all Python files in the current directory...")
        rewrite_imports_in_code(".", ignore_paths=args.ignore)
        print("Imports rewritten successfully for all files in the current directory.")
        return

    # If the user said e.g. `mydotenv --replace env <path>` 
    # then args.replace=True, args.what='env', args.path=<path or '.'>
    target = args.path if args.path else "."

    if args.what not in ["env", "imports"] and args.what is not None:
        print("You must specify 'env' or 'imports'. Example: `mydotenv --replace env .` or `mydotenv --add imports .`")
        return

    if args.what == "imports" or (args.add and not args.what):
        if not (args.add or args.replace or args.add_empty):
            # The user just typed: mydotenv imports path
            # We'll assume they meant "rewrite imports"
            args.add = True  # so we do rewrite logic

        # "Rewrite imports" path
        rewrite_imports_in_code(target, ignore_paths=args.ignore)
        print(f"Imports rewritten successfully for path '{target}'.")
        return

    # If we get here, we're handling the 'env' side of things
    # 1) Scan for env.* references in the provided path
    found_vars = scan_for_env_vars(target, ignore_paths=args.ignore)
    if not found_vars:
        print(f"No env.* references found in {target}. Nothing to do.")
        return

    # 2) Decide how to handle the .env file:
    env_file_path = args.env_file

    if args.replace:
        # Overwrite .env
        replace_env_file(found_vars, env_file_path)
        print(f"Replaced {env_file_path} with {len(found_vars)} newly discovered variables.")
    elif args.add_empty:
        # Merge new env vars as empty placeholders
        add_empty_env_vars(found_vars, env_file_path)
        print(f"Added {len(found_vars)} variables (if not present) as empty placeholders in {env_file_path}.")
    elif args.add:
        # Merge new env vars as empty placeholders 
        # (this is effectively the same as --add-empty in this example)
        add_env_vars_preserving_values(found_vars, env_file_path)
        print(f"Discovered {len(found_vars)} variables; merged them into {env_file_path}.")
    else:
        # If none of the flags were passed, we do nothing but warn
        print("No action specified (--replace, --add-empty, or --add). Nothing happened.")

def main():
    """
    Main entry point for the CLI when run directly with -m mydotenv.cli
    """
    parser = argparse.ArgumentParser(
        description="Advanced CLI for mydotenv with scanning, .env replacement, additions, and import rewriting."
    )

    # Flags/Options
    parser.add_argument("--replace", action="store_true",
                        help="Replace the existing .env file with newly discovered env vars.")
    parser.add_argument("--add-empty", action="store_true",
                        help="Add newly discovered env vars with empty values if not present.")
    parser.add_argument("--add", action="store_true",
                        help="Add newly discovered env vars (placeholder). Or if used with 'imports', rewrite imports.")
    parser.add_argument("what", nargs="?", default=None,
                        help="Specify 'env' or 'imports'. For example: '--replace env', '--add imports' etc.")
    parser.add_argument("path", nargs="?", default=".",
                        help="Optional path to scan or rewrite. Defaults to current directory.")
    parser.add_argument("--ignore", nargs="*", default=[],
                        help="Paths to ignore when scanning or rewriting (e.g. 'tests', 'venv').")
    parser.add_argument("--env-file", default=".env",
                        help="Which .env file to write to or replace (default: .env)")

    args = parser.parse_args()
    _process_cli_args(args)


if __name__ == "__main__":
    main() 