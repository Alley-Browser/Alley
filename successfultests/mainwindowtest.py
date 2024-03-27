"""
Tests for the resource_path function which handles resolving resource 
paths when running as a frozen executable or normally as a module.

Covers different use cases like:
- Running normally as __main__
- Running as frozen executable
- Empty relative path
- Absolute path 
- Invalid relative path
- Relative path with subdirectories
- Special characters in path
- Different environments like __main__ vs frozen

Ensures proper joining of paths and raising errors as needed.
"""
import os
import sys
from src.MainWindow import resource_path

def test_resource_path_main():
    # Test with __main__
    path = resource_path("relative/path")
    assert path == os.path.join(os.getcwd(), "relative/path")

def test_resource_path_frozen():
    # Test with frozen PyInstaller path
    sys._MEIPASS = "frozen/path" 
    path = resource_path("relative/path")
    assert path == os.path.join(sys._MEIPASS, "relative/path")
    
def test_resource_path_empty():
    # Test with empty relative path
    path = resource_path("")
    assert path == os.getcwd()

def test_resource_path_abs_path():
    # Test with absolute path
    path = resource_path("/abs/path")
    assert path == "/abs/path"

def test_resource_path_invalid():
    # Test with invalid relative path
    try:
        resource_path("invalid\\path")
    except ValueError:
        pass
    else:
        raise AssertionError("Did not raise ValueError for invalid path")

def test_resource_path_relative():
    # Test with relative path
    path = resource_path("relative/path")
    assert path == os.path.join(os.getcwd(), "relative/path")

def test_resource_path_frozen():
    # Test with frozen PyInstaller path
    sys._MEIPASS = "frozen/path" 
    path = resource_path("relative/path")
    assert path == os.path.join(sys._MEIPASS, "relative/path")

def test_resource_path_special_characters():
    # Test with relative path containing special characters
    path = resource_path("special!@#$%^&*()_+{}[]|\\:\";'<>?,./`~")
    assert path == os.path.join(os.getcwd(), "special!@#$%^&*()_+{}[]|\\:\";'<>?,./`~")

def test_resource_path_multiple_subdirectories():
    # Test with relative path containing multiple subdirectories
    path = resource_path("subdir1/subdir2/subdir3")
    assert path == os.path.join(os.getcwd(), "subdir1/subdir2/subdir3")

def test_resource_path_empty_string_pyinstaller():
    # Test with empty relative path
    sys._MEIPASS = "frozen/path" 
    path = resource_path("")
    assert path == sys._MEIPASS

def test_resource_path_absolute_path_pyinstaller():
    # Test with frozen PyInstaller path
    sys._MEIPASS = "frozen/path" 
    path = resource_path("/abs/path")
    assert path == "/abs/path"

def test_resource_path_multiple_subdirectories_pyinstaller():
    # Test with multiple subdirectories in relative path when running in PyInstaller environment
    sys._MEIPASS = "frozen/path" 
    path = resource_path("subdir1/subdir2/relative/path")
    assert path == os.path.join(sys._MEIPASS, "subdir1/subdir2/relative/path")

def test_resource_path_special_characters_abs_path():
    # Test with a path containing special characters as the absolute path input
    path = resource_path("/abs/path!@#$%^&*()")
    assert path == "/abs/path!@#$%^&*()"

def test_resource_path_invalid_pyinstaller():
    # Test with invalid relative path in PyInstaller environment
    sys._MEIPASS = "frozen/path" 
    try:
        resource_path("invalid\\path")
    except ValueError:
        pass
    else:
        raise AssertionError("Did not raise ValueError for invalid path")
