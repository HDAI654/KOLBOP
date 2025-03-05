from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
from PyQt5.QtTextToSpeech import *
from PyQt5.QtWebEngineWidgets import *
import pandas as pd
import sqlite3

# function for convert html to css
def convert_html_to_pdf(source_html, output_filename):
    pass


engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))

class ReportUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(PRR.Style())
        self.AllTables_names = ['Clients', 'Suppliers', 'Products', 'Buy', 'Sale']
        self.combo_box_text = 'Select Table To Show'
        self.selected_export_type = None
        self.ToolBarUI()
        self.UI()
        self.TablesUI()
    
    def UI(self):
        pass
    
    def ToolBarUI(self):
        # Toolbar
        self.toolbar = QToolBar("Reports Page Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
    
        self.addToolBar(self.toolbar)

        # Icon
        self.Icon = QLabel()
        self.Icon.setPixmap(QPixmap("Assets/Images/Reports.png"))
        self.Icon.setAlignment(Qt.AlignCenter)
        self.toolbar.addWidget(self.Icon)
        self.toolbar.addSeparator()
        
        # comboo box of name of all Tables and its Label
        self.combo_widget = QWidget()
        self.combo_layout = QVBoxLayout()
        self.combo_widget.setLayout(self.combo_layout)
        self.combo_box_label = QLabel("Select Table To Show")
        self.combo_box_label.setStyleSheet("font-size: 16px;font-weight: bold;color: #ffffff;")
        self.combo_box_label.setAlignment(Qt.AlignCenter)
        self.combo_layout.addWidget(self.combo_box_label)
        self.combo_box = QComboBox()
        self.combo_box.addItems([self.combo_box_text]+self.AllTables_names)
        self.combo_box.setCurrentText(self.combo_box_text)
        self.combo_box.currentIndexChanged.connect(self.combo_box_changed)
        self.combo_layout.addWidget(self.combo_box)
        self.toolbar.addWidget(self.combo_widget)
        
        self.toolbar.addSeparator()
        
        self.refresh_action = QAction(QIcon(QPixmap("Assets/Images/refresh.png")), "Refresh (Ctrl+R)", self)
        self.refresh_action.setShortcut("Ctrl+R")
        self.refresh_action.triggered.connect(self.RefreshAll)
        self.toolbar.addAction(self.refresh_action)
        
        self.export_action = QAction(QIcon(QPixmap("Assets/Images/Export.png")), "Export (Ctrl+E)", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.triggered.connect(self.Export)
        self.toolbar.addAction(self.export_action)
    
    def TablesUI(self):
        # Prepration all tables' dock widgets
        self.AllTables = []
        for idx, tbl in enumerate(self.AllTables_names):
            dock = QDockWidget(f"{tbl} Data")
            dock.setAllowedAreas(Qt.AllDockWidgetAreas)
            dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
            dock.setContextMenuPolicy(Qt.PreventContextMenu)

            dock_win = QMainWindow()
            dock.setWidget(dock_win)
            
            df = {}
            df_datas = None
            df_heads = None
            
            # Data
            if tbl == "Clients" or tbl == "Suppliers":
                data = PRR.Select("*", tbl, "True")
            if tbl == "Products":
                data = [list(p) for p in PRR.Select("*", tbl, "True")]
                # convert supplier code to  supplier name
                for i in range(len(data)):
                    data[i][2] = PRR.Select("CompanyName", "Suppliers", f"ID = '{data[i][2]}'")[0][0]
            if tbl == "Buy":
                data = []
                for b in PRR.Select("*", tbl, "True"):
                    d = []
                    # ID
                    d.append(b[0])
                    
                    # Suppliers
                    sp = [s[0] for s in PRR.Select("Supplier_Name", "Buy_Suppliers", f"BC = {b[0]}")]
                    sp = " - ".join(sp)
                    d.append(sp)
                    
                    # Services
                    sv = [s[0] for s in PRR.Select("Explanation", "Buy_Services", f"BC = {b[0]}")]
                    sv = " - ".join(sv)
                    d.append(sv)
                    
                    # Products
                    pr = [s[0] for s in PRR.Select("Name", "Buy_Products", f"BC = {b[0]}")]
                    pr = " - ".join(pr)
                    d.append(pr)
                    
                    # total price
                    d.append(b[1])
                    
                    # date
                    d.append(b[2])
                    
                    # add data to data
                    data.append(d)
            if tbl == "Sale":
                data = []
                for s in PRR.Select("*", tbl, "True"):
                    d = []
                    # ID
                    d.append(s[0])
                    
                    # Clients
                    cl = [f[0] for f in PRR.Select("Client_Name", "Sale_Clients", f"SLC = {s[0]}")]
                    cl = " - ".join(cl)
                    d.append(cl)
                    
                    # Services
                    sv = [f[0] for f in PRR.Select("Explanation", "Sale_Services", f"SLC = {s[0]}")]
                    sv = " - ".join(sv)
                    d.append(sv)
                    
                    # Products
                    pr = [f[0] for f in PRR.Select("Name", "Sale_Products", f"SLC = {s[0]}")]
                    pr = " - ".join(pr)
                    d.append(pr)
                    
                    # total price
                    d.append(s[1])
                    
                    # date
                    d.append(s[2])
                    
                    # add data to data
                    data.append(d)
            # html code
            HTML = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                <style>
                {BootStrap}
                </style>
                </head>
                
                <body style="background-color: #000000;">

                    <div class="container-fluid">
                        <div class="jumbotron bg-dark">
                            <h1 class="text-light">{table_name}</h1>  
                            <table class="table table-dark table-hover">
                                <thead>
                                    <tr>
                                    {heads}
                                    </tr>
                                </thead>
                                <tbody>
                                {rows}
                                </tbody>
                            </table>    
                        </div>
                    </div>

                </body>
            </html>

            """
            
            # prepration html code
            with open("Assets/DataBases/bootstrap.css", "r") as bt:
                bootstrap = bt.read()
                
                # heads
                heads = PRR.GetFields_of_a_table(tbl)
                if tbl == "Products":
                    heads[2] = "Supplier Company Name"
                
                if tbl == "Buy":
                    heads = ["ID", "Suppliers", "Services", "Products", "Total Price", "Date"]
                
                if tbl == "Sale":
                    heads = ["ID", "Clients", "Services", "Products", "Total Price", "Date"]
                
                if tbl == str(PRR.GetCustomTableFromJsonFile()['Table_name']):
                    heads = [c[0] for c in PRR.GetCustomTableFromJsonFile()['Columns']]
                
                df_heads = [hd for hd in heads]
                
                for hi, h in enumerate(heads):
                    heads[hi] = f"<th>{h}</th>"
                
                heads = "\n".join(heads)
                
                # rows
                df_datas = [dt for dt in data]
                rows = []
                for ri, row in enumerate(data):
                    r = []
                    r.append(f"<tr>\n")
                    for j, col in enumerate(row):
                        r.append(f"<td>{col}</td>\n")
                    r.append(f"</tr>")
                    rows.append(''.join(r))
                    r = []
                rows = "\n".join(rows)
        
                # HTML
                HTML = HTML.format(BootStrap=bootstrap, table_name=tbl, heads=heads, rows=rows)
            
            
            page = QWebEngineView()
            page.setHtml(HTML)
            dock_win.setCentralWidget(page)
                
                
            for hix, he in enumerate(df_heads):
                df[str(he)] = [r[hix] for r in df_datas]
                
            self.AllTables.append([str(tbl), dock, df, HTML])
    
    def combo_box_changed(self):
        if self.combo_box.currentText() == "Select Table To Show":
            return
        else:
            # get table name
            tbl = self.combo_box.currentText()
            self.combo_box_text = tbl
            dw = None
            self.Refresh()
            for i in self.AllTables:
                if str(i[0]) == str(tbl):
                    dw = i[1]
                    break
            self.addDockWidget(Qt.RightDockWidgetArea, dw)

    def Refresh(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                try:
                    attr.deleteLater()
                except:
                    pass
        # Delete Docks
        self.destroy_all_dockwidgets_in_page()
        
            
        # Remake
        self.ToolBarUI()
        self.UI()
        self.TablesUI()   
      
    def RefreshAll(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                try:
                    attr.deleteLater()
                except:
                    pass
        # Delete Docks
        self.destroy_all_dockwidgets_in_page()
        
        # reset  self.combo_box_text
        self.combo_box_text = "Select Table To Show"
            
        # Remake
        self.ToolBarUI()
        self.UI()
        self.TablesUI()  
      
    def destroy_all_dockwidgets_in_page(self):
        for child in self.children():
                if isinstance(child, QDockWidget):
                    child.deleteLater()
      
    def Export(self):
        if self.combo_box_text != "Select Table To Show":
            # show dialog to choose type of export file
            dialog = QDialog(self)
            dialog.setWindowFlag(Qt.FramelessWindowHint)
            dialog.setFixedSize(320, 400)
            dialog.setWindowOpacity(1)
                
            # Create a layout for the dialog
            layout = QVBoxLayout(dialog)
            
            # Table Name Label
            table_name_label = QLabel(f"Table Name: {self.combo_box_text}")
            layout.addWidget(table_name_label)
                
            # Create a label for the dialog
            label = QLabel("Choose Your Export File Type:")
            layout.addWidget(label)
            
            # button to show file dialog to choose export file location
            ch_button = QPushButton("Choose File Location")
            location_dialog = QFileDialog(directory='C:\\Users')
            location_dialog.setFileMode(QFileDialog.Directory)
            location_dialog.setOption(QFileDialog.ShowDirsOnly)
            # change the text of the button to dir location when dialog closed
            location_dialog.fileSelected.connect(lambda path: ch_button.setText(path))
            
            ch_button.clicked.connect(lambda: location_dialog.exec_())
            
            layout.addWidget(ch_button)
                
            # Create radio buttons for the dialog
            radio_buttons = []
            for i, tp in enumerate(["CSV", "JSON", "SQL", "HTML"]):
                radio_button = QRadioButton(tp)
                # change selected radio button variable when each radio button is clicked
                radio_button.clicked.connect(lambda checked, radio_button=radio_button: self.selected_radio_button_changed(radio_button))
                radio_button.setChecked(False)
                radio_buttons.append(radio_button)
                # set icon for radio button
                radio_button.setIcon(QIcon(f"Assets/Images/{tp}.png"))
                layout.addWidget(radio_buttons[i])
                
                
            # Create a button for the dialog
            button = QPushButton("OK")
            layout.addWidget(button)
            button.clicked.connect(lambda: self.export_func(dialog, location_dialog))
                
            # Cancel button
            cancel_button = QPushButton("Cancel")
            layout.addWidget(cancel_button)
            cancel_button.clicked.connect(dialog.close)
            # set dialog to center of screen
            dialog.move(self.geometry().center() - dialog.rect().center())
            # set dialog to be on top of all windows
            dialog.setWindowModality(Qt.ApplicationModal)
            # show dialog
            dialog.exec_()  
        
        else:
            text_to_speech("Please select a table to export.")
            self.RefreshAll()
        
    def selected_radio_button_changed(self, radio_button):
        self.selected_export_type = radio_button.text()
      
    def export_func(self, dialog, location_dialog):           
        if self.selected_export_type != None:   
            if  location_dialog.selectedFiles() != []:
                # get selected dir from location_dialog
                selected_dir = location_dialog.selectedFiles()[0]
                
                # create dataframe from selected table
                df = None
                tbl_name = None
                _html_btsp = None
                for t in self.AllTables:
                    if str(t[0]) == str(self.combo_box_text):
                        df = t[2]
                        tbl_name = t[0]
                        _html_btsp = t[3]
                df = pd.DataFrame(df)
                  
                if self.selected_export_type == "CSV":
                    df.to_csv(f"{selected_dir}/{self.combo_box_text}.csv", index=False)
                if self.selected_export_type == "JSON":
                    df.to_json(f"{selected_dir}/{self.combo_box_text}.json", orient="records")
                if self.selected_export_type == "SQL":
                    conn = sqlite3.connect(f"{selected_dir}/{self.combo_box_text}.db")
                    df.to_sql(f"{self.combo_box_text}", conn, if_exists="replace", index=False)
                if self.selected_export_type == "HTML":
                    with open(f"{selected_dir}/{self.combo_box_text}.html", "w") as h:
                        h.write(_html_btsp)

                
                # close dialog and refresh
                dialog.close()
                self.RefreshAll()
            
            else:
                text_to_speech("Please select a file location")
                dialog.close()
                self.RefreshAll()
                
        else:
            text_to_speech("Please select a type of export file")
            dialog.close()
            self.RefreshAll()
      
      
        