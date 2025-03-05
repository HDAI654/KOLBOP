from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtTextToSpeech import *
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))

def list_isnumbric(data): 
    flag = True
    for i in data:
        if str(i).isnumeric():
            pass
        else :
            flag = False
    
    return flag

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super(MplCanvas, self).__init__(fig)

class XYTBLCHART_win:
    def __init__(self, all_fields, tilte, parent):
        self.Title = tilte
        self.all_fields = dict(all_fields)
        self.return_page = QMainWindow()
        self.canvas = MplCanvas(self.return_page)
        self.return_page.setCentralWidget(self.canvas)
        
        # show dialog
        self.dialog = QDialog(parent=parent)
        self.dialog.setWindowFlag(Qt.FramelessWindowHint)
        self.dialog.setFixedSize(300, 500)
        self.dialog.setWindowOpacity(1)
        
        self.selected_chart_type = None
        
        self.UI()
        
        
        # set dialog to center of screen
        self.dialog.move(parent.geometry().center() - self.dialog.rect().center())
        # set dialog to be on top of all windows
        self.dialog.setWindowModality(Qt.ApplicationModal)
        # show dialog
        self.dialog.exec_()
    
    def UI(self):
        
        # Create a layout for the self.dialog
        self.layout = QVBoxLayout(self.dialog)
        
        # Create widgets
        self.tplabel = QLabel("Choose Chart Type :")
        self.layout.addWidget(self.tplabel)
        
        # Create radio buttons for the dialog
        self.radio_buttons = []
        for i, tp in enumerate(['Bar', 'Pie', 'Plot', 'Scatter']):
            radio_button = QRadioButton(tp)
            #radio_button.setStyleSheet("color: #ffffff;font-size: 16px;font-weight: bold;")
            # change selected radio button variable when each radio button is clicked
            radio_button.clicked.connect(lambda checked, radio_button=radio_button: self.selected_radio_button_changed(radio_button))
            radio_button.setChecked(False)
            self.radio_buttons.append(radio_button)
            # set icon for radio button
            radio_button.setIcon(QIcon(f"Assets/Images/{tp.title()}.png"))
            self.layout.addWidget(self.radio_buttons[i])
                 
        self.fllabel = QLabel("Choose X and Y fields :")
        self.layout.addWidget(self.fllabel)
        
        self.fl_combo_X_lbl = QLabel("Choose X field :")
        self.layout.addWidget(self.fl_combo_X_lbl)
        self.fl_combo_X = QComboBox()
        self.layout.addWidget(self.fl_combo_X)
        
        self.fl_combo_Y_lbl = QLabel("Choose Y field :")
        self.layout.addWidget(self.fl_combo_Y_lbl)
        self.fl_combo_Y = QComboBox()
        self.layout.addWidget(self.fl_combo_Y)
        
        # Create OK button
        button = QPushButton("OK")
        self.layout.addWidget(button)
        button.clicked.connect(self.create_chart)
            
        # Cancel button
        cancel_button = QPushButton("Cancel")
        self.layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.dialog.close)
    
    def selected_radio_button_changed(self, button):
        self.selected_chart_type = button.text()
        
        if self.selected_chart_type == None:
            self.fl_combo_X.setEnabled(False)
            self.fl_combo_Y.setEnabled(False)
        
        if self.selected_chart_type == "Bar":
            self.fl_combo_X.setEnabled(True)
            self.fl_combo_Y.setEnabled(True)
            self.fl_combo_X.clear()
            self.fl_combo_Y.clear()
            for k, v in self.all_fields.items():
                self.fl_combo_X.addItem(str(k))
                self.fl_combo_Y.addItem(str(k))
            
        if self.selected_chart_type == "Pie":
            self.fl_combo_X.setEnabled(True)
            self.fl_combo_Y.setEnabled(True)
            self.fl_combo_X.clear()
            self.fl_combo_Y.clear()
            for k1, v1 in self.all_fields.items():
                self.fl_combo_X.addItem(str(k1))
                self.fl_combo_Y.addItem(str(k1))
            
        if self.selected_chart_type == "Plot":
            self.fl_combo_X.setEnabled(True)
            self.fl_combo_Y.setEnabled(True)
            self.fl_combo_X.clear()
            self.fl_combo_Y.clear()
            plt_valid_items = []
            for k2, v2 in self.all_fields.items():
                if list_isnumbric(list(v2)):
                    plt_valid_items.append(k2)
            if plt_valid_items != []:
                self.fl_combo_X.addItems(plt_valid_items)
                self.fl_combo_Y.addItems(plt_valid_items)
            else:
                text_to_speech("you don't have valid data to plot")
            
        if self.selected_chart_type == "Scatter":
            self.fl_combo_X.setEnabled(True)
            self.fl_combo_Y.setEnabled(True)
            self.fl_combo_X.clear()
            self.fl_combo_Y.clear()
            sct_valid_items = []
            for k3, v3 in self.all_fields.items():
                if list_isnumbric(list(v3)):
                    sct_valid_items.append(k3)
            if sct_valid_items != []:
                self.fl_combo_X.addItems(sct_valid_items)
                self.fl_combo_Y.addItems(sct_valid_items)
            else:
                text_to_speech("you don't have valid data to plot")
  
    def create_chart(self):
        if self.selected_chart_type == "Plot":
            try:
                self.canvas.ax.clear()
                x =  np.array(self.all_fields[self.fl_combo_X.currentText()])
                y =  np.array(self.all_fields[self.fl_combo_Y.currentText()])
                self.canvas.ax.plot(x, y)
                self.canvas.ax.set_title(f'Line Chart {self.Title}')
                self.canvas.draw()
            except:
                text_to_speech("error in making chart")   
        if self.selected_chart_type == "Scatter":
            try:
                self.canvas.ax.clear()
                x =  np.array(self.all_fields[self.fl_combo_X.currentText()])
                y =  np.array(self.all_fields[self.fl_combo_Y.currentText()])
                self.canvas.ax.scatter(x, y)
                self.canvas.ax.set_title(f'Scatter Chart {self.Title}')
                self.canvas.draw()
            except:
                text_to_speech("error in making chart") 
        if self.selected_chart_type == "Bar":
            try:
                self.canvas.ax.clear()
                x =  np.array(self.all_fields[self.fl_combo_X.currentText()])
                y =  np.array(self.all_fields[self.fl_combo_Y.currentText()])
                if list_isnumbric(x) == False and list_isnumbric(y) == False:
                    text_to_speech("error in making chart")
                else:
                    if list_isnumbric(y):
                        self.canvas.ax.bar(x, y)
                        self.canvas.ax.set_title(f'Bar Chart {self.Title}')
                        self.canvas.draw()
                    else:
                        text_to_speech("error in making chart")
            except:
                text_to_speech("error in making chart") 
        if self.selected_chart_type == "Pie":
            try:
                self.canvas.ax.clear()
                x =  np.array(self.all_fields[self.fl_combo_X.currentText()])
                y =  np.array(self.all_fields[self.fl_combo_Y.currentText()])
                if list_isnumbric(x) == False and list_isnumbric(y) == False:
                    text_to_speech("error in making chart")
                else:
                    self.canvas.ax.pie(x, labels=y, autopct='%1.1f%%')
                    self.canvas.ax.set_title(f'Line Chart {self.Title}')
                    self.canvas.draw()
            except:
                text_to_speech("error in making chart") 
        self.dialog.close()
    
    def rtn_fig(self):
        return self.canvas.figure
    
    def getPage(self):
        return self.return_page

