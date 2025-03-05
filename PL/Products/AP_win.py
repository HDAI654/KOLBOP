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

class APW(QMainWindow):
    def __init__(self, cf):
        super().__init__()
        self.__cf = cf
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
        self.name_label = QLabel("Name:")
        self.sc_label = QLabel("Supplier:")
        self.unit_label = QLabel("Unit")
        self.amount_label = QLabel("Amount:")
        self.bp_label = QLabel("BuyPrice:")
        self.sp_label = QLabel("SalePrice:")

        # Line Edits
        self.name_input = QLineEdit()

        self.sc_input = QComboBox()
        sc_data = PRR.Select("ID, CompanyName", "Suppliers", "true")
        sc_data = [str(sc[0])+' - '+str(sc[1]) for sc in sc_data]
        self.sc_input.addItems(sc_data)
        

        self.unit_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.amount_input.setValidator(QIntValidator())
        self.bp_input = QLineEdit()
        self.bp_input.setValidator(QIntValidator())
        self.sp_input = QLineEdit()
        self.sp_input.setValidator(QIntValidator())


        # Info Button as label
        self.info = QPushButton("Add Prodcut")
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
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.Submit)
        self.submit_button.setStyleSheet("margin-top: 10px;")

        # Add To Window
        self.main_layout.addWidget(self.info)
        self.main_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.name_input)
        self.main_layout.addWidget(self.sc_label)
        self.main_layout.addWidget(self.sc_input)
        self.main_layout.addWidget(self.unit_label)
        self.main_layout.addWidget(self.unit_input)
        self.main_layout.addWidget(self.amount_label)
        self.main_layout.addWidget(self.amount_input)
        self.main_layout.addWidget(self.bp_label)
        self.main_layout.addWidget(self.bp_input)
        self.main_layout.addWidget(self.sp_label)
        self.main_layout.addWidget(self.sp_input)
        self.main_layout.addWidget(self.submit_button)


        # Add stretch to push everything to the top
        self.main_layout.addStretch()

    def Submit(self):
        # Get the values from the line edits
        name = self.name_input.text()
        sc = str(self.sc_input.currentText().split("-")[0]).strip()
        unit = self.unit_input.text()
        amount = self.amount_input.text()
        bp = self.bp_input.text()
        sp = self.sp_input.text()


        # Add to DataBase
        if name.strip() == "" and sc.strip() == "" and unit.strip() == "" and amount.strip() == "" and bp.strip() == "" and sp.strip() == "":
            winsound.MessageBeep()
            text_to_speech("Please fill all the fields")
        else:
            PRR.Insert("Products", "Name, SC, Unit, Amount, BuyPrice, SalePrice", f"'{name}', {sc}, '{unit}', {amount}, {bp}, {sp}")
            self.__cf()


