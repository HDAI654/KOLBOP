from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTextToSpeech import *
import requests
import base64

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))
 
    
class Load_win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.all_file_names = None
        self.GetNames()
        self.ToolBar()
        self.UI()
        
    def GetNames(self):
        try:
            if self.username != None:
                url = f"http://127.0.0.1:8000/bkup/get_names/AkkOk0d5seeS5S29eDe25ddDEc/{self.username}"
                response = requests.get(url)
                self.all_file_names = response.json()
                return
            else:
                self.all_file_names = []
                
                
        except:
            self.all_file_names = []
    
    def ToolBar(self):
        self.toolbar = QToolBar("Tools")
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addToolBar(self.toolbar)
        
        self.download_action = QAction(QIcon(QPixmap("Assets/Images/download.png")), "Download", self) 
        self.download_action.triggered.connect(self.download_file)
        
        self.delete_all_action = QAction(QIcon(QPixmap("Assets/Images/Delete All.png")), "Delete All Files From Server", self) 
        self.delete_all_action.triggered.connect(self.delete_all)
        
        self.Refresh_action = QAction(QIcon(QPixmap("Assets/Images/Refresh.png")), "Refresh", self) 
        self.Refresh_action.triggered.connect(self.Refresh)
        
        self.delete_selected_action = QAction(QIcon(QPixmap("Assets/Images/Delete2.png")), "Delete Selected File From Server", self) 
        self.delete_selected_action.triggered.connect(self.delete_selected)
        
        self.toolbar.addActions([self.delete_all_action, self.download_action, self.Refresh_action, self.delete_selected_action])
        
    def UI(self):
        # list of files
        self.list_widget = QListWidget()
        self.list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_widget.addItems(self.all_file_names)
        self.setCentralWidget(self.list_widget)
        
    def download_file(self):
        try:
            if self.username != None:
                file_selected = self.list_widget.currentItem() 
                if file_selected:
                    file_selected = file_selected.text()
                    dg = QFileDialog.getExistingDirectory(self, "Select Folder", "C:\\Users")
                    if dg:
                        url = f"http://127.0.0.1:8000/bkup/get_files/AkkOk0d5seeS5S29eDe25ddDEc/{self.username}"
                        response = requests.get(url)
                        files = response.json()
                        
                        
                        # download selected files
                        for key in files.keys():
                            if file_selected == key:
                                with open(f"{dg}/{key}", "wb") as file:
                                    file.write(base64.b64decode(files[key]))
                        
                        
                        text_to_speech("file downloaded successfully")
                        return
                    else:
                        text_to_speech(' select a folder first to download file ')
                        return
                else:
                    text_to_speech(' select a file first to download ')
                    return
            else:
                text_to_speech('download faild . ,  It seems that you are not logged in')
                return
        except:
            text_to_speech('download failed')
            return
    
    def Refresh(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                attr.deleteLater()
        # Remake
        self.all_file_names = None
        self.GetNames()
        self.ToolBar()
        self.UI()
      
    def delete_all(self):
        try:
            if self.username != None:
                url = f"http://127.0.0.1:8000/bkup/delete_all_files/K5DKdid45doNDOJM5885sD5dojdOIJDddojm5/{self.username}"
                res = requests.delete(url)
                if res.content == b'DELETED':
                    self.Refresh()
                    text_to_speech("all files deleted successfully")
                    return
                else:
                    self.Refresh()
                    text_to_speech("delete failed")
                    return
            else:
                return
        except:
            text_to_speech("delete failed")
            return
    
    def delete_selected(self):
        try:
            file_selected = self.list_widget.currentItem()
            if file_selected:
                url = f"http://127.0.0.1:8000/bkup/delete_one_file"
                res = requests.delete(url, params={"name":file_selected.text(), "tkn":"G71fT9oqLp2BZx80h"})
                if res.content == b'DELETED':
                    self.Refresh()
                    text_to_speech("file deleted successfully")
                    return
                else:
                    self.Refresh()
                    text_to_speech("delete failed")
                    return
        except:
            text_to_speech("delete failed")
            return
            