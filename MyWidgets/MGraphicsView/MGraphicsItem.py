
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


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
    def __init_MRoiItem__(self, parent=None) -> None:
        super().__init_MGraphicsItem__()
        self.ItemType = 'roi'
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setSelected(False) 
        self.setAcceptHoverEvents(True)
        self._HoverEntered = True
        if parent is not None:
            self._menu = QMenu(parent)
        else:
            self._menu = QMenu()
        
        self._ColorDialog = QColorDialog()

        self.setup_menu()

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

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = True
        self.setSelected(True)
        self.setZValue(2)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(False)
        self.setZValue(1)
        return super().hoverEnterEvent(event)

    def setup_menu(self) -> None:
        pass

    @property
    def hoverEnter(self) -> bool:
        return self._HoverEntered
    
    @hoverEnter.setter
    def hoverEnter(self, enter: bool) -> None:
        self._HoverEntered = enter

    @property
    def menu(self) -> QMenu:
        return self._menu

    @property
    def ColorDialog(self) -> QColorDialog:
        return self._ColorDialog
