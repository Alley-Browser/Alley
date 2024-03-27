"""
Tests for the CustomizeDialog class.

Sets up a fixture dialog instance and tests:
- Initial state of dialog matches expected 
- Switching to dark mode updates styles correctly
- Switching to light mode updates styles correctly
- Switching to default mode clears styles
"""
import pytest
from src.CustomizeDialog import CustomizeDialog

@pytest.fixture
def dialog():
    return CustomizeDialog()

def test_init(dialog):
    assert dialog.windowTitle() == 'Appearance'
    assert dialog.minimumWidth() == 300
    assert dialog.dark_mode_radio.text() == 'Dark Mode'
    assert dialog.light_mode_radio.text() == 'Light Mode'
    assert dialog.default_radio.text() == 'Default'

def test_dark_mode(dialog):
    dialog.dark_mode_radio.click()
    assert 'background-color: #333333' in dialog.styleSheet()
    assert 'color: white' in dialog.styleSheet()

def test_light_mode(dialog):
    dialog.light_mode_radio.click() 
    assert 'background-color: #F5F5F5' in dialog.styleSheet()
    assert 'color: black' in dialog.styleSheet()

def test_default_mode(dialog):
    dialog.default_radio.click()
    assert dialog.styleSheet() == ''
