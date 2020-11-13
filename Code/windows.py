from PyQt5 import uic

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Code.dialogs import Form_login
from Code.data_base import get_data_base
from Code.widgets import WidgetCard


class WindowCinemas(QWidget):
    def __init__(self, path_base_file, user='Пользователь'):
        super().__init__()
        uic.loadUi('../qt/cinemas.ui', self)
        self.cards = None
        self.path_base_file = path_base_file
        self.user = user
        self.label_user.setText(self.user)
        self.update_()

    def update_(self):
        self.cards = QListWidget()
        for id_, title in get_data_base(self.path_base_file, """SELECT * FROM Cinemas"""):
            quantity_halls = get_data_base(
                self.path_base_file,
                """SELECT COUNT(*) FROM Halls h WHERE h.cinema_id = ?""",
                (id_,)
            )[0][0]
            quantity_sessions = get_data_base(
                self.path_base_file,
                """SELECT COUNT(*) FROM Sessions s, Halls h WHERE h.cinema_id = ? AND s.hall_id = h.id""",
                (id_,)
            )[0][0]
            quantity_places = sum([i[0] for i in get_data_base(
                self.path_base_file,
                """SELECT rows * places_pow FROM Halls h WHERE h.cinema_id = ?""",
                (id_,)
            )])
            card = WidgetCard(self.user, id_, title, quantity_halls, quantity_sessions, quantity_places)
            q_list_card = QListWidgetItem(self.cards)
            q_list_card.setSizeHint(card.sizeHint())
            self.cards.addItem(q_list_card)
            self.cards.setItemWidget(q_list_card, card)
        self.grid.addWidget(self.cards, 1, 0, 2, 0)


class WindowStart(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('../qt/start.ui', self)
        pix_map = QPixmap('../image/start.jpg')
        self.path_base_file = None
        self.cinema = None
        self.image.setPixmap(pix_map.scaled(365, 400))
        self.button_create.clicked.connect(self.create_base)
        self.button_load.clicked.connect(self.load_base)

    def create_base(self):
        pass

    def load_base(self):
        self.path_base_file = QFileDialog.getOpenFileName(
            self, 'Выбрать базу', '',
            'SQLite (*.sqlite);;Все файлы (*)')[0]
        if self.path_base_file:
            dialog = Form_login()
            if dialog.exec_() == QDialog.Accepted:
                self.cinema = WindowCinemas(self.path_base_file, dialog.user)
                self.cinema.button_exit.clicked.connect(self.show)
                self.cinema.button_exit.clicked.connect(self.cinema.hide)
                self.cinema.show()
                self.hide()
            dialog.deleteLater()


class Controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start = WindowStart()
        self.start.show()
