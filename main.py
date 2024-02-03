from methods import get_image, get_toponym_coords
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel

WIDTH, HEIGHT = 900, 600  # Размеры окна
SCREENX, SCREENY = 1920, 1080  # Разрешение экрана

img = get_image("37.530887", "55.703118", "0.002")
img.save('img.png')


class YandexMap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(SCREENX // 2 - WIDTH // 2, SCREENY // 2 - HEIGHT // 2, WIDTH, HEIGHT)
        self.setWindowTitle('Яндекс карты')

        self.pixmap = QPixmap('img.png')
        self.image = QLabel(self)
        self.image.move(80, 60)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ym = YandexMap()
    ym.show()
    sys.exit(app.exec())
