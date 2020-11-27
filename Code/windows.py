import datetime
import os
import shutil
from threading import Thread

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from Code.MyMainWindow import MainWindow
from Code.dialogs import FormLogin, Login, FormCinema, FormHall, FormSession, Message
from Code.data_base import get_data_base, get_base, Base
from Code.image import ticket
from Code.widgets import WidgetCinemasCard, WidgetCinemaCard, WidgetHallCard, WidgetPlacement
from settings import path_icon, path_image_start, time_restart_session


class WindowStart(QWidget):
    def __init__(self, window: MainWindow = None) -> None:
        super().__init__()
        self.path_base_file = None
        self.cinemas = None
        self.window = window
        self._init_ui()

    def _init_ui(self):
        #
        self.layout = QVBoxLayout(self, spacing=0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('background: rgb(255, 186, 0);')
        #
        self.image = QLabel('')
        self.image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.button_create = QPushButton("Создать базу данных")
        self.button_load = QPushButton("Загрузить базу данных")
        #
        self.button_create.setFont(QFont('MS Shell Dlg 2', 20))
        self.button_create.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                         'QPushButton:hover {background-color: rgb(200, 200, 200);}')
        self.button_load.setFont(QFont('MS Shell Dlg 2', 20))
        self.button_load.setStyleSheet('QPushButton:!hover{background-color: rgb(255, 255, 255);}'
                                       'QPushButton:hover {background-color: rgb(200, 200, 200);}')
        #
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.button_create)
        self.layout.addWidget(self.button_load)
        #
        pix_map = QPixmap(path_image_start)
        self.image.setPixmap(pix_map.scaled(365, 400))
        self.button_create.clicked.connect(self.create_base)
        self.button_load.clicked.connect(self.load_base)

    def _init_cinemas(self, user: str = 'Пользователь') -> None:
        """
        Инициализация окна с кинотеатрами

        :param user: Права пользователя (кассир или администратор)
        :return: Эта функция ничего не возвращает
        """
        self.cinemas = MainWindow()
        self.cinemas.setWindowTitle('Кинотеатры')
        self.cinemas.setWindowIcon(QIcon(path_icon))
        self.cinemas.setWidget(WindowCinemas(self, user))
        self.cinemas.show()
        self.window.hide()

    @staticmethod
    def db_create(base):
        base.execute("""
                                           create table Cinemas
                                           (
                                               id    INTEGER not null
                                                   primary key autoincrement
                                                   unique,
                                               title STRING  not null
                                           );
                                           """)
        base.execute("""
                                           create table Halls
                                           (
                                               id         INTEGER not null
                                                   constraint Halls_pk
                                                       primary key autoincrement,
                                               title      STRING  not null,
                                               cinema_id  INTEGER not null
                                                   references Cinemas,
                                               rows       INTEGER not null,
                                               places_row INTEGER not null
                                           );
                                           """)
        base.execute("""create unique index Halls_id_uindex on Halls (id);""")
        base.execute("""
                                           create table Sessions
                                           (
                                               id       INTEGER not null
                                                   primary key autoincrement
                                                   unique,
                                               title    STRING  not null,
                                               hall_id  INTEGER not null
                                                   references Halls,
                                               date     TEXT    not null,
                                               time     TEXT    not null,
                                               duration TEXT    not null,
                                               price    INTEGER default 0 not null
                                           );
                                           """)
        base.execute("""
                       create table Places
                       (
                           row        INTEGER not null,
                           place      INTEGER not null,
                           session_id INTEGER
                               references Sessions
                       );
                                           """)

    def create_base(self) -> None:
        """
        Созадние базы данных и её использование

        :return: Эта функция ничего не возвращает
        """
        dialog = Login()
        if dialog.exec_() == QDialog.Accepted:
            date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S-%f")
            temp_base_path = os.path.abspath(f'../temp/temp_base_{date}.sqlite')
            with open(temp_base_path, mode='w') as _:
                with get_base(temp_base_path, True) as base:
                    self.db_create(base)
            self.path_base_file = os.path.abspath(QFileDialog.getSaveFileName(
                self, caption='Сохранить базу', directory='../bases', filter='SQLite (*.sqlite);;Все файлы (*)')[0])
            if self.path_base_file:
                shutil.copy2(temp_base_path, self.path_base_file)
                self._init_cinemas('Администратор')
            os.remove(temp_base_path)
        dialog.deleteLater()

    def load_base(self) -> None:
        """
        Загрузка базы данных и её использование

        :return: Эта функция ничего не возвращает
        """
        self.path_base_file = QFileDialog.getOpenFileName(
            self, caption='Выбрать базу', directory='../bases', filter='SQLite (*.sqlite);;Все файлы (*)')[0]
        if self.path_base_file:
            dialog = FormLogin()
            if dialog.exec_() == QDialog.Accepted:
                self._init_cinemas(dialog.user)
            dialog.deleteLater()


