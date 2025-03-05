from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class HomeUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        # set an responsive image as window background
        self.setStyleSheet("background-image: url(Assets/Images/txt.png); background-repeat: no-repeat;background-position: center;")
        