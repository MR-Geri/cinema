from PyQt5 import uic

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from Code.MyMainWindow import MainWindow
from Code.dialogs import Form_login
from Code.data_base import get_data_base
from Code.widgets import WidgetCinemasCard, WidgetCinemaCard, WidgetHallCard, WidgetPlacement


class Window(QMainWindow):
    def __init__(self, start=None, user='Пользователь'):
        super().__init__()
        uic.loadUi('../qt/window.ui', self)
        self.cards = None
        self.start = start
        self.path_base_file = start.path_base_file
        self.user = user
        self.label_user.setText(self.user)
        #
        self.menubar = self.menuBar()
        self.ActMenu = self.menubar.addMenu('&Навигация')
        self.gen_bar()
        # self.start.main_window.buttonMy.clicked.connect(self.close)
        # self.start.main_window.buttonMy.clicked.connect(self.start.main_window.show)
        action_exit = QAction('Выйти', self)
        action_exit.triggered.connect(self.close)
        action_exit.triggered.connect(self.start.main_window.show)
        self.ActMenu.addAction(action_exit)
        #
        self.update_()

    def gen_card(self, id_, title):
        card = self.card(self.user, title, *self.card_data(id_))
        card.button_browse.clicked.connect(lambda state, _id=id_: self.browse(_id))
        if self.user == 'Администратор':
            card.button_edit.clicked.connect(lambda state, _id=id_: self.edit(_id))
        return card

    def update_(self):
        self.cards = QListWidget()
        for id_, title in self.base:
            #
            card = self.gen_card(id_, title)
            #
            q_list_card = QListWidgetItem(self.cards)
            q_list_card.setSizeHint(card.sizeHint())
            self.cards.addItem(q_list_card)
            self.cards.setItemWidget(q_list_card, card)
        self.grid.addWidget(self.cards, 1, 0, 2, 0)


class WindowSession(QWidget):
    def __init__(self, hall=None, session_id=None):
        super().__init__()
        self.hall = hall
        self.user = self.hall.user
        self.session_id = session_id
        #
        # self.menubar = self.menuBar()
        # self.ActMenu = self.menubar.addMenu('&Навигация')
        # self.gen_bar()
        self.start.main_window.buttonMy.clicked.connect(self.close)
        self.start.main_window.buttonMy.clicked.connect(self.start.main_window.show)
        #
        self.update_()

    def gen_bar(self):
        action_hall = QAction('Зал', self)
        action_hall.triggered.connect(self.close)
        action_hall.triggered.connect(self.hall.show)
        self.ActMenu.addAction(action_hall)
        action_cinema = QAction('Кинотеатр', self)
        action_cinema.triggered.connect(self.close)
        action_cinema.triggered.connect(self.hall.cinema.show)
        self.ActMenu.addAction(action_cinema)
        action_cinemas = QAction('Кинотеатры', self)
        action_cinemas.triggered.connect(self.close)
        action_cinemas.triggered.connect(self.hall.cinema.cinemas.show)
        self.ActMenu.addAction(action_cinemas)

    def card_data(self, id_):
        pass

    def new_reservations(self):
        pass

    def update_(self):
        d_row, d_places = get_data_base(self.hall.start.path_base_file,
                                        """SELECT rows, places_pow FROM Halls WHERE  id = ?""",
                                        (self.hall.hall_id,))[0]
        place = WidgetPlacement(d_row, d_places)
        self.grid = QGridLayout()
        self.grid.addWidget(place)
        self.setLayout(self.grid)


