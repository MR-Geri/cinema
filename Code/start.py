import sys

from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import *

from Code.MyMainWindow import MainWindow
from Code.windows import WindowStart
from settings import path_icon

StyleSheet = """
TitleBar {
    background-color: rgb(60, 63, 65);
}
#buttonMinimum,#buttonMaximum,#buttonClose, #buttonInfo {
    border: none;
    background-color: rgb(60, 63, 65);
    color: white;
}
#buttonMinimum:hover,#buttonMaximum:hover {
    color: black;
    background-color: rgb(48, 141, 162);
}
#buttonClose:hover {
    color: black;
    background-color: rgb(232, 17, 35);
}
#buttonInfo:hover {
    color: black;
    background-color: green;
}
#buttonMinimum:pressed,#buttonMaximum:pressed {
    color: black;
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: black;
    background-color: rgb(161, 73, 92);
}
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    ex = MainWindow()
    ex.setWindowTitle('Кино')
    ex.setWindowIcon(QIcon(path_icon))
    ex.setWidget(WindowStart(ex))
    ex.show()
    sys.exit(app.exec_())
