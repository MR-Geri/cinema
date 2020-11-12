import sys
from PyQt5.QtWidgets import *
from Code.widgets import WidgetStart


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetStart()
    ex.show()
    sys.exit(app.exec_())
