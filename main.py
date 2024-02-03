from methods import get_image, get_toponym_coords
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel

WIDTH, HEIGHT = 900, 600  # Размеры окна
SCREENX, SCREENY = 1920, 1080  # Разрешение экрана


class YandexMap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()  # инициализация окна
        self.add_data()  # метод добавления данных об изображении карты
        self.change_image()  # метод смены изображения

    def initUI(self):
        self.setGeometry(SCREENX // 2 - WIDTH // 2, SCREENY // 2 - HEIGHT // 2, WIDTH, HEIGHT)
        self.setWindowTitle('Яндекс карты')

        self.image = QLabel(self)
        self.image.move(80, 60)
        self.image.resize(600, 450)

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

    def add_data(self):
        self.views = ["map", "sat", "skl"]  # режимы показа карты
        self.lon = "37.530887"  # долгота
        self.lat = "55.703118"  # ширина
        self.delta = "0.002"  # масштаб
        self.view_id = 0  # текущий режим показа карты

    def change_image_view(self):  # метод смены режима показа карты
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
