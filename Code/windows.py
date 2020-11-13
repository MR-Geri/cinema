from PyQt5 import uic

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Code.dialogs import Form_login
from Code.data_base import get_data_base
from Code.widgets import WidgetCard


class WindowCinema(QMainWindow):
    def __init__(self, path_base_file, user='Пользователь'):
        super().__init__()
        uic.loadUi('../qt/cinema.ui', self)
        self.cards = None
        self.path_base_file = path_base_file
        self.label_user.setText(user)
        self.update_()

    def update_(self):
        self.cards = QListWidget()
        for id_, title in get_data_base(self.path_base_file, """SELECT * FROM Cinemas"""):
            num_halls = str(get_data_base(
                self.path_base_file,
                """SELECT COUNT(*) FROM Halls h WHERE h.cinema_id = ?""",
                (id_,)
            )[0][0])
            card = WidgetCard(id_, title, num_halls, '0', '0')
            q_list_card = QListWidgetItem(self.cards)
            q_list_card.setSizeHint(card.sizeHint())
            self.cards.addItem(q_list_card)
            self.cards.setItemWidget(q_list_card, card)
        self.grid.addWidget(self.cards, 1, 0, 2, 0)


class WindowStart(QMainWindow):
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
                self.cinema = WindowCinema(self.path_base_file, dialog.user)
                self.cinema.show()
                self.hide()
            dialog.deleteLater()