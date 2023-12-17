import os
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

class SaveFromNet(QDialog):
    def __init__(self, parent=None):
        super(SaveFromNet, self).__init__(parent)

        self.setWindowTitle('Save Media As')
        self.setWindowIcon(QIcon('Icons/Logo.png'))

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
        self.save_button.clicked.connect(self.save_media)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def select_file_path(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Save Location", "", "All Files (*)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def save_media(self):
        url = self.url_bar.text()
        file_path = self.file_path_edit.text()

        if not url or not file_path:
            QMessageBox.warning(self, "Error", "URL and file path must be specified.")
            return

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            QMessageBox.information(self, "Success", "Media saved successfully.")
            self.close()

        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Error", f"Failed to download media: {str(e)}")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    media_downloader = SaveFromNet()
    media_downloader.exec_()