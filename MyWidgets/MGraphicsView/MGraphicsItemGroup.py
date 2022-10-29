from math import ceil

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class MGraphicsItemGroup(QGraphicsItemGroup):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable)
        # self.setFlag(QGraphicsPixmapItem.ItemIsMovable) 

