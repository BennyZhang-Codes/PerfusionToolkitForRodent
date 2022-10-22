import numpy as np
from PIL import Image

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal
from PySide6.QtGui import QImage, QPixmap, QIcon, QCursor, QColor, QTransform, QPen
from PySide6.QtGui import QMouseEvent, QWheelEvent, QResizeEvent, QKeyEvent 

from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsSceneWheelEvent, QGraphicsSceneContextMenuEvent
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMenu, QScrollBar, QGraphicsTextItem
from PySide6.QtWidgets import  QGraphicsView, QLabel, QSizePolicy, QFrame
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsEllipseItem

from MyWidgets.MGraphicsItem import MGraphicsPixmapItem
from MyWidgets.MGraphicsItemGroup import MGraphicsItemGroup
from MyWidgets.MGraphicsItem import MGraphicsEllipseItem, MGraphicsPolygonItem, MGraphicsItem

from modules.utils.shape import shape_to_mask, get_index_of_mask

class MGraphicsScene(QGraphicsScene):
    _mask = Signal(list)
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.setup()
        self.ROI = []

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.item = self.itemAt(event.scenePos(), QTransform())
        print('pressed', self.item)
        
        if hasattr(self, 'item'):
            if self.item:
                self.item.mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # print('scene mouse move')
        if hasattr(self, 'item'):
            if self.item:
                self.item.mouseMoveEvent(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if hasattr(self, 'item'):
            if self.item:
                self.item.mouseReleaseEvent(event)

    # def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
    #     self.item = self.itemAt(event.scenePos(), QTransform())
    #     if self.item:
    #         self.item.wheelEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        print(event)
        print(self.selectedItems())
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                self.removeItem(item)
            print('Key_delete scene')

        return super().keyPressEvent(event)

    def setup(self) -> None:
        self.item_img = MGraphicsPixmapItem()
        self.item_info_RightTop = QGraphicsTextItem()
        self.item_info_LeftBottom = QGraphicsTextItem()
        self.item_info_LeftTop = QGraphicsTextItem()
        self.item_info_RightBottom = QGraphicsTextItem()
        self.item_info_group = MGraphicsItemGroup()
        self.item_info_LeftBottom.setZValue(-1)
        self.item_info_LeftTop.setZValue(-1)
        self.item_info_RightTop.setZValue(-1)
        self.item_info_RightBottom.setZValue(-1)
        self.item_info_RightTop.setGroup(self.item_info_group)
        self.item_info_LeftBottom.setGroup(self.item_info_group)
        self.item_info_LeftTop.setGroup(self.item_info_group)
        self.item_info_RightBottom.setGroup(self.item_info_group)
        self.item_roi_group = MGraphicsItemGroup()

        self.item_img.setZValue(-2)
        self.item_info_group.setZValue(-1)
        self.item_roi_group.setZValue(1)
        self.addItem(self.item_img)
        self.addItem(self.item_info_group)
        self.addItem(self.item_roi_group)

    def add_Mellipse(self) -> MGraphicsEllipseItem:
        ellipse = MGraphicsEllipseItem()
        ellipse.setPen(QPen(QColor(0,0,255,255), 1, Qt.SolidLine))
        ellipse.setBrush(QColor(255,0,0,255))
        ellipse.setPos(self.width()/2, self.height()/2)
        ellipse.setOpacity(0.5)
        ellipse.setZValue(1)
        ellipse.signal.ellipse_location.connect(self.__slot_Mellipse_location)
        self.__add_roi(ellipse)
        return ellipse

    def add_Mpolygon(self) -> MGraphicsPolygonItem: 
        polygon = MGraphicsPolygonItem()
        polygon.setPolygon([QPointF(30, 30), QPointF(40, 30),QPointF(30, 40)])
        polygon.setPen(QPen(QColor(0,0,255,255), 1, Qt.SolidLine))
        polygon.setBrush(QColor(255,0,0,255))
        polygon.setPos(self.width()/2, self.height()/2)
        polygon.setZValue(1)
        self.__add_roi(polygon)
        return polygon

    def __add_roi(self, item: MGraphicsItem):
        self.addItem(item)
        self.ROI.append(item)

    def __slot_Mellipse_location(self, location: tuple):
        lt, rb = location

        lt = self.item_img._maptoPixmap(lt)
        rb = self.item_img._maptoPixmap(rb)
        lt = (lt.x()-1, lt.y()-1)
        rb = (rb.x()-1, rb.y()-1)
        pix = self.item_img.pixmap()
        shape = (pix.height(), pix.width())
        # print(lt, rb)
        # print(shape)
        mask = shape_to_mask(img_shape=shape, points=(lt, rb), shape_type='ellipse')
        img = Image.fromarray(mask)
        img.save('mask.png')
        img.toqimage()

        index = get_index_of_mask(mask)
        # print(index)
        self._mask.emit(index)
        # print(img.toqpixmap().width())
        # print(img.toqpixmap().height())
        

        # print(index)
        # print('//////')


    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        if hasattr(self, 'item'):
            if self.item:
                self.item.contextMenuEvent(event)
        print(event)
        return super().contextMenuEvent(event)

