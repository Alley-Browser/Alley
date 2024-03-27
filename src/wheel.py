import sys
import random
from math import cos, sin, radians
from PyQt5.QtCore import pyqtSignal, Qt, QPoint, QSize, QFile, QTextStream, QPropertyAnimation, QRectF, QSequentialAnimationGroup, QEvent, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QDesktopWidget, QLineEdit, QHBoxLayout, QTextEdit, QFileDialog, QGraphicsDropShadowEffect, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QIcon, QBrush, QLinearGradient, QPainterPath, QFont

class NotepadWidget(QWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Notepad")
        self.setGeometry(0, 0, 500, 600)
        self.center_on_screen()
        layout = QVBoxLayout()

        title_label = QLabel("Notepad")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #FFFFFF; padding: 10px; background-color: #303030;")
        layout.addWidget(title_label)

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("font-size: 16px; background-color: #252525; color: #FFFFFF; border: 2px solid #404040; padding: 10px;")
        layout.addWidget(self.text_edit)

        save_button = QPushButton("Save")
        save_button.setStyleSheet("font-size: 18px; background-color: #606060; color: #FFFFFF; border: none; padding: 10px;")
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)

        load_button = QPushButton("Load")
        load_button.setStyleSheet("font-size: 18px; background-color: #606060; color: #FFFFFF; border: none; padding: 10px;")
        load_button.clicked.connect(self.load_file)
        layout.addWidget(load_button)

        close_button = QPushButton("Close Notepad")
        close_button.setStyleSheet("font-size: 18px; background-color: #606060; color: #FFFFFF; border: none; padding: 10px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                text = self.text_edit.toPlainText()
                file.write(text)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                self.text_edit.setPlainText(text)

    def center_on_screen(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        center_point = screen_geometry.center() - QPoint(self.width() // 2, self.height() // 2)
        self.move(center_point)

class CalculatorWidget(QWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Calculator")
        self.setGeometry(0, 0, 300, 400)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 20px; background-color: #303030; color: #FFFFFF; border: none; padding: 10px;")
        layout.addWidget(self.display)

        buttons = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+")
        ]

        for row in buttons:
            button_row = QWidget()
            row_layout = QHBoxLayout(button_row)
            for text in row:
                button = QPushButton(text)
                button.setStyleSheet("font-size: 18px; background-color: #606060; color: #FFFFFF; border: none; padding: 10px;")
                button.clicked.connect(lambda _, text=text: self.on_button_click(text))
                row_layout.addWidget(button)
            layout.addWidget(button_row)

        close_button = QPushButton("Close Calculator")
        close_button.setStyleSheet("font-size: 16px; background-color: #C0C0C0; color: #000000; border: none; padding: 10px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)

    def on_button_click(self, text):
        if text == "=":
            try:
                result = eval(self.display.text())
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + text)

class SnakeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent) 
        self.setWindowTitle("Snake Game")
        self.snake = [(0, 0)]  # Initial position of the snake
        self.direction = Qt.Key_Right  # Initial direction of the snake
        self.food = self.generate_food()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(100)  # Set snake speed (milliseconds)
        self.score = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(30, 30, 30))  # Background color

        # Draw snake
        painter.setBrush(Qt.green)
        for segment in self.snake:
            painter.drawRect(segment[0] * 10, segment[1] * 10, 10, 10)

        # Draw food
        painter.setBrush(Qt.red)
        painter.drawRect(self.food[0] * 10, self.food[1] * 10, 10, 10)

        # Draw score
        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial', 12))
        painter.drawText(self.rect(), Qt.AlignTop | Qt.AlignRight, f"Score: {self.score}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up and self.direction != Qt.Key_Down:
            self.direction = Qt.Key_Up
        elif event.key() == Qt.Key_Down and self.direction != Qt.Key_Up:
            self.direction = Qt.Key_Down
        elif event.key() == Qt.Key_Left and self.direction != Qt.Key_Right:
            self.direction = Qt.Key_Left
        elif event.key() == Qt.Key_Right and self.direction != Qt.Key_Left:
            self.direction = Qt.Key_Right

    def move_snake(self):
        x, y = self.snake[0]
        if self.direction == Qt.Key_Up:
            y -= 1
        elif self.direction == Qt.Key_Down:
            y += 1
        elif self.direction == Qt.Key_Left:
            x -= 1
        elif self.direction == Qt.Key_Right:
            x += 1

        # Check collision with food
        if (x, y) == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.generate_food()
            self.score += 1

        # Check collision with boundaries
        if x < 0 or x >= self.width() / 10 or y < 0 or y >= self.height() / 10:
            self.game_over()
            return

        # Check collision with itself
        if (x, y) in self.snake[1:]:
            self.game_over()
            return

        # Move snake
        self.snake = [(x, y)] + self.snake[:-1]

        self.update()

    def generate_food(self):
        x = random.randint(0, (self.width() / 10) - 1)
        y = random.randint(0, (self.height() / 10) - 1)
        return x, y

    def game_over(self):
        self.timer.stop()
        print("Game Over")

class CustomOverlay(QWidget):
    closed = pyqtSignal()

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)  # Start with opacity 0 for smooth fade-in animation
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(500)  # Animation duration in milliseconds

        self.setFixedSize(500, 500)
        self.setupButtons()
        self.setupHomeButton()

    def setupButtons(self):
        self.buttons = []
        num_divisions = 7  # Updated for 7 features
        angle_step = 360 / num_divisions
        button_radius = 30
        for i in range(num_divisions):
            angle = i * angle_step
            if i == 0:
                button = QPushButton(self)
                calculator_icon = QIcon("Icons/calculator.svg")
                calculator_icon_actual_size = calculator_icon.actualSize(QSize(50, 50))  # Adjust icon size here
                button.setIcon(calculator_icon)
                button.setIconSize(calculator_icon_actual_size)
                button.setStyleSheet("background-color: none; border: none; padding: 0px;")
                button.clicked.connect(self.show_calculator)
                button.setToolTip("Calculator")
            elif i == 1:
                button= QPushButton(self)
                notes_icon = QIcon("Icons/notepad.svg")
                notes_icon_actual_size = notes_icon.actualSize(QSize(50, 50))  # Adjust icon size here
                button.setIcon(notes_icon)
                button.setIconSize(notes_icon_actual_size)
                button.setStyleSheet("background-color: none; border: none;")
                button.clicked.connect(self.show_notepad)
                button.setToolTip("Notepad")
            elif i == 2:
                # Add Feature 5
                button = QPushButton(self)
                feature5_icon = QIcon("Icons/screenwheeln.svg")  # Replace "feature5.png" with actual icon path
                feature5_icon_actual_size = feature5_icon.actualSize(QSize(50, 50))  # Adjust icon size here
                button.setIcon(feature5_icon)
                button.setIconSize(feature5_icon_actual_size)
                button.setStyleSheet("background-color: none; border: none; padding: 0px;")
                button.clicked.connect(self.main_window.start_recording)  # Connect to the function for feature 5
                button.setToolTip("Start Recording")
            elif i == 3:
                # Add Feature 6
                button = QPushButton(self)
                feature6_icon = QIcon("Icons/probot.svg")  # Replace "feature6.png" with actual icon path
                feature6_icon_actual_size = feature6_icon.actualSize(QSize(50, 50))  # Adjust icon size here
                button.setIcon(feature6_icon)
                button.setIconSize(feature6_icon_actual_size)
                button.setStyleSheet("background-color: none; border: none; padding: 0px;")
                button.clicked.connect(self.main_window.open_chatbot_overlay)  # Connect to the function for feature 6
                button.setToolTip("Chatbot")
            elif i == 4:
                # Add Feature 7
                button = QPushButton(self)
                feature7_icon = QIcon("Icons/screenshotn.svg")  # Replace "feature7.png" with actual icon path
                feature7_icon_actual_size = feature7_icon.actualSize(QSize(50, 50))  # Adjust icon size here
                button.setIcon(feature7_icon)
                button.setIconSize(feature7_icon_actual_size)
                button.setStyleSheet("background-color: none; border: none; padding: 0px;")
                button.clicked.connect(self.main_window.take_screenshot)# Connect to the function for feature 7
                button.setToolTip("Screenshot")
            elif i == 5:
                # Add Feature 8
                button = QPushButton(self)
                feature8_icon = QIcon("Icons/vault.svg")  # Replace "feature8.png" with actual icon path
                feature8_icon_actual_size = feature8_icon.actualSize(QSize(50, 50))  # Adjust icon size here
                button.setIcon(feature8_icon)
                button.setIconSize(feature8_icon_actual_size)
                button.setStyleSheet("background-color: none; border: none; padding: 0px;")
                button.clicked.connect(self.feature_8_function)  # Connect to the function for feature 8
                button.setToolTip("Feature 8")
            elif i == 6:
                # Add Feature 9
                button = QPushButton(self)
                feature9_icon = QIcon("Icons/gamep.svg")  # Replace "feature9.png" with actual icon path
                feature9_icon_actual_size = feature9_icon.actualSize(QSize(50, 50))  # Adjust icon size here
                button.setIcon(feature9_icon)
                button.setIconSize(feature9_icon_actual_size)
                button.setStyleSheet("background-color: none; border: none; padding: 0px;")
                button.clicked.connect(self.feature_9_function)  # Connect to the function for feature 9
                button.setToolTip("Snake Game")
            # Add other feature buttons similarly
            else:
                button = QPushButton('Feature {}'.format(i), self)
                button.setStyleSheet("background-color: none; border: none; padding: 0px;")

            button.setCursor(Qt.PointingHandCursor)
            shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
            button.setGraphicsEffect(shadow)
            button.installEventFilter(self)  # Install event filter to handle hover events
            self.buttons.append((button, angle, angle + angle_step / 2))

    def setupHomeButton(self):
        self.home_button = QPushButton(self)
        self.home_button.setIcon(QIcon("homewheel.png"))
        self.home_button.setIconSize(QSize(30, 30))  # Adjusted size
        self.home_button.setStyleSheet("background-color: #CCCCCC; border: none; border-radius: 15px;")

        self.home_button.setCursor(Qt.PointingHandCursor)
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        self.home_button.setGraphicsEffect(shadow)
        self.home_button.clicked.connect(self.close)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw gradient background
        gradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
        gradient.setColorAt(0, QColor("#000000"))  # Black
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(self.rect())

        # Draw a circle in the center
        center_circle_radius = 60  # Increased radius for the center circle background
        center_circle_center = self.rect().center()
        center_circle_rect = QRectF(center_circle_center.x() - center_circle_radius, center_circle_center.y() - center_circle_radius,
                                    2 * center_circle_radius, 2 * center_circle_radius)
        painter.setBrush(QColor("#000000"))  # Set color to black for the center circle
        painter.drawEllipse(center_circle_rect)

        # Position buttons inside each divided part
        for button, angle, _ in self.buttons:
            button_center = self.get_point_on_circle(self.rect().center(), self.rect().height() / 3, angle)
            button_radius = button.width() // 2
            button.setGeometry(button_center.x() - button_radius, button_center.y() - button_radius, 2 * button_radius, 2 * button_radius)

        # Position home button in the center
        home_button_radius = self.home_button.width() // 2
        self.home_button.setGeometry(self.rect().center().x() - home_button_radius, self.rect().center().y() - home_button_radius, 2 * home_button_radius, 2 * home_button_radius)

    def get_point_on_circle(self, center, radius, angle):
        x = center.x() + radius * cos(radians(angle))
        y = center.y() + radius * sin(radians(angle))
        return QPoint(int(x), int(y))

    def center_on_screen(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        center_point = screen_geometry.center() - QPoint(self.width() // 2, self.height() // 2)
        self.move(center_point)

    def animate(self, fade_in=True):
        if fade_in:
            self.animation.setStartValue(0.0)
            self.animation.setEndValue(0.95)
        else:
            self.animation.setStartValue(0.95)
            self.animation.setEndValue(0.0)
        self.animation.start()

    def show_calculator(self):
        self.calculator_widget = CalculatorWidget()
        self.calculator_widget.show()
        self.close()

    def show_notepad(self):
        self.notepad_widget = NotepadWidget()
        self.notepad_widget.show()
        self.close()

    def feature_5_function(self):
        # Implement functionality for Feature 5
        pass

    def feature_6_function(self):
                # Implement functionality for Feature 6
        pass

    def feature_7_function(self):
        # Implement functionality for Feature 7
        pass

    def feature_8_function(self):
        # Implement functionality for Feature 8
        pass

    def feature_9_function(self):
        self.snake_widget = SnakeWidget()
        self.snake_widget.show()
        self.close()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            for button, _, _ in self.buttons:
                if obj == button:
                    button.setToolTip(button.toolTip())  # Refresh tooltip to display the name on hover
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        self.animate(fade_in=True)

    def closeEvent(self, event):
        self.animate(fade_in=False)
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 800, 600)

        self.custom_overlay = CustomOverlay(self)
        self.setCentralWidget(self.custom_overlay)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
