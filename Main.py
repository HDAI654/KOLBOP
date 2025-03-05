from PL.main_window import MainWindow as App
from BLL.PublicRrep import PRR
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
from PyQt5.QtTextToSpeech import *

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))


class Register_AuthPage(QMainWindow):
    def __init__(self, rgs_callback, Back_func):
        super().__init__()
        self.rgs_callback = rgs_callback
        self.back_func = Back_func
        self.setStyleSheet(PRR.Style())
        self.StackUI()
    
    def StackUI(self):
        # create main layers
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)
        
        # Back Link
        self.back_link = QCommandLinkButton("Back To Login")
        self.back_link.clicked.connect(self.back_func)
        self.main_layout.addWidget(self.back_link)

        # UserName InputBoxe
        self.user_name = QLineEdit()
        self.user_name.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.user_name.setPlaceholderText("Username")
        self.user_name.setEchoMode(QLineEdit.Normal)
        self.main_layout.addWidget(self.user_name)

        # Password InputBox
        W = QWidget()
        HL = QHBoxLayout()
        W.setLayout(HL)
        self.password = QLineEdit()
        self.password.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        HL.addWidget(self.password)
        # show/hide button for password
        self.show_password_button = QPushButton("Show")
        self.show_password_button.setStyleSheet("""
                                                QPushButton {
                                                    background-color: #2196F3;
                                                    border-radius: 4px;
                                                    color: #ffffff;
                                                    margin-top: 1px;
                                                    padding: 8px 16px;
                                                    font-size: 14px;
                                                    font-weight: bold;
                                                }
                                                QPushButton:hover {
                                                    background-color: #1976D2;
                                                }
                                                QPushButton:pressed {
                                                    background-color: #0D47A1;
                                                }
                                            
                                            """)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        HL.addWidget(self.show_password_button)
        self.main_layout.addWidget(W)
        
        # license Input
        self.license = QLineEdit()
        self.license.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.license.setPlaceholderText("License")
        self.license.setEchoMode(QLineEdit.Normal)
        self.main_layout.addWidget(self.license)

        # Login Button and auth label
        self.auth_label = QLabel("")
        self.auth_label.setStyleSheet("""
                                      QLabel {
                                            font-size: 14px;
                                            color: #d71111;
                                            margin-top: 10px;
                                            margin-bottom: 1px;
                                        }
                                    """)
        self.main_layout.addWidget(self.auth_label)

        self.rgs_button = QPushButton("Register")
        self.rgs_button.setStyleSheet("""
        QPushButton {
            background-color: #2196F3;
            border-radius: 4px;
            color: #ffffff;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: bold;
            margin-top:2px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
    """)
        self.rgs_button.clicked.connect(self.rgs)
        self.main_layout.addWidget(self.rgs_button)

    def rgs(self):
        username = str(self.user_name.text()).strip()
        password = str(self.password.text()).strip()
        tkn = str(self.license.text()).strip()
        if len(username) >= 8 and len(password) >= 8 and len(tkn) != 0:
            url = f"http://127.0.0.1:8000/auth/reg/{username}/{password}/{tkn}"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            res = int(response.text)
            if res == 1:
                self.rgs_callback()
            if res == 0:
                self.auth_label.setText("This username has already been used")
                # clear inputboxes
                self.user_name.clear()
                self.password.clear()
                self.license.clear()
                self.password.setEchoMode(QLineEdit.Password)
                self.show_password_button.setText("Show")
            if res == 2:
                self.auth_label.setText("The license is not correct")
                # clear inputboxes
                self.user_name.clear()
                self.password.clear()
                self.license.clear()
                self.password.setEchoMode(QLineEdit.Password)
                self.show_password_button.setText("Show") 
        else:
            self.auth_label.setText("Password and username must be more than 7 characters")
            # clear inputboxes
            self.user_name.clear()
            self.password.clear()
            self.license.clear()
            self.password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")

    def toggle_password_visibility(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")

    def Clear(self):
        self.user_name.clear()
        self.password.clear()
        self.license.clear()
        self.password.setEchoMode(QLineEdit.Password)
        self.show_password_button.setText("Show")
        self.auth_label.setText("")

    def return_username(self):
        return str(self.user_name.text()).strip()

class Login_AuthPage(QMainWindow):
    def __init__(self, login_callback, gotorgs_func):
        super().__init__()
        self.login_callback = login_callback
        self.Rgs_func = gotorgs_func
        self.setStyleSheet(PRR.Style())
        self.UI()
    
    def UI(self):
        # create main layers
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        # UserName InputBoxe
        self.user_name = QLineEdit()
        self.user_name.setPlaceholderText("Username")
        self.user_name.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.user_name.setEchoMode(QLineEdit.Normal)
        self.main_layout.addWidget(self.user_name)

        # Password InputBox
        W = QWidget()
        HL = QHBoxLayout()
        W.setLayout(HL)
        self.password = QLineEdit()
        self.password.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        HL.addWidget(self.password)
        
        
        # show/hide button for password
        self.show_password_button = QPushButton("Show")
        self.show_password_button.setStyleSheet("""
                                                QPushButton {
                                                    background-color: #2196F3;
                                                    border-radius: 4px;
                                                    color: #ffffff;
                                                    margin-top: 1px;
                                                    padding: 8px 16px;
                                                    font-size: 14px;
                                                    font-weight: bold;
                                                }
                                                QPushButton:hover {
                                                    background-color: #1976D2;
                                                }
                                                QPushButton:pressed {
                                                    background-color: #0D47A1;
                                                }
                                            
                                            """)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        HL.addWidget(self.show_password_button)
        self.main_layout.addWidget(W)
        
        # Keep me logged in checkbox
        self.keep_me_logged_in = QCheckBox("Keep me logged in")
        self.main_layout.addWidget(self.keep_me_logged_in)
        

        # auth label
        self.auth_label = QLabel("")
        self.auth_label.setStyleSheet("""
                                      QLabel {
                                            font-size: 14px;
                                            color: #d71111;
                                            margin-top: 10px;
                                            margin-bottom: 1px;
                                        }
                                    """)
        self.main_layout.addWidget(self.auth_label)
        
        # Register Link
        self.link = QCommandLinkButton("Register")
        self.link.clicked.connect(self.Rgs_func)
        self.main_layout.addWidget(self.link)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
        QPushButton {
            background-color: #2196F3;
            border-radius: 4px;
            color: #ffffff;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: bold;
            margin-top:2px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
    """)
        self.login_button.clicked.connect(self.login)
        self.main_layout.addWidget(self.login_button)

    def login(self):
        username = str(self.user_name.text()).strip()
        password = str(self.password.text()).strip()
        if len(username) >= 8 and len(password) >= 8:
            url = f"http://127.0.0.1:8000/auth/login/{username}/{password}"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            res = int(response.text)
            if res == 1:
                if self.keep_me_logged_in.isChecked():
                    PRR.set_KL(1, username, password)
                else:
                    PRR.set_KL(0, "", "")
                           
                self.login_callback()
            if res == 0:
                self.auth_label.setText("Invalid username or password")
                # clear inputboxes
                self.user_name.clear()
                self.password.clear()
                self.password.setEchoMode(QLineEdit.Password)
                self.show_password_button.setText("Show")
        else:
            self.auth_label.setText("Password and username must be more than 7 characters")
            # clear inputboxes
            self.user_name.clear()
            self.password.clear()
            self.password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")

    def toggle_password_visibility(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")

    def Clear(self):
        self.user_name.clear()
        self.password.clear()
        self.password.setEchoMode(QLineEdit.Password)
        self.show_password_button.setText("Show")
        self.auth_label.setText("")

    def return_username(self):
        return str(self.user_name.text()).strip()

class LockPage(QMainWindow):
    def __init__(self, open_func):
        super().__init__()
        self.open_func = open_func
        self.setStyleSheet(PRR.Style())
        self.UI()

    def UI(self):
        # create main layers
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        # Password InputBox
        W = QWidget()
        HL = QHBoxLayout()
        W.setLayout(HL)
        self.password = QLineEdit()
        self.password.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        HL.addWidget(self.password)
        
        # show/hide button for password
        self.show_password_button = QPushButton("Show")
        self.show_password_button.setStyleSheet("""
                                                QPushButton {
                                                    background-color: #2196F3;
                                                    border-radius: 4px;
                                                    color: #ffffff;
                                                    margin-top: 1px;
                                                    padding: 8px 16px;
                                                    font-size: 14px;
                                                    font-weight: bold;
                                                }
                                                QPushButton:hover {
                                                    background-color: #1976D2;
                                                }
                                                QPushButton:pressed {
                                                    background-color: #0D47A1;
                                                }
                                            
                                            """)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        HL.addWidget(self.show_password_button)
        self.main_layout.addWidget(W)
        
        # Label
        self.auth_label = QLabel("")
        self.auth_label.setStyleSheet("color: #dc3545;")
        self.main_layout.addWidget(self.auth_label)
        
        
        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.main_layout.addWidget(self.submit_button)
        
    def toggle_password_visibility(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")

    def submit(self):
        password = self.password.text()
        try:
            real_password = PRR.get_lock_info()
            if real_password:
                if real_password[0] == "True":
                    if password == real_password[1]:
                        self.auth_label.setText("")
                        self.password.clear()
                        self.password.setEchoMode(QLineEdit.Password)
                        self.show_password_button.setText("Show")
                        self.open_func()
                    
                    else:
                        self.password.clear()
                        self.auth_label.setText("Password is incorrect")
                        self.password.setEchoMode(QLineEdit.Password)
                        self.show_password_button.setText("Show")
                else:
                    self.auth_label.setText("")
                    self.password.clear()
                    self.password.setEchoMode(QLineEdit.Password)
                    self.show_password_button.setText("Show")
                    self.open_func()
                    
            
            else:
                self.password.clear()
                self.auth_label.setText("")
                self.password.setEchoMode(QLineEdit.Password)
                self.show_password_button.setText("Show")
                self.open_func()
        
        except:
            self.password.clear()
            self.auth_label.setText("")
            self.password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")
            text_to_speech('Opennig faild')
                  
class NoConnectionPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #000000;')
        self.UI()

    def UI(self):
        # create main layers
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)
        
        # Label
        self.label = QLabel("")
        self.label.setPixmap(QPixmap("Assets/Images/Internet_Error.png"))
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        
        

#
class Main_(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.loggined = False
        
        #  این کد الان نیاز نبود کار کنه چود کد سایت و ای پی آی ها روی سرور قرار ندارد و برای دسترسی به آنها نیاز به اینترنت نیست و از روی سیستم این کد ها اجرا میشه
        #self.connection = self.check_internet_connection()
        self.connection = True
        
        self.try_log()
        
        
        
        self.setStyleSheet(PRR.Style())
        self.StackUI()
    
        # set window icon
        self.setWindowIcon(QIcon("Assets/Images/Icon.png"))
    
    def try_log(self):
        if PRR.KL()[0] == 1:
            username = str(PRR.KL()[1]).strip()
            password = str(PRR.KL()[2]).strip()
            self.__username = username
            self.loggined = True
        else:
            pass
        
    def check_internet_connection(self, url="http://www.google.com", timeout=3):
        try:
            requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False
    
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
        self.auth_frame = Login_AuthPage(self.lf, self.GoToRegisterPage)
        self.rgs_frame = Register_AuthPage(self.rf, self.BackToLogin)
        self.main_page_frame = App(lock_func=self.LockFunc, logout_func=self.Logout, conn=self.connection)
        self.lock_page = LockPage(self.OpenFunc)
        self.net_error_frame = NoConnectionPage()

        # Add Frames to Stacked Widget
        self.stacked_widget.addWidget(self.auth_frame)
        self.stacked_widget.addWidget(self.rgs_frame)
        self.stacked_widget.addWidget(self.main_page_frame)
        self.stacked_widget.addWidget(self.lock_page)
        self.stacked_widget.addWidget(self.net_error_frame)
            
            
            
        self.login_keep()
        
        
    
    # Login Finished
    def lf(self):
        self.stacked_widget.setCurrentIndex(2)
        # set window title
        self.setWindowTitle("KOLBOP")
        self.showMaximized()
        self.main_page_frame.usr_change(self.auth_frame.return_username())
        self.auth_frame.Clear()
        self.rgs_frame.Clear()
    
    # Register Finished         
    def rf(self):
        self.stacked_widget.setCurrentIndex(2)
        # set window title
        self.setWindowTitle("KOLBOP")
        self.showMaximized()
        self.main_page_frame.usr_change(self.rgs_frame.return_username())
        self.auth_frame.Clear()
        self.rgs_frame.Clear()
        
    def GoToRegisterPage(self):
        self.stacked_widget.setCurrentIndex(1)
        # set window title
        self.setWindowTitle("KOLBOP - Register")
    
    def BackToLogin(self):
        self.stacked_widget.setCurrentIndex(0)
        # set window title
        self.setWindowTitle("KOLBOP - Login")
            
    def LockFunc(self): 
        self.showNormal()
        self.stacked_widget.setCurrentIndex(3)
        # set window title
        self.setWindowTitle("KOLBOP - Lock")
        self.resize(100, 200)
        

    def login_keep(self):
        if self.loggined:
            if not self.CheckLock():
                
                self.stacked_widget.setCurrentIndex(2)
                # set window title
                self.setWindowTitle("KOLBOP")
                self.showMaximized()
                self.main_page_frame.usr_change(str(self.__username))
                self.main_page_frame.lock_status(False)
                
            else:
                self.main_page_frame.usr_change(str(self.__username))
                self.LockFunc()
        
        else:
            if self.connection == True:
                self.stacked_widget.setCurrentIndex(0)
                self.setWindowTitle("KOLBOP - Login")
                self.resize(350, 450)
                self.showNormal()
            
            else:
                self.stacked_widget.setCurrentIndex(4)
                self.setWindowTitle("KOLBOP - No Connection")
                self.resize(100, 100)
                self.showNormal()
            
    def CheckLock(self):
        li = PRR.get_lock_info()
        if li:
            if li[0] == 'True':
                return True
                
            elif li[1] == 'False':
                return False
            
            else:
                return False
        
        else:
            return False
                   
    def OpenFunc(self):
        self.showMaximized()
        self.stacked_widget.setCurrentIndex(2)
        self.setWindowTitle("KOLBOP")
              
    def Logout(self):
        self.showNormal()
        PRR.set_KL(0, "", "")
        self.stacked_widget.setCurrentIndex(0)
        self.resize(350, 450)
        # set window title
        self.setWindowTitle("KOLBOP - Login")
        
              
        
        
