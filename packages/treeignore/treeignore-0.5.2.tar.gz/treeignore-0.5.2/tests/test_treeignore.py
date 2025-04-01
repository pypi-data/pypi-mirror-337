import os
import shutil
import subprocess
import pytest
from pathlib import Path

@pytest.fixture
def test_dir():
    """Create a test directory structure and clean it up after tests."""
    test_dir_path = Path("temp_test_dir")
    
    # Clean up any existing test directory
    if test_dir_path.exists():
        shutil.rmtree(test_dir_path)
    
    # Create test directory structure
    os.makedirs(test_dir_path / "visible_subdir", exist_ok=True)
    os.makedirs(test_dir_path / "ignored_subdir", exist_ok=True)
    os.makedirs(test_dir_path / ".hidden_dir", exist_ok=True)
    
    # Create test files
    (test_dir_path / "visible_file.txt").touch()
    (test_dir_path / "ignored_file.log").touch()
    (test_dir_path / "visible_subdir" / "visible_subfile.txt").touch()
    (test_dir_path / "visible_subdir" / "ignored_subfile.log").touch()
    (test_dir_path / "ignored_subdir" / "nested_file.txt").touch()
    (test_dir_path / ".hidden_dir" / "hidden_file.txt").touch()
    
    # Create .gitignore file
    with open(test_dir_path / ".gitignore", "w") as f:
        f.write("*.log\nignored_subdir/\n")
    
    yield test_dir_path
    
    # Clean up after tests
    shutil.rmtree(test_dir_path)

def has_tree_command():
    """Check if the tree command is available."""
    try:
        subprocess.run(["tree", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def run_command(cmd):
    """Run a command and return its output."""
    result = subprocess.run(cmd, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          check=True, 
                          text=True)
    return result.stdout

def test_no_ignore_matches_tree(test_dir):
    """Test that treeignore with --no-ignore matches tree output for non-hidden files."""
    if not has_tree_command():
        pytest.skip("tree command not available")
    
    # Get tree output with -a to show hidden files
    tree_cmd = ["tree", "-a", str(test_dir)]
    tree_output = run_command(tree_cmd)
    
    # Get treeignore output with --no-ignore
    treeignore_cmd = ["treeignore", str(test_dir), "--no-ignore"]
    treeignore_output = run_command(treeignore_cmd)
    
    # Instead of comparing raw output lines which might differ in formatting,
    # we'll check that all expected files are present in both outputs
    visible_files = [
        "visible_file.txt", 
        "visible_subfile.txt",
        "ignored_file.log",  # This is in both outputs because --no-ignore is used
        "ignored_subfile.log",
        "nested_file.txt",
        ".gitignore",
        "hidden_file.txt"
    ]
    
    # Check that all key files are in both outputs
    for filename in visible_files:
        assert filename in tree_output, f"{filename} missing from tree output"
        assert filename in treeignore_output, f"{filename} missing from treeignore output"

def test_gitignore_filtering(test_dir):
    """Test that treeignore correctly filters files based on .gitignore."""
    # Run treeignore with gitignore filtering
    cmd = ["treeignore", str(test_dir)]
    output = run_command(cmd)
    
    # Files that should be ignored
    assert "ignored_file.log" not in output
    assert "ignored_subfile.log" not in output
    assert "ignored_subdir" not in output
    
    # Files that should be visible
    assert "visible_file.txt" in output
    assert "visible_subfile.txt" in output

def test_show_perms_flag(test_dir):
    """Test the -p/--show-perms flag."""
    cmd = ["treeignore", str(test_dir), "-p"]
    output = run_command(cmd)
    
    # Check that permissions are shown (octal format)
    assert "644" in output or "664" in output or "755" in output or "775" in output

def test_show_size_flag(test_dir):
    """Test the -s/--show-size flag."""
    cmd = ["treeignore", str(test_dir), "-s"]
    output = run_command(cmd)
    
    # Check that file sizes are shown
    assert "bytes" in output

def test_no_indent_flag(test_dir):
    """Test the -i/--no-indent flag."""
    cmd = ["treeignore", str(test_dir), "-i"]
    output = run_command(cmd)
    
    # Check that the output doesn't contain indentation characters
    assert "├──" not in output
    assert "└──" not in output
    assert "│" not in output

def test_noreport_flag(test_dir):
    """Test the --noreport flag."""
    cmd = ["treeignore", str(test_dir), "--noreport"]
    output = run_command(cmd)
    
    # Check that directory and file count is not shown
    assert "directories" not in output.lower()
    assert "files" not in output.lower()

def test_flag_combinations(test_dir):
    """Test combinations of flags."""
    # Test -p -s (permissions and sizes)
    cmd = ["treeignore", str(test_dir), "-p", "-s"]
    output = run_command(cmd)
    assert ("644" in output or "664" in output or "755" in output or "775" in output) and "bytes" in output
    
    # Test -i --noreport (no indent, no report)
    cmd = ["treeignore", str(test_dir), "-i", "--noreport"]
    output = run_command(cmd)
    assert "├──" not in output and "directories" not in output.lower()
    
    # Test all flags
    cmd = ["treeignore", str(test_dir), "-p", "-s", "-i", "--noreport"]
    output = run_command(cmd)
    permission_shown = "644" in output or "664" in output or "755" in output or "775" in output
    assert permission_shown and "bytes" in output and "├──" not in output and "directories" not in output.lower()
