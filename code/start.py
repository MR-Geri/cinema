import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *


class Form_login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../qt/form_login.ui', self)
        self.button_cashier.clicked.connect(self.cashier)
        self.button_admin.clicked.connect(self.admin)

    def cashier(self):
        pass

    def admin(self):
        pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../qt/start.ui', self)
        pix_map = QPixmap('../image/start.jpg')
        self.path_base_file = None
        self.form_login = None
        self.image.setPixmap(pix_map.scaled(365, 400))
        self.button_create.clicked.connect(self.create_base)
        self.button_load.clicked.connect(self.load_base)

    def create_base(self):
        #
        self.hide()

    def load_base(self):
        self.path_base_file = QFileDialog.getOpenFileName(
            self, 'Выбрать базу', '',
            'SQLite (*.sqlite);;Все файлы (*)')[0]
        self.form_login = Form_login()
        self.form_login.show()
        #
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
