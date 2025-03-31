import os
import pathlib
import sys
import subprocess
import argparse
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

# Files and directories that Git ignores internally
GIT_INTERNAL_IGNORES = ['.git', '.gitmodules']

def find_git_repo_root(start_path):
    """Find the git repository root containing the start_path."""
    path = pathlib.Path(start_path).resolve()
    for parent in [path] + list(path.parents):
        if (parent / '.git').is_dir():
            return parent
    return None

def parse_args():
    parser = argparse.ArgumentParser(
        description="A tree-like directory listing that respects gitignore patterns"
    )

    # Core tree options
    parser.add_argument("-L", "--level", type=int, help="Descend only level directories deep")
    parser.add_argument("-d", "--dirs-only", action="store_true", help="List directories only")
    parser.add_argument("-f", "--full-path", action="store_true", help="Print the full path prefix for each file")
    parser.add_argument("-a", "--all", action="store_true", help="All files are listed, including hidden files")
    parser.add_argument("-p", "--show-perms", action="store_true", help="Print file permissions")
    parser.add_argument("-s", "--show-size", action="store_true", help="Print file sizes")
    parser.add_argument("-i", "--no-indent", action="store_true", help="Don't print indentation lines")
    parser.add_argument("--noreport", action="store_true", help="Omit file/directory count at end")

    # TreeIgnore specific options
    parser.add_argument("--no-ignore", action="store_true", help="Do not use gitignore filtering")
    parser.add_argument("--version", action="store_true", help="Show version information and exit")

    # Path argument
    parser.add_argument("path", nargs="?", default=".", help="Directory path to list")

    return parser.parse_args()

def main():
    args = parse_args()

    # Check if version flag is set
    if args.version:
        from treeignore import __version__
        print(f"treeignore version {__version__}")
        return

    # Get the starting directory from args
    start_dir = os.path.abspath(args.path)

    # Find git repository root
    repo_root = find_git_repo_root(start_dir)

    # If not in a git repo, just check for a .gitignore in the current directory
    if not repo_root:
        print(f"Not in a git repository. Looking for .gitignore in {start_dir}")
        if not os.path.exists(os.path.join(start_dir, '.gitignore')):
            print("No .gitignore found. Showing all files.")

    # Use git command if in a git repository
    use_git_command = repo_root is not None

    # Load gitignore patterns only if not using git command directly
    gitignore_spec = None
    if repo_root and not use_git_command:
        gitignore_spec = load_all_gitignores(repo_root, start_dir)

    # Track directory counts for summary
    dir_count = 0
    file_count = 0

    def is_ignored(path, args):
        # If --no-ignore is specified, don't ignore anything except .git internal folders
        if args.no_ignore:
            basename = os.path.basename(path)
            return basename in GIT_INTERNAL_IGNORES
            
        # If -a/--all is specified, don't ignore anything except .git internal folders
        if args.all:
            basename = os.path.basename(path)
            return basename in GIT_INTERNAL_IGNORES

        # Otherwise, use the original gitignore logic
        # Don't ignore the root directory
        if path == start_dir:
            return False

        # Check if this path should be always ignored (like Git does internally)
        basename = os.path.basename(path)
        if basename in GIT_INTERNAL_IGNORES:
            return True

        if use_git_command and repo_root:
            return is_git_ignored(path, repo_root)
        elif gitignore_spec:
            # Convert to path relative to repo root for top-level .gitignore patterns
            if repo_root:
                rel_path = os.path.relpath(path, repo_root)
            else:
                rel_path = os.path.relpath(path, start_dir)

            # Convert to forward slashes for matching (Git style)
            rel_path = rel_path.replace(os.sep, '/')

            # Git treats patterns that contain / as anchored to the root
            # Patterns without / match anywhere in the path
            is_dir = os.path.isdir(path)
            return gitignore_spec.match_file(rel_path) or (is_dir and gitignore_spec.match_file(rel_path + '/'))

        return False

    def print_tree(dir_path, prefix="", args=None, level=0):
        nonlocal dir_count, file_count
        
        if args is None:
            args = type('Args', (), {'level': None, 'dirs_only': False, 'full_path': False,
                                     'all': False, 'show_perms': False, 'show_size': False,
                                     'no_indent': False})
        # Check recursion level limit
        if args.level is not None and level >= args.level:
            return

        try:
            # Get and sort directory contents
            contents = sorted(os.listdir(dir_path))
        except (PermissionError, FileNotFoundError):
            print(f"{prefix}[error reading directory]")
            return

        # PHASE 1: Collect and filter - Apply all filters upfront
        display_items = []
        for item in contents:
            full_path = os.path.join(dir_path, item)
            
            # Skip ignored files
            if is_ignored(full_path, args):
                continue
                
            # Skip non-directories if dirs_only is enabled
            is_dir = os.path.isdir(full_path)
            if args.dirs_only and not is_dir:
                continue
                
            # Item passed all filters, add it to display list
            display_items.append((item, full_path, is_dir))

        # PHASE 2: Render the filtered list
        count = len(display_items)
        for i, (item, full_path, is_dir) in enumerate(display_items):
            is_last = i == count - 1
            
            # Choose the appropriate prefix symbols
            if is_last:
                connector = "└── " if not args.no_indent else ""
                new_prefix = prefix + "    " if not args.no_indent else ""
            else:
                connector = "├── " if not args.no_indent else ""
                new_prefix = prefix + "│   " if not args.no_indent else ""
            
            # Print full path if requested
            display_path = full_path if args.full_path else item

            # Print file permissions if requested
            if args.show_perms:
                perms = oct(os.stat(full_path).st_mode)[-3:]
                display_path = f"{perms} {display_path}"

            # Print file size if requested
            if args.show_size:
                size = os.path.getsize(full_path)
                display_path = f"{display_path} [{size} bytes]"

            print(f"{prefix}{connector}{display_path}")

            # Recursively print subdirectories
            if is_dir:
                dir_count += 1
                print_tree(full_path, new_prefix, args, level + 1)
            else:
                file_count += 1

    # Print the root directory (always show this regardless of dirs_only)
    print(os.path.basename(start_dir) or start_dir)
    
    # Start the tree
    print_tree(start_dir, args=args)

    # Print summary (like the tree command)
    if not args.noreport:
        print(f"\n{dir_count} directories, {file_count} files")

