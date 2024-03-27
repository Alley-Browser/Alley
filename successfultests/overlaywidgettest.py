"""
Unit tests for OverlayWidget.

Tests the behavior of OverlayWidget during showEvent:
- Setting geometry to match parent 
- Setting transparent background
- Adding default border
"""
import unittest
from src.OverlayWidget import OverlayWidget
from PyQt5.QtWidgets import QWidget, QApplication
class TestOverlayWidget(unittest.TestCase):

    def test_showEvent_sets_geometry(self):
        parent = QWidget()
        parent.setGeometry(100, 200, 300, 400)
        
        overlay = OverlayWidget(QWidget(), parent)
        overlay.showEvent(None)

        self.assertEqual(overlay.geometry(), parent.geometry())


class TestOverlayWidget(unittest.TestCase):

    def test_showEvent_sets_transparent_background(self):
        app = QApplication([])
        overlay = OverlayWidget(QWidget())
        overlay.showEvent(None)

        self.assertTrue(overlay.testAttribute(QApplication.WA_TranslucentBackground))


    def test_showEvent_sets_border(self):
        overlay = OverlayWidget(QWidget())
        overlay.showEvent(None)
        
        self.assertRegex(overlay.styleSheet(), "border: 1px solid black;")
