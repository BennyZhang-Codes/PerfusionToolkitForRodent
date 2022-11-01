
import numpy as np
import cv2
from PIL import Image

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *

from modules.utils.colormap import MColorMap


class MColorMapComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)


        self.addItem()