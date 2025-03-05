from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
from PL.Clients.Clients import CW
from PL.Suppliers.Suppliers import SW as SPW
from PL.Products.Products import PW
from PL.Buy.Buy import BW
from PL.Sale.Sale import SW
from PL.ML.Main import ML_win
from PL.BackUp.backup import backup_win
from PL.CustomDashboard.CDMW import IM_win
from PL.HomePage import HomeUI
from PL.Report.RMW import ReportUI
from PL.HelpChat.HC_win import HC_win
from PL.Chart_Page import CP
from PL.Services.Services import ScW
from PL.Setting.Setting_win import Setting


class MainWindow(QMainWindow):
    
    def __init__(self, lock_func, logout_func, conn=True):
        super().__init__()
        self.lock_func = lock_func
        self.conn = conn
        self.logout_func = logout_func
        self.UI()
        self.StackUI()

    def UI(self):
        # Main ToolBar
        self.toolbar = QToolBar("Main ToolBar")
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addToolBar(self.toolbar)
        
        # UserName Label and Icon
        self.usr_icon = QAction(QIcon(QPixmap("Assets/Images/User.png")), "User",self)
        self.usr_lbl = QLabel("")
        self.toolbar.addAction(self.usr_icon)
        self.toolbar.addWidget(self.usr_lbl)
        if self.usr_lbl.text() == "":
            self.usr_icon.setText("Not Logged In")
            self.usr_icon.setEnabled(False)
        self.toolbar.addSeparator()

        # Actions
        self.client_action = QAction(QIcon(QPixmap("Assets/Images/Clients.png")), "Clients", self)
        self.supplier_action = QAction(QIcon(QPixmap("Assets/Images/Suppliers.png")), "Suppliers", self)
        self.product_action = QAction(QIcon(QPixmap("Assets/Images/Products.png")), "Products", self)
        self.service_action = QAction(QIcon(QPixmap("Assets/Images/Services.png")), "Services", self)
        self.buy_action = QAction(QIcon(QPixmap("Assets/Images/buy.png")), "Buy", self)
        self.sale_action = QAction(QIcon(QPixmap("Assets/Images/Sale2.png")), "Sale", self)
        self.ML_action = QAction(QIcon(QPixmap("Assets/Images/BS.png")), "My Business Status", self)
        self.net_server_action = QAction(QIcon(QPixmap("Assets/Images/Server.png")), "Server Data", self)
        self.custom_data_action = QAction(QIcon(QPixmap("Assets/Images/CustomData.png")), "Custom Data", self)
        self.home_action = QAction(QIcon(QPixmap("Assets/Images/Home.png")), "Home",self)
        self.report_action = QAction(QIcon(QPixmap("Assets/Images/Reports.png")), "Reports", self)
        self.lock_action = QAction(QIcon(QPixmap("Assets/Images/Lock.png")), "Lock (Ctrl+L)", self)
        self.lock_action.setShortcut("Ctrl+L")
        self.lock_action.triggered.connect(self.lock_func)
        self.help_chat_action = QAction(QIcon(QPixmap("Assets/Images/HelpChat.png")), "Help Chat", self)
        self.chart_action = QAction(QIcon(QPixmap("Assets/Images/Chart2.png")), "Create Chart", self)
        self.setting_action = QAction(QIcon(QPixmap("Assets/Images/Setting.png")), "Setting", self)
        
        self.toolbar.addActions([self.home_action, self.lock_action, self.client_action, self.supplier_action, self.product_action, self.service_action,  self.buy_action, self.sale_action, self.ML_action, self.net_server_action, self.custom_data_action, self.report_action, self.help_chat_action, self.chart_action, self.setting_action])
        if self.conn == False:
            self.net_server_action.setEnabled(False)
            self.net_server_action.setText("Server Data (No Connection)")
            
    
    def StackUI(self):
        # create main layers
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Create Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create Frames
        self.clients_frame = CW()
        self.suppliers_frame = SPW()
        self.product_frame = PW()
        self.buy_frame = BW()
        self.sale_frame = SW()
        self.ML_frame = ML_win()
        self.net_server_frame = backup_win()
        self.custom_data_frame = IM_win()
        self.home_frame = HomeUI()
        self.report_frame = ReportUI() 
        self.help_chat_frame = HC_win()
        #self.help_chat_frame = QMainWindow()
        #self.addToolBar(self.help_chat_frame.Xen())
        self.chart_frame = CP()
        self.service_frame = ScW()
        self.setting_frame = Setting(self.reset_func, self.lock_func, self.conn, self.logout_func, self.lock_status)

        # Add Frames to Stacked Widget
        self.stacked_widget.addWidget(self.clients_frame)
        self.stacked_widget.addWidget(self.suppliers_frame)
        self.stacked_widget.addWidget(self.product_frame)
        self.stacked_widget.addWidget(self.buy_frame)
        self.stacked_widget.addWidget(self.sale_frame)
        self.stacked_widget.addWidget(self.ML_frame)
        self.stacked_widget.addWidget(self.net_server_frame)
        self.stacked_widget.addWidget(self.custom_data_frame)
        self.stacked_widget.addWidget(self.home_frame)
        self.stacked_widget.addWidget(self.report_frame)
        self.stacked_widget.addWidget(self.help_chat_frame)
        self.stacked_widget.addWidget(self.chart_frame)
        self.stacked_widget.addWidget(self.service_frame)
        self.stacked_widget.addWidget(self.setting_frame)




        # Connect Buttons to Stacked Widget
        self.client_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.supplier_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.product_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.buy_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.sale_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.ML_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.net_server_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(6))
        self.custom_data_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(7))
        self.home_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(8))
        self.report_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(9))
        self.help_chat_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(10))
        self.chart_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(11))
        self.service_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(12))
        self.setting_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(13))
        
        
        
        # Set the current page to the Home Page
        self.stacked_widget.setCurrentIndex(8)
   
    def usr_change(self, text):
        self.usr_lbl.setText(str(text))
        self.usr_icon.setEnabled(True)
        self.usr_icon.setText("User")
        
        self.setting_frame.user_chng(str(text))
        self.net_server_frame.upload_page.username = str(text)
        self.net_server_frame.load_page.username = str(text)

    def reset_func(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                attr.deleteLater()
                
        
        # Remake
        self.UI()
        self.StackUI()
        
        self.usr_change(PRR.KL()[1])
        

    def lock_status(self, status):
        self.lock_made = status
        self.lock_action.setEnabled(status)
        if status == False:
            self.lock_action.setText(f"No Password saved to lock app")
        else:
            self.lock_action.setText(f"Lock (Ctrl+L)")