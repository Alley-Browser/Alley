"""
Test suite for MainWindow class.

Includes tests for:

- Importing required modules
- Initializing attributes 
- Initializing UI elements
- Opening URLs

"""
import pytest
from src.MainWindow import MainWindow
from PyQt5.QtCore import QUrl
@pytest.fixture
def main_window():
    return MainWindow()

def test_import_statements(main_window):
    assert main_window.re is not None
    assert main_window.os is not None
    # Test imports of other modules


def test_init_attributes(main_window):
    assert isinstance(main_window.url, QUrl) 
    assert main_window.window_width == 1024
    assert main_window.window_height == 768
    # Test initialization of other attributes


def test_init_ui(main_window):
    assert main_window.tab_widget is not None
    assert main_window.toolbar is not None
    assert main_window.status_bar is not None
    # Test initialization of UI elements

def test_open_url(main_window):
    test_url = 'https://www.python.org'
    main_window.open_url(test_url)
    assert main_window.tab_widget.currentWidget().url().toString() == test_url

