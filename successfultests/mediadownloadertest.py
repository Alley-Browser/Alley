"""
Unit test cases for the SaveFromNet dialog in MediaDownloader.

Contains tests for:
- Initializing the dialog
- Selecting a file path 
- Saving media with invalid/valid inputs
"""
import unittest
from PyQt5.QtTest import QTest
from src.MediaDownloader import SaveFromNet
from PyQt5.QtCore import Qt
class TestSaveFromNet(unittest.TestCase):

    def setUp(self):
        self.dialog = SaveFromNet()

    def test_init(self):
        self.assertEqual(self.dialog.windowTitle(), 'Save Media As')
        self.assertIsNotNone(self.dialog.url_bar)
        self.assertIsNotNone(self.dialog.file_path_edit)
        self.assertIsNotNone(self.dialog.save_button)

    def test_select_file_path(self):
        QTest.mouseClick(self.dialog.file_path_button, Qt.LeftButton)
        self.assertNotEqual(self.dialog.file_path_edit.text(), '')

    def test_save_media_invalid(self):
        QTest.mouseClick(self.dialog.save_button, Qt.LeftButton)
        self.assertEqual(self.dialog.result(), 0) # dialog should not close

    def test_save_media_valid(self):
        self.dialog.url_bar.setText('http://test.com/image.jpg')
        self.dialog.file_path_edit.setText('/tmp/image.jpg')
        QTest.mouseClick(self.dialog.save_button, Qt.LeftButton)
        self.assertEqual(self.dialog.result(), 1) # dialog should close


