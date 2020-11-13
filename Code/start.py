import sys
from PyQt5.QtWidgets import QApplication
from Code.windows import WindowStart


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowStart()
    ex.show()
    sys.exit(app.exec_())
