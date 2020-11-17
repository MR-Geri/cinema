from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WidgetCinemasCard(QWidget):
    def __init__(self, user, title, quantity_halls, quantity_sessions, quantity_places):
        super().__init__()
        self.gridLayout = QGridLayout()
        #
        self.label_title = QLabel(title)
        self.label_halls = QLabel(f'Всего залов: {quantity_halls}')
        self.label_sessions = QLabel(f'Всего сеансов: {quantity_sessions}')
        self.label_places = QLabel(f'Всего мест: {quantity_places}')
        #
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_title.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_halls.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_sessions.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_places.setFont(QFont('MS Shell Dlg 2', 16))
        #
        self.button_browse = QPushButton('Просмотреть')
        self.button_browse.setFont(QFont('MS Shell Dlg 2', 16))
        #
        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 0)
        self.gridLayout.addWidget(self.label_halls, 2, 0, 1, 0)
        self.gridLayout.addWidget(self.label_sessions, 3, 0, 1, 0)
        self.gridLayout.addWidget(self.label_places, 4, 0, 1, 0)
        if user == 'Администратор':
            self.button_edit = QPushButton('Изменить')
            self.button_edit.setFont(QFont('MS Shell Dlg 2', 16))
            self.gridLayout.addWidget(self.button_edit, 5, 0)
            self.gridLayout.addWidget(self.button_browse, 5, 1)
            #
        else:
            self.gridLayout.addWidget(self.button_browse, 5, 0, 1, 0)
        #
        self.setLayout(self.gridLayout)


class WidgetCinemaCard(QWidget):
    def __init__(self, user, title, quantity_sessions, quantity_places, sessions):
        super().__init__()
        self.gridLayout = QGridLayout()
        #
        self.label_title = QLabel(title)
        self.label_sessions = QLabel(f'Количество сеансов: {quantity_sessions}')
        self.label_places = QLabel(f'Количество мест: {quantity_places}')
        #
        self.sessions = QListWidget()
        self.sessions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        for title_session in sessions:
            #
            card = QLabel(title_session)
            card.setFont(QFont('MS Shell Dlg 2', 16))
            card.setAlignment(Qt.AlignHCenter)
            #
            q_list_card = QListWidgetItem(self.sessions)
            q_list_card.setSizeHint(card.sizeHint())
            self.sessions.addItem(q_list_card)
            self.sessions.setItemWidget(q_list_card, card)
        #
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_title.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_sessions.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_places.setFont(QFont('MS Shell Dlg 2', 16))
        #
        self.button_browse = QPushButton('Просмотреть')
        self.button_browse.setFont(QFont('MS Shell Dlg 2', 16))
        #
        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 0)
        self.gridLayout.addWidget(self.label_sessions, 2, 0)
        self.gridLayout.addWidget(self.label_places, 3, 0)
        self.gridLayout.addWidget(self.label_places, 3, 0)
        self.gridLayout.addWidget(self.sessions, 2, 1, 2, 1)
        if user == 'Администратор':
            self.button_edit = QPushButton('Изменить')
            self.button_edit.setFont(QFont('MS Shell Dlg 2', 16))
            self.gridLayout.addWidget(self.button_edit, 4, 0)
            self.gridLayout.addWidget(self.button_browse, 4, 1)
            #
        else:
            self.gridLayout.addWidget(self.button_browse, 4, 0, 1, 0)
        #
        self.setLayout(self.gridLayout)


class WidgetHallCard(QWidget):
    def __init__(self, user, title, date, time, duration):
        super().__init__()
        self.gridLayout = QGridLayout()
        #
        self.label_title = QLabel(title)
        self.label_date = QLabel(f'Дата: {date}')
        self.label_time = QLabel(f'Время: {time}')
        self.label_duration = QLabel(f'Продолжительность: {duration}')
        #
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_title.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_date.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_time.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_duration.setFont(QFont('MS Shell Dlg 2', 16))
        #
        self.button_browse = QPushButton('Просмотреть')
        self.button_browse.setFont(QFont('MS Shell Dlg 2', 16))
        #
        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 0)
        self.gridLayout.addWidget(self.label_date, 2, 0, 1, 0)
        self.gridLayout.addWidget(self.label_time, 3, 0, 1, 0)
        self.gridLayout.addWidget(self.label_duration, 4, 0, 1, 0)
        if user == 'Администратор':
            self.button_edit = QPushButton('Изменить')
            self.button_edit.setFont(QFont('MS Shell Dlg 2', 16))
            self.gridLayout.addWidget(self.button_edit, 5, 0)
            self.gridLayout.addWidget(self.button_browse, 5, 1)
            #
        else:
            self.gridLayout.addWidget(self.button_browse, 5, 0, 1, 0)
        #
        self.setLayout(self.gridLayout)
