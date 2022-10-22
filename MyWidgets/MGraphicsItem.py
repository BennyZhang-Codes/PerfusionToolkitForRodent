from math import ceil
from matplotlib.pyplot import cla

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal, QLine, QObject
from PySide6.QtGui import QImage, QPixmap, QIcon, QResizeEvent, QMouseEvent, QCursor, QColor, QWheelEvent
from PySide6.QtGui import QPainter, QPainterPath, QPen

from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsSceneMoveEvent, QGraphicsSceneWheelEvent, QGraphicsSceneHoverEvent
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMenu, QScrollBar
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsPixmapItem
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem
from PySide6.QtWidgets import QGraphicsSceneContextMenuEvent

class MGraphicsItem_Signal(QObject):
    ellipse_location = Signal(tuple)
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

class MGraphicsItem(QGraphicsItem):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.setSelected(False)   
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        # self.setSelected(True)
        pos = event.scenePos()
        self.x_init = pos.x()
        self.y_init = pos.y()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        pos = event.scenePos()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            x_diff = pos.x() - self.x_init
            y_diff = pos.y() - self.y_init
            self.setX(self.x() + x_diff)
            self.setY(self.y() + y_diff)
            self.x_init = pos.x()
            self.y_init = pos.y()

    # def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
    #     self.setSelected(False)


class MGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super().__init__(None)

    def _maptoPixmap(self, pos: QPointF) -> QPointF:
        pix_pos = self.mapFromScene(pos)
        x = pix_pos.x()
        y = pix_pos.y()
        return QPointF(ceil(x), ceil(y))

        # width = self.pixmap().width()
        # height = self.pixmap().height()
        # x_check = x > 0 and x < width
        # y_check = y > 0 and y < height 
        # print(x, y)   
        # if x_check and y_check:
            # return QPointF(ceil(x), ceil(y))
        # else:
        #     return QPointF(0, 0)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pass
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return None
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return None

