from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QObject
from PyQt5.QtGui import QFont, QEnterEvent, QPainter, QColor, QPen
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpacerItem, QSizePolicy, QPushButton)

from Code.dialogs import FormInfo


class TitleBar(QWidget):
    # Сигнал минимизации окна
    windowMinimumed = pyqtSignal()
    # увеличить максимальный сигнал окна
    windowMaximumed = pyqtSignal()
    # сигнал восстановления окна
    windowNormaled = pyqtSignal()
    # сигнал закрытия окна
    windowClosed = pyqtSignal()
    # Окно мобильных
    windowMoved = pyqtSignal(QPoint)
    # Сигнал информации
    signalButtonInfo = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super(TitleBar, self).__init__(*args, **kwargs)

        # Поддержка настройки фона qss
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        self.iconSize = 20  # Размер значка по умолчанию

        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        # значок окна
        self.iconLabel = QLabel(self)
        # self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)

        # название окна
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        layout.addWidget(self.titleLabel)

        # Средний телескопический бар
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Использовать шрифт для отображения значков
        font = QFont()
        font.setFamily('Webdings')

        self.buttonInfo = QPushButton(
            'i', self, clicked=self.showButtonInfo, font=font, objectName='buttonInfo')
        layout.addWidget(self.buttonInfo)

        self.buttonMinimum = QPushButton(
            '0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        layout.addWidget(self.buttonMinimum)

        self.buttonMaximum = QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)

        self.buttonClose = QPushButton(
            'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)

        # начальная высота
        self.setHeight()

    # Вызывается по нажатию кнопки buttonInfo
    def showButtonInfo(self) -> None:
        dialog = FormInfo()
        dialog.exec_()
        dialog.deleteLater()
        self.signalButtonInfo.emit()

    def showMaximized(self) -> None:
        if self.buttonMaximum.text() == '1':
            # Максимизировать
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # Восстановить
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height: int = 38) -> None:
        """ Установка высоты строки заголовка """
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # Размер правой кнопки
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

        self.buttonInfo.setMinimumSize(height, height)
        self.buttonInfo.setMaximumSize(height, height)

    def setTitle(self, title: str = '') -> None:
        """ Установить заголовок """
        self.titleLabel.setText(title)
        self.titleLabel.setStyleSheet('color: white;')

    def setIcon(self, icon: QtGui) -> None:
        """ настройки значокa """
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size) -> None:
        """ Установить размер значка """
        self.iconSize = size

    def enterEvent(self, event: QtGui) -> None:
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui) -> None:
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event: QtGui) -> None:
        """ Событие клика мыши """
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event: QtGui) -> None:
        """ Событие отказов мыши """
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event: QtGui) -> None:
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()


# Перечислить верхнюю левую, нижнюю правую и четыре неподвижные точки
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class MainWindow(QWidget):
    Margins = 5

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self._pressed = False
        self.Direction = None

        # Фон прозрачный
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Нет границы
        self.setWindowFlag(Qt.FramelessWindowHint)
        # Отслеживание мыши
        self.setMouseTracking(True)

        layout = QVBoxLayout(self, spacing=0)
        # Зарезервировать границы для изменения размера окна без полей
        layout.setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)
        # Панель заголовка
        self.titleBar = TitleBar(self)
        layout.addWidget(self.titleBar)

        # сигналы
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)

    def setTitleBarHeight(self, height: int = 38) -> None:
        """ Установка высоты строки заголовка """
        self.titleBar.setHeight(height)

    def setIconSize(self, size) -> None:
        """ Установка размера значка """
        self.titleBar.setIconSize(size)

    def setWidget(self, widget: QWidget) -> None:
        """ Настройте свои собственные элементы управления """
        if hasattr(self, '_widget'):
            return
        self._widget = widget
        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos: QtCore) -> None:
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # перемещать максимизированный или полноэкранный режим не допускается
            return
        super(MainWindow, self).move(pos)

    def showMaximized(self) -> None:
        """ Чтобы максимизировать, удалите верхнюю, нижнюю, левую и правую границы.
            Если вы не удалите его, в пограничной области будут пробелы. """
        super(MainWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self) -> None:
        """ Восстановить, сохранить верхнюю и нижнюю левую и правую границы,
            иначе нет границы, которую нельзя отрегулировать """
        super(MainWindow, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

    def eventFilter(self, obj: QObject, event: QtGui):
        """ Фильтр событий, используемый для решения мыши в других элементах
            управления и восстановления стандартного стиля мыши """
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(MainWindow, self).eventFilter(obj, event)

    def paintEvent(self, event: QtGui) -> None:
        """ Поскольку это полностью прозрачное фоновое окно, жесткая для поиска
            граница с прозрачностью 1 рисуется в событии перерисовывания, чтобы отрегулировать размер окна. """
        super(MainWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event: QtGui) -> None:
        """ Событие клика мыши """
        super(MainWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._m_pos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event: QtGui) -> None:
        """ Событие отказов мыши """
        super(MainWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event: QtGui) -> None:
        """ Событие перемещения мыши """
        super(MainWindow, self).mouseMoveEvent(event)
        pos = event.pos()
        x_pos, y_pos = pos.x(), pos.y()
        w_m, h_m = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if x_pos <= self.Margins and y_pos <= self.Margins:  # Верхний левый угол
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif w_m <= x_pos <= self.width() and h_m <= y_pos <= self.height():  # Нижний правый угол
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif w_m <= x_pos and y_pos <= self.Margins:  # верхний правый угол
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif x_pos <= self.Margins and h_m <= y_pos:  # Нижний левый угол
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= x_pos <= self.Margins <= y_pos <= h_m:  # Влево
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif w_m <= x_pos <= self.width() and self.Margins <= y_pos <= h_m:  # Право
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif w_m >= x_pos >= self.Margins >= y_pos >= 0:  # выше
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= x_pos <= w_m and h_m <= y_pos <= self.height():  # ниже
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def _resizeWidget(self, pos: QtCore) -> None:
        """ Отрегулируйте размер окна """
        if self.Direction is None:
            return
        m_pos = pos - self._m_pos
        x_pos, y_pos = m_pos.x(), m_pos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:  # Верхний левый угол
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos
        elif self.Direction == RightBottom:  # Нижний правый угол
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._m_pos = pos
            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._m_pos = pos
        elif self.Direction == RightTop:  # верхний правый угол
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._m_pos.setX(pos.x())
        elif self.Direction == LeftBottom:  # Нижний левый угол
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos
            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._m_pos.setY(pos.y())
        elif self.Direction == Left:  # Влево
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos
            else:
                return
        elif self.Direction == Right:  # Право
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._m_pos = pos
            else:
                return
        elif self.Direction == Top:  # выше
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos
            else:
                return
        elif self.Direction == Bottom:  # ниже
            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._m_pos = pos
            else:
                return
        self.setGeometry(x, y, w, h)
