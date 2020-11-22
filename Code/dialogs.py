import json
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from settings import *


class Login(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('../form/login.ui', self)
        self.setWindowIcon(QIcon(path_icon))
        self.button_sign_in.clicked.connect(self.sign_in)
        self.line_login.textChanged.connect(self.update_line)
        self.line_password.textChanged.connect(self.update_line)

        self.button_sign_in.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                          'QPushButton:hover {background-color: rgb(200, 200, 200);}')

    def update_line(self) -> None:
        self.label_info.setText('Введите логин и пароль')

    def sign_in(self) -> None:
        accounts = json.load(open(path_accounts))
        if accounts.get(self.line_login.text(), None) == self.line_password.text():
            print('Вход разрешён')
            self.accept()
        else:
            self.label_info.setText('Неправильный логин или пароль')


class FormLogin(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('../form/form_login.ui', self)
        self.setWindowIcon(QIcon(path_icon))
        self.button_cashier.clicked.connect(self.cashier)
        self.button_admin.clicked.connect(self.admin)
        self.button_cashier.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                          'QPushButton:hover {background-color: rgb(200, 200, 200);}')
        self.button_admin.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                        'QPushButton:hover {background-color: rgb(200, 200, 200);}')
        self.user = None

    def cashier(self) -> None:
        self.user = 'Кассир'
        self.accept()

    def admin(self) -> None:
        dialog = Login()
        if dialog.exec_() == QDialog.Accepted:
            self.user = 'Администратор'
            self.accept()
        dialog.deleteLater()


class FormInfo(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('../form/form_info.ui', self)
        pix_map = QPixmap(path_image_start)
        self.setWindowIcon(QIcon(path_icon))
        self.image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image.setPixmap(pix_map.scaled(365, 400))
        self.setLayout(self.gridLayout)


class FormNewCinema(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('../form/new_cinema.ui', self)
        self.button_add.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.close)
        self.setLayout(self.gridLayout)


class FormNewHall(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('../form/new_cinema.ui', self)
        self.button_add.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.close)
        self.setLayout(self.gridLayout)
