from math import ceil, sqrt

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


from MyWidgets.MGraphicsItem import MRoiItem


class MGraphicsRectItem(QGraphicsRectItem, MRoiItem):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.__init_MRoiItem__()
        
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('press')
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # print('move'
        return super().mouseMoveEvent(event)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print('hover enter')
        self.hoverEnter = True
        self.setSelected(True)
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(False)
        return super().hoverLeaveEvent(event)

    def sceneEvent(self, event: QEvent) -> bool:
        return super().sceneEvent(event)

    

class MGraphicsPolygonItem(QGraphicsPolygonItem, MRoiItem):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.__init_MRoiItem__()
        # self.setHandlesChildEvents(True)
        poly = QPolygon()

        self.points = []
        for point in [QPoint(200, 250), QPoint(250, 290), QPoint(300, 380), QPoint(400, 300)]:

            rect_item = MGraphicsRectItem(-5,-5, 10, 10)
            rect_item.setPen(QColor(123,68,55,255))
            rect_item.setParentItem(self)
            rect_item.setPos(point)
            self.points.append(rect_item)

            poly.append(point)
        self.setPolygon(poly)
        # print(self.scene().items())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # pass

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # pass
        return super().mouseMoveEvent(event)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = True
        # self.setSelected(True)
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.update()
        # print('move')
        for item in self.childItems():
            pos = item.mapFromParent(self.mapFromScene(event.scenePos()))
            item.contains(pos)
        print(self.contains(event.scenePos()))
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(False)
        # print('leave')
        return super().hoverLeaveEvent(event)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        # angle = event.delta()
        # value = int(angle//120)

        # bef_scale = self.scale()
        # cur_scale = bef_scale + 0.1 * value
        # rect = self.boundingRect()
        # bef_pos = self.pos()
        # cursor_pos = event.scenePos()
        # cursor_pos_x = cursor_pos.x()
        # cursor_pos_y = cursor_pos.y()
        # ratio_x = (cursor_pos_x - bef_pos.x())/(rect.width()*bef_scale)
        # ratio_y = (cursor_pos_y - bef_pos.y())/(rect.height()*bef_scale)
        # aft_cursor_pos_x = bef_pos.x() + ratio_x * (rect.width()*cur_scale)
        # aft_cursor_pos_y = bef_pos.y() + ratio_y * (rect.height()*cur_scale)
        # self.setScale(cur_scale)
        # self.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
        # self.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))
        return super().wheelEvent(event)
    
    def sceneEvent(self, event: QEvent) -> bool:
        return super().sceneEvent(event)
    

