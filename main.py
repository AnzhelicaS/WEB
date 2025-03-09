import sys
import os

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication, QRadioButton
from utilities2 import get_static_api_image


class MainWindow(QMainWindow):
    map_label: QLabel
    dark_theme: QRadioButton
    light_theme: QRadioButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('window_for_map.ui', self)
        self.map = [2.2944813, 48.8583701]
        self.z = 12
        self.theme = 'light'
        self.refresh_map()
        self.dark_theme.clicked.connect(self.change_theme_on_dark)
        self.light_theme.clicked.connect(self.change_theme_on_light)

    def refresh_map(self):
        response = get_static_api_image(self.map, self.z, self.theme)
        if response:
            with open('tmp.png', mode='wb') as tmp:
                tmp.write(response)
            pixmap = QPixmap()
            pixmap.load('tmp.png')
            os.remove('tmp.png')
            self.map_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        n = 0.01 if self.z in range(13, 17) else 0.1 if self.z in range(8, 12) else 1 if range(3, 7) else 0
        if key == Qt.Key.Key_PageUp:
            self.z += 1 if self.z < 19 else 0
        elif key == Qt.Key.Key_PageDown:
            self.z -= 1 if self.z > 6 else 0
        elif key == Qt.Key.Key_Left:
            self.map[0] -= n
        elif key == Qt.Key.Key_Right:
            self.map[0] += n
        elif key == Qt.Key.Key_Up:
            self.map[1] += n
        elif key == Qt.Key.Key_Down:
            self.map[1] -= n
        self.refresh_map()

    def change_theme_on_dark(self):
        self.theme = 'dark'
        self.refresh_map()

    def change_theme_on_light(self):
        self.theme = 'light'
        self.refresh_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())