class Window(QWidget):
    def __init__(self, start: WindowStart = None, user: str = 'Пользователь') -> None:
        super().__init__()
        self.cards = None
        self.start = start
        self.path_base_file = start.path_base_file
        self.user = user
        #
        self._init_ui()
        self.update_()

    def _init_ui(self):
        #
        self.grid = QGridLayout(spacing=0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid_card = QGridLayout(spacing=0)
        self.grid_card.setContentsMargins(3, 3, 3, 3)
        #
        self.menubar = QMenuBar()
        self.menubar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        #
        self.ActMenu = self.menubar.addMenu('&Навигация')
        self.gen_bar()
        action_exit = QAction('Выйти', self)
        action_exit.triggered.connect(self.window.close)
        action_exit.triggered.connect(self.start.window.show)
        self.ActMenu.addAction(action_exit)
        #
        self.label_user = QLabel(self.user)
        self.label_user.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_user.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.label_user.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #
        self.window.resize(800, 800)
        #
        self.setLayout(self.grid)
        self.grid.addWidget(self.menubar)
        self.grid.addWidget(self.label_user)
        self.grid.addLayout(self.grid_card, 3, 0)

    def gen_card(self, id_: int, title: str) -> QWidget:
        """
        Генерация карточек с информацией

        :param id_: номер объекта
        :param title: название объекта
        :return: Виджет со всеми карточками с информацией
        """
        card = self.card(self.user, title, *self.card_data(id_))
        card.button_browse.clicked.connect(lambda state, _id=id_: self.browse(_id))
        if self.user == 'Администратор':
            card.button_edit.clicked.connect(lambda state, _id=id_: self.edit(_id))
            card.button_delete.clicked.connect(lambda state, _id=id_: self.delete(_id))
        return card

    def update_(self) -> None:
        """
        Обновление информации

        :return: Эта функция ничего не возвращает
        """
        self.cards = QListWidget()
        layout = QGridLayout()
        layout.addWidget(self.cards)
        for id_, title in self.base:
            #
            card = self.gen_card(id_, title)
            #
            list_card = QListWidgetItem(self.cards)
            list_card.setSizeHint(card.sizeHint())
            self.cards.addItem(list_card)
            self.cards.setItemWidget(list_card, card)
        self.grid_card.addLayout(layout, 0, 0)


class WindowCinemas(Window):
    def __init__(self, start: WindowStart = None, user: str = 'Пользователь') -> None:
        self.window = start.cinemas
        self.cinema = None
        self.card = WidgetCinemasCard
        self.base = Base(start.path_base_file, """SELECT id, title FROM Cinemas""")
        super().__init__(start, user)

    def gen_bar(self) -> None:
        """
        Генерация ToolBar`a

        :return:  Эта функция ничего не возвращает
        """
        if self.user == 'Администратор':
            action_new_cinema = QAction('Добавить кинотеатр', self)
            action_new_cinema.setShortcut('Ctrl+N')
            action_new_cinema.triggered.connect(self.new_cinema)
            self.menubar.addAction(action_new_cinema)

    def card_data(self, id_: int) -> tuple:
        """
        Информация о кинотеатре

        :param id_: номер кинотеатра
        :return: tuple(кол-во залов, кол-во сеансов, кол-во мест)
        """
        quantity_halls = int(get_data_base(
            self.path_base_file,
            """SELECT COUNT(*) FROM Halls h WHERE h.cinema_id = ?""",
            (id_,)
        )[0][0])
        quantity_sessions = int(get_data_base(
            self.path_base_file,
            """SELECT COUNT(*) FROM Sessions s, Halls h WHERE h.cinema_id = ? AND s.hall_id = h.id""",
            (id_,)
        )[0][0])
        quantity_places = sum([i[0] for i in get_data_base(
            self.path_base_file,
            """SELECT rows * places_row FROM Halls h WHERE h.cinema_id = ?""",
            (id_,)
        )])
        return quantity_halls, quantity_sessions, quantity_places

    def new_cinema(self) -> None:
        """
        Добавление в базу данных нового кинотеатра с проверкой на название
        (Не может быть несколько кинотеатров с одинаковым названием)

        :return: Эта функция ничего не возвращает
        """
        dialog = FormCinema('Добавление кинотеатра')
        if dialog.exec_() == QDialog.Accepted:
            with get_base(self.path_base_file, True) as base:
                count = int(get_data_base(self.path_base_file,
                                          """SELECT COUNT(*) FROM Cinemas WHERE title = ?""",
                                          (dialog.title.text(),))[0][0])
                if count == 0:
                    base.execute("""
                    INSERT INTO Cinemas (id, title) VALUES ((SELECT id FROM Cinemas ORDER BY id DESC LIMIT 1) + 1, ?);
                    """, (dialog.title.text(),))
                else:
                    error_message = Message(title_window='Ошибка!',
                                            text=f'Кинотеатр с таким названием уже есть!',
                                            informative_text='Введите другое название.')
                    error_message.exec()
                    self.new_cinema()
            self.update_()
        dialog.deleteLater()

    def edit(self, id_: int) -> None:
        """
        Изменение кинотеатра

        :param id_: номер изменяемого объекта
        :return: Эта функция ничего не возвращает
        """
        dialog = FormCinema('Изменение кинотеатра',
                            get_data_base(self.path_base_file,
                                          """SELECT title FROM Cinemas WHERE id = ?""",
                                          (id_,))[0][0])
        if dialog.exec_() == QDialog.Accepted:
            with get_base(self.path_base_file, True) as base:
                base.execute("""UPDATE Cinemas SET title = ? WHERE id = ?""", (dialog.title.text(), id_))
            self.update_()
        dialog.deleteLater()

    def delete(self, id_: int) -> None:
        """
        Каскадное удаление из базы данных.

        :param id_: номер удаляемого объекта
        :return: Эта функция ничего не возвращает
        """
        valid = QMessageBox.question(
                self, 'Удаление', "Действительно удалить элемент и всё что с ним связано?!",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if valid == QMessageBox.Yes:
            valid = QMessageBox.question(
                self, 'Удаление ЛИ!?', "ВЫ УВЕРЕНЫ, ЧТО НУЖНО УДАЛИТЬ ЭЛЕМЕНТ?!!",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if valid == QMessageBox.Yes:
                with get_base(self.path_base_file, True) as base:
                    base.execute("""DELETE FROM Places WHERE session_id in 
                    (SELECT s.id FROM Halls h, Sessions s WHERE h.cinema_id = ?)""", (id_,))
                    base.execute("""DELETE FROM Sessions WHERE hall_id in 
                    (SELECT h.id FROM Halls h WHERE h.cinema_id = ?)""", (id_,))
                    base.execute("""DELETE FROM Halls WHERE cinema_id = ?""", (id_,))
                    base.execute("""DELETE FROM Cinemas WHERE id = ?""", (id_,))
                self.update_()

    def browse(self, id_: int) -> None:
        """
        Подробная информация о кинотеатре

        :param id_: номер просматриваемого кинотеатра
        :return: Эта функция ничего не возвращает
        """
        self.cinema = MainWindow()
        self.cinema.setWindowTitle('Кинотеатр')
        self.cinema.setWindowIcon(QIcon(path_icon))
        self.cinema.setWidget(WindowCinema(self, id_))
        self.cinema.show()
        self.window.hide()


class WindowCinema(Window):
    def __init__(self, cinemas: WindowCinemas = None, cinema_id: int = None) -> None:
        self.window = cinemas.cinema
        self.hall = None
        self.cinemas = cinemas
        self.cinema_id = cinema_id
        self.base = Base(cinemas.start.path_base_file,
                         """SELECT id, title FROM Halls WHERE  cinema_id = ?""",
                         (self.cinema_id,))
        self.card = WidgetCinemaCard
        super().__init__(self.cinemas.start, self.cinemas.user)

    def gen_bar(self) -> None:
        """
        Генерация ToolBar`a

        :return:  Эта функция ничего не возвращает
        """
        if self.user == 'Администратор':
            action_new_hall = QAction('Добавить зал', self)
            action_new_hall.setShortcut('Ctrl+N')
            action_new_hall.triggered.connect(self.new_hall)
            self.menubar.addAction(action_new_hall)
        #
        action_cinemas = QAction('Кинотеатры', self)
        action_cinemas.triggered.connect(self.window.close)
        action_cinemas.triggered.connect(self.cinemas.window.show)
        self.ActMenu.addAction(action_cinemas)

    def card_data(self, id_: int) -> tuple:
        """
        Информация о зале

        :param id_: номер зала
        :return: tuple(кол-во идущих сеансов, кол-во мест во всем зале, список сеансов)
        """
        sessions = [i[0] for i in get_data_base(
            self.path_base_file,
            """SELECT title FROM Sessions s WHERE s.hall_id = ?""",
            (id_,)
        )]
        quantity_sessions = len(sessions)
        quantity_places = int(get_data_base(
            self.path_base_file,
            """SELECT rows * places_row FROM Halls h WHERE h.id = ?""",
            (id_,)
        )[0][0])
        return quantity_sessions, quantity_places, sessions

    def new_hall(self) -> None:
        """
        Добавление в базу данных нового зала с проверкой на название
        (Не может быть несколько залов с одинаковым названием)

        :return: Эта функция ничего не возвращает
        """
        dialog = FormHall('Добавление зала')
        if dialog.exec_() == QDialog.Accepted:
            with get_base(self.path_base_file, True) as base:
                count = int(get_data_base(self.path_base_file,
                                          """SELECT COUNT(*) FROM Halls WHERE title = ?""",
                                          (dialog.title.text(),))[0][0])
                if count == 0:
                    base.execute("""
                                    INSERT INTO Halls (id, title, cinema_id, rows, places_row) 
                                    VALUES ((SELECT id FROM Halls ORDER BY id DESC LIMIT 1) + 1, ?, ?, ?, ?);
                                    """, (
                        dialog.title.text(),
                        self.cinema_id,
                        dialog.rows.value(),
                        dialog.places_row.value()))
                else:
                    error_message = Message(title_window='Ошибка!',
                                            text=f'Зал с таким названием уже есть!',
                                            informative_text='Введите другое название.')
                    error_message.exec()
                    self.new_hall()
            self.update_()
        dialog.deleteLater()

    def edit(self, id_: int) -> None:
        """
        Изменение зала

        :param id_: номер изменяемого объекта
        :return: Эта функция ничего не возвращает
        """
        dialog = FormHall('Изменение зала',
                          *get_data_base(self.path_base_file,
                                         """SELECT title, rows, places_row FROM Halls WHERE id = ?""",
                                         (id_,))[0])
        if dialog.exec_() == QDialog.Accepted:
            with get_base(self.path_base_file, True) as base:
                base.execute("""UPDATE Halls SET title = ?, rows = ?, places_row = ? WHERE id = ?""",
                             (dialog.title.text(), dialog.rows.value(), dialog.places_row.value(), id_))
            self.update_()
        dialog.deleteLater()

    def delete(self, id_: int) -> None:
        """
        Каскадное удаление из базы данных.

        :param id_: номер удаляемого объекта
        :return: Эта функция ничего не возвращает
        """
        valid = QMessageBox.question(
                self, 'Удаление', "Действительно удалить элемент и всё что с ним связано?!",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if valid == QMessageBox.Yes:
            valid = QMessageBox.question(
                self, 'Удаление ЛИ!?', "ВЫ УВЕРЕНЫ, ЧТО НУЖНО УДАЛИТЬ ЭЛЕМЕНТ?!!",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if valid == QMessageBox.Yes:
                with get_base(self.path_base_file, True) as base:
                    base.execute("""DELETE FROM Places WHERE session_id in 
                    (SELECT s.id FROM Sessions s, Halls h WHERE s.hall_id = ?)""", (id_,))
                    base.execute("""DELETE FROM Sessions WHERE hall_id = ?""", (id_,))
                    base.execute("""DELETE FROM Halls WHERE id = ?""", (id_,))
                self.update_()

    def browse(self, id_: int) -> None:
        """
        Подробная информация о зале

        :param id_: номер просматриваемого зала
        :return: Эта функция ничего не возвращает
        """
        self.hall = MainWindow()
        self.hall.setWindowTitle('Зал')
        self.hall.setWindowIcon(QIcon(path_icon))
        self.hall.setWidget(WindowHall(self, id_))
        self.hall.show()
        self.window.hide()


class WindowHall(Window):
    def __init__(self, cinema: WindowCinema = None, hall_id: int = None) -> None:
        self.window = cinema.hall
        self.session = None
        self.cinema = cinema
        self.hall_id = hall_id
        self.base = Base(self.cinema.start.path_base_file,
                         """SELECT id, title, date, time FROM Sessions WHERE  hall_id = ?""",
                         (self.hall_id,),
                         key=lambda x: datetime.datetime(
                             *reversed(list(map(int, x[2].split('.')))), *list(map(int, x[3].split(':')))
                         ))
        self.card = WidgetHallCard
        super().__init__(self.cinema.start, self.cinema.user)

    def gen_bar(self) -> None:
        """
        Генерация ToolBar`a

        :return:  Эта функция ничего не возвращает
        """
        if self.user == 'Администратор':
            action_new_hall = QAction('Добавить сеанс', self)
            action_new_hall.setShortcut('Ctrl+N')
            action_new_hall.triggered.connect(self.new_session)
            self.menubar.addAction(action_new_hall)
        #
        action_cinema = QAction('Кинотеатр', self)
        action_cinema.triggered.connect(self.window.close)
        action_cinema.triggered.connect(self.cinema.window.show)
        self.ActMenu.addAction(action_cinema)
        #
        action_cinemas = QAction('Кинотеатры', self)
        action_cinemas.triggered.connect(self.window.close)
        action_cinemas.triggered.connect(self.cinema.cinemas.window.show)
        self.ActMenu.addAction(action_cinemas)

    def card_data(self, id_: int) -> tuple:
        """
        Информация о сеансе

        :param id_: номер сеанса
        :return: tuple(дата, время, продолжительность, цена)
        """
        date, time, duration, price = get_data_base(
            self.cinema.start.path_base_file,
            """SELECT date, time, duration, price FROM Sessions WHERE id = ?""",
            (id_,)
        )[0]

        return date, time, duration, price

    def new_session(self) -> None:
        """
        Добавление в базу данных нового сеанса с проверкой на валидность времени
        (Сеансы в одном зале не могут идти одновременно)
        В настройках указано время на уборку зала. Это время тоже учитывается.
        По умолчанию 30 минут.

        :return: Эта функция ничего не возвращает
        """
        dialog = FormSession('Добавление сеанса')
        if dialog.exec_() == QDialog.Accepted:
            with get_base(self.path_base_file, True) as base:
                date_inp = dialog.date.dateTime().toString('dd.MM.yyyy')
                time_inp = dialog.time.dateTime().toString('HH:mm')
                duration_inp = dialog.duration.dateTime().toString('HH:mm')
                #
                inp_start = datetime.datetime(
                    *reversed(list(map(int, date_inp.split('.')))), *list(map(int, time_inp.split(':')))
                )
                # Время сеанса с учётом уборки в зале
                h, m = map(int, duration_inp.split(':'))
                inp_finish = inp_start + datetime.timedelta(hours=h, minutes=m + time_restart_session)
                #
                list_time = get_data_base(self.path_base_file,
                                          f"""SELECT date, time, duration FROM Sessions WHERE hall_id = ?""",
                                          (self.hall_id,))
                for date, time, duration in list_time:
                    h, m = map(int, duration.split(':'))
                    start = datetime.datetime(
                        *reversed(list(map(int, date.split('.')))), *list(map(int, time.split(':')))
                    )
                    finish = start + datetime.timedelta(hours=h, minutes=m)
                    if start <= inp_start <= finish or start <= inp_finish <= finish:
                        error_message = Message(title_window='Ошибка!', text=f'Сеанс пересекается с другим сеансом!')
                        error_message.exec()
                        self.new_session()
                        return
                base.execute("""
                                INSERT INTO Sessions (id, title, hall_id, date, time, duration, price)
                                VALUES ((SELECT id FROM Sessions ORDER BY id DESC LIMIT 1) + 1, ?, ?, ?, ?, ?, ?);
                                """,
                             (dialog.title.text(),
                              self.hall_id,
                              date_inp,
                              time_inp,
                              duration_inp,
                              dialog.price.value()))
            self.update_()
        dialog.deleteLater()

    def edit(self, id_: int) -> None:
        """
        Изменение сессии

        :param id_: номер изменяемого объекта
        :return: Эта функция ничего не возвращает
        """
        dialog = FormSession('Изменение зала',
                             *get_data_base(self.path_base_file,
                                            """SELECT title, date, time, duration FROM Sessions WHERE id = ?""",
                                            (id_,))[0])
        if dialog.exec_() == QDialog.Accepted:
            with get_base(self.path_base_file, True) as base:
                base.execute("""
                UPDATE Sessions SET title = ?, date = ?, time = ?, duration = ?, price = ? WHERE id = ?""",
                             (dialog.title.text(),
                              dialog.date.dateTime().toString('dd.MM.yyyy'),
                              dialog.time.dateTime().toString('HH:mm'),
                              dialog.duration.dateTime().toString('HH:mm'),
                              dialog.price.value(),
                              id_))
            self.update_()
        dialog.deleteLater()

    def delete(self, id_: int) -> None:
        """
        Каскадное удаление из базы данных.

        :param id_: номер удаляемого объекта
        :return: Эта функция ничего не возвращает
        """
        valid = QMessageBox.question(
            self, 'Удаление', "Действительно удалить элемент и всё что с ним связано?!",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if valid == QMessageBox.Yes:
            valid = QMessageBox.question(
                self, 'Удаление ЛИ!?', "ВЫ УВЕРЕНЫ, ЧТО НУЖНО УДАЛИТЬ ЭЛЕМЕНТ?!!",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if valid == QMessageBox.Yes:
                with get_base(self.path_base_file, True) as base:
                    base.execute("""DELETE FROM Places WHERE session_id = ?""", (id_,))
                    base.execute("""DELETE FROM Sessions WHERE id = ?""", (id_,))
                self.update_()

    def browse(self, id_: int) -> None:
        """
        Подробная информация о сеансе

        :param id_: номер просматриваемого сеанса
        :return: Эта функция ничего не возвращает
        """
        self.session = MainWindow()
        self.session.setWindowTitle('Сеанс')
        self.session.setWindowIcon(QIcon(path_icon))
        self.session.setWidget(WindowSession(self, id_))
        self.session.show()
        self.window.hide()


class WindowSession(Window):
    def __init__(self, hall: WindowHall = None, session_id: int = None) -> None:
        self.window = hall.session
        self.hall = hall
        self.session_id = session_id
        super().__init__(self.hall.start, self.hall.user)
        #  Информация о сессии
        self.price = get_data_base(self.path_base_file,
                                   """SELECT price FROM Sessions WHERE id = ?""",
                                   (self.session_id,))[0][0]
        self.title_hall = get_data_base(
            self.path_base_file,
            """SELECT h.title FROM Halls h, Sessions s WHERE h.id = s.hall_id AND s.id = ?""",
            (self.session_id,))[0][0]
        self.date = get_data_base(
            self.path_base_file,
            """SELECT date FROM Sessions WHERE id = ?""",
            (self.session_id,))[0][0]
        #
        d_row, d_places = map(int, get_data_base(self.path_base_file,
                                                 """SELECT rows, places_row FROM Halls WHERE  id = ?""",
                                                 (self.hall.hall_id,))[0])
        take_place = get_data_base(self.path_base_file,
                                   "SELECT p.row, p.place FROM Places p WHERE p.session_id = ?",
                                   (self.session_id,))
        self.placement = WidgetPlacement(take_place, d_row, d_places)
        layout = QGridLayout()
        layout.addWidget(self.placement)
        self.grid_card.addLayout(layout, 0, 0)
        self.label_user.hide()

    def gen_bar(self) -> None:
        """
        Генерация ToolBar`a

        :return:  Эта функция ничего не возвращает
        """
        action_hall = QAction('Зал', self)
        action_hall.triggered.connect(self.window.close)
        action_hall.triggered.connect(self.hall.window.show)
        self.ActMenu.addAction(action_hall)
        #
        action_cinema = QAction('Кинотеатр', self)
        action_cinema.triggered.connect(self.window.close)
        action_cinema.triggered.connect(self.hall.cinema.window.show)
        self.ActMenu.addAction(action_cinema)
        #
        action_cinemas = QAction('Кинотеатры', self)
        action_cinemas.triggered.connect(self.window.close)
        action_cinemas.triggered.connect(self.hall.cinema.cinemas.window.show)
        self.ActMenu.addAction(action_cinemas)
        #
        action_reservation = QAction('Обновить', self)
        action_reservation.triggered.connect(self.reservations)
        self.menubar.addAction(action_reservation)

    def reservations(self) -> None:
        """
        Покупка и печать билетов.
        Отмена забронированного места.

        :return: Эта функция ничего не возвращает
        """
        take_place_base = set(get_data_base(self.path_base_file,
                                            "SELECT p.row, p.place FROM Places p WHERE p.session_id = ?",
                                            (self.session_id,)))
        deleted = take_place_base - self.placement.take_place
        added = self.placement.take_place - take_place_base
        with get_base(self.path_base_file, True) as base:
            if deleted:
                for row, place in deleted:
                    base.execute("""DELETE FROM Places WHERE row = ? AND place = ? AND session_id = ?""",
                                 (row, place, self.session_id))
            if added:
                for row, place in added:
                    base.execute("""INSERT INTO Places (row, place, session_id) VALUES (?, ?, ?)""",
                                 (row, place, self.session_id))
                    th = Thread(target=ticket, args=(row, place, self.title_hall, self.price, self.date))
                    th.start()

    def update_(self) -> None:
        """ Эта функция должна быть пустой """
        pass
