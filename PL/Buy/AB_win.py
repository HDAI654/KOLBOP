from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
import datetime
import winsound
from PL.PSTW import PSTW
from PL.SSTW import SSTW
from PL.SPSTW import SPSTW
from PyQt5.QtTextToSpeech import *

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))

class ABW(QMainWindow):
    
    def __init__(self, cf):
        super().__init__()
        self.__cf = cf
        self.UI()
        self.fields_page_UI()
    
    def UI(self):
        # the main notebook
        self.notebook = QTabWidget()
        self.notebook.setTabPosition(QTabWidget.South)
        self.notebook.setDocumentMode(True)
        self.setCentralWidget(self.notebook)

        # add three page to notebook
        self.fields_page = QMainWindow()
        self.products_page = PSTW("Buy")
        self.services_page = SSTW()
        self.suppliers_page = SPSTW()

        self.notebook.addTab(self.fields_page, "Fields")
        self.notebook.addTab(self.products_page, "Products")
        self.notebook.addTab(self.services_page, "Services")
        self.notebook.addTab(self.suppliers_page, "Suppliers")
        

    def fields_page_UI(self):
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a new widget and set the layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignTop)


        # Set the widget as the scroll area widget
        scroll_area.setWidget(self.main_widget)
        
        # Set the scroll area as the page
        self.fields_page.setCentralWidget(scroll_area)

        
        # Date Time ,  Entry  and labels
        v = str(datetime.date.today()).split("-")
        self.date_time_label = QDateEdit(date=QDate(int(v[0]), int(v[1]), int(v[2])))
        df = PRR.DF()
        self.date_time_label.setDisplayFormat(df)
        self.tp = QLabel("Total Price")
        self.tp_LE = QLineEdit()
        self.calc_tp_btn = QPushButton("Calculate Total Price")
        self.calc_tp_btn.clicked.connect(self.calc_fast)
        

        # Info Button as label 
        self.info = QPushButton("Add Buy")
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
        self.main_layout.addWidget(self.tp)
        self.main_layout.addWidget(self.tp_LE)
        self.main_layout.addWidget(self.calc_tp_btn)
        self.main_layout.addWidget(self.date_time_label)
        self.main_layout.addWidget(self.submit_button)
        
    def calc_fast(self):
        pr = self.products_page.GetData()
        sc = self.services_page.GetData()
        tp = 0
        for p in pr:
            tp += int(p[3])*int(p[4])
        for s in sc:
            tp += int(s[3])
        self.tp_LE.setText(f"{tp}")
    
    def Submit(self):
        # Get the values from the line edits
        tp = "".join(self.tp_LE.text().strip().split(' '))
        date_time = self.date_time_label.text()

        # Add to DataBase
        if tp.strip() == "" or date_time.strip() == "" or self.products_page.GetData() == []:
            winsound.MessageBeep()
            text_to_speech("Please fill all the fields")
        else:
            # Buy
            PRR.Insert("Buy", "TotalPrice, Date", f"{tp}, '{date_time}'")
            bI = int(PRR.Select("ID", "Buy", "true")[-1][0])

            # Product
            for p in self.products_page.GetData():
                PRR.Insert("Buy_Products", "PC, Name, Unit, Amount, Price, BC", f"{p[0]}, '{p[1]}', '{p[2]}', '{p[3]}', {p[4]}, {bI}")

            # Sevice
            for s in self.services_page.GetData():
                PRR.Insert("Buy_Services", "BC, SVC, Explanation, Unit, Price", f"{bI}, {s[0]}, '{s[1]}', '{s[2]}', {s[3]}")

            # Suppliers
            for sp in self.suppliers_page.GetData():
                PRR.Insert("Buy_Suppliers", "BC, SC, Supplier_Name", f"{bI}, {sp[0]}, '{sp[1]}'")

            self.products_page.clear_table()
            self.services_page.clear_table()
            self.suppliers_page.clear_table()
            v = str(datetime.date.today()).split("-")
            self.date_time_label.setDate(QDate(int(v[0]), int(v[1]), int(v[2])))
            self.tp_LE.setText('')
            self.__cf()
