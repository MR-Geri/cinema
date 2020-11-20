import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from Code.MyMainWindow import MainWindow
from Code.windows import WindowStart
from settings import *

StyleSheet = """
TitleBar {
    background-color: rgb(60, 63, 65);
}
#buttonMinimum,#buttonMaximum,#buttonClose, #buttonMy {
    border: none;
    background-color: rgb(60, 63, 65);
}
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: rgb(48, 141, 162);
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}
#buttonMy:hover {
    color: white;
    background-color: green;   /* rgb(232, 17, 35) */
}
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: white;
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
