from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTextToSpeech import *
from BLL.PublicRrep import PRR
import requests

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))

class Setting(QMainWindow):
    def __init__(self, reset_func, lock_func, conn, logout_func, lock_sts_func):
        super().__init__()
        self.reset_backfunc = reset_func
        self.username = None
        self.lock_func = lock_func
        self.conn = conn
        self.logout_func = logout_func
        self.lock_sts_func = lock_sts_func
        self.UI()
        self.ToolBar()
    
    def UI(self):
        pass
    
    def ToolBar(self):
        # Main ToolBar
        self.toolbar = QToolBar("Setting ToolBar")
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addToolBar(self.toolbar)
        
        self.reset_action = QAction(QIcon(QPixmap("Assets/Images/Clear.png")), "Reset app and clear all data",self)
        self.reset_action.triggered.connect(self.reset_func)
        self.toolbar.addAction(self.reset_action)
        
        self.del_acc = QAction(QIcon(QPixmap("Assets/Images/Del_ACC.png")), "Delete My Account",self)
        self.del_acc.triggered.connect(self.delete_account)
        self.toolbar.addAction(self.del_acc)
        
        self.logout_action = QAction(QIcon(QPixmap("Assets/Images/Logout.png")), "Logout",self)
        self.logout_action.triggered.connect(self.logout_func)
        self.toolbar.addAction(self.logout_action)
        
        self.toolbar.addSeparator()
        
        ## Change Password of app part
        # lbl
        self.psw_chg_lbl = QLabel('Change Lock Pin :')
        self.toolbar.addWidget(self.psw_chg_lbl)
        
        # current password input
        W = QWidget()
        HL = QHBoxLayout()
        W.setLayout(HL)
        self.password = QLineEdit()
        self.password.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.password.setPlaceholderText("Current Password :")
        self.password.setEchoMode(QLineEdit.Password)
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
        HL.addWidget(self.password)
        
        # new password input
        nW = QWidget()
        nHL = QHBoxLayout()
        nW.setLayout(nHL)
        self.new_password = QLineEdit()
        self.new_password.setValidator(QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")))
        self.new_password.setPlaceholderText("New Password :")
        self.new_password.setEchoMode(QLineEdit.Password)
        # show/hide button for password
        self.show_new_password_button = QPushButton("Show")
        self.show_new_password_button.setStyleSheet("""
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
        self.show_new_password_button.clicked.connect(self.toggle_new_password_visibility)
        nHL.addWidget(self.show_new_password_button)
        nHL.addWidget(self.new_password)
        
        self.remove_psw_btn = QAction(QIcon(QPixmap('Assets/Images/Delete2.png')), 'Remove Lock (Ctrl+Alt+R)')
        self.remove_psw_btn.setShortcut('Ctrl+Alt+R')
        self.remove_psw_btn.triggered.connect(self.remove_pin_func)
        
        self.chg_psw_btn = QAction(QIcon(QPixmap('Assets/Images/check.png')), 'Change Lock Pin (Ctrl+Alt+C)')
        self.chg_psw_btn.setShortcut('Ctrl+Alt+C')
        self.chg_psw_btn.triggered.connect(self.chg_pin_func)
        
        
        li = PRR.get_lock_info()
        if li:
            if li[0] == "True":
                self.toolbar.addWidget(W)
                self.toolbar.addWidget(nW)
                self.toolbar.addAction(self.remove_psw_btn)
                self.toolbar.addAction(self.chg_psw_btn)
            else:
                self.toolbar.addWidget(nW)
                self.toolbar.addAction(self.chg_psw_btn)   
        else:
            self.toolbar.addWidget(nW)
            self.toolbar.addAction(self.chg_psw_btn)
        
        
        if self.conn == False:
            self.del_acc.setText("Delete My Account (No Connection)")
            self.del_acc.setEnabled(False)
            self.logout_action.setText("Logout (No Connection)")
            self.logout_action.setEnabled(False)
            
    
    def reset_func(self):
        try:
            # show cancel|ok dialog
            dialog = QMessageBox()
            dialog.setWindowTitle("Reset App")
            dialog.setText("Are you sure you want to reset the app and clear all data?")
            dialog.setIcon(QMessageBox.Warning)
            dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            dialog.setDefaultButton(QMessageBox.Cancel)
            dialog.setWindowIcon(QIcon(QPixmap("Assets/Images/Error.png")))
            
            dialog.show()
            if dialog.exec() == QMessageBox.Ok:
                PRR.Delete('Buy', 'true')
                PRR.Delete('Buy_Products', 'true')
                PRR.Delete('Buy_Services', 'true')
                PRR.Delete('Buy_Suppliers', 'true')
                PRR.Delete('Clients', 'true')
                PRR.Delete('Employees', 'true')
                PRR.Delete('Products', 'true')
                PRR.Delete('Sale', 'true')
                PRR.Delete('Sale_Clients', 'true')
                PRR.Delete('Sale_Products', 'true')
                PRR.Delete('Sale_Services', 'true')
                PRR.Delete('Services', 'true')
                PRR.Delete('Suppliers', 'true')
                PRR.AddCustomTableToJsonFile({"Table_name": "", "Columns": [], "Rows_data": [], "Primary_status": [], "Columns_Charts_index": []})
                PRR.del_saved_Table_by_index('All')
                PRR.set_lock_info("False", "")
                self.reset_backfunc()
                self.lock_sts_func(False)
                text_to_speech('Reset successful')
                return
            
            else:
                return
        except:
            text_to_speech('Reset Faild')
            return
     
    def delete_account_func(self, psw, dialog):
        
        if self.username != None:
            dialog.close()
            try:
                url = f"http://127.0.0.1:8000/auth/del_acc/{self.username}/{psw}"
                res = requests.delete(url, params={"tkn":"JDR55EECncd88Ddd"})
                if res.text == "1":
                    text_to_speech('Delete Account Successful')
                    self.lock_func()
                    return
                else:
                    text_to_speech('Delete Account Faild 11')
                    return
            except:
                text_to_speech('Delete Account Faild 00')
                return
        
        else:
            return
     
    def delete_account(self):
        if self.username != None:
            try:
                # show dialog to  get password
                dialog = QDialog(self)
                dialog.setWindowFlag(Qt.FramelessWindowHint)
                dialog.setWindowIcon(QIcon(QPixmap("Assets/Images/Error.png")))
                dialog.setFixedSize(300, 150)
                dialog.setWindowModality(Qt.ApplicationModal)
                # Create a layout for the dialog
                layout = QVBoxLayout()
                dialog.setLayout(layout)
                # Create a label for the password input
                password_label = QLabel("Enter your password:")
                layout.addWidget(password_label)
                # Create a line edit for the password input
                password_input = QLineEdit()
                password_input.setEchoMode(QLineEdit.Password)
                layout.addWidget(password_input)
                # Create a button to submit the password
                submit_button = QPushButton("Submit")
                submit_button.clicked.connect(lambda: self.delete_account_func(password_input.text(), dialog))
                layout.addWidget(submit_button)
                
                dialog.exec()
                
            except:
                text_to_speech('Delete Account Faild')
                return
        
        else:
            return
    
    def user_chng(self, txt):
        self.username = txt
        return
    
    def Refresh(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                try:
                    attr.deleteLater()
                except:
                    pass
        
        self.UI()
        self.ToolBar()
        
    def remove_pin_func(self):
        PRR.set_lock_info('False', '')
        self.lock_sts_func(False)
        self.Refresh()
        
    def chg_pin_func(self):
        try:
            
            tcp = PRR.get_lock_info()
            if tcp:
                
                # set new password when app has password
                if tcp[0] == 'True':
                    cp = self.password.text()
                    np = self.new_password.text()
                    if len(str(np)) >= 8:
                        
                        if str(cp) == str(tcp[1]) :
                            PRR.set_lock_info('True', str(np))
                            self.Refresh()
                            self.lock_sts_func(True)
                            self.lock_func()
                        else:
                            text_to_speech("Password Incorect")
                            self.Refresh()
                    
                    else:
                        text_to_speech('new password must be more than 7 character')
                        self.Refresh()     
                    
                # set new password when app doesn't have password
                else:
                    np = self.new_password.text()
                    if len(str(np)) >= 8:
                        PRR.set_lock_info('True', str(np))
                        self.Refresh()
                        self.lock_sts_func(True)
                        self.lock_func()
                    
                    else:
                        text_to_speech('new password must be more than 7 character')
                        self.Refresh()     
                         
            else:
                text_to_speech("Changing faild")
                self.Refresh()
                
        except:
            text_to_speech("Changing faild")
            self.Refresh()
            
            
    
    def toggle_password_visibility(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")
            
    def toggle_new_password_visibility(self):      
        if self.new_password.echoMode() == QLineEdit.Password:
            self.new_password.setEchoMode(QLineEdit.Normal)
            self.show_new_password_button.setText("Hide")
        else:
            self.new_password.setEchoMode(QLineEdit.Password)
            self.show_new_password_button.setText("Show")  
            
            
    