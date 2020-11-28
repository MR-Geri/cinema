import datetime
import json
import os

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt

from Code.crypto import cipher
from settings import path_accounts, path_icon, path_image_start, path_password_font


class Login(QDialog):
    def __init__(self) -> None:
        super().__init__()
        path = os.path.abspath('../form/login.ui')
        uic.loadUi(path, self)
        self.setWindowIcon(QIcon(path_icon))
        #  Безопасный шрифт для пароля
        font_id = QFontDatabase.addApplicationFont(path_password_font)
        font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.line_password.setFont(QFont(font_name, 20))
        #
        self.button_sign_in.clicked.connect(self.sign_in)
        self.line_login.textChanged.connect(self.update_line)
        self.line_password.textChanged.connect(self.update_line)
        #
        self.button_sign_in.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                          'QPushButton:hover {background-color: rgb(200, 200, 200);}')

    def update_line(self) -> None:
        self.label_info.setText('Введите логин и пароль')

    def sign_in(self) -> None:
        accounts = {
            cipher.decrypt(bytes(i[0], 'utf-8')): cipher.decrypt(bytes(i[1], 'utf-8'))
            for i in json.load(open(path_accounts))
        }
        login = bytes(self.line_login.text(), 'utf-8')
        password = bytes(self.line_password.text(), 'utf-8')
        if accounts.get(login, None) == password:
            self.accept()
        else:
            self.label_info.setText('Неправильный логин или пароль')


class FormLogin(QDialog):
    def __init__(self) -> None:
        super().__init__()
        path = os.path.abspath('../form/form_login.ui')
        uic.loadUi(path, self)
        self.setWindowIcon(QIcon(path_icon))
        #
        self.button_cashier.clicked.connect(self.cashier)
        self.button_admin.clicked.connect(self.admin)
        self.button_cashier.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                          'QPushButton:hover {background-color: rgb(200, 200, 200);}')
        self.button_admin.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                        'QPushButton:hover {background-color: rgb(200, 200, 200);}')
        #
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
        path = os.path.abspath('../form/form_info.ui')
        self.setWindowIcon(QIcon(path_icon))
        uic.loadUi(path, self)
        #
        pix_map = QPixmap(path_image_start)

        self.image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image.setPixmap(pix_map.scaled(365, 400))
        #
        self.setLayout(self.gridLayout)


class Message(QMessageBox):
    def __init__(self, title_window: str = '', text: str = '', informative_text: str = '') -> None:
        super().__init__()
        self.setWindowIcon(QIcon(path_icon))
        self.setWindowTitle(title_window)
        self.setIcon(QMessageBox.Warning)
        self.setText(text)
        self.setInformativeText(informative_text)


class FormCinema(QDialog):
    def __init__(self, title_window: str = '', title: str = '') -> None:
        super().__init__()
        path = os.path.abspath('../form/cinema.ui')
        uic.loadUi(path, self)
        self.setWindowIcon(QIcon(path_icon))
        self.setWindowTitle(title_window)
        #
        self.title.setText(title)
        #
        self.button_save.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.close)
        self.setLayout(self.gridLayout)


class FormHall(QDialog):
    def __init__(self, title_window: str = '',  title: str = '', rows: int = 1, places_row: int = 1) -> None:
        super().__init__()
        path = os.path.abspath('../form/hall.ui')
        uic.loadUi(path, self)
        self.setWindowIcon(QIcon(path_icon))
        self.setWindowTitle(title_window)
        #
        self.title.setText(title)
        self.rows.setValue(rows)
        self.places_row.setValue(places_row)
        #
        self.button_save.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.close)
        #
        self.setLayout(self.gridLayout)


class FormSession(QDialog):
    def __init__(self, title_window: str = '', title: str = '', date: str = '1.1.2000',
                 time: str = '0:0', duration: str = '0:0', price: int = 250) -> None:
        super().__init__()
        path = os.path.abspath('../form/session.ui')
        uic.loadUi(path, self)
        self.setWindowIcon(QIcon(path_icon))
        self.setWindowTitle(title_window)
        #
        self.title.setText(title)
        self.date.setDate(datetime.date(*reversed(list(map(int, date.split('.'))))))
        self.time.setTime(datetime.time(*map(int, time.split(':'))))
        self.duration.setTime(datetime.time(*map(int, duration.split(':'))))
        self.price.setValue(price)
        #
        self.button_save.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.close)
        #
        self.setLayout(self.gridLayout)
