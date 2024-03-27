import json
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon,QCursor
from PyQt5.QtWidgets import QAction, QMenu, QMessageBox

class HistoryManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.history_file = "history.json"
        self.history = []
        self.history_menu = QMenu("History", self.main_window)
        self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                self.history = json.load(file)

    def save_history(self):
        try:
            with open(self.history_file, "w") as file:
                json.dump(self.history, file)
            print("History saved successfully.")
        except Exception as e:
            print("Error saving history:", e)


    def add_to_history(self, url, title):
        self.history.append({"url": url, "title": title})

    def clear_history(self):
        self.history.clear()
        self.save_history()

    def show_history_menu(self, position):
        self.history_menu.clear()

        if not self.history:
            history_action = QAction("No history available", self.main_window)
            history_action.setEnabled(False)
            self.history_menu.addAction(history_action)
        else:
            for item in self.history:
                url = QUrl(item["url"])
                title = item["title"]
                
                # Check if the title is empty and use the URL as the title
                display_title = title if title else url.toString()

                action = QAction(display_title, self.main_window)
                action.triggered.connect(lambda checked, url=url: self.open_url(url))
                self.history_menu.addAction(action)

            clear_history_action = QAction("Clear History", self.main_window)
            clear_history_action.triggered.connect(self.clear_history)
            self.history_menu.addAction(clear_history_action)

        self.history_menu.exec_(self.main_window.mapToGlobal(position))

    def open_url(self, url):
        browser = self.main_window.current_browser()
        if browser:
            browser.setUrl(url)

def add_history_action(self, main_window):
    history_icon = QIcon(os.path.join(os.path.dirname(__file__), "Icons", "history.png"))
    history_action = QAction(history_icon, "History", main_window)
    history_action.triggered.connect(lambda: self.show_history_menu(main_window.mapToGlobal(QCursor.pos())))
    return history_action