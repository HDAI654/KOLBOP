from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from BLL.PublicRrep import PRR
from PL.Products.AP_win import APW
from PL.Products.SE_win import EPW

class PW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search_combo_index = 0
        self.search_input_text = ""
        self.HEADS = ["ID", "Name", "Supplier", "Unit", "Amount", "Buy Price", "Sale Price", "Delete Tool", "Show/Edit"]
        self.StackUI()
        self.ToolbarUI()
        self.TableUI()      
    def StackUI(self):
        # create main layers
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Create Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create Frames
        self.table_frame = QMainWindow()
        self.add_frame = APW(self.apw_close)
        self.edit_show_frame = QMainWindow()

        # Add Frames to Stacked Widget
        self.stacked_widget.addWidget(self.table_frame)
        self.stacked_widget.addWidget(self.add_frame)
        self.stacked_widget.addWidget(self.edit_show_frame)
        self.stacked_widget.setCurrentIndex(0)
    def ToolbarUI(self):
        # Toolbar
        self.toolbar = QToolBar("Products Page Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.table_frame.addToolBar(self.toolbar)

        # Icon
        self.Icon = QLabel()
        self.Icon.setPixmap(QPixmap("Assets/Images/Products.png"))
        self.Icon.setAlignment(Qt.AlignCenter)
        self.toolbar.addWidget(self.Icon)
        self.toolbar.addSeparator()

        # Actions
        self.delete_all_action = QAction(QIcon(QPixmap("Assets/Images/Delete All.png")), "Delete All Products (Ctrl+Alt+D)", self)
        self.delete_all_action.setShortcut("Ctrl+Alt+D")
        self.delete_all_action.triggered.connect(self.DeleteAll)
        self.toolbar.addAction(self.delete_all_action)

        self.refresh_action = QAction(QIcon(QPixmap("Assets/Images/Refresh.png")), "Refresh (Ctrl+R)", self)
        self.refresh_action.setShortcut("Ctrl+R")
        self.refresh_action.triggered.connect(self.RefreshAll)
        self.toolbar.addAction(self.refresh_action)

        self.add_action = QAction(QIcon(QPixmap("Assets/Images/Add2.png")), "Add New Product (Ctrl+N)", self)
        self.add_action.setShortcut("Ctrl+N")
        self.add_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.toolbar.addAction(self.add_action)


        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setPlaceholderText("Search")
        self.search_input.setText(self.search_input_text)
        self.search_input.textChanged.connect(self.Search)
        self.toolbar.addWidget(self.search_input)

        self.toolbar.addSeparator()

        # Search ComboBox
        self.search_combo = QComboBox()
        self.search_combo.addItems(["All", "ID", "Name", "Supplier", "Unit", "Amount", "Buy Price", "Sale Price"])
        self.search_combo.setCurrentIndex(self.search_combo_index)
        self.search_combo.currentIndexChanged.connect(self.ComboChange)
        self.toolbar.addWidget(self.search_combo)
    def TableUI(self):
        # create table of clients info
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.HEADS))
        self.table_widget.setHorizontalHeaderLabels(self.HEADS)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_frame.setCentralWidget(self.table_widget)

        # Do search
        self.Search()
    def Search(self):
        # set new data of input
        self.search_input_text = self.search_input.text()

        # Get Table Data
        table_data = list(PRR.SelectProducts("true"))
        
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
                        if PRR.Filter(search_text, row[0]) or PRR.Filter(search_text, row[1]) or PRR.Filter(search_text, row[2]) or PRR.Filter(search_text, row[3]) or PRR.Filter(search_text, row[4]) or PRR.Filter(search_text, row[5]) or PRR.Filter(search_text, row[6]):
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
                self.FillTable(data=list(PRR.SelectProducts("true")))
    def FillTable(self, data):
        if data != None :
            self.table_widget.setRowCount(len(data))

            # Set Data
            for row in range(len(data)):
                for column in range(len(data[row])):
                    self.table_widget.setItem(row, column, QTableWidgetItem(str(data[row][column])))

            # Set Delete Buttons
            for row_index, row_data in enumerate(data):
                button = QPushButton("Delete")
                #button.setStyleSheet("""""")
                self.table_widget.setCellWidget(row_index, 7, button)
                button.clicked.connect(lambda checked, row=row_index, id=row_data[0]: self.DeleteProduct(row, id))
            
            # Set Show/Edit Buttons
            for row_index, row_data in enumerate(data):
                button = QPushButton("Show/Edit")
                #button.setStyleSheet("""""")
                self.table_widget.setCellWidget(row_index, 8, button)
                button.clicked.connect(lambda checked, row=row_index, id=row_data[0]: self.ShowEdit(row, id))
    def ComboChange(self):
        self.search_combo_index = self.search_combo.currentIndex()
        if self.search_input.text().strip() != "" :
            self.Search()
    def RefreshAll(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                attr.deleteLater()
        # Remake
        self.search_input_text = ""

        self.StackUI()
        self.ToolbarUI()
        self.TableUI()
    def Refresh(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                attr.deleteLater()
        # Remake
        self.StackUI()
        self.ToolbarUI()
        self.TableUI()
    def DeleteAll(self):
        PRR.Delete("Products", "true")
        self.RefreshAll()
    def DeleteProduct(self, row, id):
        PRR.Delete("Products", f"ID={int(id)}")
        self.Refresh()

    def apw_close(self):
        self.stacked_widget.setCurrentIndex(0)
        self.RefreshAll()
    def shw_close(self):
        self.stacked_widget.setCurrentIndex(0)
        self.RefreshAll()
    def ShowEdit(self, row, id):
        self.stacked_widget.removeWidget(self.edit_show_frame)
        self.edit_show_frame = EPW(int(id), self.shw_close)
        self.stacked_widget.addWidget(self.edit_show_frame)
        self.stacked_widget.setCurrentIndex(2)








