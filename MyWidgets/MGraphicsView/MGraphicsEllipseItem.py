from math import sqrt
from tkinter import Menu

from PySide6 import QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from MyWidgets.MGraphicsView.MGraphicsItem import MRoiItem


class MEllipseItem_Signal(QObject):
    ellipse_location = Signal(tuple)
    ellipse_shape = Signal(QPainterPath)
    item_delete = Signal(QGraphicsItem)
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

class MGraphicsEllipseItem(QGraphicsEllipseItem, MRoiItem):
    PEN_COLOR = QColor(49, 200, 10, 255)
    DEFAULT_COLOR = QColor(118,185,172,128)
    def __init__(self, parent) -> None:
        super().__init__()  
        self.__init_MRoiItem__(parent)
        self.signal = MEllipseItem_Signal()
        self.x_negtive = False
        self.x_positive = False
        self.y_negtive = False
        self.y_positive = False
        self._delete = False
        self._func = 'zoom'
        self._axis_long = 50
        self._axis_short = 50
        self.__updateRect()

        pen = QPen(self.PEN_COLOR)
        pen.setWidthF(2.5)
        self.setPen(pen)
        self.setBrush(self.DEFAULT_COLOR)

    @property
    def axis_long(self) -> float:
        return max(10, self._axis_long)

    @axis_long.setter
    def axis_long(self, value: float) -> None: 
        self._axis_long = value

    @property
    def axis_short(self) -> float:
        return max(10, self._axis_short)

    @axis_short.setter
    def axis_short(self, value: float) -> None: 
        self._axis_short = value

    @property
    def point_lefttop(self) -> QPointF:
        return QPointF(-(self.axis_long/2), -(self.axis_short)/2)

    @property
    def point_rightbottom(self) -> QPointF:
        return QPointF(-(self.axis_long/2), -(self.axis_short)/2)

    def __updateRect(self) -> None:
        self.setRect(self.point_lefttop.x(), self.point_lefttop.y(), self.axis_long, self.axis_short)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.init_pos = self.mapFromScene(event.scenePos())
        self.__distance_init = self.__DistanceToCenter(self.init_pos)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        item_pos = self.mapFromScene(pos)
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            x_diff = pos.x() - self.x_init
            y_diff = pos.y() - self.y_init
            if self.x_positive or self.x_negtive or self.y_positive or self.y_negtive:
                cur_distance = self.__DistanceToCenter(item_pos)
                if self.x_positive or self.x_negtive:
                    self.axis_long = self.axis_long + (cur_distance-self.__distance_init)*2
                elif self.y_positive or self.y_negtive:
                    self.axis_short = self.axis_short + (cur_distance-self.__distance_init)*2
                self.__distance_init = cur_distance
                self.__updateRect()
                self.update()
            else:
                self.setX(self.x() + x_diff)
                self.setY(self.y() + y_diff)
                self.x_init = pos.x()
                self.y_init = pos.y()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.signal.ellipse_location.emit((self.mapToScene(self.point_lefttop), self.mapToScene(self.point_rightbottom)))
        self.signal.ellipse_shape.emit(self.mapToScene(self.shape()))
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        angle = event.delta()
        value = int(angle//120)
        if self.func == 'zoom':
            cur_scale = 1 + 0.1 * value
            self.axis_long = cur_scale * self.axis_long
            self.axis_short = cur_scale * self.axis_short

            bef_pos = self.pos()
            cursor_pos = event.scenePos()
            cursor_pos_x = cursor_pos.x()
            cursor_pos_y = cursor_pos.y()
            ratio_x = (cursor_pos_x - bef_pos.x())/(self.rect().width())
            ratio_y = (cursor_pos_y - bef_pos.y())/(self.rect().height())
            aft_cursor_pos_x = bef_pos.x() + ratio_x * (self.rect().width()*cur_scale)
            aft_cursor_pos_y = bef_pos.y() + ratio_y * (self.rect().height()*cur_scale)
            self.__updateRect()
            self.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
            self.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))
        elif self.func == 'rotate':
            self.setRotation(self.rotation()+value*5)
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:

        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if event.pos().x() > self.axis_long * 0.45:
            self.x_positive = True
        elif event.pos().x() < - self.axis_long * 0.45:
            self.x_negtive = True
        else:
            self.x_negtive = False
            self.x_positive = False

        if event.pos().y() > self.axis_short * 0.45:
            self.y_positive = True
        elif event.pos().y() < - self.axis_short * 0.45:
            self.y_negtive = True
        else:
            self.y_negtive = False
            self.y_positive = False

        self.update()
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:

        self.update()
        return super().hoverLeaveEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            self.Delete = True

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            if self.Delete:
                
                self.signal.item_delete.emit(self)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        self.menu.exec_(QCursor.pos())

    def paint(self, painter: QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        option.state = QtWidgets.QStyle.State_None
        pen = painter.pen()
        pen.setWidthF(0)

        super().paint(painter, option, widget)
        
        if self.hoverEnter:
            pen.setColor(QColor(255,255,255, 200))
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



    def __DistanceToCenter(self, point: QPointF) -> float:
        return sqrt(point.x() ** 2 + point.y() ** 2)

    @property
    def func(self) -> str:
        return self._func

    @func.setter
    def func(self, func: str) -> None:
        self._func = func

    @property
    def Delete(self) -> bool:
        return self._delete

    @Delete.setter
    def Delete(self, delete: bool) -> None:
        self._delete = delete




    def setup_menu(self) -> None:
        menu = self.menu
        action_zoom = menu.addAction('Zoom')
        action_zoom.triggered.connect(self.__action_zoom)
        action_rotate = menu.addAction('Rotate')
        action_rotate.triggered.connect(self.__action_rotate)
        action_color = menu.addAction('Color')
        action_color.triggered.connect(self.__action_color)
        action_delete = menu.addAction('Delete')
        action_delete.triggered.connect(self.__action_delete)

    def __action_color(self) -> None:
        cd = QColorDialog(self.brush().color())
        cd.setOption(cd.ShowAlphaChannel)
        cd.setOption(cd.DontUseNativeDialog)
        cd.exec()
        color = cd.selectedColor()
        self.setBrush(color)

    def __action_delete(self) -> None:
        self.signal.item_delete.emit(self)

    def __action_rotate(self) -> None:
        self.func = 'rotate'
    
    def __action_zoom(self) -> None:
        self.func = 'zoom'