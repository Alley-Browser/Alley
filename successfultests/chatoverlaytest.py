"""
Test suite for ChatOverlay UI component.

Covers:
- Initializing ChatOverlay
- Setting up UI elements
- Testing UI interaction methods like exit_overlay and clear_chat_display
- Stubbing chatbot integration to test UI flow

Limitations: 
- Full UI behavior requires application launch
- Actual chatbot integration not tested here
"""
import pytest
from pytestqt.qt_compat import qt_api
from PyQt5 import QtCore
from src.ChatOverlay import ChatOverlay


@pytest.fixture
def chat_overlay(qtbot):
    test_chatbot = None  # mock chatbot
    overlay = ChatOverlay(test_chatbot)
    qtbot.addWidget(overlay)
    return overlay


def test_init(chat_overlay):
    assert chat_overlay.chatbot is None



def test_init_ui(chat_overlay, qtbot):
    chat_overlay.init_ui()
    assert chat_overlay.user_input
    assert chat_overlay.chat_display
    qtbot.mouseClick(chat_overlay.exit_button, QtCore.Qt.LeftButton)


def test_exit_overlay(chat_overlay, qtbot):
    chat_overlay.show()
    qtbot.mouseClick(chat_overlay.exit_button, QtCore.Qt.LeftButton)
    assert not chat_overlay.isVisible()


def test_clear_chat_display(chat_overlay):
    chat_overlay.chat_display.setPlainText("Hello")
    chat_overlay.clear_chat_display()
    assert chat_overlay.chat_display.toPlainText() == ""


def test_get_chatbot_response(chat_overlay, qtbot):
    chat_overlay.init_ui()
    qtbot.keyClicks(chat_overlay.user_input, "Hi")
    qtbot.mouseClick(chat_overlay.submit_button, QtCore.Qt.LeftButton)
    assert "Hi" in chat_overlay.chat_display.toPlainText()



#The tests will cover:

#Initializing the ChatOverlay class
#Calling the init_ui method to set up the UI
#Testing the exit_overlay, clear_chat_display, and get_chatbot_response methods
#Limitations:

#Cannot fully test UI without application launch
#Chatbot integration not tested
