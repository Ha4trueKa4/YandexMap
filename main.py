from methods import get_image, get_toponym_coords
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMainWindow

WIDTH, HEIGHT = 900, 600  # Размеры окна
SCREENX, SCREENY = 1920, 1080  # Разрешение экрана


class YandexMap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.toponym = None
        self.delta = 18  # масштаб
        self.initUI()  # инициализация окна

    def initUI(self):
        self.setGeometry(SCREENX // 2 - WIDTH // 2, SCREENY // 2 - HEIGHT // 2, WIDTH, HEIGHT)
        self.setWindowTitle('Яндекс карты')
        self.status_bar = self.statusBar()

        self.image = QLabel(self)
        self.image.move(80, 80)
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
        self.change_button.move(700, 80)
        self.change_button.clicked.connect(self.change_image_view)

    def set_placeholder(self):  # Метод установки шаблона, если изображение не найдено
        self.pixmap = QPixmap('placeholder.png')
        self.image.setPixmap(self.pixmap)
        self.status_bar.showMessage(self.line_edit.text() + ' не найдено')

    def change_image(self):  # Метод смены изображения карты
        img = get_image(self.lon, self.lat, self.delta, self.views[self.view_id])
        img.save('img.png')
        self.pixmap = QPixmap('img.png')
        self.image.setPixmap(self.pixmap)
        self.status_bar.clearMessage()

    def add_data(self):  # Инициализация данных карты
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
        self.view_id = 0  # текущий режим показа карты
        self.change_image()

    def change_image_view(self):  # метод смены режима показа карты
        if not self.toponym:
            return
        if self.view_id < 2:
            self.view_id += 1
        else:
            self.view_id = 0
        self.change_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ym = YandexMap()
    ym.show()
    sys.exit(app.exec())
