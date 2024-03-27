import sys
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_path = 'themes/Sub-Zero.qss'
    with open(style_path, 'r') as f:
        app.setStyleSheet(f.read())
    app.setApplicationName("Alley")
    app.setApplicationDisplayName("Alley")
    app.setOrganizationName("SDCCE")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())



