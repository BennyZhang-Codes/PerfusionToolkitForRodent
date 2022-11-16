import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from MyWidgets.MGraphicsView.MGraphicsView import MGraphicsView

class MGraphicsView_TimeSeries(MGraphicsView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def resizeEvent(self, event: QResizeEvent) -> None:
        return super().resizeEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        return super().mouseMoveEvent(event)
 
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)








if __name__ == '__main__':
    mGraphicView = MGraphicsView_TimeSeries()