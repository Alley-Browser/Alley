import re
import os
import datetime
from PyQt5.QtCore import QUrl, Qt,QSize
from PyQt5.QtGui import QKeySequence,QCursor, QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView,QWebEnginePage
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QDockWidget,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QTabWidget,
    QToolBar,
    QToolButton,
    QApplication,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QShortcut,
)
from PyQt5.QtCore import QTimer
import pyautogui
import cv2
import numpy as np

from PyQt5.QtWidgets import QFileDialog
import sys
import json
from urllib.parse import urlparse
from src.CustomChatbot import CustomChatbot
from src.MediaDownloader import SaveFromNet
from src.ChatOverlay import ChatOverlay
from src.BookmarksManager import BookmarkDialog
from src.CustomizeDialog import CustomizeDialog
from src.ShortcutManager import ShortcutManager
from src.DownloadManager import DownloadDialog,DownloadManager
from src.HistoryManager import HistoryManager
from src.wheel import CustomOverlay
from PyQt5.QtCore import pyqtSlot

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.shortcut_manager = ShortcutManager(self)

        self.setWindowTitle("Alley Browser")
        self.setWindowIcon(QIcon(resource_path("Icons\\Logo.png")))
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.update_url_from_active_tab)
        self.download_manager = DownloadManager(parent=self)
        self.download_manager.hide()
        self.history_manager = HistoryManager(self)
        self.history_manager.load_history()
        self.custom_overlay = CustomOverlay(self)
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.setFixedHeight(55)

        self.setMinimumSize(QSize(600, 350))
        # Create an instance of ShortcutManager
        self.shortcut_manager = ShortcutManager(self)
        # Call the method to create shortcuts
        self.shortcut_manager.create_shortcuts()

        self.setWindowTitle("Alley Browser")
        self.setGeometry(100, 100, 800, 600)

        self.recording = False
        self.video_writer = None

        icon_width = 12
        icon_height = 12
        self.icon_width = 12
        self.icon_height = 12 
        self.tabs.currentChanged.connect(self.update_url_from_active_tab)
        self.tabs.currentChanged.connect(self.update_url_from_tab)
        home_btn = QAction(QIcon(QPixmap(resource_path("Icons\\h.svg")).scaled(2*icon_width,2* icon_height)), "⌂ HomePage", self)
        toolbar.setMovable(False)
        #home_btn.setShortcut('Alt+H')
        home_btn.triggered.connect(self.navigate_home)
        toolbar.addAction(home_btn)
        
        back_btn = QAction(
            QIcon(QPixmap(resource_path("Icons\\l.svg")).scaled(4*icon_width,4* icon_height)), "⮜ Navigate to Previous Page", self
        )
        back_btn.triggered.connect(
            lambda: self.current_browser().back() if self.current_browser() else None
        )
        toolbar.addAction(back_btn)
        forward_btn = QAction(
            QIcon(QPixmap(resource_path("Icons\\rn.png")).scaled(4*icon_width,4* icon_height)), "⮞ Navigate to Next Page", self
        )
        forward_btn.triggered.connect(
            lambda: self.current_browser().forward() if self.current_browser() else None
        )
        toolbar.addAction(forward_btn)
        reload_btn = QAction(
            QIcon(QPixmap(resource_path("Icons\\rd.svg")).scaled(4*icon_width,4* icon_height)), "⟳ Reload the Page", self
        )
        reload_btn.triggered.connect(
            lambda: self.current_browser().reload() if self.current_browser() else None
        )
        toolbar.addAction(reload_btn)
        self.url_bar = QLineEdit()
        self.url_bar.setFixedHeight(34)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("margin-left: 60%; margin-right: 60%; font-size: 14px")
        toolbar.addWidget(self.url_bar)
        toolbar_layout = QVBoxLayout(toolbar)
        toolbar_layout.addWidget(self.url_bar)
        toolbar.setLayout(toolbar_layout)

        # Add screenshot button
        screenshot_btn = QAction(QIcon(QPixmap(resource_path("Icons\\screenshot_icon.png"))), "Screenshot  Alt + S", self)
        screenshot_btn.triggered.connect(self.take_screenshot)
        toolbar.addAction(screenshot_btn)

        # Add start recording button
        start_recording_btn = QAction(QIcon(QPixmap(resource_path("Icons\\start_recording_icon.png"))), "Start Recording  Ctrl + Alt + R", self)
        start_recording_btn.triggered.connect(self.start_recording)
        toolbar.addAction(start_recording_btn)

        # Add stop recording button
        stop_recording_btn = QAction(QIcon(QPixmap(resource_path("Icons\\stop_recording_icon.png"))), "Stop Recording  Ctrl + Alt + S", self)
        stop_recording_btn.triggered.connect(self.stop_recording)
        toolbar.addAction(stop_recording_btn)
    
        add_tab_btn = QAction(
            QIcon(QPixmap(resource_path("Icons\\a.svg")).scaled(3*icon_width,3* icon_height)), "+ New Tab", self
        )
        add_tab_btn.triggered.connect(self.add_tab)
        toolbar.addAction(add_tab_btn)
        
        self.bookmarks_action = QAction(
            QIcon(QPixmap(resource_path("Icons\\sr.svg")).scaled(4 * icon_width, 4 * icon_height)),
            "Bookmarks",
            self,
        )
        self.bookmarks_action.triggered.connect(self.show_bookmarks)
        
        toolbar.addAction(self.bookmarks_action)

        self.dropdown_menu = QMenu(self)
        self.bookmarks_action = QAction("Bookmarks", self)
        self.history_action = QAction("History", self)
        self.customize_ui_action = QAction("Customize", self)
        self.dropdown_menu.addAction(self.bookmarks_action)
        self.dropdown_menu.addAction(self.history_action)
        icon_size = 24
        menu_stylesheet = """
QMenu {
    background-color: qlineargradient(x2:1, y2:1, x2:1, y2:1, stop:0 #1e1e1e, stop:1 purple);
    border: 1px solid #2e2e2e;
    width: 280px; 
    height: 480px; 
}

QMenu::item {
    padding: 12px 22px;
    color: #ffffff;
}

QMenu::item:selected {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e1e, stop:1 black);
    border-radius:4px;
    border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: #ffffff;
	border-bottom-color: transparent;
	border-left-width: 2px;
}

QMenu::icon {{
    width: {icon_size}px;
    height: {icon_size}px;
}}

QMenu::separator {
    height: 1px;
    background-color: #2e2e2e;
}
        """
        self.dropdown_menu.setStyleSheet(menu_stylesheet)

        dropdown_btn = QToolButton(self)
        dropdown_btn.setMenu(self.dropdown_menu)
        dropdown_btn.setPopupMode(QToolButton.InstantPopup)
        dropdown_btn.setIcon(QIcon(resource_path("Icons\\m.svg")))
        # Add a separator to make the menu visually more appealing
        self.dropdown_menu.addSeparator()

        # Create actions for zoom in and zoom out
        zoom_in_dropdown_action = QAction(QIcon(QPixmap(resource_path('Icons\\zi.svg')).scaled(3* self.icon_width, 3 * self.icon_height)), 'Zoom In', self)
        zoom_in_dropdown_action.triggered.connect(self.zoom_in)

        zoom_out_dropdown_action = QAction(QIcon(QPixmap(resource_path('Icons\\zo.svg')).scaled(3*self.icon_width,3* self.icon_height)), 'Zoom Out', self)
        zoom_out_dropdown_action.triggered.connect(self.zoom_out)

        # Add a separator before adding zoom actions
        self.dropdown_menu.addSeparator()

        # Add zoom in and zoom out actions to the dropdown menu
        self.dropdown_menu.addAction(zoom_out_dropdown_action)
        self.dropdown_menu.addAction(zoom_in_dropdown_action)

        # Create action for reset zoom
        reset_zoom_action = QAction(QIcon(resource_path('Icons\\zr.svg')), 'Reset Zoom', self)
        reset_zoom_action.triggered.connect(self.reset_zoom)

        # Add reset zoom action to the dropdown menu
        self.dropdown_menu.addAction(reset_zoom_action)

        self.dropdown_menu.addSeparator()
        self.customize_ui_action = QAction(QIcon(resource_path("Icons\\dm.svg")), "Appearance", self)
        self.customize_ui_action.triggered.connect(self.open_customize_dialog)
        self.dropdown_menu.addAction(self.customize_ui_action)

        # Connect CustomizeDialog to main window for color changes
        self.customize_dialog = CustomizeDialog(self)
        self.customize_ui_action.triggered.connect(self.customize_dialog.show)

        # Replace 'Icons/bookmarks_icon.ico' with the actual path to your bookmarks icon
        bookmarks_icon_path = resource_path('Icons\\saved.png')
        self.bookmarks_action.setIcon(QIcon(bookmarks_icon_path))

        inspect_element_action_dropdown = QAction(QIcon(resource_path('Icons\\dt.svg')), 'Dev tool', self)
        inspect_element_action_dropdown.triggered.connect(self.inspect_element)
        self.dropdown_menu.addAction(inspect_element_action_dropdown)
        
        # Replace 'Icons/bookmarks_icon.ico' with the actual path to your bookmarks icon
        bookmarks_icon_path = resource_path("Icons\\bm.svg")
        self.bookmarks_action.setIcon(QIcon(bookmarks_icon_path))

        # Replace 'Icons/history_icon.ico' with the actual path to your history icon
        history_icon_path = resource_path("Icons\\hr.svg")
        self.history_action.setIcon(QIcon(history_icon_path))
        toolbar.addWidget(dropdown_btn)

        self.bookmarks_action.triggered.connect(self.show_bookmarks)
        self.history_action.triggered.connect(lambda: self.history_manager.show_history_menu(self.mapToGlobal(QCursor.pos())))

        # Chatbot instance
        self.chatbot = CustomChatbot()

        # Action for opening chatbot overlay
        chatbot_icon_path = resource_path("Icons\\cb.svg")
        chatbot_action = QAction(QIcon(chatbot_icon_path), "Chatbot", self)
        chatbot_action.triggered.connect(self.open_chatbot_overlay)
        self.dropdown_menu.addAction(chatbot_action)

        # Downloads action in the dropdown
        self.downloaded_files = []  # List to keep track of downloaded files
        downloads_icon_path = resource_path("Icons\\d.svg")
        download_action = QAction(QIcon(QIcon(downloads_icon_path)), "Downloads", self)
        download_action.triggered.connect(self.show_download_manager)
        self.dropdown_menu.addAction(download_action)

        # Media Downloader instance
        self.media_downloader = SaveFromNet()

        # Media Downloader action in the dropdown
        media_downloader_icon_path = resource_path("Icons\\md.png")
        media_downloader_action = QAction(
            QIcon(media_downloader_icon_path), "Media Downloader", self
        )
        media_downloader_action.triggered.connect(self.open_media_downloader)
        self.dropdown_menu.addAction(media_downloader_action)

        self.add_tab()

        # Chatbot overlay
        self.chat_overlay = ChatOverlay(chatbot=self.chatbot)
        self.chat_overlay.setVisible(False)  # Initially hide the chat overlay
        self.layout().addWidget(self.chat_overlay)  # Add to the main window layout

        wheel_action = QAction("Widgets", self)
        wheel_action.triggered.connect(self.toggle_custom_overlay)
        self.dropdown_menu.addAction(wheel_action)
        # Connect the closed signal of CustomOverlay to hide the overlay
        self.custom_overlay.closed.connect(self.hide_custom_overlay)

        # Connect Alt+E shortcut to close the wheel
        self.close_wheel_shortcut = QShortcut(QKeySequence("Alt+E"), self)
        self.close_wheel_shortcut.activated.connect(self.close_wheel)

        self.load_tabs_data()  # Load saved tabs when the application starts

    def start_recording(self):
        if not self.recording:
            self.recording = True
            screen_width, screen_height = pyautogui.size()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Videos (*.mp4)")
            if file_path:
                self.video_writer = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (screen_width, screen_height))

            if self.video_writer is not None:  # Check if video_writer is properly initialized
                self.timer = QTimer()
                self.timer.timeout.connect(self.capture_screen)
                self.timer.start(100)  # Capture screen every 100 milliseconds
            else:
                print("Failed to initialize video writer.")

    def capture_screen(self):
        if self.recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.video_writer.write(frame)

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.timer.stop()
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None

    def take_screenshot(self):
        if self.current_browser():
            screenshot = self.current_browser().grab()
            # Get the user's Pictures directory
            pictures_directory = os.path.join(os.path.expanduser("~"), "Pictures")
            # Create the Screenshots directory path within the Pictures directory
            screenshots_directory = os.path.join(pictures_directory, "Screenshots")
            # Ensure that the Screenshots directory exists
            if not os.path.exists(screenshots_directory):
                os.makedirs(screenshots_directory)
            # Generate a unique filename based on the current date and time
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_file = os.path.join(screenshots_directory, f"screenshot_{timestamp}.png")
            # Save the screenshot
            screenshot.save(screenshot_file)
            QMessageBox.information(self, "Screenshot Taken", f"Screenshot saved as '{screenshot_file}'")

    def on_download_requested(self, download):
        download.finished.connect(self.on_download_finished)
        download.downloadProgress.connect(self.on_download_progress)

        suggested_file_name = download.suggestedFileName()
        mime_type = download.mimeType()

        default_downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

        download_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", os.path.join(default_downloads_path, suggested_file_name),
            f"{mime_type} (*.{suggested_file_name.split('.')[-1]})"
        )

        if download_path:
            download.setPath(download_path)
            download.accept()

            # Use the DownloadManager to add the download
            self.download_manager.add_download(download.url().toString(), suggested_file_name)
        else:
            download.cancel()

    def on_download_progress(self, bytes_received, bytes_total):
        print(f"Downloaded {bytes_received} of {bytes_total} bytes")

    def on_download_finished(self):
        print("Download finished")
         
    def show_download_manager(self):
    # Toggle the visibility of the DownloadDialog
        self.download_manager.setVisible(not self.download_manager.isVisible())

    def show_download_manager(self):
        self.download_manager.show()

    def reset_zoom(self):
        if self.current_browser():
            self.current_browser().setZoomFactor(1.0)
            self.update_zoom_label()

    def set_zoom_factor(self, factor):
        if self.current_browser():
            self.current_browser().setZoomFactor(factor)
            self.update_zoom_label()

    def zoom_in(self):
        if self.current_browser():
            current_factor = self.current_browser().zoomFactor()
            self.current_browser().setZoomFactor(current_factor + 0.1)
            self.update_zoom_label()

    def zoom_out(self):
        if self.current_browser():
            current_factor = self.current_browser().zoomFactor()
            self.current_browser().setZoomFactor(max(current_factor - 0.1, 0.1))
            self.update_zoom_label()

    def update_zoom_label(self):
        if self.current_browser():
            zoom_percentage = int(self.current_browser().zoomFactor() * 100)
            self.statusBar().showMessage(f"Zoom: {zoom_percentage}%")

    def update_url_from_active_tab(self, index):
        current_browser = self.tabs.widget(index)
        if current_browser:
            self.url_bar.setText(current_browser.url().toString())

    def focus_address_bar(self):
        self.url_bar.setFocus()
        self.url_bar.selectAll()

    def open_settings(self):
        # Replace this with your actual settings implementation
        QMessageBox.information(
            self,
            "Settings",
            "Placeholder for settings. Implement your settings logic here.",
        )

    def current_browser(self):
        return self.tabs.currentWidget() if self.tabs.count() > 0 else None

    def load_tabs_data(self):
        if not os.path.exists(resource_path("tabs_data.json")):  # Check if the file exists
            with open(resource_path("tabs_data.json"), "w") as file:  # Create the file
                json.dump([], file)  # Write an empty list to the file
                print("tabs_data.json file created.")
        else:
            try:
                with open(resource_path("tabs_data.json"), "r") as file:
                    tabs_data = json.load(file)
                    if not tabs_data:  # Check if the file is empty
                        print("No data found in tabs_data.json")
                        return
                    for tab_data in tabs_data:
                        if tab_data["url"] != "https://duckduckgo.com/":
                            self.add_tab(url=tab_data["url"])
            except FileNotFoundError:
                print("File tabs_data.json not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON data in tabs_data.json")

    def save_tabs_data(self):
        tabs_data = []
        for i in range(self.tabs.count()):
            browser = self.tabs.widget(i)
            url = browser.url().toString()
            # Exclude 'https://www.google.com/' from being saved
            if url != "https://duckduckgo.com/":
                tabs_data.append({"url": url})

        with open(resource_path("tabs_data.json"), "w") as file:
            json.dump(tabs_data, file)

    def closeEvent(self, event):
        self.save_tabs_data()  # Save tabs data when the application is closed
        self.history_manager.save_history()  # Save history when the application is closed
        event.accept()


    def current_browser(self):
        return self.tabs.currentWidget() if self.tabs.count() > 0 else None

    def add_tab(self, url=None):
        # Check if there are no tabs open and the JSON file is empty or not found
        if self.tabs.count() == 0 or (
            not self.is_tabs_data_file_found() or self.is_tabs_data_empty()
        ):
            self.open_default_tab()
        else:
            browser = QWebEngineView()

            # Connect the browser's urlChanged signal to track visited URLs
            if url:
                browser.setUrl(QUrl(url))
            else:
                browser.setUrl(QUrl("https://duckduckgo.com/"))

            self.tabs.addTab(browser, "New Tab")
            self.tabs.setCurrentWidget(browser)
            self.tabs.setTabText(self.tabs.currentIndex(), "Loading...")

            browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser))
            if self.current_browser():
                browser.urlChanged.connect(lambda url, browser=browser: self.update_url(url) if self.current_browser() == browser else None)
                browser.page().profile().downloadRequested.connect(self.on_download_requested)

            # Set the favicon for the new tab
            browser.loadFinished.connect(lambda: self.update_tab_title(browser))

            if self.current_browser():
                browser.urlChanged.connect(
                    lambda url, browser=browser: self.update_url(url)
                    if self.current_browser() == browser
                    else None
                )
            
                browser.page().profile().downloadRequested.connect(self.on_download_requested)

    #commitfix
    # Helper methods for file and data checks
    def is_tabs_data_file_found(self):
        try:
            with open(resource_path("tabs_data.json"), "r") as file:
                return True
        except FileNotFoundError:
            return False

    def is_tabs_data_empty(self):
        try:
            with open(resource_path("tabs_data.json"), "r") as file:
                tabs_data = json.load(file)
                return not bool(tabs_data)
        except json.JSONDecodeError:
            return True

    def open_default_tab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://duckduckgo.com/"))

        self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)
        browser.page().profile().downloadRequested.connect(self.on_download_requested)
        self.tabs.setTabText(self.tabs.currentIndex(), "Loading...")

        browser.titleChanged.connect(
            lambda title, browser=browser: self.update_tab_title(browser)
        )

        if self.current_browser():
            browser.urlChanged.connect(
                lambda url, browser=browser: self.update_url(url)
                if self.current_browser() == browser
                else None
            )
    
    def update_tab_title(self, browser):
        # Get the domain name from the URL without "www."
        parsed_url = urlparse(browser.url().toString())
        domain = parsed_url.hostname.replace("www.", "") if parsed_url.hostname else "Unknown"

        # Get the webpage title and limit it to 15 characters
        title = browser.page().title()[:15]

        # Set the tab text with the title and show the full title on hover
        tab_text = f"{title} "  # Adjust spacing as needed
        self.tabs.setTabText(self.tabs.indexOf(browser), tab_text)
        self.tabs.setTabToolTip(self.tabs.indexOf(browser), browser.page().title())

        # Fetch the website favicon
        def favicon_changed(icon):
            favicon_pixmap = icon.pixmap(16, 16) if not icon.isNull() else None
            if favicon_pixmap is not None:
                tab_icon = QIcon(favicon_pixmap)
                self.tabs.setTabIcon(self.tabs.indexOf(browser), tab_icon)

        # Connect the favicon_changed function to the iconChanged signal
        browser.page().iconChanged.connect(favicon_changed)

    def close_tab(self, index):
        browser_widget = self.tabs.widget(index)

        if browser_widget.url().host() == "www.youtube.com":
            browser_widget.page().runJavaScript(
                "document.getElementsByTagName('video')[0].pause();"
            )

        if self.tabs.count() < 2:
            self.close()
        else:
            self.tabs.removeTab(index)
            browser_widget.deleteLater()

    def navigate_home(self):

        if self.current_browser():
            self.current_browser().setUrl(QUrl("https://duckduckgo.com/"))

    def navigate_to_url(self):
        if self.current_browser():
            input_text = self.url_bar.text()

            if ".com" in input_text:
                url = input_text
            else:
                url = f'https://duckduckgo.com/?hps=1&q={"+".join(input_text.split())}&ia=web'


            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            self.current_browser().setUrl(QUrl(url))

    def update_url(self, q):
        if self.current_browser() and self.sender() == self.current_browser():
            url = q.toString()
            title = self.current_browser().page().title()

            if url != "https://duckduckgo.com/":
                self.history_manager.add_to_history(url, title)

            self.url_bar.setText(url)
            self.url_bar.setCursorPosition(0)


    def update_url_from_tab(self, index):
        current_browser = self.tabs.widget(index)
        if current_browser:
            if current_browser == self.current_browser():
                url = current_browser.url()
                title = current_browser.page().title()
                self.history_manager.add_to_history(url.toString(), title)
            self.update_url(current_browser.url())

    def show_bookmarks(self):
        if not hasattr(self, 'bookmark_dialog') or not self.bookmark_dialog.isVisible():
            self.bookmark_dialog = BookmarkDialog(browser=self.current_browser())
            self.bookmark_dialog.set_main_window(self)
            self.bookmark_dialog.show()
        else:
            self.bookmark_dialog.activateWindow()

    def show_bookmark_dialog(self):
        dialog = BookmarkDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            bookmark_name = dialog.get_bookmark_name()
            current_url = self.url_bar.text()

            if bookmark_name and current_url:
                # Save the bookmark (you can implement your saving logic here)
                print(f"Bookmark saved - Name: {bookmark_name}, URL: {current_url}")
            else:
                print("Bookmark not saved - Name or URL is empty.")

    def create_toolbar_action(self, icon_path, callback, shortcut=None, text=''):
        # Use self.icon_width and self.icon_height to access class attributes
        action = QAction(QIcon(QPixmap(icon_path).scaled(self.icon_width, self.icon_height)), text, self)
        if shortcut:
            action.setShortcut(shortcut)
        if text == 'Bookmark':
            action.triggered.connect(self.show_bookmark_dialog)  # Corrected this line
        else:
            action.triggered.connect(callback)
        return action

    def show_bookmarks_dialog(self):
            # Create an instance of BookmarkDialog and show it
            bookmarks_dialog = BookmarkDialog(parent=self)
            bookmarks_dialog.set_main_window(self)  # Pass the main window reference if needed
            bookmarks_dialog.exec_()

    def open_customize_dialog(self):
        customize_dialog = CustomizeDialog(self)
        customize_dialog.exec_()

    def truncate_url(self, url, max_length=40):
        # Truncate the URL to a maximum length
        if len(url) > max_length:
            return f"{url[:max_length-3]}..."
        return url
            
    def open_chatbot_overlay(self):
        # Toggle the visibility of the chat overlay
        self.chat_overlay.setVisible(not self.chat_overlay.isVisible())

    def open_media_downloader(self):
        # Show the Media Downloader dialog
        result = self.media_downloader.exec_()
        if result == QDialog.Accepted:
            # Handle downloaded file
            filename = self.media_downloader.file_path_edit.text()
            print(f"File path: {filename}")
            
            if filename and os.path.exists(filename):
                try:
                    self.downloaded_files.append(filename)
                    QMessageBox.information(
                        self,
                        "Download Complete",
                        f"File '{filename}' downloaded successfully.",
                    )
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"Failed to handle downloaded file: {str(e)}",
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"The file '{filename}' does not exist.",
                )

    def show_downloads(self):
        if not self.downloaded_files:
            QMessageBox.information(self, "Downloads", "No files downloaded yet.")
            return

        downloads_text = "\n".join(self.downloaded_files)
        QMessageBox.information(
            self, "Downloads", f"Downloaded Files:\n{downloads_text}"
        )

    def cut_text(self):
        if hasattr(self, 'current_browser') and self.current_browser():
            self.current_browser().page().triggerAction(QWebEnginePage.Cut)

    def copy_text(self):
        if hasattr(self, 'current_browser') and self.current_browser():
            self.current_browser().page().triggerAction(QWebEnginePage.Copy)

    def paste_text(self):
        if hasattr(self, 'current_browser') and self.current_browser():
            self.current_browser().page().triggerAction(QWebEnginePage.Paste)

    def undo_text(self):
        if hasattr(self, 'current_browser') and self.current_browser():
            self.current_browser().page().triggerAction(QWebEnginePage.Undo)

    def redo_text(self):
        if hasattr(self, 'current_browser') and self.current_browser():
            self.current_browser().page().triggerAction(QWebEnginePage.Redo)

    def inspect_element(self):
        if self.current_browser():
            # Get the current browser page
            page = self.current_browser().page()
            # Enable remote debugging
            page.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
            # Create a new QWebEngineView for DevTools
            dev_tools_browser = QWebEngineView()
            dev_tools_browser.page().setDevToolsPage(page)
            # Create a QDockWidget to contain the DevTools browser
            dock_widget = QDockWidget("DevTools", self)
            dock_widget.setWidget(dev_tools_browser)

            # Add a close button
            close_button = QPushButton("Close DevTools", dock_widget)
            close_button.clicked.connect(dock_widget.close)
            dock_widget.setTitleBarWidget(close_button)

            dock_widget.setFeatures(
                QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
            )
            # Set the QDockWidget to be a right dock
            self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)
            # Open DevTools using the remote debugging URL
            dev_tools_url = (
                page.url()
                .toString()
                .replace("http://", "chrome-devtools://devtools/remote/")
            )
            dev_tools_browser.setUrl(QUrl(dev_tools_url))

    def toggle_custom_overlay(self):
        if self.custom_overlay.isVisible():
            self.hide_custom_overlay()
        else:
            self.show_custom_overlay()

    def show_custom_overlay(self):
        self.custom_overlay.show()

    def hide_custom_overlay(self):
        self.custom_overlay.hide()

    def open_wheel(self):
        # Implement the logic to open the wheel here
        self.toggle_custom_overlay()

    def close_wheel(self):
        # Implement the logic to close the wheel here
        self.home_button.clicked.emit()