from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PL.XY_TBL_CHART import XYTBLCHART_win
from PyQt5.QtTextToSpeech import *
from BLL.PublicRrep import PRR

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))

class CP(QMainWindow):
    def __init__(self):
        super(CP, self).__init__()
        self.dt = PRR.get_CSPBS_tbls_dt_pd()
        self.current_chart_widget = None
        self.current_chart_fig = None
        self.UI()
        self.ToolBar()
    
    def UI(self):
        pass
    
    def ToolBar(self):
        # Main ToolBar
        self.toolbar = QToolBar("Chart ToolBar")
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addToolBar(self.toolbar)
        
        # widgets
        self.tbl_combo = QComboBox()
        self.tbl_combo.addItems(["Select Table", "Clients", "Suppliers", "Products", "Buy", "Sale"])
        self.tbl_combo.setCurrentText("Select Table")
        self.toolbar.addWidget(self.tbl_combo)
        
        self.make_action = QAction(QIcon(QPixmap("Assets/Images/create_chart.png")), "Make Chart",self)
        self.make_action.triggered.connect(self.open_make_dg)
        self.toolbar.addAction(self.make_action)
        
        self.save_action = QAction(QIcon(QPixmap("Assets/Images/Save_As.png")), "Save Chart", self)
        self.save_action.triggered.connect(self.save_chart)
        self.toolbar.addAction(self.save_action)
        
    def open_make_dg(self):
        if self.tbl_combo.currentText() == "Select Table":
            text_to_speech("select a table first to make chart")
            return
        else:
            try:
                dg = XYTBLCHART_win(self.dt[self.tbl_combo.currentText()], f"Of {self.tbl_combo.currentText()} Table", self)
                self.current_chart_widget = dg.getPage()
                self.current_chart_fig = dg.rtn_fig()
                self.setCentralWidget(dg.getPage())
            except:
                text_to_speech("problem in make chart")
                return
        
    
    def save_chart(self):
        if self.current_chart_widget is None:
            text_to_speech("no chart to save")
            return
        else:
            try:
                file_name, _ = QFileDialog.getSaveFileName(self, "Save Chart", "", "PNG (*.png);;JPEG (*.jpg)")
                
                if file_name:
                    self.current_chart_fig.savefig(file_name, bbox_inches='tight')
                    text_to_speech("chart saved")
            except:
                text_to_speech("problem in save chart")
                return
        