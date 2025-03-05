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

class ACW(QMainWindow):
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
        self.company_name_label = QLabel("Company Name/Name:")
        self.address_label = QLabel("Address:")
        self.contact_name_label = QLabel("Contact Name:")
        self.phone_label = QLabel("Phone:")
        self.mobile_label = QLabel("Mobile:")
        self.email_label = QLabel("Email:")
        self.postal_code_label = QLabel("Postal Code:")
        self.economic_number_label = QLabel("Economic Number:")
        self.date_time_lbl = QLabel("Date :")

        v = str(datetime.date.today()).split("-")
        self.date_time_label = QDateEdit(date=QDate(int(v[0]), int(v[1]), int(v[2])))
        df = PRR.DF()
        self.date_time_label.setDisplayFormat(df)

        # Line Edits
        self.company_name_line_edit = QLineEdit()
        self.address_line_edit = QLineEdit()
        self.contact_name_line_edit = QLineEdit()

        self.phone_line_edit = QLineEdit()
        self.phone_line_edit.setValidator(QIntValidator())

        self.mobile_line_edit = QLineEdit()
        self.mobile_line_edit.setValidator(QIntValidator())

        self.email_line_edit = QLineEdit()
        self.email_line_edit.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.email_line_edit.setPlaceholderText("example@example.com")

        self.postal_code_line_edit = QLineEdit()
        self.postal_code_line_edit.setValidator(QIntValidator())

        self.economic_number_line_edit = QLineEdit()
        self.economic_number_line_edit.setValidator(QIntValidator())

        # Info Button as label
        self.info = QPushButton("Add Client")
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
        self.main_layout.addWidget(self.company_name_label)
        self.main_layout.addWidget(self.company_name_line_edit)
        self.main_layout.addWidget(self.address_label)
        self.main_layout.addWidget(self.address_line_edit)
        self.main_layout.addWidget(self.contact_name_label)
        self.main_layout.addWidget(self.contact_name_line_edit)
        self.main_layout.addWidget(self.phone_label)
        self.main_layout.addWidget(self.phone_line_edit)
        self.main_layout.addWidget(self.mobile_label)
        self.main_layout.addWidget(self.mobile_line_edit)
        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.email_line_edit)
        self.main_layout.addWidget(self.postal_code_label)
        self.main_layout.addWidget(self.postal_code_line_edit)
        self.main_layout.addWidget(self.economic_number_label)
        self.main_layout.addWidget(self.economic_number_line_edit)
        self.main_layout.addWidget(self.date_time_lbl)
        self.main_layout.addWidget(self.date_time_label)
        self.main_layout.addWidget(self.submit_button)


        # Add stretch to push everything to the top
        self.main_layout.addStretch()

    def Submit(self):
        # Get the values from the line edits
        company_name = self.company_name_line_edit.text()
        address = self.address_line_edit.text()
        contact_name = self.contact_name_line_edit.text()
        phone = self.phone_line_edit.text()
        mobile = self.mobile_line_edit.text()
        email = self.email_line_edit.text()
        postal_code = self.postal_code_line_edit.text()
        economic_number = self.economic_number_line_edit.text()
        date_time = self.date_time_label.text()

        # Add to DataBase
        if company_name.strip() == "" or address.strip() == "" or contact_name.strip() == "" or phone.strip() == "" or mobile.strip() == "" or email.strip() == "" or postal_code.strip() == "" or economic_number.strip() == "" or date_time.strip() == "":
            winsound.MessageBeep()
            text_to_speech("Please fill all the fields")
        else:
            PRR.Insert("Clients", "CompanyName, Address, ContactName, Phone, Mobile, Email, PS, EN, Date", f"'{company_name}', '{address}', '{contact_name}', {phone}, {mobile}, '{email}', {postal_code}, {economic_number}, '{date_time}'")
            self.__cf()



