from PyQt6.QtWidgets import *


class MyLabel(QLabel):
    def __init__(self, window, text, font, setX, setY, width, height):
        super().__init__(window)
        self.setText(str(text))
        self.setFont(font)
        self.setGeometry(setX, setY, width, height)