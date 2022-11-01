import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *

from PIL import Image, ImageColor
from pydicom import dcmread
import numpy as np
import cv2

from MyWidgets.MWidget import MResult

class Example(QMainWindow):
    def __init__(self):
        super().__init__()


        ds = dcmread(r'E:\A30\DSC\Im00008.dcm')


        res = MResult(self)
        res.setImgArray(ds.pixel_array)
        
        self.setCentralWidget(res)
        self.resize(500, 300)
        self.setWindowTitle('Color')






def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()