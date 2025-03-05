from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtTextToSpeech import *
from PL.ColorInput_Widget import CI
from PL.MIPCW import Charts
from BLL.PublicRrep import PRR
import pandas as pd
import sqlite3




engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))
    
    
class IM_win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_row = None
        self.selected_column = None
        self.selected_chart_type = None
        self.TableData = PRR.GetCustomTableFromJsonFile()
        self.ToolbarUI()
        self.BottomToolbarUI()
        self.UI()
        
    def UI(self):
        # Table
        self.Table = QTableWidget()
        self.Table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.Table.horizontalHeader().sectionClicked.connect(self.column_click)
        self.Table.verticalHeader().sectionClicked.connect(self.row_click)
        self.Table.cellClicked.connect(self.ItemClick)
        self.setCentralWidget(self.Table)
        
        # add columns
        self.Table.setColumnCount(len(self.TableData["Columns"]))
        self.Table.setHorizontalHeaderLabels([str(col_name[0]) for col_name in self.TableData["Columns"]])
        
        # add rows 
        row_data = []
        
        for r_r in self.TableData['Rows_data']:
            row_data.append([])
        
        prm = 1
        self.TableData["Primary_status"] = []
        for idx, col in enumerate(self.TableData["Columns"]):
            if col[1] == "Primary":
                for r_idx, r in enumerate(self.TableData['Rows_data']):
                    if idx not in self.TableData["Primary_status"]:
                        self.TableData["Primary_status"].append(idx)
                    row_data[r_idx].append(prm)
                    prm += 1
                prm = 1
            if col[1] == "String":
                for r_idx, r in enumerate(self.TableData['Rows_data']):
                    try:
                        row_data[r_idx].append(str(r[idx]))
                    except:
                        row_data[r_idx].append("NULL")
            if col[1] == "Integer":
                for r_idx, r in enumerate(self.TableData['Rows_data']):
                    try:
                        row_data[r_idx].append(int(r[idx]))
                    except:
                        row_data[r_idx].append(0)
            if col[1] == "Free":
                for r_idx, r in enumerate(self.TableData['Rows_data']):
                    try:
                        row_data[r_idx].append(r[idx])
                    except:
                        row_data[r_idx].append("NULL")
            if col[1] != "Integer" and col[1] != "String" and col[1] != "Primary" and col[1] != "Free":
                for r_idx, r in enumerate(self.TableData['Rows_data']):
                    row_data[r_idx].append("NULL")
        

        
        # Set Data
        self.Table.setRowCount(len(row_data))
        for row in range(len(row_data)):
            for column in range(len(row_data[row])):
                item = QTableWidgetItem(str(row_data[row][column]))
                self.Table.setItem(row, column, item)
                
        # set colors
        for ix, cl in enumerate(self.TableData["Columns"]):
            for i, r in enumerate(self.TableData['Rows_data']):
                    item = self.Table.item(i, ix)
                    item.setForeground(QColor(cl[3]))
                    item.setBackground(QColor(cl[2]))
                    self.Table.update()
                        
        self.TableData['Rows_data'] = row_data
        
        # Charts
        # create charts dock widgets
        self.charts_lst = []
        for i, ch in enumerate(self.TableData['Columns_Charts_index']):
            ChartType = ch[1]
            if ChartType == 'Bar':
                # get all cells data of selected column
                column_data = [row[ch[0]] for row in self.TableData['Rows_data'] if str(row[ch[0]]).isnumeric()]
                chart = Charts(column_data, self.chart_error, Title_add=f"Column '{self.TableData['Columns'][ch[0]][0]}'")
                chart.bar()
                self.charts_lst.append(chart)
            if ChartType == 'Pie':
                # get all cells data of selected column
                column_data = [row[ch[0]] for row in self.TableData['Rows_data'] if str(row[ch[0]]).isnumeric()]
                chart = Charts(column_data, self.chart_error, Title_add=f"Column '{self.TableData['Columns'][ch[0]][0]}'")
                chart.pie()
                self.charts_lst.append(chart)
            if ChartType == 'Plot':
                # get all cells data of selected column
                column_data = [row[ch[0]] for row in self.TableData['Rows_data'] if str(row[ch[0]]).isnumeric()]
                chart = Charts([list(range(1, len(column_data)+1, 1)), column_data], self.chart_error, Title_add=f"Column '{self.TableData['Columns'][ch[0]][0]}'")
                chart.plot()
                self.charts_lst.append(chart)
            if ChartType == 'Scatter':
                # get all cells data of selected column
                column_data = [row[ch[0]] for row in self.TableData['Rows_data'] if str(row[ch[0]]).isnumeric()]
                chart = Charts([list(range(1, len(column_data)+1, 1)), column_data], self.chart_error)
                chart.scatter()
                self.charts_lst.append(chart)
                
        self.create_all_charts(self.charts_lst)
        self.Table.cellChanged.connect(self.cell_changed_func)
             
    def ToolbarUI(self):
        # Toolbar
        self.toolbar = QToolBar("Custom Data Page Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
    
        self.addToolBar(self.toolbar)

        # Icon
        self.Icon = QLabel()
        self.Icon.setPixmap(QPixmap("Assets/Images/CustomData.png"))
        self.Icon.setAlignment(Qt.AlignCenter)
        self.toolbar.addWidget(self.Icon)
        self.toolbar.addSeparator()
        
        # Actions
        
        self.add_row_action = QAction(QIcon(QPixmap('Assets/Images/Add_row.png')), "Add Row to Table (Shift+Alt+R)")
        self.add_row_action.setShortcut("Shift+Alt+R")
        self.add_row_action.triggered.connect(self.AR_func)
        
        
        self.add_col_action = QAction(QIcon(QPixmap('Assets/Images/Add_col.png')), "Add Columns to Table (Shift+Alt+A)")
        self.add_col_action.setShortcut("Shift+Alt+A")
        self.add_col_action.triggered.connect(self.AC_func)
        
        self.open_color_dialog_action = QAction(QIcon(QPixmap('Assets/Images/ColorBar.png')), "Open Color Dialog (Shift+Alt+C)")
        self.open_color_dialog_action.setShortcut("Shift+Alt+C")
        self.open_color_dialog_action.triggered.connect(self.change_cell_color_func)
        
        self.set_validation_action = QAction(QIcon(QPixmap('Assets/Images/validation.png')), "Set Validation For Columns (Shift+Alt+V)")
        self.set_validation_action.setShortcut("Shift+Alt+V")
        self.set_validation_action.triggered.connect(self.set_validation_func)
        
        self.open_chart_action = QAction(QIcon(QPixmap('Assets/Images/Chart.png')), "Show Chart (Shift+Alt+G)")
        self.open_chart_action.setShortcut("Shift+Alt+G")
        self.open_chart_action.triggered.connect(self.open_chart_func)
        
        self.save_table_action = QAction(QIcon(QPixmap('Assets/Images/save.png')), "Save Table (Ctrl+S)")
        self.save_table_action.setShortcut("Ctrl+S")
        self.save_table_action.triggered.connect(self.save_table_func)
        
        self.refresh_table_action = QAction(QIcon(QPixmap('Assets/Images/Refresh.png')), "Refresh Table (Ctrl+R)")
        self.refresh_table_action.setShortcut("Ctrl+R")
        self.refresh_table_action.triggered.connect(self.Refresh)
        
        self.del_row_or_col_button = QAction(QIcon(QPixmap('Assets/Images/delete.png')), "Delete Row or Column (Ctrl+D)")
        self.del_row_or_col_button.setShortcut("Ctrl+D")
        self.del_row_or_col_button.triggered.connect(self.del_row_or_col)
        
        self.new_Table_button = QAction(QIcon(QPixmap('Assets/Images/AddTable.png')), "New Table (Ctrl+N)")
        self.new_Table_button.setShortcut("Ctrl+N")
        self.new_Table_button.triggered.connect(self.new_table)
        
        self.exp_button = QAction(QIcon(QPixmap('Assets/Images/Export.png')), "Export Selected Table (Ctrl+Alt+E)")
        self.exp_button.setShortcut("Ctrl+Alt+E")
        self.exp_button.triggered.connect(lambda:self.exp_tbl(self.Tables_combo_box.currentText()))
        
        
        self.dbtoct_button = QAction(QIcon(QPixmap('Assets/Images/Convert.png')), "convert Sql file to custom table (Ctrl+Alt+Q)")
        self.dbtoct_button.setShortcut("Ctrl+Alt+Q")
        self.dbtoct_button.triggered.connect(self.dbtoct)
        
        self.clear_act = QAction(QIcon(QPixmap('Assets/Images/Clear.png')), "Clear All Data (Ctrl+Alt+C)")
        self.clear_act.setShortcut("Ctrl+Alt+C")
        self.clear_act.triggered.connect(self.Clear_func)
        

         
        # Add Actions to Toolbar
        if self.TableData != {"Table_name": "", "Columns": [], "Rows_data": [], "Primary_status": [], "Columns_Charts_index": []}:
            self.toolbar.addActions([self.add_row_action, self.open_color_dialog_action, self.clear_act, self.set_validation_action, self.add_col_action, self.open_chart_action, self.save_table_action, self.refresh_table_action, self.del_row_or_col_button, self.new_Table_button, self.dbtoct_button])
        else:
            self.toolbar.addActions([self.add_row_action, self.add_col_action, self.refresh_table_action, self.new_Table_button, self.dbtoct_button])
            
        
        self.toolbar.addSeparator()
        
        
        
        
        # delete chart combo box and buttons
        if self.TableData != {"Table_name": "", "Columns": [], "Rows_data": [], "Primary_status": [], "Columns_Charts_index": []}:
            self.delete_chart_combo_box = QComboBox()
            self.delete_chart_combo_box.addItems(["Select Chart to Delete", "All Charts"])
            for chart in self.TableData['Columns_Charts_index']:
                self.delete_chart_combo_box.addItem(f"{self.TableData['Columns'][chart[0]][0]}")    
            self.delete_chart_combo_box.setCurrentText("Select Chart to Delete")
        
            self.delete_chart_button = QAction(QIcon(QPixmap('Assets/Images/delete.png')), "Delete Chart")
            self.delete_chart_button.triggered.connect(lambda:self.delete_charts_func(self.delete_chart_combo_box.currentText()))
            self.toolbar.addWidget(self.delete_chart_combo_box)
            self.toolbar.addAction(self.delete_chart_button)
            self.toolbar.addSeparator()
        else:
            pass
        
        
        
        
        
        # all Tables
        self.Tables_combo_box = QComboBox()
        self.toolbar.addWidget(self.Tables_combo_box)
        if PRR.Get_Saved_Tables() == []:
            self.Tables_combo_box.addItems(["No Saved Table To Select"])
            self.Tables_combo_box.setCurrentText("No Saved Table To Select")
        else:
            self.Tables_combo_box.addItems(["Select Table", "All", "Current Table"])
            self.Tables_combo_box.addItems([n['Table_name'] for n in PRR.Get_Saved_Tables()])
            self.Tables_combo_box.setCurrentText("Select Table")
        
            # open table button
            self.open_button = QAction(QIcon(QPixmap('Assets/Images/Open.png')), "Open Table (Ctrl+O)")
            self.open_button.triggered.connect(lambda : self.open_table(self.Tables_combo_box.currentText()))
            self.open_button.setShortcut("Ctrl+O")
            
            # delete table button
            self.del_button = QAction(QIcon(QPixmap('Assets/Images/Delete3.png')), "Delete Table (Ctrl+Shift+D)")
            self.del_button.triggered.connect(lambda : self.del_tbl(self.Tables_combo_box.currentText()))
            self.del_button.setShortcut("Ctrl+Shift+D")
            
            
            self.toolbar.addAction(self.open_button)
            self.toolbar.addAction(self.del_button)
            self.toolbar.addAction(self.exp_button)
        
        
        # Table name input
        if self.TableData != {"Table_name": "", "Columns": [], "Rows_data": [], "Primary_status": [], "Columns_Charts_index": []}:
            self.toolbar.addSeparator()
            
            self.table_name_input_label = QLabel("Table Name:")
            self.table_name_input_label.setStyleSheet("font-size: 20px;font-weight: bold;color: #ffffff;")
            self.toolbar.addWidget(self.table_name_input_label)
            self.table_name_input = QLineEdit()
            self.table_name_input.setPlaceholderText("Enter Table Name")
            self.table_name_input.setAlignment(Qt.AlignCenter)
            if self.TableData['Table_name'].strip() != '':
                self.table_name_input.setText(self.TableData['Table_name'])
            self.toolbar.addWidget(self.table_name_input)
        else:
            pass
        
    def BottomToolbarUI(self):
        # Bottom Toolbar
        self.bottom_toolbar = QToolBar()
        self.bottom_toolbar.setMovable(False)
        self.bottom_toolbar.setFloatable(False)
        self.bottom_toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.bottom_toolbar.setOrientation(Qt.Horizontal)
        self.addToolBar(Qt.BottomToolBarArea, self.bottom_toolbar)
        
        # Labels
        self.row_and_col_selected_label = QLabel("selected row: None, selected column: None")
        self.row_and_col_selected_label.setAlignment(Qt.AlignCenter)
        self.row_and_col_selected_label.setStyleSheet("font-size: 15px;margin-top: 2px;color: #ffffff;font-weight: bold;")
        self.bottom_toolbar.addWidget(self.row_and_col_selected_label)
    
    def Refresh(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                try:
                    attr.deleteLater()
                except:
                    pass
        # Delete Dock if exists
        if hasattr(self, 'dock'):
            self.dock.deleteLater()
            
        # Remake
        self.ToolbarUI()
        self.BottomToolbarUI()
        self.UI()
       
    def AR_func(self):
        if len(self.TableData["Primary_status"]) == 0:
            if len(self.TableData["Columns"]) > 0 :
                row = []
                for i, c in enumerate(self.TableData["Columns"]):
                    row.append("NULL")
                self.TableData["Rows_data"].append(row)
            else:
                text_to_speech("please add columns first to add row")
        if len(self.TableData["Primary_status"]) != 0:
            if len(self.TableData["Columns"]) > 0 :
                row = []
                for i, c in enumerate(self.TableData["Columns"]):
                    if c[1] == "Primary":
                        row.append(int(self.TableData["Rows_data"][-1][i])+1)
                    else:
                        row.append("NULL")
                self.TableData["Rows_data"].append(row)
            else:
                text_to_speech("please add columns first to add row")
        self.Refresh()
        
    def AC_func(self):
        # Show Dialog
        dialog = QDialog(self)
        dialog.setFixedSize(300, 450)
        dialog.setStyleSheet("background-color: #333333;")
        dialog.setWindowOpacity(0.9)
        dialog.setWindowFlag(Qt.FramelessWindowHint)
        # Layout
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)
        # Label
        label = QLabel("Enter Column Name:")
        label.setStyleSheet("font-size: 20px;color: #ffffff;font-weight: bold;")
        dialog_layout.addWidget(label)
        # Line Edit
        line_edit = QLineEdit()
        line_edit.setStyleSheet("background-color: #444444;color: #ffffff;")
        dialog_layout.addWidget(line_edit)
        # combo box and its label
        label = QLabel("Column Type:")
        label.setStyleSheet("font-size: 20px;color: #ffffff;font-weight: bold;")
        dialog_layout.addWidget(label)
        combo_box = QComboBox()
        combo_box.setStyleSheet("background-color: #444444;color: #ffffff;")
        combo_box.addItems(["Primary", "Free", "String", "Integer"])
        combo_box.setCurrentText("Free")
        dialog_layout.addWidget(combo_box)
        
        # bg color choose widgets
        bg_color_label = QLabel("Background Color:")
        bg_color_label.setStyleSheet("font-size: 20px;color: #ffffff;font-weight: bold;")
        dialog_layout.addWidget(bg_color_label)
        bg_color_widget = CI()
        dialog_layout.addWidget(bg_color_widget)
        
        # text color choose widgets
        tx_color_label = QLabel("Text Color:")
        tx_color_label.setStyleSheet("font-size: 20px;color: #ffffff;font-weight: bold;")
        dialog_layout.addWidget(tx_color_label)
        tx_color_widget = CI("#000000")
        dialog_layout.addWidget(tx_color_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        dialog_layout.addLayout(button_layout)
        # OK Button
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: #444444;color: #ffffff;")
        ok_button.clicked.connect(lambda: self.add_column(line_edit.text(), combo_box.currentText(),  bg_color_widget.GetColor(), tx_color_widget.GetColor(), dialog))
        button_layout.addWidget(ok_button)
        # Cancel Button
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("background-color: #444444;color: #ffffff;")
        cancel_button.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_button)
        # Show Dialog
        dialog.exec_()
    
    def add_column(self, column_name, type, bg, fg, dialog):
        if column_name.strip() != "":
            # Check if column already exists
            for column in self.TableData["Columns"]:
                if column[0] == column_name:
                    text_to_speech("column already exists")
                    dialog.close()
                    self.Refresh()
                    return
            # Add column to Columns list
            self.TableData["Columns"].append([str(column_name), str(type), str(bg), str(fg)])
            # Add column to Rows_data
            for i in range(len(self.TableData["Rows_data"])):
                self.TableData["Rows_data"][i].append("NULL")
            # Refresh Table
            dialog.close()
            self.Refresh()
        else:
            text_to_speech("Invalid column name")
            dialog.close()
            self.Refresh()
        
    def ItemClick(self, row, column):
        self.selected_row = row
        self.selected_column = column
        self.row_and_col_selected_label.setText(f"selected row: {row+1}, selected column: {column+1}")
        
    def row_click(self, row):
        self.selected_column = None
        self.selected_row = row
        self.row_and_col_selected_label.setText(f"selected row: {row+1}, selected column: None")
        
    def column_click(self, column):
        self.selected_row = None
        self.selected_column = column
        self.row_and_col_selected_label.setText(f"selected row: None, selected column: {column+1}")
    
    def change_color_of_a_col(self, col, bg, fg, dialog):
        self.TableData['Columns'][col][2] = str(bg)
        self.TableData['Columns'][col][3] = str(fg)
        dialog.close()
        self.Refresh()
    
    def change_cell_color_func(self):
        row = self.selected_row
        column = self.selected_column
        
        # A cell selected
        if row is not None and column is not None:
            # change color of a cell
            pass
        
        # A column selected
        if row is None and column is not None:
            try:
            
                # Show Dialog
                dialog = QDialog(self)
                dialog.setFixedSize(300, 450)
                dialog.setStyleSheet("background-color: #333333;")
                dialog.setWindowOpacity(0.9)
                dialog.setWindowFlag(Qt.FramelessWindowHint)
                # Layout
                dialog_layout = QVBoxLayout()
                dialog.setLayout(dialog_layout)
                
                # bg color choose widgets
                bg_color_label = QLabel("Background Color:")
                bg_color_label.setStyleSheet("font-size: 20px;color: #ffffff;font-weight: bold;")
                dialog_layout.addWidget(bg_color_label)
                bg_color_widget = CI()
                dialog_layout.addWidget(bg_color_widget)
                
                # text color choose widgets
                tx_color_label = QLabel("Text Color:")
                tx_color_label.setStyleSheet("font-size: 20px;color: #ffffff;font-weight: bold;")
                dialog_layout.addWidget(tx_color_label)
                tx_color_widget = CI("#000000")
                dialog_layout.addWidget(tx_color_widget)
                
                
                # Buttons
                button_layout = QHBoxLayout()
                dialog_layout.addLayout(button_layout)
                # OK Button
                ok_button = QPushButton("OK")
                ok_button.setStyleSheet("background-color: #444444;color: #ffffff;")
                ok_button.clicked.connect(lambda: self.change_color_of_a_col(column, bg_color_widget.GetColor(), tx_color_widget.GetColor(), dialog))
                button_layout.addWidget(ok_button)
                # Cancel Button
                cancel_button = QPushButton("Cancel")
                cancel_button.setStyleSheet("background-color: #444444;color: #ffffff;")
                cancel_button.clicked.connect(dialog.close)
                button_layout.addWidget(cancel_button)
                # Show Dialog
                dialog.exec_()
            except:
                text_to_speech("Color Changing Faild")
            
        # a row selected
        if row is not None and column is None:
            text_to_speech("select a column to change its color")
        
        # Nothing selected
        if row is None and column is None:
            text_to_speech("select a column to change its color")
       
    def set_validation_func(self, cr=None):
            
        if self.selected_row is None and self.selected_column is not None:
            # show choose validation type dialog
            dialog = QDialog(self)
            dialog.setFixedSize(300, 260)
            dialog.setStyleSheet("background-color: #333333;")
            dialog.setWindowOpacity(0.9)
            dialog.setWindowFlag(Qt.FramelessWindowHint)
            # Create a layout for the dialog
            layout = QVBoxLayout(dialog)
            # Create a label for the dialog
            label = QLabel("Choose Validation Type:")
            label.setStyleSheet("color: #ffffff;")
            layout.addWidget(label)
            # Create a combo box for the dialog
            combo_box = QComboBox()
            combo_box.addItems(["Free", "String", "Integer", "Primary"])
            combo_box.setStyleSheet("background-color: #444444;color: #ffffff;")
            combo_box.setCurrentText(self.TableData['Columns'][self.selected_column][1])
            layout.addWidget(combo_box)
            # Create a button for the dialog
            button = QPushButton("OK")
            button.setStyleSheet("background-color: #444444;color: #ffffff;")
            layout.addWidget(button)
            button.clicked.connect(lambda: self.set_validation(combo_box.currentText(), dialog))
            # Cancel button
            cancel_button = QPushButton("Cancel")
            cancel_button.setStyleSheet("background-color: #444444;color: #ffffff;")
            layout.addWidget(cancel_button)
            cancel_button.clicked.connect(dialog.close)
                
            # set dialog to center of screen
            dialog.move(self.geometry().center() - dialog.rect().center())
            # set dialog to be on top of all windows
            dialog.setWindowModality(Qt.ApplicationModal)
                
                
            # show dialog
            dialog.exec_()
                
        else:
            text_to_speech("Please select a columns first")
              
    def set_validation(self, validation_type, dialog):
        # set validation type for the selected column
        if self.selected_column is not None:
            self.TableData['Columns'][self.selected_column][1] = validation_type
            self.Refresh()
            dialog.close()
        
    def cell_changed_func(self, row, column):
        try:
            # get the value of the cell
            value = self.Table.item(row, column).text()
            # validation and set the value of the cell
            if self.TableData['Columns'][column][1] == 'Primary':
                self.Refresh()
            if self.TableData['Columns'][column][1] == 'Free':
                self.TableData['Rows_data'][row][column] = value
                self.Refresh()
            if self.TableData['Columns'][column][1] == 'String':
                if value.isalpha():
                    self.TableData['Rows_data'][row][column] = value
                    self.Refresh()
                else:
                    self.Refresh()
                    text_to_speech("Please enter a string")
            if self.TableData['Columns'][column][1] == 'Integer':
                if value.isdigit():
                    self.TableData['Rows_data'][row][column] = int(value)
                    self.Refresh()
                else:
                    self.Refresh()
                    text_to_speech("Please enter an integer")
        except Exception as e:
            text_to_speech("Problem in setting the value of the cells")
            self.Refresh()
        
    def chart_error(self, txt):
        text = "error in showing chart" + "\n" + str(txt)
        text_to_speech(text)
        self.chart_widget.close()
        self.chart_dock.close()
    
    def selected_radio_button_changed(self, button):
        self.selected_chart_type = button.text()
    
    def open_chart_func(self):
        
        if self.selected_row is None and self.selected_column is not None:
            # show dialog to select chart type
            dialog = QDialog(self)
            dialog.setWindowFlag(Qt.FramelessWindowHint)
            dialog.setFixedSize(300, 300)
            dialog.setWindowOpacity(0.9)
            
            # Create a layout for the dialog
            layout = QVBoxLayout(dialog)
            
            # Create a label for the dialog
            label = QLabel("Choose Chart Type:")
            layout.addWidget(label)
            
            # Create radio buttons for the dialog
            radio_buttons = []
            for i, tp in enumerate(['Bar', 'Pie', 'Plot', 'Scatter']):
                radio_button = QRadioButton(tp)
                # change selected radio button variable when each radio button is clicked
                radio_button.clicked.connect(lambda checked, radio_button=radio_button: self.selected_radio_button_changed(radio_button))
                radio_button.setChecked(False)
                radio_buttons.append(radio_button)
                # set icon for radio button
                radio_button.setIcon(QIcon(f"Assets/Images/{tp.title()}.png"))
                layout.addWidget(radio_buttons[i])
            
            
            # Create a button for the dialog
            button = QPushButton("OK")
            layout.addWidget(button)
            button.clicked.connect(lambda: self.open_chart(dialog))
            
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
            
        elif self.selected_row is None and self.selected_column is None:
            pass
               
        else:
            text_to_speech("Please select a columns first to show or click on chart button")
            
    def open_chart(self, dialog=None):
        if self.selected_chart_type is not None:
            if dialog is not None:
                dialog.close()
            ChartType = self.selected_chart_type
            
            # set the chart widget
            # get all cells data of selected column
            column_data = [row[self.selected_column] for row in self.TableData['Rows_data'] if str(row[self.selected_column]).isnumeric()]
            if len(column_data) == 0:
                text_to_speech("No valid data to show")
                self.Refresh()
            else:
                self.add_col_chart_to_DB(ChartType, self.selected_column)
                self.Refresh()         

        else:
            dialog.close()
            self.Refresh()
            text_to_speech("Please select a chart type first")
    
    def add_col_chart_to_DB(self, ct, col):
        # check if the chart is already in the data
        exist = False
        for i, cci in enumerate(self.TableData['Columns_Charts_index']):
            if cci[0] == col :
                exist = True
                self.TableData['Columns_Charts_index'][i][1] = ct
                break
        if exist == False:
            self.TableData['Columns_Charts_index'].append([col, ct])
            self.Refresh()

    def create_all_charts(self, data):
        # destroy all charts dock widgets
        for dock in self.findChildren(QDockWidget):
            dock.close()
            dock.deleteLater()
               
        for chart in data:
            # create dock widget
            dock_widget = QDockWidget()
            # set context menu
            dock_widget.setContextMenuPolicy(Qt.PreventContextMenu)
            dock_widget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
            dock_widget.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
            dock_widget.setWindowTitle("chart")
            # create chart widget
            chart_widget = chart
            dock_widget.setWidget(chart_widget)
            # add chart widget to dock widget
            self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
            
    def save_table_func(self):
        tn = self.table_name_input.text()
        if tn.strip() != "":
            if len(self.TableData['Columns']) != 0:
                self.TableData['Table_name'] = tn
                # add table data to json file
                PRR.AddCustomTableToJsonFile(self.TableData)
                self.Refresh()
            else:
                text_to_speech("Table is null")
                self.Refresh()
        
        else:
            text_to_speech("Please enter a table name")
            self.Refresh()
    
    def delete_charts_func(self, col):
        if col == "All Charts":
            self.TableData['Columns_Charts_index'] = []
            text_to_speech("All Charts deleted successfully")
            self.Refresh()    
        if col == "Select Chart to Delete":
            text_to_speech("Please select a chart to delete")
            self.Refresh()
        if col != "All Charts" and col != "Select Chart to Delete":
            # get charts columns names and indexes
            charts_cols_name = {}
            for ch in self.TableData['Columns_Charts_index']:
                charts_cols_name[self.TableData['Columns'][ch[0]][0]] = ch[0]
        
            # delete chart from data
            for ch in self.TableData['Columns_Charts_index']:
                if int(ch[0]) == int(charts_cols_name[col]):
                    self.TableData['Columns_Charts_index'].remove(ch)
            text_to_speech("Chart deleted successfully")
            self.Refresh()
    
    
    def del_row_or_col(self):
        row = self.selected_row
        col = self.selected_column
        if row is not None and col is not None:
            text_to_speech("select a column or row to delete")
        if row is None and col is None:
            text_to_speech("select a column or row to delete")
        # delete row
        if row is not None and col is None:
            self.TableData['Rows_data'].pop(row)
            self.Refresh()
        
        # delete column            
        if row is None and col is not None:
            self.TableData['Columns'].remove(self.TableData['Columns'][col])
            for i, r in enumerate(self.TableData['Rows_data']):
                self.TableData['Rows_data'][i].pop(col)
            self.Refresh()
                
            
    def new_table(self):
        try:
            tn = self.table_name_input.text()
            if tn.strip() != "":
                if len(self.TableData['Columns']) != 0:
                    self.TableData['Table_name'] = tn
                    # add table data to json file
                    PRR.add_to_Saved_Tables(self.TableData)
                    self.TableData = {
                        "Table_name": "",
                        "Columns": [],
                        "Rows_data": [],
                        "Primary_status": [],
                        "Columns_Charts_index": []
                    }
                    PRR.AddCustomTableToJsonFile(self.TableData)
                    self.Refresh()
                else:
                    self.TableData = {
                        "Table_name": "",
                        "Columns": [],
                        "Rows_data": [],
                        "Primary_status": [],
                        "Columns_Charts_index": []
                    }
                    PRR.AddCustomTableToJsonFile(self.TableData)
                    self.Refresh()
            
            else:
                text_to_speech("Please enter a table name")
                self.Refresh()
        except:
            pass 
    def open_table(self, tbl):
        if tbl == "All":
            text_to_speech("You Can't Open All Table")
            return
        if tbl == "Select Table":
            text_to_speech("Select a Table first to open")
            return
        if tbl == 'Current Table':
            text_to_speech("Current Table is open now")
            return
        if tbl != "Select Table" and tbl != "All" and tbl != 'Current Table':
            for i, n in enumerate(PRR.Get_Saved_Tables()):
                if n["Table_name"] == tbl:
                    self.TableData = PRR.Get_Saved_Tables()[i]
                    break
            self.Refresh()
    
    def del_tbl(self, tbl):
        if tbl == "All":
            res = PRR.del_saved_Table_by_index("All")
            if res:
                text_to_speech("All Tables Deleted successful")
            else:
                text_to_speech("Delete failed")
            self.TableData = {
                    "Table_name": "",
                    "Columns": [],
                    "Rows_data": [],
                    "Primary_status": [],
                    "Columns_Charts_index": []
                }
            self.Refresh()
        if tbl == "Select Table":
            text_to_speech("Select a Table first to Delete")
            return
        if tbl == 'Current Table':
            self.TableData = {
                    "Table_name": "",
                    "Columns": [],
                    "Rows_data": [],
                    "Primary_status": [],
                    "Columns_Charts_index": []
                }
            self.Refresh()
        if tbl != "Select Table" and tbl != "All" and tbl != 'Current Table':
            for i, n in enumerate(PRR.Get_Saved_Tables()):
                if n["Table_name"] == tbl:
                    res = PRR.del_saved_Table_by_index(int(i))
                    if res:
                        text_to_speech("Table Deleted successful")
                    else:
                        text_to_speech("Delete failed")
                    break
            self.Refresh()
          
    def exp_tbl(self, tbl):
        if tbl == "All":
            text_to_speech("You Can't Export All Tables At Once")
            return
        if tbl == "Select Table":
            text_to_speech("Select a Table first to Print")
            return
        if tbl == 'Current Table':
            return
        if tbl != "Select Table" and tbl != "All" and tbl != 'Current Table':
            dt = None
            for i, n in enumerate(PRR.Get_Saved_Tables()):
                if n["Table_name"] == tbl:
                    dt = PRR.Get_Saved_Tables()[int(i)]
                    break
            heads = []
            name = dt['Table_name']
            
            for ih, h in enumerate(dt['Columns']):
                heads.append(h[0])
            
            df = {}
            for hi, hn in enumerate(heads):
                df[str(hn)] = [row[hi] for row in dt['Rows_data']]                
            df = pd.DataFrame(df)
            
            # show the dialog to get the dir to save the file
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;JSON File (*.json);;HTML File (*.html);;SQL File (*.db)", options=options)
            if fileName:
                if fileName.endswith('.csv'):
                    df.to_csv(fileName, index=False)
                    text_to_speech("File Saved Successfully")
                elif fileName.endswith('.json'):
                    df.to_json(fileName, orient='records')
                    text_to_speech("File Saved Successfully")
                elif fileName.endswith('.html'):
                    df.to_html(fileName, index=False)
                    text_to_speech("File Saved Successfully")
                elif fileName.endswith('.db'):
                    df.to_sql(name, con=sqlite3.connect(fileName), if_exists='replace', index=False)
                    text_to_speech("File Saved Successfully")
                else:
                    text_to_speech("Invalid file format")
            else:
                text_to_speech("File not saved")
            self.Refresh()
            
    
    def FileDialog(self, btn):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a file", "C:\\Users", "SQL Files (*.db)")
        if fileName:
            btn.setText(fileName)
            return True
            
    def dbtoct(self):
        db_address = None
        # open dialog to get file to convert a table or all tables of sql file to custom table
        dialog = QDialog(self)
        dialog.setWindowFlag(Qt.FramelessWindowHint)
        dialog.setFixedSize(320, 400)
        dialog.setWindowOpacity(1)
                
        # Create a layout for the dialog
        layout = QVBoxLayout(dialog)
            
        # Widgets
        header = QLabel(f"SQL Table To Custom Table")
        layout.addWidget(header)
        
        
        table_name_label = QLabel(f"Table Name:")
        layout.addWidget(table_name_label)
        
        table_name_tb = QLineEdit()
        layout.addWidget(table_name_tb)
        
        name_label = QLabel(f"*Custom Name:")
        layout.addWidget(name_label)
        
        name_tb = QLineEdit()
        layout.addWidget(name_tb)
        
        
            
        all_table_chackbox = QCheckBox('All Tables')
        def all_table_chackbox_click():
            if all_table_chackbox.isChecked():
                table_name_tb.setHidden(True)
                table_name_label.setHidden(True)
                name_tb.setHidden(True)
                name_label.setHidden(True)
            else:
                table_name_tb.setHidden(False)
                table_name_label.setHidden(False)
                name_tb.setHidden(False)
                name_label.setHidden(False)
                table_name_tb.clear()
                name_tb.clear()
                ch_button.setText('Choose SQL File ')
                table_name = None
        all_table_chackbox.clicked.connect(all_table_chackbox_click)
        layout.addWidget(all_table_chackbox)
        
            
        ch_button = QPushButton("Choose SQL File ")
        def ch_button_ck():
            global db_address
            res = self.FileDialog(ch_button)
            if res :
                db_address = ch_button.text()
        ch_button.clicked.connect(ch_button_ck)
            
        layout.addWidget(ch_button)
                
           
        sub_button = QPushButton("Submit")
        layout.addWidget(sub_button)
        def submit():
            try:
                global db_address 
                table_name = table_name_tb.text()
                if table_name_tb.isHidden():
                    table_name = True
                if db_address:
                    if table_name != None:
                        if table_name == True:
                            # convert all tables of db file to custom table
                            if name_tb.text().strip() != '':
                                cn = name_tb.text().strip()
                            else:
                                cn = None
                                
                            try:
                                for tbl in PRR.GetTablesOfAsqlFile(db_address):
                                    table = PRR.SQL_Table_to_custom_data(db_address=db_address, table_name=tbl, table_custom_name=tbl)
                                    PRR.add_to_Saved_Tables(table)
                                self.Refresh()
                                text_to_speech('all converting  successfull')
                                dialog.close()
                                return
                            except:
                                text_to_speech('converting faild')
                                table_name_tb.setHidden(True)
                                table_name_tb.clear()
                                table_name_label.setHidden(True)
                                name_tb.setHidden(True)
                                name_tb.clear()
                                name_label.setHidden(True)
                                ch_button.setText('Choose SQL File ')
                                return
                                
                                
                        else:
                            # convert one tables of db file to custom table
                            if name_tb.text().strip() != '':
                                cn = name_tb.text().strip()
                            else:
                                cn = None
                            try:  
                                table = PRR.SQL_Table_to_custom_data(db_address=db_address, table_name=table_name, table_custom_name=cn)
                                PRR.add_to_Saved_Tables(table)
                                self.Refresh()
                                text_to_speech('converting  successfull')
                                dialog.close()
                                return
                            except:
                                text_to_speech('converting faild')
                                table_name_tb.setHidden(True)
                                table_name_tb.clear()
                                table_name_label.setHidden(True)
                                name_tb.setHidden(True)
                                name_tb.clear()
                                name_label.setHidden(True)
                                ch_button.setText('Choose SQL File ')
                                return
                                
                            
                    else:
                        text_to_speech('enter table name')
                        table_name_tb.setHidden(True)
                        table_name_tb.clear()
                        table_name_label.setHidden(True)
                        name_tb.setHidden(True)
                        name_tb.clear()
                        name_label.setHidden(True)
                        ch_button.setText('Choose SQL File ')
                        
                else:
                    text_to_speech('select a SQL file first')
                    table_name_tb.setHidden(True)
                    table_name_tb.clear()
                    table_name_label.setHidden(True)
                    name_tb.setHidden(True)
                    name_tb.clear()
                    name_label.setHidden(True)
                    ch_button.setText('Choose SQL File ')
            except:
                self.Refresh()
                text_to_speech('Converting Faild')
                dialog.close()
                return
                
                     
        sub_button.clicked.connect(submit)    
                
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

        
    def Clear_func(self):
        self.TableData = {"Table_name": "", "Columns": [], "Rows_data": [], "Primary_status": [], "Columns_Charts_index": []}
        self.Refresh()
            
            
            