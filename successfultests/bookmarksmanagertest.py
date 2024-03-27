"""
Unit tests for the BookmarkDialog class.

Includes tests for:

- Saving and removing bookmarks
- Opening bookmarks
- Adding and removing bookmark folders

"""
import unittest
from unittest.mock import MagicMock
from src.BookmarksManager import BookmarkDialog
from PyQt5.QtWidgets import QWidget
class TestBookmarkDialog(unittest.TestCase):

    def test_save_bookmark(self):
        dialog = BookmarkDialog()
        dialog.bookmark_name_input.setText("Test")
        dialog.save_bookmark()
        self.assertIn("Test", dialog.bookmarks)

    def test_remove_bookmark(self):
        dialog = BookmarkDialog()
        dialog.bookmarks.append("Test")
        dialog.bookmarks_list_widget.addItem("Test")
        dialog.remove_bookmark()
        self.assertNotIn("Test", dialog.bookmarks)
        self.assertEqual(dialog.bookmarks_list_widget.count(), 0)


class TestBookmarkDialog(unittest.TestCase):

    def test_open_bookmark(self):
        dialog = BookmarkDialog()
        url = "http://www.example.com"
        title = "Example"
        dialog.bookmarks.append({"url": url, "title": title})
        mock_item = MagicMock() 
        dialog.bookmarks_list_widget.addItem(mock_item)
        dialog.open_bookmark(mock_item)
        self.assertEqual(dialog.main_window.current_tab.url().toString(), url)


    def test_add_folder(self):
        dialog = BookmarkDialog()
        folder = "New Folder"
        dialog.add_folder(folder)
        self.assertIn(folder, dialog.folders)

    def test_remove_folder(self):
        dialog = BookmarkDialog()
        folder = "Folder"
        dialog.folders.append(folder)
        dialog.remove_folder(folder)
        self.assertNotIn(folder, dialog.folders)
