import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *

from PIL import Image, ImageColor
from pydicom import dcmread
import numpy as np
import cv2

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        label = QLabel()
        g = QLinearGradient()
        g.setColorAt(0, Qt.red)
        g.setColorAt(1, Qt.blue)


        ds = dcmread(r'E:\A30\DSC\Im00008.dcm')

        
        img = np.clip(ds.pixel_array, a_min=100, a_max=2000)
        img = ((img - img.min()) / max(1, img.max() - img.min()))*255

        a = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_RAINBOW)
        img = Image.fromarray(a)
        pix = img.toqpixmap()
        
        label.setPixmap(pix)
        self.setCentralWidget(label)
        self.resize(500, 300)
        self.setWindowTitle('Color')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()