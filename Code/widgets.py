from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Code.dialogs import Form_login
from Code.data_base import get_data_base


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


class WidgetCinema(QMainWindow):
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


class WidgetStart(QMainWindow):
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
                self.cinema = WidgetCinema(self.path_base_file, dialog.user)
                self.cinema.show()
                self.hide()
            dialog.deleteLater()