def is_git_ignored(path, repo_root):
    """
    Use actual Git to check if a path is ignored.
    This ensures we're matching Git's behavior precisely.
    """
    try:
        # Use git check-ignore command to check if a path is ignored
        rel_path = os.path.relpath(path, repo_root)
        result = subprocess.run(
            ['git', '-C', str(repo_root), 'check-ignore', '-q', rel_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Return code 0 means ignored, 1 means not ignored, 128 means error
        return result.returncode == 0
    except Exception:
        # Fall back to our own implementation if git command fails
        return False

def load_all_gitignores(repo_root, current_dir):
    """
    Load gitignore patterns exactly as Git does:
    1. Global gitignore file (from git config)
    2. Repository excludes file (.git/info/exclude)
    3. All .gitignore files from root to current directory
    """
    patterns = []
    
    # 1. Get global gitignore path from git config
    try:
        global_gitignore = subprocess.run(
            ['git', 'config', '--get', 'core.excludesFile'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout.strip()
        
        # If not configured, use default location
        if not global_gitignore:
            global_gitignore = os.path.expanduser('~/.config/git/ignore')
        
        if os.path.exists(global_gitignore):
            with open(global_gitignore, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
    except Exception:
        # If git config fails, try default location
        global_gitignore = os.path.expanduser('~/.config/git/ignore')
        if os.path.exists(global_gitignore):
            with open(global_gitignore, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
    
    # 2. Load repository-specific excludes
    exclude_file = repo_root / '.git' / 'info' / 'exclude'
    if exclude_file.exists():
        with open(exclude_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    
    # 3. Load all .gitignore files from repository root to current directory
    # Get relative path from repo root to current directory
    rel_path = os.path.relpath(current_dir, repo_root)
    path_parts = rel_path.split(os.sep) if rel_path != '.' else []
    
    # Check each directory from root to current
    current_path = repo_root
    for part in [''] + path_parts:  # Start with root, then add each part
        if part:
            current_path = current_path / part
        
        gitignore_file = current_path / '.gitignore'
        if gitignore_file.exists():
            with open(gitignore_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
    
    # Create a PathSpec with the collected patterns
    return PathSpec.from_lines(GitWildMatchPattern, patterns) if patterns else None

if __name__ == '__main__':
    main()
