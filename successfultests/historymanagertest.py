"""
Tests for the HistoryManager class.

Includes tests for:

- Saving history to a JSON file
- Loading history from a JSON file
- Adding to history
- Clearing history
- Handling errors saving/loading history

Mocks are used to simulate a main window.
"""
import json
from unittest.mock import MagicMock
import pytest
from src.HistoryManager import HistoryManager

@pytest.fixture
def history_manager():
    return HistoryManager()

def test_save_history_success(history_manager):
    history_manager.history = [{"url": "https://www.python.org", "title": "Python"}]
    
    with open("test_history.json", "w") as f:
        json.dump(history_manager.history, f)
        
    assert history_manager.save_history() is None
    
def test_save_history_failure(history_manager):
    with pytest.raises(Exception):
        history_manager.save_history()
        
def test_save_history_empty(history_manager):
    history_manager.history = []
    
    assert history_manager.save_history() is None

def test_load_history_success(self):
        main_window = MagicMock()
        history_manager = HistoryManager(main_window)
        history_manager.history_file = "test_history.json"
        history_manager.load_history()
        assert len(history_manager.history) == 1
        assert history_manager.history[0]["url"] == "https://www.python.org"
        assert history_manager.history[0]["title"] == "Python"

def test_add_to_history_with_main_window(self):
        main_window = MagicMock()
        history_manager = HistoryManager(main_window)
        history_manager.add_to_history("https://www.python.org", "Python")
        assert len(history_manager.history) == 1
        assert history_manager.history[0]["url"] == "https://www.python.org"
        assert history_manager.history[0]["title"] == "Python"

def test_clear_history_with_mock_main_window(self):
        main_window_mock = MagicMock()
        history_manager = HistoryManager(main_window_mock)
        history_manager.add_to_history("https://www.python.org", "Python")
        history_manager.clear_history()
        assert len(history_manager.history) == 0

def test_save_history_failure(self):
        main_window = MagicMock()
        history_manager = HistoryManager(main_window)
        with pytest.raises(Exception):
            history_manager.save_history()
