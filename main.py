import sys
import os

import requests
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication, QRadioButton, QLineEdit, QPushButton, QStatusBar
from utilities2 import get_static_api_image

API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"


class MainWindow(QMainWindow):
    map_label: QLabel
    dark_theme: QRadioButton
    light_theme: QRadioButton
    lineEdit: QLineEdit
    search_button: QPushButton
    mainWindow: QMainWindow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('window_for_map.ui', self)
        self.map = [2.2944813, 48.8583701]
        self.z = 12
        self.theme = 'light'
        self.refresh_map()
        self.dark_theme.clicked.connect(self.change_theme)
        self.light_theme.clicked.connect(self.change_theme)
        self.search_button.clicked.connect(self.search_address)
        self.lineEdit.setPlaceholderText('Введит адрес')

        self.statusbar = QStatusBar(self)
        self.statusbar.move(20, 500)
        self.statusbar.resize(400, 30)

    def refresh_map(self, flag=False):
        response = get_static_api_image(self.map, self.z, self.theme, True if flag else False)
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
        if key == Qt.Key.Key_Enter:
            self.search_address()
        else:
            if key == Qt.Key.Key_PageUp:
                self.z += 1 if self.z < 19 else 0
            elif key == Qt.Key.Key_PageDown:
                self.z -= 1 if self.z > 2 else 0
            elif key == Qt.Key.Key_Left:
                self.map[0] -= n
            elif key == Qt.Key.Key_Right:
                self.map[0] += n
            elif key == Qt.Key.Key_Up:
                self.map[1] += n
            elif key == Qt.Key.Key_Down:
                self.map[1] -= n
            self.refresh_map()

    def change_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.refresh_map()

    def search_address(self):
        address = self.lineEdit.text()
        geo_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json"
        if address:
            self.statusbar.showMessage('') if self.statusbar.currentMessage() != '' else False

            try:
                response = requests.get(geo_request)
                if response:
                    json_response = response.json()
                else:
                    return None
                features = json_response['response']['GeoObjectCollection']['featureMember']
                t = features[0]['GeoObject'] if features else None
                coords = t["Point"]["pos"]
                self.map = [float(coords.split()[0]), float(coords.split()[1])]
                self.refresh_map(True)
            except:
                self.statusbar.showMessage('Вы ввели неправельный адрес')
        else:
            self.statusbar.showMessage('Вы ввели неправельный адрес')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