class WindowHall(Window):
    def __init__(self, cinema=None, hall_id=None):
        self.session = None
        self.cinema = cinema
        self.hall_id = hall_id
        self.base = get_data_base(self.cinema.start.path_base_file,
                                  """SELECT id, title FROM Sessions WHERE  hall_id = ?""",
                                  (self.hall_id,))
        self.card = WidgetHallCard
        super().__init__(self.cinema.start, self.cinema.user)

    def gen_bar(self):
        if self.user == 'Администратор':
            action_new_hall = QAction('Добавить сеанс', self)
            action_new_hall.setShortcut('Ctrl+N')
            action_new_hall.triggered.connect(self.new_session)
            self.menubar.addAction(action_new_hall)
        action_cinema = QAction('Кинотеатр', self)
        action_cinema.triggered.connect(self.close)
        action_cinema.triggered.connect(self.cinema.show)
        self.ActMenu.addAction(action_cinema)
        action_cinemas = QAction('Кинотеатры', self)
        action_cinemas.triggered.connect(self.close)
        action_cinemas.triggered.connect(self.cinema.cinemas.show)
        self.ActMenu.addAction(action_cinemas)

    def card_data(self, id_):
        date, time, duration = get_data_base(
            self.cinema.start.path_base_file,
            """SELECT date, time, duration FROM Sessions WHERE id = ?""",
            (id_,)
        )[0]
        return date, time, duration

    def new_session(self):
        pass

    def edit(self, id_):
        pass

    def browse(self, id_):
        self.session = MainWindow()
        self.session.setWindowTitle('Зал')
        self.session.setWindowIcon(QIcon('../yandex.ico'))
        self.session.setWidget(WindowSession(self, id_))
        self.session.show()
        # self.session = WindowSession(self, id_)
        # self.session.show()
        self.hide()


class WindowCinema(Window):
    def __init__(self, cinemas=None, cinema_id=None):
        self.hall = None
        self.cinemas = cinemas
        self.cinema_id = cinema_id
        self.base = get_data_base(cinemas.start.path_base_file,
                                  """SELECT id, title FROM Halls WHERE  cinema_id = ?""",
                                  (self.cinema_id,))
        self.card = WidgetCinemaCard
        super().__init__(self.cinemas.start, self.cinemas.user)

    def gen_bar(self):
        if self.user == 'Администратор':
            action_new_hall = QAction('Добавить зал', self)
            action_new_hall.setShortcut('Ctrl+N')
            action_new_hall.triggered.connect(self.new_hall)
            self.menubar.addAction(action_new_hall)
        action_cinemas = QAction('Кинотеатры', self)
        action_cinemas.triggered.connect(self.close)
        action_cinemas.triggered.connect(self.cinemas.show)
        self.ActMenu.addAction(action_cinemas)

    def card_data(self, id_):
        sessions = [i[0] for i in get_data_base(
            self.path_base_file,
            """SELECT title FROM Sessions s WHERE s.hall_id = ?""",
            (id_,)
        )]
        quantity_sessions = len(sessions)
        quantity_places = get_data_base(
            self.path_base_file,
            """SELECT rows * places_pow FROM Halls h WHERE h.id = ?""",
            (id_,)
        )[0][0]
        return quantity_sessions, quantity_places, sessions

    def new_hall(self):
        pass

    def edit(self, id_):
        pass

    def browse(self, id_):
        self.hall = WindowHall(self, id_)
        self.hall.show()
        self.hide()


class WindowCinemas(Window):
    def __init__(self, start=None, user='Пользователь'):
        self.cinema = None
        self.card = WidgetCinemasCard
        self.base = get_data_base(start.path_base_file, """SELECT id, title FROM Cinemas""")
        super().__init__(start, user)

    def gen_bar(self):
        if self.user == 'Администратор':
            action_new_cinema = QAction('Добавить кинотеатр', self)
            action_new_cinema.setShortcut('Ctrl+N')
            action_new_cinema.triggered.connect(self.new_cinema)
            self.menubar.addAction(action_new_cinema)

    def card_data(self, id_):
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
        return quantity_halls, quantity_sessions, quantity_places

    def new_cinema(self):
        pass

    def edit(self, id_):
        pass

    def browse(self, id_):
        self.cinema = WindowCinema(self, id_)
        self.cinema.show()
        self.hide()


class WindowStart(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout(self, spacing=1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('background: rgb(255, 186, 0);')
        #
        self.image = QLabel('')
        self.image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.button_create = QPushButton("Создать базу данных")
        self.button_load = QPushButton("Загрузить базу данных")
        #
        self.image.setFont(QFont('MS Shell Dlg 2', 16))
        self.button_create.setFont(QFont('MS Shell Dlg 2', 16))
        self.button_create.setStyleSheet('background: rgb(255, 255, 255);')
        self.button_load.setFont(QFont('MS Shell Dlg 2', 16))
        self.button_load.setStyleSheet('background: rgb(255, 255, 255);')
        #
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.button_create)
        self.layout.addWidget(self.button_load)
        #
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
                self.main_window.hide()
            dialog.deleteLater()
