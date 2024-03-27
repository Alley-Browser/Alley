import unittest
from src.MainWindow import MainWindow
from PyQt5.QtWidgets import QTabWidget
from src.MainWindow import MainWindow      
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QCloseEvent
# The MainWindow is initialized with the correct window title and icon.

app = QApplication([]) 

class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.window = MainWindow()

    def test_initialized_with_correct_title_and_icon(self):
        self.assertEqual(self.window.windowTitle(), 'Alley Browser')
        self.assertFalse(self.window.windowIcon().isNull())

    def test_has_qtabwidget_as_central_widget(self):
        self.assertIsInstance(self.window.centralWidget(), QTabWidget)

    def test_can_add_new_tabs_with_default_url(self):
        self.assertEqual(self.window.tabCount(), 1)
        self.assertEqual(self.window.tabText(0), 'Loading...')
        
        self.window.addNewTab()
        
        self.assertEqual(self.window.tabCount(), 2)


class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.window = MainWindow()

    def test_can_handle_closing_application(self):
        event = QCloseEvent()
        self.window.closeEvent(event)
        
        self.assertFalse(self.window.isVisible())


    def test_can_handle_closing_tab(self):
        self.window.addNewTab()
        self.assertEqual(self.window.tabCount(), 2)
        
        self.window.closeTab(0)
        self.assertEqual(self.window.tabCount(), 1)

    def test_can_add_new_tab_when_no_tabs(self):
        self.window.closeAllTabs()
        self.assertEqual(self.window.tabCount(), 0)

        self.window.addNewTab()
        self.assertEqual(self.window.tabCount(), 1)

    def test_initialized_with_correct_title_and_icon(self):
            from PyQt5.QtWidgets import QApplication
            app = QApplication([])
            window = MainWindow()
            assert window.windowTitle() == 'Alley Browser'
            assert window.windowIcon().isNull() == False

        # The MainWindow has a QTabWidget as its central widget.

    def test_has_qtabwidget_as_central_widget(self):
        from PyQt5.QtWidgets import QApplication
        app = QApplication([])
        window = MainWindow()
        assert isinstance(window.centralWidget(), QTabWidget)

    # The MainWindow can add new tabs with a default URL.

    def test_can_add_new_tabs_with_default_url(self):
            from PyQt5.QtWidgets import QApplication
            app = QApplication([])
            window = MainWindow()
            assert window.tabs.count() == 1
            assert window.tabs.tabText(0) == 'Loading...'

        # The MainWindow can handle closing the application.
    def test_can_handle_closing_application(self):
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtGui import QCloseEvent
            app = QApplication([])
            window = MainWindow()
            window.closeEvent(QCloseEvent())
            assert window.isVisible() == False

        # The MainWindow can handle closing a tab.
    def test_can_handle_closing_tab(self):
            from PyQt5.QtWidgets import QApplication
            app = QApplication([])
            window = MainWindow()
            window.add_tab()
            window.close_tab(0)
            assert window.tabs.count() == 1

            # The MainWindow can handle adding a new tab when there are no existing tabs.
    def test_can_handle_adding_new_tab_with_no_existing_tabs(self):
            from PyQt5.QtWidgets import QApplication
            app = QApplication([])
            window = MainWindow()
            window.add_tab()
            window.close_tab(0)
            window.add_tab()
            assert window.tabs.count() == 2       

if __name__ == '__main__':
    unittest.main()
    app.exec_()