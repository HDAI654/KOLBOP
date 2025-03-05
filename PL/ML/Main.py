from BLL.ML_data import ML_Data
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *



class ML_win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UI()
        self.ToolBar()
    
    def ToolBar(self):
        self.toolbar = QToolBar("ML Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addToolBar(self.toolbar)
        self.refresh_action = QAction(QIcon(QPixmap("Assets/Images/Refresh.png")), "Refresh (Ctrl+R)", self)
        self.refresh_action.setShortcut("Ctrl+R")
        self.refresh_action.triggered.connect(self.RefreshAll)
        self.toolbar.addAction(self.refresh_action)
    
    def UI(self):
        # Sales and Buy status for years  Page
        self.dock = QDockWidget("Sales and Buys status for years")
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        self.dock_win = QMainWindow()
        self.dock.setWidget(self.dock_win)

        # Data
        Data = ML_Data.Quarter_Years()
        
        if Data == "No Data 025ScniS4ecn8W":
            self.HTML = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Bootstrap Example</title>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                    {BootStrap}
                    </style>
                </head>
                
                <body style="background-color: #000000;">

                    <div class="container">
                        <div class="jumbotron bg-dark">
                            <h1 class="text-light">No Data To Show</h1>
                        </div>    
                    </div>

                </body>
            </html>

            """
            
            with open("Assets/DataBases/bootstrap.css", "r") as bt:
                bootstrap = bt.read()
                self.HTML = self.HTML.format(BootStrap=bootstrap)
            
            self.page = QWebEngineView()
            self.page.setHtml(self.HTML)
            self.dock_win.setCentralWidget(self.page)
        elif Data == "Not Enough Data dneeEED2eceE5":
            self.HTML = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Bootstrap Example</title>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                    {BootStrap}
                    </style>
                </head>
                
                <body style="background-color: #000000;">

                    <div class="container">
                        <div class="jumbotron bg-dark">
                            <h1 class="text-light">Your data is not enough to access this feature</h1>
                        </div>    
                    </div>

                </body>
            </html>

            """
            
            with open("Assets/DataBases/bootstrap.css", "r") as bt:
                bootstrap = bt.read()
                self.HTML = self.HTML.format(BootStrap=bootstrap)
            
            self.page = QWebEngineView()
            self.page.setHtml(self.HTML)
            self.dock_win.setCentralWidget(self.page)
        else:

            self.HTML = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <title>Bootstrap Example</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
            {BootStrap}
            </style>
            </head>
            <body style="background-color: #000000;">

            <div class="container">
            <div class="jumbotron bg-dark">
                <h1 class="text-light">Bad Situation</h1>
                <table class="table table-dark table-hover">
                    <thead>
                        <tr>
                        <th>Year</th>
                        <th>Profit</th>
                        </tr>
                    </thead>
                    <tbody>
                    {Bad_ROWS}
                    </tbody>
                </table> 
                </table>

                        

            </div> 
            <div class="jumbotron bg-dark">
                <h1 class="text-light">Average Situation</h1>  
                <table class="table table-dark table-hover">
                    <thead>
                        <tr>
                        <th>Year</th>
                        <th>Profit</th>
                        </tr>
                    </thead>
                    <tbody>
                    {Avg_ROWS}
                    </tbody>
                </table>    
            </div>
            <div class="jumbotron bg-dark">
                <h1 class="text-light">Excellent Situation</h1> 
                <table class="table table-dark table-hover">
                    <thead>
                        <tr>
                        <th>Year</th>
                        <th>Profit</th>
                        </tr>
                    </thead>
                    {Good_ROWS}
                </table>     
            </div>   
            </div>

            </body>
            </html>

            """
            
            bad_rows = ['<tr><td>'+str(Y)+'</td><td>'+str(P)+'</td></tr>'+'\n' for Y, P in Data["BAD"]]
            avg_rows = ['<tr><td>'+str(Y)+'</td><td>'+str(P)+'</td></tr>'+'\n' for Y, P in Data["MEDIUM"]]
            ex_rows = ['<tr><td>'+str(Y)+'</td><td>'+str(P)+'</td></tr>'+'\n' for Y, P in Data["GOOD"]]
            with open("Assets/DataBases/bootstrap.css", "r") as bt:
                bootstrap = bt.read()
                self.HTML = self.HTML.format(Bad_ROWS=''.join(bad_rows), Avg_ROWS=''.join(avg_rows), Good_ROWS=''.join(ex_rows), BootStrap=bootstrap)
            
            self.page = QWebEngineView()
            self.page.setHtml(self.HTML)
            self.dock_win.setCentralWidget(self.page)
        
    def RefreshAll(self):
        if hasattr(self, 'dock'):
            # Destroy etoolbar
            self.removeDockWidget(self.dock )
            self.dock.deleteLater()
            delattr(self, 'dock')
            self.UI()



