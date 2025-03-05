from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTextToSpeech import *
from PyQt5.QtWebEngineWidgets import *
import requests

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))
    
class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drop a file here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel { background-color: #343a40; border: 2px dashed #aaa; border-radius: 10px; }")
        self.setAcceptDrops(True)
        self.path = None
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("QLabel { background-color: #28a745; border: 2px dashed #aaa; border-radius: 20px; }")
    
    def dropEvent(self, event):
        self.setStyleSheet("QLabel { background-color: #343a40; border: 2px dashed #aaa; border-radius: 10px; }")
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.path = file_path
            self.setText(f"File Path: {file_path}")
    
    def get_path(self):
        return self.path
    
    def clear(self):
        self.setText("Drop a file here")
        self.path = None




class Upload_win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.ctn_widget = DropLabel(self)
        self.setCentralWidget(self.ctn_widget)
        self.ToolBar()
    
    def ToolBar(self):
        self.toolbar = QToolBar("Tools")
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addToolBar(self.toolbar)
        
        self.upload_action = QAction(QIcon(QPixmap("Assets/Images/Upload.png")), "Upload", self) 
        self.upload_action.triggered.connect(self.upload_file)
        self.toolbar.addAction(self.upload_action)
        
        self.backup_data_action = QAction(QIcon(QPixmap("Assets/Images/data_cloud.png")), "Backup Data", self)
        self.backup_data_action.triggered.connect(self.bda)
        self.toolbar.addAction(self.backup_data_action)
        
        
        
        
    
    def upload_file(self):
        if self.username != None:
            file_path = self.ctn_widget.get_path()
            if file_path != None:
                try:
                    url = "http://127.0.0.1:8000/bkup/"
                    file_path = str(file_path)
                    files = {"file": open(file_path, "rb")}
                    requests.post(url, files=files, data={"user": self.username})
                    
                    
                    self.ctn_widget.clear()
                    text_to_speech("File uploaded successfully")
                    return
                except:
                    text_to_speech("upload faild ")
                    return
                
            else:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(self, "Select a file", "C:\\Users", "All Files (*);;Text Files (*.txt)")
                if fileName:
                    try:
                        url = "http://127.0.0.1:8000/bkup/"
                        file_path = str(fileName)
                        files = {"file": open(file_path, "rb")}
                        requests.post(url, files=files, data={"user": self.username})
                        
                        
                        self.ctn_widget.clear()
                        text_to_speech("File uploaded successfully")
                        return
                    except:
                        text_to_speech("upload faild ")
                        return
        else:
            text_to_speech("Upload faild . ,  It seems that you are not logged in")
            return
        
    def bda(self):
        if self.username != None:
            file_path = 'Assets/DataBases/data.db'
            if file_path != None:
                try:
                    url = "http://127.0.0.1:8000/bkup/"
                    file_path = str(file_path)
                    files = {"file": open(file_path, "rb")}
                    requests.post(url, files=files, data={"user": self.username})
                    
                    self.ctn_widget.clear()
                    text_to_speech("File uploaded successfully")
                    return
                except:
                    text_to_speech("upload faild ")
                    return
                
            else:
                text_to_speech("Please drop a file first to upload")
                return
        else:
            text_to_speech("Upload faild . ,  It seems that you are not logged in")
            return

