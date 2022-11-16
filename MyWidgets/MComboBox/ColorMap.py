
import numpy as np
import cv2
from PIL import Image

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *

from modules.utils.colormap import MColorMap


class MColorMapComboBox(QComboBox):
    ColorMap_size = QSize(120, 18)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ColorMap = MColorMap()


        self.setIconSize(self.ColorMap_size)
        # self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.setup()

    def setup(self) -> None:

        for i in range(len(self.ColorMap.colorlists)+22):
            self.ColorMap.idx = i

            a = np.expand_dims(np.arange(256), axis=0)
            cb = [a for i in range(25)]
            cb = np.concatenate(cb, axis=0).astype(np.uint8)
            cb = self.ColorMap.applyColorMap(cb)
            cb = Image.fromarray(cb)
            cb = cb.toqpixmap()
            cb = cb.scaled(self.ColorMap_size, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.addItem(cb, None)
