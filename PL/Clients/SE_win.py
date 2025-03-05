from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
import datetime

class SEW(QMainWindow):
    def __init__(self, cf, id):
        super().__init__()
        self.__cf = cf
        self.__id = id
        self.UI()
        self.Fill()
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
        self.company_name_label = QLabel("Company Name/Name:")
        self.address_label = QLabel("Address:")
        self.contact_name_label = QLabel("Contact Name:")
        self.phone_label = QLabel("Phone:")
        self.mobile_label = QLabel("Mobile:")
        self.email_label = QLabel("Email:")
        self.postal_code_label = QLabel("Postal Code:")
        self.economic_number_label = QLabel("Economic Number:")
        self.date_time_lbl = QLabel("Date :")

        self.date_time_label = QDateEdit()

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
        self.info = QPushButton("Edit Client")
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
    def Fill(self):
        # Get the data from the database
        data = PRR.Select("*", "Clients", f"ID={int(self.__id)}")
        if data:
            self.company_name_line_edit.setText(data[0][1])
            self.address_line_edit.setText(data[0][2])
            self.contact_name_line_edit.setText(data[0][3])
            self.phone_line_edit.setText(str(data[0][4]))
            self.mobile_line_edit.setText(str(data[0][5]))
            self.email_line_edit.setText(data[0][6])
            self.postal_code_line_edit.setText(str(data[0][7]))
            self.economic_number_line_edit.setText(str(data[0][8]))
            # Set the date and time
            self.date_time_label.setDisplayFormat(PRR.DF())
            self.date_time_label.setDate(QDate.fromString(data[0][9], PRR.DF()))
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

        # Update data
        PRR.Update("Clients", f"CompanyName='{company_name}', Address='{address}', ContactName='{contact_name}', Phone={phone}, Mobile={mobile}, Email='{email}', PS={postal_code}, EN={economic_number}, Date='{date_time}'", f"ID={int(self.__id)}")
        self.__cf()



