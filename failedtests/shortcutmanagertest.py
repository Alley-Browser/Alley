from msilib.schema import Shortcut
import unittest
from unittest.mock import patch

from PyQt5.QtTest import QTest
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow

from src.ShortcutManager import ShortcutManager

import unittest
from unittest.mock import patch

from PyQt5.QtTest import QTest
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut

from src.ShortcutManager import ShortcutManager

import unittest
from unittest.mock import patch

from PyQt5.QtTest import QTest
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtCore import Qt

from src.ShortcutManager import ShortcutManager

class TestShortcutManager(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.manager = ShortcutManager(self.window)

    def test_create_shortcuts(self):
        self.manager.create_shortcuts()
        
        # Verify new tab shortcut
        new_tab_shortcut = self.manager.main_window.findChild(QShortcut, "new tab")
        self.assertEqual(new_tab_shortcut.key(), QKeySequence("Ctrl+T"))
        self.assertTrue(new_tab_shortcut.activated.connect.called_with(self.manager.main_window.add_tab))
        
        # Verify close tab shortcut
        close_tab_shortcut = self.manager.main_window.findChild(QShortcut, "close tab")
        self.assertEqual(close_tab_shortcut.key(), QKeySequence("Ctrl+W"))
        self.assertTrue(close_tab_shortcut.activated.connect.called_with(self.manager.main_window.close_tab))

        # ... Verify other shortcuts

    def test_shortcut_actions(self):
        self.manager.create_shortcuts()
        
        # Trigger new tab shortcut and verify tab added
        new_tab_shortcut = self.manager.main_window.findChild(QShortcut, "new tab")
        with patch.object(self.manager.main_window, 'add_tab') as mock_add_tab:
            QTest.keyClick(self.manager.main_window, Qt.Key_T, Qt.ControlModifier)
            mock_add_tab.assert_called_once()

        # Trigger close tab shortcut and verify tab closed
        close_tab_shortcut = self.manager.main_window.findChild(QShortcut, "close tab")
        with patch.object(self.manager.main_window, 'close_tab') as mock_close_tab:
            QTest.keyClick(self.manager.main_window, Qt.Key_W, Qt.ControlModifier)
            mock_close_tab.assert_called_once()

        # ... Verify actions for other shortcuts



if __name__ == '__main__':
    unittest.main()
