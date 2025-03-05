from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
import winsound
from PyQt5.QtTextToSpeech import *

engine = QTextToSpeech()
def text_to_speech(text):
    engine.say(str(text))

class SSTW(QMainWindow):
    def __init__(self, data=[], Page_Name="Buy Services"):
        super().__init__()
        self.setStyleSheet("""
            QLabel{
                    font-size: 14px;
                    font-weight: bold;
                    color: #FFFFFF;
                    background-color: transparent;
                    border: none;
                    alignment: center;
                           }
            """)
        self.HEADS = ["Service Code", "Explanation", "Unit", "Price", "Delete Tool", "Edit Tool"]
        self.Data = data
        self.search_combo_index = 0
        self.search_input_text = ""
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.bs = QPushButton(Page_Name)
        self.bs.setStyleSheet("""
        QPushButton {
                    background-color: #cfa379ff;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #cfa379ff;
                    padding: 5px;
                    margin-bottom: 10px;
                }
        """)
        self.central_layout.addWidget(self.bs)
        self.setCentralWidget(self.central_widget)
        self.ToolbarUI()
        self.SearchToolbarUI()
        self.TableUI()
    
    def TableUI(self):
        # Table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.HEADS))
        self.table_widget.setHorizontalHeaderLabels(self.HEADS)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.central_layout.addWidget(self.table_widget)

        # Do Search
        self.Search()

    def ToolbarUI(self):
        # Toolbar
        self.toolbar = QToolBar("Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addToolBar(self.toolbar)

        # Entry and Label
        self.C_label = QLabel("Service ID :")
        self.C_entry = QComboBox()
        
        # Services IDs
        pis = PRR.Select("ID, Explanation", "Services", "true")
        self.C_entry.addItem("NULL")
        for i in pis:
            self.C_entry.addItem(" - ".join([str(i[0]), str(i[1])]))
        self.C_entry.setCurrentIndex(0)
        self.C_entry.currentIndexChanged.connect(self.C_entry_change)

        self.name_label = QLabel("Explanation :")
        self.name_entry = QLineEdit()

        self.unit_label = QLabel("Unit :")
        self.unit_entry = QLineEdit()

        self.price_label = QLabel("Price :")
        self.price_entry = QLineEdit()
        self.price_entry.setValidator(QIntValidator())

        # Action
        self.add_action = QAction(QIcon(QPixmap("Assets/Images/Add3.png")), "Add", self)
        self.add_action.triggered.connect(self.AddFunc)

        # Add to ToolBar
        self.toolbar.addWidget(self.C_label)
        self.toolbar.addWidget(self.C_entry)
        self.toolbar.addWidget(self.name_label)
        self.toolbar.addWidget(self.name_entry)
        self.toolbar.addWidget(self.unit_label)
        self.toolbar.addWidget(self.unit_entry)
        self.toolbar.addWidget(self.price_label)
        self.toolbar.addWidget(self.price_entry)
        self.toolbar.addAction(self.add_action)
    
    def SearchToolbarUI(self):
        # Toolbar
        self.stoolbar = QToolBar("Search Tools")
        self.stoolbar.setMovable(False)
        self.addToolBar(self.stoolbar)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setPlaceholderText("Search")
        self.search_input.setText(self.search_input_text)
        self.search_input.textChanged.connect(self.Search)
        self.stoolbar.addWidget(self.search_input)

        self.toolbar.addSeparator()

        # Search ComboBox
        self.search_combo = QComboBox()
        self.search_combo.addItems(["All", "Service Code", "Explanation", "Unit", "Price"])
        self.search_combo.setCurrentIndex(self.search_combo_index)
        self.search_combo.currentIndexChanged.connect(self.ComboChange)
        self.stoolbar.addWidget(self.search_combo)
    
    def EditToolbarUI(self, data):
        # Remove existing etoolbar if it exists
        if hasattr(self, 'etoolbar'):
            self.central_layout.removeWidget(self.etoolbar)
            self.etoolbar.deleteLater()
            delattr(self, 'etoolbar')
        # Toolbar
        self.etoolbar = QToolBar("Tools")
        self.etoolbar.setMovable(False)
        self.central_layout.addWidget(self.etoolbar)

        # Icon
        self.Icon = QLabel()
        self.Icon.setToolTip("Edit Row")
        self.Icon.setPixmap(QPixmap("Assets/Images/Edit3.png"))
        self.Icon.setAlignment(Qt.AlignCenter)
        self.etoolbar.addWidget(self.Icon)
        self.etoolbar.addSeparator()

        # close button
        self.close_button = QAction(QIcon(QPixmap("Assets/Images/Close.png")), "Close", self)
        self.close_button.triggered.connect(self.remove_etoolbar)
        self.etoolbar.addAction(self.close_button)

        # Entry and Label
        self.eC_label = QLabel("Services ID :")
        self.eC_entry = QComboBox()
        
        # Products IDs
        pis = PRR.Select("ID, Explanation", "Services", "true")
        self.eC_entry.addItem("NULL")
        for i in pis:
            self.eC_entry.addItem(" - ".join([str(i[0]), str(i[1])]))
        all_items = [self.eC_entry.itemText(i) for i in range(self.eC_entry.count())]
        self.eC_entry.setCurrentText("NULL")
        for i in all_items:
            if str(i).split(' - ')[0].strip() == str(data[0]):
                self.eC_entry.setCurrentText(str(i))
                break
        self.eC_entry.currentIndexChanged.connect(self.eC_entry_change)

        self.ename_label = QLabel("Explanation :")
        self.ename_entry = QLineEdit()
        self.ename_entry.setText(data[1])

        self.eunit_label = QLabel("Unit :")
        self.eunit_entry = QLineEdit()
        self.eunit_entry.setText(data[2])

        self.eprice_label = QLabel("Price :")
        self.eprice_entry = QLineEdit()
        self.eprice_entry.setValidator(QIntValidator())
        self.eprice_entry.setText(str(data[3]))

        if self.eC_entry.currentText() != "NULL":
            self.ename_entry.setReadOnly(True)

        # Action
        self.edit_action = QAction(QIcon(QPixmap("Assets/Images/Edit3.png")), "Add", self)
        self.edit_action.triggered.connect(lambda:self.edit_func(data, [self.eC_entry.currentText().split(' - ')[0], self.ename_entry.text(), self.eunit_entry.text(), self.eprice_entry.text()]))

        # Add to ToolBar
        self.etoolbar.addWidget(self.eC_label)
        self.etoolbar.addWidget(self.eC_entry)
        self.etoolbar.addWidget(self.ename_label)
        self.etoolbar.addWidget(self.ename_entry)
        self.etoolbar.addWidget(self.eunit_label)
        self.etoolbar.addWidget(self.eunit_entry)
        self.etoolbar.addWidget(self.eprice_label)
        self.etoolbar.addWidget(self.eprice_entry)
        self.etoolbar.addAction(self.edit_action)
    
    def AddFunc(self):
        # Add To Data
        if self.name_entry.text() != "" and self.unit_entry.text() != "" and self.price_entry.text() != "":
            self.Data.append([self.C_entry.currentText().split(' - ')[0].strip(), self.name_entry.text(), self.unit_entry.text(), self.price_entry.text()])
        else:
            winsound.MessageBeep()
            text_to_speech("Please fill all the fields")


        # Clear Entry
        self.C_entry.setCurrentIndex(0)
        self.name_entry.clear()
        self.unit_entry.clear()
        self.price_entry.clear()
        # ReFill
        self.Search()
    
    def FillTable(self, data):
        if data != None or len(data) > 0:
            self.table_widget.setRowCount(len(data))

            # Set Data
            for row in range(len(data)):
                for column in range(len(data[row])):
                    self.table_widget.setItem(row, column, QTableWidgetItem(str(data[row][column])))

            # Set Delete Buttons
            for row_index, row_data in enumerate(data):
                button = QPushButton("Delete")
                button.setStyleSheet("""
                QPushButton {
                    background-color: #a0144f;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #a0144f;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #c81861;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #a0144f;
                    padding: 5px;
                }
                """)
                self.table_widget.setCellWidget(row_index, 4, button)
                button.clicked.connect(lambda checked, row=row_index, rd=row_data: self.DelRow(row, rd))
            
            # Set Edit Buttons
            for row_index, row_data in enumerate(data):
                button = QPushButton("Edit")
                button.setStyleSheet("""
                QPushButton {
                    background-color: #04aa6d;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #04aa6d;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #038f5a;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #04aa6d;
                    padding: 5px;
                }
                """)
                self.table_widget.setCellWidget(row_index, 5, button)
                button.clicked.connect(lambda checked, row=row_index, rd=row_data: self.EditRow(row, rd))
    
    def DelRow(self, ri, rd):
        # Delete Row From Table
        for row in self.Data:
            if row == rd:
                self.Data.remove(row)
                break
        # ReFill
        self.Search()
    
    def EditRow(self, ri, rd):
        er = []
        for row in self.Data:
            if row == rd:
                er = row.copy()
                break
        if er != []:
            self.EditToolbarUI(er)
    
    def Search(self):
        # set new data of input
        self.search_input_text = self.search_input.text()

        # Get Table Data
        table_data = self.Data
        
        # Input Text
        search_text = self.search_input.text()

        # End Data After Search
        filtered_data = []

        if table_data != None:

            # Search
            if search_text.strip() != "" :

                # Search By All Field
                if self.search_combo.currentIndex() == 0 :
                    for row in table_data :
                        if PRR.Filter(search_text, row[0]) or PRR.Filter(search_text, row[1]) or PRR.Filter(search_text, row[2]) or PRR.Filter(search_text, row[3]) :
                            if row not in filtered_data:
                                filtered_data.append(row)
                
                # Search By a Field
                else :
                    for row in table_data :
                        if PRR.Filter(search_text, row[self.search_combo.currentIndex()-1]) :
                            if row not in filtered_data:
                                filtered_data.append(row)

                # Fill Table With Filtered Data
                self.FillTable(data=filtered_data)
            
            
            # if search input not filled
            if self.search_input.text().strip() == "" :
                self.FillTable(data=self.Data)
    
    def ComboChange(self):
        self.search_combo_index = self.search_combo.currentIndex()
        if self.search_input.text().strip() != "" :
            self.Search()
    
    def C_entry_change(self):
        if self.C_entry.currentIndex() != 0:
            d = list(PRR.Select(f"Explanation, Unit, Price", "Services", f"ID={self.C_entry.currentText().split(' - ')[0].strip()}")[0])
            if d != None:
                self.name_entry.setText(str(d[0]))
                self.name_entry.setReadOnly(True)
                self.unit_entry.setText(str(d[1]))
                self.price_entry.setText(str(d[2]))
        else:
            # Clear Entry
            self.C_entry.setCurrentIndex(0)
            self.name_entry.clear()
            self.name_entry.setReadOnly(False)
            self.unit_entry.clear()
            self.unit_entry.setReadOnly(False)
            self.price_entry.clear()
            self.price_entry.setReadOnly(False)
    
    def eC_entry_change(self):
        if self.eC_entry.currentIndex() != 0:
            d = list(PRR.Select(f"Explanation, Unit, Price", "Services", f"ID={str(self.eC_entry.currentText().split(' - ')[0]).strip()}")[0])
            if d != None:
                self.ename_entry.setText(str(d[0]))
                self.ename_entry.setReadOnly(True)
                self.eunit_entry.setText(str(d[1]))
                self.eprice_entry.setText(str(d[2]))
        else:
            # Clear Entry
            self.eC_entry.setCurrentIndex(0)
            self.ename_entry.clear()
            self.ename_entry.setReadOnly(False)
            self.eunit_entry.clear()
            self.eunit_entry.setReadOnly(False)
            self.eprice_entry.clear()
            self.eprice_entry.setReadOnly(False)
    
    def edit_func(self, old_data, data):
        if hasattr(self, 'etoolbar'):
            # Destroy etoolbar
            self.central_layout.removeWidget(self.etoolbar)
            self.etoolbar.deleteLater()
            delattr(self, 'etoolbar')

            # Edit Data
            d = [[str(b) for b in i] for i in self.Data]
            od = [str(j) for j in old_data]
            for r in d:
                if r==od:
                    self.Data[d.index(r)] = data
                    break
            # Refresh
            self.Search()
    
    def remove_etoolbar(self):
        if hasattr(self, 'etoolbar'):
            # Destroy etoolbar
            self.central_layout.removeWidget(self.etoolbar)
            self.etoolbar.deleteLater()
            delattr(self, 'etoolbar')
    
    def GetData(self):
        return self.Data

    def clear_table(self):
        self.Data = []
        self.Search()
