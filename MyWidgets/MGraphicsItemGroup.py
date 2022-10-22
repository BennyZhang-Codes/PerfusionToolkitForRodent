from math import ceil

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal
from PySide6.QtGui import QImage, QPixmap, QIcon, QResizeEvent, QMouseEvent, QCursor, QColor, QWheelEvent

from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsSceneMoveEvent, QGraphicsSceneWheelEvent
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMenu, QGraphicsItemGroup
from PySide6.QtWidgets import  QGraphicsView, QLabel, QSizePolicy, QFrame
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsPixmapItem
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem


class MGraphicsItemGroup(QGraphicsItemGroup):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable)
        # self.setFlag(QGraphicsPixmapItem.ItemIsMovable) 

