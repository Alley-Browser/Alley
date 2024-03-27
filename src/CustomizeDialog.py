from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QRadioButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class CustomizeDialog(QDialog):
    def __init__(self, parent=None):
        super(CustomizeDialog, self).__init__(parent)

        self.setWindowTitle('Appearance')
        self.setMinimumWidth(300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        self.dark_mode_radio = QRadioButton('Dark Mode')
        self.light_mode_radio = QRadioButton('Light Mode')
        self.default_radio = QRadioButton('Default')

        layout.addWidget(self.dark_mode_radio)
        layout.addWidget(self.light_mode_radio)
        layout.addWidget(self.default_radio)

        layout.addSpacing(15)  # Add spacing between color and theme sections

        # Button Box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Set fixed size for each button
        ok_button = button_box.button(QDialogButtonBox.Ok)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)

        button_width = 100 
        button_height = 34 
        button_width1 = 70  
        button_height1 = 34 
        ok_button.setFixedSize(button_width1, button_height1)
        cancel_button.setFixedSize(button_width, button_height)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

        # Connect radio buttons to change_color method
        self.dark_mode_radio.clicked.connect(lambda: self.change_color("dark"))
        self.light_mode_radio.clicked.connect(lambda: self.change_color("light"))
        self.default_radio.clicked.connect(lambda: self.change_color("default"))
        
        
        
    def change_color(self, mode):
        template = "background-color: {}; color: {};"
        if mode == "dark":
            style = template.format("#333333", "white")
        elif mode == "light":
            style = template.format("#F5F5F5", "black")
        else:
            style = ""
        self.parent().setStyleSheet(style)


