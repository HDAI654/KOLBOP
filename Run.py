import sys
from PyQt5.QtWidgets import QApplication
from Splash import Splash
from BLL.PublicRrep import PRR

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        main_window = Splash()
        main_window.setStyleSheet(PRR.Style())
        main_window.show()
    except:
        pass
    sys.exit(app.exec_())