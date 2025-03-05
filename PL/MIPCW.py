import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super(MplCanvas, self).__init__(fig)

class Charts(QMainWindow):
    def __init__(self, data, error_func, Title_add=''):
        super().__init__()
        self.data = data
        self.error_func = error_func
        self.Title_add =  Title_add
        
        self.canvas = MplCanvas(self)
        self.setCentralWidget(self.canvas)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def pie(self):
        try:
            self.canvas.ax.clear() 
            d = np.array(self.data)
            self.canvas.ax.pie(d, labels=list(range(1, len(d)+1, 1)), autopct='%1.1f%%')
            self.canvas.ax.set_title(f'Pie Chart - {self.Title_add}')
            self.canvas.draw()
        except Exception as e:
            self.error_func(str(e))

    def bar(self):
        try:
            self.canvas.ax.clear()
            d = np.array(self.data)
            self.canvas.ax.bar(list(range(1, len(d)+1, 1)), d)
            self.canvas.ax.set_title(f'Bar Chart - {self.Title_add}')
            # set range of numbers of x-axis
            self.canvas.ax.set_xticks(list(range(1, len(d)+1, 1)))
            self.canvas.draw()
        except Exception as e:
            self.error_func(str(e))

    def plot(self):
        try:
            self.canvas.ax.clear()
            x =  np.array(self.data[0])
            y =  np.array(self.data[1])
            self.canvas.ax.plot(x, y)
            self.canvas.ax.set_title(f'Line Chart - {self.Title_add}')
            # set range of numbers of x-axis
            self.canvas.ax.set_xticks(list(range(1, len(x)+1, 1)))
            self.canvas.draw()
        except Exception as e:
            self.error_func(str(e))
        
    def scatter(self):
        try:
            self.canvas.ax.clear()
            x =  np.array(self.data[0])
            y =  np.array(self.data[1])
            self.canvas.ax.scatter(x, y)
            self.canvas.ax.set_title(f'Scatter Plot - {self.Title_add}')
            # set range of numbers of x-axis
            self.canvas.ax.set_xticks(list(range(1, len(x)+1, 1)))
            self.canvas.draw()
        except Exception as e:
            self.error_func(str(e))
