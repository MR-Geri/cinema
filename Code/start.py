import sys
from PyQt5.QtWidgets import *
from Code.widgets import MyWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
