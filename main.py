from methods import get_image, get_toponym_coords
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel

WIDTH, HEIGHT = 900, 600  # Размеры окна
SCREENX, SCREENY = 1920, 1080  # Разрешение экрана


class YandexMap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()  # инициализация окна
        self.toponym = None
        self.add_data()  # метод добавления данных об изображении карты
        self.change_image()  # метод смены изображения
        self.setFocus()

    def initUI(self):
        self.setGeometry(SCREENX // 2 - WIDTH // 2, SCREENY // 2 - HEIGHT // 2, WIDTH, HEIGHT)
        self.setWindowTitle('Яндекс карты')

        self.image = QLabel(self)
        self.image.move(80, 60)
        self.image.resize(600, 450)

        self.line_edit = QLineEdit(self)
        self.line_edit.resize(600, 30)
        self.line_edit.move(80, 30)

        self.search_button = QPushButton(self)
        self.search_button.setText('Искать')
        self.search_button.move(700, 30)
        self.search_button.resize(100, 30)
        self.search_button.clicked.connect(self.add_data)

        self.change_button = QPushButton(self)
        self.change_button.resize(150, 30)
        self.change_button.setText('Переключить слой карты')
        self.change_button.move(700, 60)
        self.change_button.clicked.connect(self.change_image_view)


    def change_image(self):
        img = get_image(self.lon, self.lat, self.delta, self.views[self.view_id])
        img.save('img.png')
        self.pixmap = QPixmap('img.png')
        self.image.setPixmap(self.pixmap)
        self.status_bar.clearMessage()

    def set_placeholder(self):  # Метод установки шаблона, если изображение не найдено
        self.pixmap = QPixmap('placeholder.png')
        self.image.setPixmap(self.pixmap)
        self.status_bar.showMessage(self.line_edit.text() + ' не найдено')

    def add_data(self):
        if not self.line_edit.text():
            self.set_placeholder()
            return

        self.toponym = get_toponym_coords(self.line_edit.text())

        if not self.toponym:
            self.set_placeholder()
            return
        self.views = ["map", "sat", "skl"]  # режимы показа карты
        self.lon = self.toponym[0]  # долгота
        self.lat = self.toponym[1]  # ширина
        self.delta = 15  # масштаб
        self.view_id = 0  # текущий режим показа карты

    def change_image_view(self):  # метод смены режима показа карты
        if not self.toponym:
            return
        if self.view_id < 2:
            self.view_id += 1
        else:
            self.view_id = 0
        self.change_image()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:  # перемещение центра карты влево
            if self.lon - 360 / (2 ** (self.delta + 8)) * 600 > -180:
                self.lon -= 360 / (2 ** (self.delta + 8)) * 600
                self.change_image()
        if event.key() == Qt.Key_Right:  # перемещение центра карты вправо
            if self.lon + 360 / (2 ** (self.delta + 8)) * 600 < 180:
                self.lon += 360 / (2 ** (self.delta + 8)) * 600
                self.change_image()
        if event.key() == Qt.Key_Up:  # перемещение центра карты вверх
            if self.lat + 180 / (2 ** (self.delta + 8)) * 450 < 85:
                self.lat += 180 / (2 ** (self.delta + 8)) * 450
                self.change_image()
        if event.key() == Qt.Key_Down:  # перемещение центра карты вниз
            if self.lat - 180 / (2 ** (self.delta + 8)) * 450 > -85:
                self.lat -= 180 / (2 ** (self.delta + 8)) * 450
                self.change_image()
        if event.key() == Qt.Key_PageUp:  # увеличение масштаба
            if int(self.delta) < 20:
                self.delta += 1
                self.change_image()
        if event.key() == Qt.Key_PageDown:  # уменьшение масштаба
            if int(self.delta) > 4:
                self.delta -= 1
                self.change_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ym = YandexMap()
    ym.show()
    sys.exit(app.exec())
