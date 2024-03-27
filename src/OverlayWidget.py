from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QVBoxLayout, QWidget


class OverlayWidget(QWidget):
    def __init__(self, content_widget, parent=None):
        super(OverlayWidget, self).__init__(parent)

        self.content_widget = content_widget
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border: 1px solid black;")

        layout = QVBoxLayout()
        layout.addWidget(self.content_widget)
        self.setLayout(layout)

    def showEvent(self, event):
        self.setGeometry(
            self.parent().geometry().x(),
            self.parent().geometry().y(),
            self.parent().geometry().width(),
            self.parent().geometry().height()
        )

    def create_dropdown_menu(self):
        menu = QMenu(self)

        # Add actions to the menu with icons
        actions = [
            ("Bookmarks", self.show_bookmarks,"Icons/bm.ico"),
            ("History", self.show_history, "Icons/h.ico"),
            ("Chatbot", self.open_chatbot_overlay, "Icons/cb.ico"),
            ("Downloads", self.show_downloads, "Icons/d.ico"),
            ("Media Downloader", self.open_media_downloader, "Icons/md.ico"),
        ]

        for action_text, slot, icon_path in actions:
            action = QAction(QIcon(icon_path), action_text, self)
            action.triggered.connect(slot)
            menu.addAction(action)