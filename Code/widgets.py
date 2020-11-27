from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WidgetCinemasCard(QWidget):
    def __init__(self, user: str, title: str, quantity_halls: int,
                 quantity_sessions: int, quantity_places: int, static: int) -> None:
        super().__init__()
        #
        self.label_title = QLabel(title)
        self.label_halls = QLabel(f'Всего залов: {quantity_halls}')
        self.label_sessions = QLabel(f'Всего сеансов: {quantity_sessions}')
        self.label_places = QLabel(f'Всего мест: {quantity_places}')
        self.label_static = QLabel(f'Выручка: {static}')
        #
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_title.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_halls.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_sessions.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_places.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_static.setFont(QFont('MS Shell Dlg 2', 20))
        #
        self.button_browse = QPushButton('Просмотреть')
        self.button_browse.setFont(QFont('MS Shell Dlg 2', 20))
        #
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 0)
        self.gridLayout.addWidget(self.label_halls, 2, 0, 1, 0)
        self.gridLayout.addWidget(self.label_sessions, 3, 0, 1, 0)
        self.gridLayout.addWidget(self.label_places, 4, 0, 1, 0)
        self.gridLayout.addWidget(self.label_static, 5, 0, 1, 0)
        if user == 'Администратор':
            self.button_edit = QPushButton('Изменить')
            self.button_edit.setFont(QFont('MS Shell Dlg 2', 20))
            self.button_delete = QPushButton('Удалить')
            self.button_delete.setFont(QFont('MS Shell Dlg 2', 20))
            self.gridLayout.addWidget(self.button_edit, 6, 0)
            self.gridLayout.addWidget(self.button_delete, 6, 1)
            self.gridLayout.addWidget(self.button_browse, 6, 2)
            #
        else:
            self.gridLayout.addWidget(self.button_browse, 6, 0, 1, 0)
        #
        self.setLayout(self.gridLayout)


class WidgetCinemaCard(QWidget):
    def __init__(self, user: str, title: str, quantity_sessions: int,
                 quantity_places: int, sessions: list, static: int) -> None:
        super().__init__()
        #
        self.label_title = QLabel(title)
        self.label_sessions = QLabel(f'Количество сеансов: {quantity_sessions}')
        self.label_places = QLabel(f'Количество мест: {quantity_places}')
        self.label_static = QLabel(f'Выручка: {static}')
        #
        self.sessions = QListWidget()
        self.sessions.setMaximumHeight(200)
        self.sessions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        for title_session in sessions:
            #
            card = QLabel(title_session)
            card.setFont(QFont('MS Shell Dlg 2', 20))
            card.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #
            q_list_card = QListWidgetItem(self.sessions)
            q_list_card.setSizeHint(card.sizeHint())
            self.sessions.addItem(q_list_card)
            self.sessions.setItemWidget(q_list_card, card)
        #
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_title.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_sessions.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_places.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_static.setFont(QFont('MS Shell Dlg 2', 20))
        #
        self.button_browse = QPushButton('Просмотреть')
        self.button_browse.setFont(QFont('MS Shell Dlg 2', 20))
        #
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 0)
        self.gridLayout.addWidget(self.label_sessions, 2, 0)
        self.gridLayout.addWidget(self.label_places, 3, 0)
        self.gridLayout.addWidget(self.label_static, 4, 0)
        self.gridLayout.addWidget(self.sessions, 2, 1, 3, 2)

        if user == 'Администратор':
            self.button_edit = QPushButton('Изменить')
            self.button_edit.setFont(QFont('MS Shell Dlg 2', 20))
            self.button_delete = QPushButton('Удалить')
            self.button_delete.setFont(QFont('MS Shell Dlg 2', 20))
            self.gridLayout.addWidget(self.button_edit, 5, 0)
            self.gridLayout.addWidget(self.button_delete, 5, 1)
            self.gridLayout.addWidget(self.button_browse, 5, 2)
            #
        else:
            self.gridLayout.addWidget(self.button_browse, 5, 0, 1, 0)
        #
        self.setLayout(self.gridLayout)


