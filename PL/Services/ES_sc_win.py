from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
import datetime
import winsound
from PyQt5.QtTextToSpeech import *

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))


class ES_sc_W(QMainWindow):
    def __init__(self, id, cf):
        super().__init__()
        self.__id = id
        self.__cf = cf
        self.data = PRR.Select("*", "Services", f"ID = {str(self.__id)}")[0]
        self.UI()
    def UI(self):
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a new widget and set the layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # Set the widget as the scroll area widget
        scroll_area.setWidget(self.main_widget)
        
        # Set the scroll area as the page
        self.setCentralWidget(scroll_area)

        # Labels
        self.id_label = QLabel(F"ID :  {str(self.__id)}")
        self.exp_label = QLabel("Explanation:")
        self.unt_label = QLabel("Unit:")
        self.prc_label = QLabel("Price:")
        
        # Line Edits
        self.exp_line_edit = QLineEdit()
        self.exp_line_edit.setText(str(self.data[1]))
        self.unt_line_edit = QLineEdit()
        self.unt_line_edit.setText(str(self.data[2]))
        self.prc_line_edit = QLineEdit()
        self.prc_line_edit.setText(str(self.data[3]))
        self.prc_line_edit.setValidator(QIntValidator())


        # Info Button as label
        self.info = QPushButton("Edit Service")
        self.info.setStyleSheet("""
        QPushButton {
                    background-color: #cfa379ff;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #cfa379ff;
                    padding: 5px;
                    margin-bottom: 10px;
                }
        """)

        # Close Button
        self.close_button = QPushButton("Back")
        self.close_button.setShortcut("Ctrl+Q")
        self.close_button.setToolTip("Back (Ctrl+Q)")
        self.close_button.clicked.connect(self.__cf)
        self.close_button.setStyleSheet("""
        QPushButton {
                    background-color: #a0144f;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #a0144f;
                    padding: 5px;
                    margin-bottom: 10px;
                }
        QPushButton:hover {
                    background-color: #c81861;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #a0144f;
                    padding: 5px;
                }
        """)

        # Submit Button
        self.submit_button = QPushButton("Edit")
        self.submit_button.setShortcut("Ctrl+S")
        self.submit_button.setToolTip(" Save Data (Ctrl+S)")
        self.submit_button.clicked.connect(self.Submit)
        self.submit_button.setStyleSheet("margin-top: 10px;")

        # Add To Window
        self.main_layout.addWidget(self.info)
        self.main_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.id_label)
        self.main_layout.addWidget(self.exp_label)
        self.main_layout.addWidget(self.exp_line_edit)
        self.main_layout.addWidget(self.unt_label)
        self.main_layout.addWidget(self.unt_line_edit)
        self.main_layout.addWidget(self.prc_label)
        self.main_layout.addWidget(self.prc_line_edit)
        self.main_layout.addWidget(self.submit_button)


        # Add stretch to push everything to the top
        self.main_layout.addStretch()
    

    def Submit(self):
        # Get the values from the line edits
        exp = self.exp_line_edit.text()
        unt = self.unt_line_edit.text()
        prc = self.prc_line_edit.text()

        # Edit From DataBase
        if exp.strip() == "" or unt.strip() == "" or prc.strip() == "":
            winsound.MessageBeep()
            text_to_speech("Please fill all the fields")
        else:
            PRR.Update("Services", f"Explanation='{exp}', Unit='{unt}', Price={prc}", where=f"ID={self.data[0]}")
            self.__cf()