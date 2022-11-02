from asyncio.windows_events import NULL
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *

from PIL import Image
from pydicom import dcmread
import numpy as np
import cv2

from MyWidgets.MWidget import MResult
from modules.utils.colormap import MColorMap
from MyWidgets.MComboBox.ColorMap import MColorMapComboBox

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        img = MResult(self)
        ds = dcmread(r'E:\A30\DSC\Im00008.dcm')
        img.setImgArray(ds.pixel_array)

        combox = MColorMapComboBox()
        

        self.ColorMap = MColorMap()

        self.w = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(combox)
        layout.addWidget(img)
        layout.setStretch(0,1)
        layout.setStretch(1,5)

        self.w.setLayout(layout)


        xdata = np.arange(20)
        ydata = np.arange(20)**2
        
        




        self.setCentralWidget(self.w)
        self.resize(500, 300)
        self.setWindowTitle('Color')






def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()