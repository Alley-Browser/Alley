from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QApplication, QFrame, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie
from pytube import YouTube
import os
import sys

class MediaDownloaderThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, file_path):
        super().__init__()
        self.url = url
        self.file_path = file_path

    def run(self):
        try:
            yt = YouTube(self.url)
            video_title = yt.title
            save_path = os.path.join(self.file_path, f"{video_title}.mp4")

            if os.path.exists(save_path):
                raise Exception("File already exists. Choose a different save location.")

            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=self.file_path)
            self.finished.emit(video_title)
        except Exception as e:
            self.error.emit(str(e))

class SaveFromNet(QDialog):
    def __init__(self, parent=None):
        super(SaveFromNet, self).__init__(parent)

        layout = QVBoxLayout()

        self.label = QLabel("Enter the URL of the media you want to save:")
        layout.addWidget(self.label)

        self.url_bar = QLineEdit()
        layout.addWidget(self.url_bar)

        self.file_path_label = QLabel("Select the path to save the media:")
        layout.addWidget(self.file_path_label)

        self.file_path_edit = QLineEdit()
        layout.addWidget(self.file_path_edit)

        self.file_path_button = QPushButton("Choose...")
        self.file_path_button.clicked.connect(self.select_file_path)
        layout.addWidget(self.file_path_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.start_download)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def select_file_path(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Save Location", "", "All Files (*)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def start_download(self):
        url = self.url_bar.text()
        file_path = self.file_path_edit.text()

        if not url or not file_path:
            QMessageBox.warning(self, "Error", "URL and file path must be specified.")
            return

        # Close current dialog
        self.close()

        # Show loading dialog
        loading_dialog = LoadingDialog(url, file_path)
        loading_dialog.finished.connect(self.download_finished)
        loading_dialog.exec_()

    def download_finished(self, video_title):
        QMessageBox.information(self, "Success", f"Media '{video_title}' saved successfully.")

class LoadingDialog(QDialog):
    finished = pyqtSignal(str)

    def __init__(self, url, file_path, parent=None):
        super(LoadingDialog, self).__init__(parent)

        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 10px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Set layout margins to zero

        # Loading GIF
        self.loading_movie = QMovie("Icons/progress.gif")
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFixedSize(320, 64)  # Set fixed size for the QLabel to match the GIF
        self.loading_label.setMovie(self.loading_movie)
        self.loading_movie.start()
        layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)
        layout.setSpacing(0)  # Set layout spacing to zero

        self.setLayout(layout)

        # Set dialog position and size
        self.resize(320, 64)  # Set window size to match the GIF size
        self.setFixedSize(self.size())  # Disable resizing

        # Center the dialog on the screen
        screen_geometry = QApplication.desktop().screenGeometry()
        self.move(screen_geometry.center() - self.rect().center())

        # Start download in a separate thread
        self.download_thread = MediaDownloaderThread(url, file_path)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.error.connect(self.download_error)
        self.download_thread.start()

    def download_finished(self, video_title):
        self.finished.emit(video_title)
        self.close()

    def download_error(self, error_message):
        QMessageBox.warning(self, "Error", f"Failed to download media: {error_message}")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    loading_dialog = LoadingDialog("https://www.example.com/video.mp4", "/path/to/save")
    loading_dialog.exec_()

    sys.exit(app.exec_())

    def download_finished(self, video_title):
        self.finished.emit(video_title)
        self.close()

    def download_error(self, error_message):
        QMessageBox.warning(self, "Error", f"Failed to download media: {error_message}")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    media_downloader = SaveFromNet()
    media_downloader.show()

    sys.exit(app.exec_())
