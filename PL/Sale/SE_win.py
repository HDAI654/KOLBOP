from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
import datetime
import winsound
from PL.PSTW import PSTW
from PL.SSTW import SSTW
from PL.CSTW import CSTW
from PyQt5.QtTextToSpeech import *

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))

class SES(QMainWindow):
    def __init__(self, cf, id):
        super().__init__()
        self.__cf = cf
        self.id = int(id)
        self.Data = self.data()
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
        self.products_page = PSTW("Sale", data=self.Data["Sale_Products"], Page_Name="Sale Products")
        self.services_page = SSTW(data=self.Data["Sale_Services"], Page_Name="Sale Services")
        self.suppliers_page = CSTW(data=self.Data["Sale_Clients"])

        self.notebook.addTab(self.fields_page, "Fields")
        self.notebook.addTab(self.products_page, "Products")
        self.notebook.addTab(self.services_page, "Services")
        self.notebook.addTab(self.suppliers_page, "Clients")

    def data(self):
        D = {"Sale":None,
            "Sale_Products":None,
            "Sale_Services":None,
            "Sale_Clients":None,
            }
        
        # Sale
        D["Sale"] =  PRR.Select("*", "Sale", f"ID={self.id}")[0]

        # Sale Products
        p = PRR.Select("PC, Name, Unit, Amount, Price", "Sale_products", f"SLC={self.id}")
        np = []
        for ap in p:
            np.append(list(ap))
        D["Sale_Products"] = np

        # Sale Services
        bsf = PRR.Select("*", "Sale_Services", f"SLC={self.id}")
        bs=[]
        for s in bsf:
            bsr = []
            # service code
            bsr.append(s[1])
            # explanation
            bsr.append(s[2])
            # unit
            bsr.append(s[3])
            # price
            bsr.append(s[4])
            bs.append(bsr)
        D["Sale_Services"] = bs

        # Sale Clients
        bspf = PRR.Select("*", "Sale_Clients", f"SLC={self.id}")
        bsp = []
        for sp in bspf:
            spr = []
            # client code
            spr.append(sp[1])
            # client name
            spr.append(sp[2])
            bsp.append(spr)
        D["Sale_Clients"] = bsp

        return D
          

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
        self.tp_LE.setText(str(self.Data["Sale"][1]))
        self.calc_tp_btn = QPushButton("Calculate Total Price")
        self.calc_tp_btn.clicked.connect(self.calc_fast)
        

        # Info Button as label 
        self.info = QPushButton("Show/Edit Sale")
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
        date_time = str(self.date_time_label.text())

        # Add to DataBase
        if tp.strip() == "" or date_time.strip() == "" or self.products_page.GetData() == []:
            winsound.MessageBeep()
            text_to_speech("Please fill all the fields")
        else:

            # Buy
            PRR.Update("Sale", f"TotalPrice={tp}, Date='{date_time}'",f"ID={self.id}")

            
            # Product
            #delete old
            PRR.Delete("Sale_Products", f"SLC={self.id}")
            #add new
            for p in self.products_page.GetData():
                PRR.Insert("Sale_Products", "PC, Name, Unit, Amount, Price, SLC", f"{p[0]}, '{p[1]}', '{p[2]}', '{p[3]}', {p[4]}, {self.id}")
            
            # Sevice
            #delete old
            PRR.Delete("Sale_Services", f"SLC={self.id}")
            #add new
            for s in self.services_page.GetData():
                PRR.Insert("Sale_Services", "SlC, SVC, Explanation, Unit, Price", f"{self.id}, {s[0]}, '{s[1]}', '{s[2]}', {s[3]}")

            # Clients
            #delete old
            PRR.Delete("Sale_Clients", f"SLC={self.id}")
            #add new
            for sp in self.suppliers_page.GetData():
                PRR.Insert("Sale_Clients", "SLC, CLC, Client_Name", f"{self.id}, {sp[0]}, '{sp[1]}'")

            self.products_page.clear_table()
            self.services_page.clear_table()
            self.suppliers_page.clear_table()
            self.__cf()



