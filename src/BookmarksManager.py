import json
import os
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QUrl, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QPushButton,QToolTip,
    QLabel, QMessageBox, QListWidgetItem, QComboBox, QWidget, QHBoxLayout,QInputDialog
)
from PyQt5.QtGui import QIcon

class BookmarkDialog(QDialog):
    def __init__(self, browser=None):
        super(BookmarkDialog, self).__init__()

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.bookmarks = []  # List to store bookmarks
        self.folders = ['Favorites', 'Personal', 'Work']  # List of folders
        self.clicked_color = "#45a049"  

        self.setWindowTitle('Bookmarks')
        self.setMinimumWidth(250)  
        self.setMinimumHeight(700) 

        layout = QVBoxLayout()

        

        layout.addWidget(QLabel("Enter a name for the bookmark:"))
        self.bookmark_name_input = QLineEdit()

        layout.addWidget(self.bookmark_name_input)

        folder_options_widget = QWidget()
        folder_options_layout = QHBoxLayout(folder_options_widget)

        add_folder_button = QPushButton()
        add_folder_button.setIcon(QIcon("add-folder.png"))
        add_folder_button.setText("Add Folder")
        add_folder_button.setToolTip("Add Folder")
        add_folder_button.clicked.connect(self.add_folder)
        add_folder_button.setStyleSheet("background-color: black;")

        remove_folder_button = QPushButton()
        remove_folder_button.setIcon(QIcon("delete-folder.png"))
        remove_folder_button.setText("Remove Folder")
        remove_folder_button.setToolTip("Remove Folder")
        remove_folder_button.clicked.connect(self.remove_folder)
        remove_folder_button.setStyleSheet("background-color: black;")

        folder_options_layout.addWidget(QLabel("Select a folder:"))
        self.folder_combo_box = QComboBox()
        self.folder_combo_box.addItems(['All'] + self.folders)
        folder_options_layout.addWidget(self.folder_combo_box)
        folder_options_layout.addWidget(add_folder_button)
        folder_options_layout.addWidget(remove_folder_button)

        layout.addWidget(folder_options_widget)

        self.bookmarks_list_widget = QListWidget()
        self.bookmarks_list_widget.itemClicked.connect(self.open_bookmark)

        save_button = QPushButton("Save Bookmark")
        save_button.clicked.connect(self.save_bookmark)  # Connect to save_bookmark method
        save_button.setStyleSheet("background-color: black; color: white;")

        remove_button = QPushButton("Remove Bookmark")
        remove_button.clicked.connect(self.remove_bookmark)
        remove_button.setStyleSheet("background-color: black; color: white;")

        view_bookmarks_button = QPushButton("View Bookmarks")
        view_bookmarks_button.clicked.connect(self.view_bookmarks)
        view_bookmarks_button.setStyleSheet("background-color: black; color: white;")
        view_bookmarks_button.setObjectName("view_bookmarks_button")  # Set object name for styling

        layout.addWidget(save_button)
        layout.addWidget(remove_button)
        layout.addWidget(view_bookmarks_button)
        layout.addWidget(self.bookmarks_list_widget)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)  # Close the dialog when the button is clicked
        close_button.setStyleSheet("background-color: black; color: white;")

        layout.addWidget(close_button)  # Add the close button

        self.setLayout(layout)

        self.main_window = None  # Initialize main_window attribute

        # Load bookmarks from file when the dialog is created
        self.load_bookmarks()

        # Apply QSS for styling and animation
        self.update_button_styles()

        self.move_center()

    def showEvent(self, event):
        # Override showEvent to move the dialog to the center without animation
        self.move_center()

    def slide_in_animation(self):
        self.animation = self.pos_anim(self.pos(), QPoint(0, self.y()), 150, self)
        self.animation.start()

    def pos_anim(self, start, end, duration, target):
        # Create a position animation
        pos_anim = QPropertyAnimation(target, b"pos")
        pos_anim.setStartValue(start)
        pos_anim.setEndValue(end)
        pos_anim.setDuration(duration)
        return pos_anim

    def set_main_window(self, main_window):
        self.main_window = main_window

    def get_bookmark_name(self):
        return self.bookmark_name_input.text()

    def get_selected_folder(self):
        return self.folder_combo_box.currentText()

    def save_bookmark(self):
        bookmark_name = self.get_bookmark_name()

        if not bookmark_name:
            QMessageBox.warning(self, 'Empty Name', 'Please enter a name for the bookmark.')
            return

        if not self.main_window:
            QMessageBox.warning(self, 'Main Window Not Set', 'Main window is not set.')
            return

        current_url = self.main_window.url_bar.text()
        if not current_url:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a valid URL.')
            return

        selected_folder = self.get_selected_folder()
        self.bookmarks.append({'name': bookmark_name, 'url': current_url, 'folder': selected_folder})
        self.update_bookmarks_list()
        self.bookmark_name_input.clear()
        # Save bookmarks to file after adding a new bookmark
        self.save_bookmarks()

    def remove_bookmark(self):
        selected_item = self.bookmarks_list_widget.currentItem()
        if selected_item:
            index = self.bookmarks_list_widget.row(selected_item)
            del self.bookmarks[index]
            QMessageBox.information(self, 'Bookmark Removed', 'Bookmark removed successfully.')
            self.update_bookmarks_list()
            # Save bookmarks to file after removing a bookmark
            self.save_bookmarks()

    def view_bookmarks(self):
        if self.bookmarks:
            self.update_bookmarks_list()
            self.show()  # Show the dialog with the slide-in animation
        else:
            QMessageBox.information(self, 'Bookmarks', 'No bookmarks available.')

    def open_bookmark(self, item):
        index = self.bookmarks_list_widget.row(item)
        bookmark = self.bookmarks[index]
        if self.main_window:
            self.main_window.current_browser().setUrl(QUrl(bookmark['url']))

    def update_bookmarks_list(self):
        selected_folder = self.get_selected_folder()
        self.bookmarks_list_widget.clear()
        for bookmark in self.bookmarks:
            folder = bookmark.get('folder', 'All')
            if selected_folder == 'All' or folder == selected_folder:
                item = QListWidgetItem(bookmark['name'])
                self.bookmarks_list_widget.addItem(item)

    def save_bookmarks(self):
        # Save bookmarks to a JSON file
        with open('bookmarks.json', 'w') as file:
            json.dump(self.bookmarks, file)

    def load_bookmarks(self):
        # Load bookmarks from the JSON file if it exists
        try:
            with open('bookmarks.json', 'r') as file:
                data = file.read()
                if data:
                    self.bookmarks = json.loads(data)
        except FileNotFoundError:
            pass  # Ignore if the file is not found
        except json.decoder.JSONDecodeError:
            # Handle the case where the file is not in the expected format
            QMessageBox.warning(self, 'Invalid Bookmarks File', 'The bookmarks file is not in the expected format.')

    def add_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Enter folder name:")
        if ok and folder_name:
            self.folders.append(folder_name)
            self.folder_combo_box.addItem(folder_name)

    def remove_folder(self):
        folder_name, ok = QInputDialog.getItem(self, "Remove Folder", "Select folder to remove:", self.folders, 0, False)
        if ok and folder_name:
            # Remove the folder and update the ComboBox
            self.folders.remove(folder_name)
            self.folder_combo_box.clear()
            self.folder_combo_box.addItems(['All'] + self.folders)
            # Update the bookmarks list to reflect the changes
            self.update_bookmarks_list()
    def populate_bookmarks(self, bookmarks):
        """
        Populate bookmarks in the dialog.

        Args:
            bookmarks (list): List of bookmarks to populate.
        """
        self.bookmarks = bookmarks
        self.update_bookmarks_list()
    
    def move_center(self):
        # Move the dialog to the left side and center vertically
        if self.main_window:
            main_window_geometry = self.main_window.geometry()
            dialog_width = self.width()
            dialog_height = self.height()
            x = main_window_geometry.x()  # Set x-coordinate to the left side
            y = main_window_geometry.y() + (main_window_geometry.height() - dialog_height) // 2
            self.setGeometry(x, y, dialog_width, dialog_height)



    def update_button_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #272727;
                border: 1px solid #444;
                border-radius: 10px;
                color: #fff;
            }

            QPushButton {
                background-color: black;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            QPushButton:hover {
                background-color: #333;
            }

            QPushButton:pressed {
                background-color: """ + self.clicked_color + """;
            }

            QPushButton#view_bookmarks_button:pressed {
                background-color: """ + self.clicked_color + """;
            }

            QLineEdit, QComboBox {
                background-color: #333;
                border: 1px solid #444;
                padding: 6px;
                color: #fff;
            }

            QListWidget {
                background-color: #333;
                border: 1px solid #444;
                color: #fff;
            }

            QListWidget::item {
                padding: 8px;
            }

            QListWidget::item:selected {
                background-color: #45a049;
            }

            QLabel {
                color: #fff;
            }
        """)
