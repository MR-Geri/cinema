from PyQt5 import uic

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Code.dialogs import Form_login
from Code.data_base import get_data_base
from Code.widgets import WidgetCinemaCard


class WindowCinemas(QMainWindow):
    def __init__(self, parent=None, user='Пользователь'):
        super().__init__()
        uic.loadUi('../qt/cinemas.ui', self)
        self.cards = None
        self.path_base_file = parent.path_base_file
        self.user = user
        self.label_user.setText(self.user)
        #
        menubar = self.menuBar()
        ActMenu = menubar.addMenu('&Действия')
        if self.user == 'Администратор':
            action_new_cinema = QAction('Добавить кинотеатр', self)
            action_new_cinema.setShortcut('Ctrl+N')
            action_new_cinema.triggered.connect(self.new_cinema)
            ActMenu.addAction(action_new_cinema)
        action_exit = QAction('Выйти', self)
        action_exit.triggered.connect(self.close)
        action_exit.triggered.connect(parent.show)
        ActMenu.addAction(action_exit)
        self.update_()

    def new_cinema(self):
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
            card = WidgetCinemaCard(self.user, id_, title, quantity_halls, quantity_sessions, quantity_places)
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
                self.cinema = WindowCinemas(self, dialog.user)
                self.cinema.show()
                self.hide()
            dialog.deleteLater()
