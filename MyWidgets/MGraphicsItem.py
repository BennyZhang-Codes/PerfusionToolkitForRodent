from math import ceil, sqrt
from types import NoneType

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal, QLine, QObject, QRectF
from PySide6.QtGui import QImage, QPixmap, QIcon, QResizeEvent, QMouseEvent, QCursor, QColor, QWheelEvent
from PySide6.QtGui import QPainter, QPainterPath, QPen, QPolygon, QPolygonF

from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsSceneMoveEvent, QGraphicsSceneWheelEvent, QGraphicsSceneHoverEvent
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMenu, QScrollBar, QColorDialog
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsPixmapItem
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem
from PySide6.QtWidgets import QGraphicsSceneContextMenuEvent


class MGraphicsItem_Signal(QObject):
    ellipse_location = Signal(tuple)
    ellipse_shape = Signal(QPainterPath)
    item_delete = Signal(QGraphicsItem)
    node_selected = Signal(QGraphicsItem)
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

class MGraphicsItem(QGraphicsItem):
    def __init_MGraphicsItem__(self) -> None:
        self._itemtype = None

    @property
    def ItemType(self) -> str:
        return self._itemtype

    @ItemType.setter
    def ItemType(self, itemtype: str) -> None:
        if itemtype in [
            'roi',
            'image',
            'info',
        ]:
            self._itemtype = itemtype
        else:
            raise ValueError('Unsupported ItemType: {}'.format(itemtype))

class MRoiItem(MGraphicsItem):
    def __init_MRoiItem__(self) -> None:
        super().__init_MGraphicsItem__()
        self.ItemType = 'roi'
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setSelected(False) 
        self.setAcceptHoverEvents(True)
        self._HoverEntered = True

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        pos = event.scenePos()
        self.x_init = pos.x()
        self.y_init = pos.y()
        

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> tuple:
        pos = event.scenePos()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            x_diff = pos.x() - self.x_init
            y_diff = pos.y() - self.y_init
            self.setX(self.x() + x_diff)
            self.setY(self.y() + y_diff)
            self.x_init = pos.x()
            self.y_init = pos.y()

    @property
    def hoverEnter(self) -> bool:
        return self._HoverEntered
    
    @hoverEnter.setter
    def hoverEnter(self, enter: bool) -> None:
        self._HoverEntered = enter