class MGraphicsEllipseItem(QGraphicsEllipseItem, MGraphicsItem):
    seleceted_color = QColor()
    signal = MGraphicsItem_Signal()
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.setFlag(MGraphicsEllipseItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.hoverentered = True
        self.x_negtive = False
        self.x_positive = False
        self.y_negtive = False
        self.y_positive = False

        self._axis_long = 60
        self._axis_short = 40
        self._updateRect()
 
    def _updateRect(self):
        self._point_lefttop = QPointF(-(self._axis_long/2), -(self._axis_short)/2)
        self._point_rightbottom = QPointF((self._axis_long/2), (self._axis_short)/2)
        self.setRect(self._point_lefttop.x(), self._point_lefttop.y(), self._axis_long, self._axis_short)

    @property
    def hoverEnter(self):
        return self.hoverentered

    def setup(self):
        print(self.rect())
        self._line_left = QGraphicsLineItem(QLine(-20,-20,-20,20), self)
        self._line_right = QGraphicsLineItem(QLine(20,-20,20,20), self)
        self._line_top = QGraphicsLineItem(QLine(-20,-20,20,-20), self)
        self._line_bottom = QGraphicsLineItem(QLine(-20,20,20,20), self)
    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        item_pos = self.mapFromScene(pos)
        x_diff = pos.x() - self.x_init
        y_diff = pos.y() - self.y_init
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            if self.x_positive or self.x_negtive or self.y_positive or self.y_negtive:
                if self.x_positive:
                    self._axis_long = self._axis_long + x_diff*2
                    print(self._axis_long)
                elif self.x_negtive:
                    self._axis_long = self._axis_long - x_diff*2
                elif self.y_positive:
                    self._axis_short = self._axis_short + y_diff*2
                elif self.y_negtive:
                    self._axis_short = self._axis_short - y_diff*2
                self.x_init = pos.x()
                self.y_init = pos.y()
                self._check_axis()
                self._updateRect()
                self.update()
            else:
                self.setX(self.x() + x_diff)
                self.setY(self.y() + y_diff)
                self.x_init = pos.x()
                self.y_init = pos.y()

        if event.buttons() == Qt.RightButton | event.button() == Qt.MouseButton.RightButton:
            self.setRotation(self.rotation()+y_diff)
        
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('ellipse released')
        self.signal.ellipse_location.emit((self.mapToScene(self._point_lefttop), self.mapToScene(self._point_rightbottom)))
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        angle = event.delta()
        value = int(angle//120)
        cur_scale = 1 + 0.1 * value
        self._axis_long = max(5, cur_scale * self._axis_long)
        self._axis_short = max(5, cur_scale * self._axis_short)

        bef_pos = self.pos()
        cursor_pos = event.scenePos()
        cursor_pos_x = cursor_pos.x()
        cursor_pos_y = cursor_pos.y()
        ratio_x = (cursor_pos_x - bef_pos.x())/(self.rect().width())
        ratio_y = (cursor_pos_y - bef_pos.y())/(self.rect().height())
        aft_cursor_pos_x = bef_pos.x() + ratio_x * (self.rect().width()*cur_scale)
        aft_cursor_pos_y = bef_pos.y() + ratio_y * (self.rect().height()*cur_scale)
        self._updateRect()
        self.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
        self.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverentered = True
        self.setSelected(True)
        self.setFocus()
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # print
        if event.pos().x() > self._axis_long * 0.45:
            self.x_positive = True
        elif event.pos().x() < - self._axis_long * 0.45:
            self.x_negtive = True
        else:
            self.x_negtive = False
            self.x_positive = False

        if event.pos().y() > self._axis_short * 0.45:
            self.y_positive = True
        elif event.pos().y() < - self._axis_short * 0.45:
            self.y_negtive = True
        else:
            self.y_negtive = False
            self.y_positive = False




        self.update()
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverentered = False
        self.setSelected(False)
        self.update()
        return super().hoverLeaveEvent(event)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        self._pop_menu()
        return super().contextMenuEvent(event)

    def paint(self, painter: QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget) -> None:
        pen = painter.pen()
        pen.setWidthF(0)
        super().paint(painter, option, widget)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.hoverentered:

            pen.setColor(QColor(255,255,255, 255))
            pen.setWidthF(2)
            painter.setPen(pen)
            painter.drawLine(-5, 0, 5, 0)
            painter.drawLine(0, -5, 0, 5)
            if self.x_positive or self.x_negtive:
                pen.setWidthF(5)
                painter.setPen(pen)
                painter.drawArc(self.rect(), -30*16, 60*16)
                painter.drawArc(self.rect(), 150*16, 60*16)

            if self.y_positive or self.y_negtive:
                pen.setWidthF(5)
                painter.setPen(pen)
                painter.drawArc(self.rect(), 60*16, 60*16)
                painter.drawArc(self.rect(), 240*16, 60*16)

    def _pop_menu(self):
        menu = QMenu()
        action_window = menu.addAction('Window')
        # action_window.triggered.connect(self._action_window)
        action_series = menu.addAction('Series Scroll')
        # action_series.triggered.connect(self._action_series)
        action_move = menu.addAction('delete')
        # action_move.triggered.connect(self._action_move)
        menu.exec_(QCursor.pos())

    def _check_axis(self):
        self._axis_long = max(10, self._axis_long)
        self._axis_short = max(10, self._axis_short)


class MGraphicsPolygonItem(QGraphicsPolygonItem, MGraphicsItem):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  


    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        rect = self.boundingRect()
        print(rect)
        print(self.pos())
        angle = event.delta()
        value = int(angle//120)
        bef_scale = self.scale()
        cur_scale = max(0.2, bef_scale+0.2*value)
        bef_pos = self.pos()
        cursor_pos = event.scenePos()
        cursor_pos_x = cursor_pos.x()
        cursor_pos_y = cursor_pos.y()
        ratio_x = (cursor_pos_x - bef_pos.x())/(rect.width()*bef_scale)
        ratio_y = (cursor_pos_y - bef_pos.y())/(rect.height()*bef_scale)
        aft_cursor_pos_x = bef_pos.x() + ratio_x * (rect.width()*cur_scale)
        aft_cursor_pos_y = bef_pos.y() + ratio_y * (rect.height()*cur_scale)
        self.setScale(cur_scale)
        self.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
        self.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))


