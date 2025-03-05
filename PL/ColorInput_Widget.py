from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CI(QWidget):
    def __init__(self, default_color="#ffffff"):
        super().__init__()
        self.default_color = default_color
        self.choosed_color = self.default_color
        self.UI()
    def UI(self):
        # main layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        # color input
        self.color_input = QPushButton()
        self.color_input.setStyleSheet(f"background-color: {self.default_color};")
        self.main_layout.addWidget(self.color_input)
        # color input edit
        self.color_input_edit = QPushButton()
        self.color_input_edit.setToolTip("Click to change color")
        self.color_input_edit.setIcon(QIcon(QPixmap('Assets/Images/ColorBar2.png')))
        self.color_input_edit.setCursor(Qt.PointingHandCursor)
        self.color_input_edit.clicked.connect(self.color_input_edit_click)
        self.main_layout.addWidget(self.color_input_edit)
        # set cursor mode on action button
        self.color_input.setCursor(Qt.PointingHandCursor)
    def color_input_edit_click(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.color_input.setStyleSheet(f"background-color: {color.name()};")
            self.choosed_color = color.name()
    def GetColor(self):
        return self.choosed_color
    
            
    