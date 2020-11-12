import json
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from Code.data_base import get_data_base


class Login(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('../qt/login.ui', self)
        self.button_sign_in.clicked.connect(self.sign_in)
        self.line_login.textChanged.connect(self.update_line)
        self.line_password.textChanged.connect(self.update_line)

    def update_line(self):
        self.label_info.setText('Введите логин и пароль')

    def sign_in(self):
        accounts = json.load(open('../accounts.json'))
        if accounts.get(self.line_login.text(), None) == self.line_password.text():
            print('Вход разрешён')
            self.accept()
        else:
            self.label_info.setText('Неправильный логин или пароль')


class Form_login(QDialog):
    def __init__(self, path_base_file):
        super().__init__()
        self.path_base_file = path_base_file
        uic.loadUi('../qt/form_login.ui', self)
        self.button_cashier.clicked.connect(self.cashier)
        self.button_admin.clicked.connect(self.admin)

    def cashier(self):
        self.accept()

    def admin(self):
        dialog = Login()
        if dialog.exec_() == QDialog.Accepted:
            self.accept()
        dialog.deleteLater()