class WidgetHallCard(QWidget):
    def __init__(self, user: str, title: str, date: str, time: str,
                 duration: str, price: str, static: int) -> None:
        super().__init__()
        self.gridLayout = QGridLayout()
        #
        self.label_title = QLabel(title)
        self.label_date = QLabel(f'Дата: {date}')
        self.label_time = QLabel(f'Время начала: {time}')
        self.label_duration = QLabel(f'Продолжительность: {duration}')
        self.label_price = QLabel(f'Цена билета: {price}')
        self.label_static = QLabel(f'Выручка: {static}')
        #
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_title.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_date.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_time.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_duration.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_price.setFont(QFont('MS Shell Dlg 2', 20))
        self.label_static.setFont(QFont('MS Shell Dlg 2', 20))
        #
        self.button_browse = QPushButton('Просмотреть')
        self.button_browse.setFont(QFont('MS Shell Dlg 2', 20))
        #
        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 0)
        self.gridLayout.addWidget(self.label_date, 2, 0, 1, 0)
        self.gridLayout.addWidget(self.label_time, 3, 0, 1, 0)
        self.gridLayout.addWidget(self.label_duration, 4, 0, 1, 0)
        self.gridLayout.addWidget(self.label_price, 5, 0, 1, 0)
        self.gridLayout.addWidget(self.label_static, 6, 0, 1, 0)
        if user == 'Администратор':
            self.button_edit = QPushButton('Изменить')
            self.button_edit.setFont(QFont('MS Shell Dlg 2', 20))
            self.button_delete = QPushButton('Удалить')
            self.button_delete.setFont(QFont('MS Shell Dlg 2', 20))
            self.gridLayout.addWidget(self.button_edit, 7, 0)
            self.gridLayout.addWidget(self.button_delete, 7, 1)
            self.gridLayout.addWidget(self.button_browse, 7, 2)
            #
        else:
            self.gridLayout.addWidget(self.button_browse, 7, 0, 1, 0)
        #
        self.setLayout(self.gridLayout)


class WidgetPlacement(QWidget):
    def __init__(self, take_place: list, d_row: int, d_places: int) -> None:
        super().__init__()
        self.take_place = set(take_place)
        self.d_row = d_row
        self.d_places = d_places
        self._init_ui()

    def _init_ui(self) -> None:
        screen = QLabel('Экран')
        screen.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        screen.setFont(QFont('MS Shell Dlg 2', 20))
        screen.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        screen.setStyleSheet('background: rgb(0, 0, 0); color: rgb(255, 255, 255);')
        #
        indent = QLabel('')
        indent.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(screen)
        self.verticalLayout.addWidget(indent)
        #
        about = len(str(self.d_row))
        for row in range(self.d_row):
            label = QLabel(f'{row + 1}{"  " * (about - len(str(row + 1)))}')
            label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
            label.setFont(QFont('PT Mono', 20))
            #
            place_layout = QHBoxLayout()
            place_layout.addWidget(label)
            for place in range(self.d_places):
                button = QPushButton(str(place + 1), objectName='buttonPlace')
                button.setFont(QFont('MS Shell Dlg 2', 20))
                button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                if (row + 1, place + 1) in self.take_place:
                    button.setStyleSheet(
                        '#buttonPlace:hover {background-color: rgb(255, 165, 0);}'
                        '#buttonPlace:!hover {background-color: rgb(31, 174, 233);}'
                    )
                    button.clicked.connect(lambda s, b=button, r=row + 1, p=place + 1: self.click_free(b, r, p))
                else:
                    button.setStyleSheet(
                        '#buttonPlace:hover {background-color: rgb(245, 245, 245);}'
                        '#buttonPlace:!hover {background-color: rgb(225, 225, 225);}'
                    )
                    button.clicked.connect(lambda s, b=button, r=row + 1, p=place + 1: self.click_occupy(b, r, p))
                #
                place_layout.addWidget(button)
            self.verticalLayout.addLayout(place_layout)

        self.setLayout(self.verticalLayout)

    def click_free(self, button: QPushButton, row: int, place: int) -> None:
        try:
            self.take_place.remove((row, place))
            button.setStyleSheet(
                '#buttonPlace:hover {background-color: rgb(245, 245, 245);}'
                '#buttonPlace:!hover {background-color: rgb(225, 225, 225);}'
            )
            button.clicked.connect(lambda s, b=button, r=row, p=place: self.click_occupy(b, r, p))
        except (ValueError, KeyError):
            pass

    def click_occupy(self, button: QPushButton, row: int, place: int) -> None:
        try:
            self.take_place.add((row, place))
            button.setStyleSheet(
                '#buttonPlace:hover {background-color: rgb(255, 165, 0);}'
                '#buttonPlace:!hover {background-color: rgb(31, 174, 233);}'
            )
            button.clicked.connect(lambda s, b=button, r=row, p=place: self.click_free(b, r, p))
        except (ValueError, KeyError):
            pass
