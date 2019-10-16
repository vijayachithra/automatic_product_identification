from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
import os,sys


def choose_image():
    app = QApplication(sys.argv)
    file_path = ''
    file_path, _ = QFileDialog.getOpenFileName(caption="Choose Image", directory=os.curdir,
                                                    filter="JPG Files (*.jpg);;BMP Files (*.bmp);;PNG Files (*.png);;")
    if file_path != '':
        return file_path
    else:
        return None
