from PyQt5 import QtWebEngineWidgets
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# open software
class WorkerThread(QThread):
    finished = pyqtSignal()

    def run(self):
        global Main_
        from Main import Main_
        self.finished.emit()

# Splash window
class Splash(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(0, 0, 800, 600)
        self.center()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("KOLBOP")
        self.setWindowIcon(QIcon("Assets/Images/Icon.png"))
        
        with open("Assets/DataBases/bootstrap.css", "r") as bt:
            bootstrap = bt.read()
            HTML = f"""
            <html>
            <head>
            <style>
            {bootstrap}
            </style>
            </head>
            <body class="bg-light">
            <div class="d-flex justify-content-center align-items-center vh-100">
                <div class="spinner-border text-primary" style="width:5rem;height:5rem">
                </div>
                </br>
                <h1 class="text-dark ml-3 font-wight-bold">KOLBOP   <h5 class="text-info ml-3 font-wight-bold">please wait ...</h5></h1>
            </div>
            </body>
            </html>
            
            """
            
            self.loading_animation = QtWebEngineWidgets.QWebEngineView()
            self.loading_animation.setFixedSize(800, 600)
            self.loading_animation.setHtml(HTML)
            self.setCentralWidget(self.loading_animation)

  
        


        
        self.worker_thread = WorkerThread()
        self.worker_thread.finished.connect(self.finish)
        self.worker_thread.start()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def finish(self):
        self.main_app = Main_()
        self.main_app.show()
        self.loading_animation.close()
        self.close()
        
