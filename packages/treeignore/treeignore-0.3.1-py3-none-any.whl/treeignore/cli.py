import os
import pathlib
import sys
import subprocess
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

def main():
    # Get the starting directory (default is current directory)
    start_dir = os.getcwd()
    
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
    
    def is_ignored(path):
        """
        Check if path should be ignored.
        Uses 'git check-ignore' command if in a git repo, otherwise falls back to our implementation.
        """
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
    
    def print_tree(dir_path, prefix=""):
        """Recursively print directory tree, filtering by gitignore patterns."""
        nonlocal dir_count, file_count
        
        try:
            # Get and sort directory contents
            contents = sorted(os.listdir(dir_path))
        except (PermissionError, FileNotFoundError):
            print(f"{prefix}[error reading directory]")
            return
            
        # Filter out ignored items
        filtered_contents = []
        for item in contents:
            full_path = os.path.join(dir_path, item)
            if not is_ignored(full_path):
                filtered_contents.append(item)
        
        # Count items for prefix calculation
        count = len(filtered_contents)
        
        # Print each item
        for i, item in enumerate(filtered_contents):
            is_last = i == count - 1
            full_path = os.path.join(dir_path, item)
            
            # Choose the appropriate prefix symbols
            if is_last:
                connector = "└── "
                new_prefix = prefix + "    "
            else:
                connector = "├── "
                new_prefix = prefix + "│   "
                
            print(f"{prefix}{connector}{item}")
            
            # Recursively print subdirectories
            if os.path.isdir(full_path):
                dir_count += 1
                print_tree(full_path, new_prefix)
            else:
                file_count += 1
    
    # Print the root and start the tree
    print(os.path.basename(start_dir) or start_dir)
    print_tree(start_dir)
    
    # Print summary (like the tree command)
    print(f"\n{dir_count} directories, {file_count} files")

if __name__ == '__main__':
    main()
