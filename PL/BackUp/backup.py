from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PL.BackUp.LoadPage import Load_win
from PL.BackUp.UploadPage import Upload_win
 
    
class backup_win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UI()
    
    def UI(self):
        # the main notebook
        self.notebook = QTabWidget()
        self.notebook.setTabPosition(QTabWidget.South)
        self.notebook.setDocumentMode(True)
        self.setCentralWidget(self.notebook)

        # add three page to notebook
        self.upload_page = Upload_win()
        self.load_page = Load_win()
        self.notebook.currentChanged.connect(self.load_page.Refresh)

        self.notebook.addTab(self.upload_page, "Upload")
        self.notebook.addTab(self.load_page, "Data")
    