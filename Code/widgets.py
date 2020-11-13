from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WidgetCard(QWidget):
    def __init__(self, id_, title, quantity_halls, quantity_sessions, quantity_places):
        super().__init__()
        self.id_ = id_
        self.gridLayout = QGridLayout()
        #
        self.label_title = QLabel(title)
        self.label_halls = QLabel(f'Всего залов: {quantity_halls}')
        self.label_sessions = QLabel(f'Всего сеансов: {quantity_sessions}')
        self.label_places = QLabel(f'Всего мест: {quantity_places}')
        self.button_edit = QPushButton('Изменить')
        self.button_browse = QPushButton('Просмотреть')
        #
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_title.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_halls.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_sessions.setFont(QFont('MS Shell Dlg 2', 16))
        self.label_places.setFont(QFont('MS Shell Dlg 2', 16))
        self.button_edit.setFont(QFont('MS Shell Dlg 2', 16))
        self.button_browse.setFont(QFont('MS Shell Dlg 2', 16))
        #
        self.button_edit.clicked.connect(self.edit)
        self.button_browse.clicked.connect(self.browse)
        #
        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 0)
        self.gridLayout.addWidget(self.label_halls, 2, 0, 1, 0)
        self.gridLayout.addWidget(self.label_sessions, 3, 0, 1, 0)
        self.gridLayout.addWidget(self.label_places, 4, 0, 1, 0)
        self.gridLayout.addWidget(self.button_edit, 5, 0)
        self.gridLayout.addWidget(self.button_browse, 5, 1)
        #
        self.setLayout(self.gridLayout)

    def edit(self):
        print(f'Изменение {self.id_}')

    def browse(self):
        print(f'Просмотр {self.id_}')

