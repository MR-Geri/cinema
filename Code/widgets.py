from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Code.dialogs import Form_login
from Code.data_base import get_data_base


class WidgetCinema(QMainWindow):
    def __init__(self, path_base_file):
        super().__init__()
        uic.loadUi('../qt/cinema.ui', self)
        self.path_base_file = path_base_file
        self.update_()

    def update_(self):
        scrollLayout = QFormLayout()
        for id_, title in get_data_base(self.path_base_file, """SELECT * FROM Cinemas"""):
            group = QGridLayout()
            label_title = QLabel(title)
            label_title.setAlignment(Qt.AlignHCenter)
            num_halls = get_data_base(
                self.path_base_file,
                """SELECT COUNT(*) FROM Halls h WHERE h.cinema_id = ?""",
                (id_, )
            )[0][0]
            label_halls = QLabel(f'Всего залов: {num_halls}')
            group.addWidget(label_title, 1, 0)
            group.addWidget(label_halls, 2, 0)
            scrollLayout.addRow(group)
        scrollWidget = QWidget()
        scrollWidget.setLayout(scrollLayout)
        self.scroll.setWidget(scrollWidget)


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
            dialog = Form_login(self.path_base_file)
            if dialog.exec_() == QDialog.Accepted:
                self.cinema = WidgetCinema(self.path_base_file)
                self.cinema.show()
                self.hide()
            dialog.deleteLater()
