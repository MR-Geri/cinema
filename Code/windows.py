from PyQt5 import uic

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Code.dialogs import Form_login
from Code.data_base import get_data_base
from Code.widgets import WidgetCinemaCard


class Window(QMainWindow):
    def __init__(self, path, start=None, user='Пользователь'):
        super().__init__()
        uic.loadUi(path, self)
        self.cards = None
        self.start = start
        self.path_base_file = start.path_base_file
        self.user = user
        self.label_user.setText(self.user)
        #
        menubar = self.menuBar()
        self.ActMenu = menubar.addMenu('&Действия')
        self.bar()
        action_exit = QAction('Выйти', self)
        action_exit.triggered.connect(self.close)
        action_exit.triggered.connect(self.start.show)
        self.ActMenu.addAction(action_exit)
        #
        self.update_()

    def update_(self):
        self.cards = QListWidget()
        self._update()
        self.grid.addWidget(self.cards, 1, 0, 2, 0)


class WindowCinema(Window):
    def __init__(self, cinemas=None, cinema_id=None):
        self.cinemas = cinemas
        self.start = cinemas.start
        self.cinema_id = cinema_id
        super().__init__('../qt/cinema.ui', self.start, self.cinemas.user)

    def bar(self):
        if self.user == 'Администратор':
            action_new_hall = QAction('Добавить зал', self)
            action_new_hall.setShortcut('Ctrl+N')
            action_new_hall.triggered.connect(self.new_hall)
            self.ActMenu.addAction(action_new_hall)
        action_cinemas = QAction('Кинотеатры', self)
        action_cinemas.triggered.connect(self.close)
        action_cinemas.triggered.connect(self.cinemas.show)
        self.ActMenu.addAction(action_cinemas)

    def _update(self):
        pass

    def new_hall(self):
        pass


class WindowCinemas(Window):
    def __init__(self, start=None, user='Пользователь'):
        self.cinema = None
        super().__init__('../qt/cinemas.ui', start, user)

    def bar(self):
        if self.user == 'Администратор':
            action_new_cinema = QAction('Добавить кинотеатр', self)
            action_new_cinema.setShortcut('Ctrl+N')
            action_new_cinema.triggered.connect(self.new_cinema)
            self.ActMenu.addAction(action_new_cinema)

    def _update(self):
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
            #
            card = WidgetCinemaCard(self.user, id_, title, quantity_halls, quantity_sessions, quantity_places)
            card.button_browse.clicked.connect(lambda state, _id=id_: self.browse(_id))
            if self.user == 'Администратор':
                card.button_edit.clicked.connect(lambda state, _id=id_: self.edit(_id))
            #
            q_list_card = QListWidgetItem(self.cards)
            q_list_card.setSizeHint(card.sizeHint())
            self.cards.addItem(q_list_card)
            self.cards.setItemWidget(q_list_card, card)

    def new_cinema(self):
        self.update_()

    def edit(self, id_):
        print(f'Изменение {id_}')

    def browse(self, id_):
        self.cinema = WindowCinema(self, id_)
        self.cinema.show()
        self.hide()


class WindowStart(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../qt/start.ui', self)
        pix_map = QPixmap('../image/start.jpg')
        self.path_base_file = None
        self.cinemas = None
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
                self.cinemas = WindowCinemas(self, dialog.user)
                self.cinemas.show()
                self.hide()
            dialog.deleteLater()
