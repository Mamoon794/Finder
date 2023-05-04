from PyQt6.QtWidgets import *
from PyQt6 import QtCore


class MyLabel(QLabel):
    def __init__(self, window, text, font, setX, setY, width, height):
        super().__init__(window)
        self.setText(str(text))
        self.setFont(font)
        self.setGeometry(setX, setY, width, height)


class MyButton(QPushButton):
    def __init__(self, window, name, setX, setY, width, height):
        super().__init__(window)
        self.setText(name)
        self.setGeometry(setX, setY, width, height)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)