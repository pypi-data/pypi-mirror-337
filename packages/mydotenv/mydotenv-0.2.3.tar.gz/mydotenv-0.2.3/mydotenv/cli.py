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

    # Regex to match env.<VAR_NAME>
    pattern = re.compile(r'\benv\.([A-Za-z_][A-Za-z0-9_]*)\b')
    found_vars = set()

    # If the user gave a single file instead of a directory, handle that
    if os.path.isfile(directory) and directory.endswith('.py'):
        _scan_file(directory, pattern, found_vars, ignore_paths)
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
                _scan_file(file_path, pattern, found_vars, ignore_paths)

    return found_vars

def _scan_file(
    file_path: str,
    pattern: "re.Pattern",
    found_vars: Set[str],
    ignore_paths: List[str]
) -> None:
    """Helper function to scan a single .py file."""
    if any(ip in file_path for ip in ignore_paths):
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = pattern.findall(content)
        if matches:
            found_vars.update(matches)
    except (UnicodeDecodeError, OSError) as e:
        print(f"Warning: Could not read file {file_path}: {e}")


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
    Naively finds any 'import mydotenv' or 'from mydotenv import ...' lines 
    and rewrites them as 'from mydotenv import env'. If there's no mydotenv import 
    found in a file, we add 'from mydotenv import env' at the top (only if the file 
    actually references 'env.*', otherwise it's pointless).
    
    :param base_path: directory or file to rewrite
    :param ignore_paths: list of paths to ignore
    """
    if ignore_paths is None:
        ignore_paths = []

    # If it's a single .py file:
    if os.path.isfile(base_path) and base_path.endswith('.py'):
        _rewrite_imports_in_single_file(base_path)
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
                _rewrite_imports_in_single_file(file_path)

def _rewrite_imports_in_single_file(file_path: str) -> None:
    """
    Naive method to remove lines containing 'import mydotenv' or 
    'from mydotenv import ...' and replace them with 'from mydotenv import env'.
    If no lines are found, we check if there's any 'env.*' usage; if yes, 
    we add 'from mydotenv import env' at the top.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, OSError) as e:
        print(f"Warning: Could not read file {file_path}: {e}")
        return

    # Pattern to detect references to env.<something>
    env_usage_regex = re.compile(r'\benv\.\w+\b')

    # Check if there's any usage of env.* in the file at all
    file_content = "".join(lines)
    uses_env = bool(env_usage_regex.search(file_content))

    # If there's no usage, don't modify anything
    if not uses_env:
        return

    # We'll store the new lines here
    new_lines = []
    found_mydotenv_import = False

    # Patterns for rewriting
    import_line_regex = re.compile(r'^\s*(import\s+mydotenv|from\s+mydotenv\s+import\s+.*)')

    for line in lines:
        if import_line_regex.match(line):
            # We'll skip this line to remove old mydotenv imports
            # But we note that we found them
            found_mydotenv_import = True
            continue
        else:
            new_lines.append(line)

    # If we need to add an import
    if found_mydotenv_import or not _has_import_of_env(new_lines):
        # Find a good place to insert the import statement
        # First look for the last import statement
        last_import_idx = _find_last_import_line(new_lines)
        if last_import_idx != -1:
            # Insert after the last import
            new_lines.insert(last_import_idx + 1, "from mydotenv import env\n")
        else:
            # No existing imports, try to insert after docstring and shebang
            insert_idx = _find_place_after_shebang_and_docstring(new_lines)
            new_lines.insert(insert_idx, "from mydotenv import env\n")
            # Add a blank line after the import if it's not already there
            if insert_idx + 1 < len(new_lines) and new_lines[insert_idx + 1].strip():
                new_lines.insert(insert_idx + 1, "\n")

    # Write back the new content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def _find_last_import_line(lines: list) -> int:
    """
    Find the index of the last import statement in the file.
    Returns -1 if none found.
    """
    import_pattern = re.compile(r'^\s*(import\s+|from\s+.*\s+import\s+)')
    last_import_idx = -1
    
    for i, line in enumerate(lines):
        if import_pattern.match(line):
            last_import_idx = i
    
    return last_import_idx

def _find_place_after_shebang_and_docstring(lines: list) -> int:
    """
    Find the index to insert an import after shebang and docstring.
    """
    i = 0
    n = len(lines)
    
    # Skip shebang if it exists
    if i < n and lines[i].startswith('#!'):
        i += 1
    
    # Skip blank lines
    while i < n and not lines[i].strip():
        i += 1
    
    # Check for docstring
    if i < n and (lines[i].startswith('"""') or lines[i].startswith("'''")):
        # Skip until end of docstring
        doc_start = lines[i][:3]  # Grab the first 3 chars (''' or """)
        i += 1
        while i < n and doc_start not in lines[i]:
            i += 1
        if i < n:  # Found the end of the docstring
            i += 1
    
    # Skip any blank lines after the docstring
    while i < n and not lines[i].strip():
        i += 1
    
    return i

def _has_import_of_env(lines: list) -> bool:
    """
    Quick check if lines contain "from mydotenv import env" already.
    """
    for line in lines:
        if "from mydotenv import env" in line:
            return True
    return False


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
    # If the user said e.g. `mydotenv --replace env <path>` 
    # then args.replace=True, args.what='env', args.path=<path or '.'>
    target = args.path if args.path else "."

    if args.what not in ["env", "imports"]:
        print("You must specify 'env' or 'imports'. Example: `mydotenv --replace env .` or `mydotenv --add imports .`")
        return

    if args.what == "imports":
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