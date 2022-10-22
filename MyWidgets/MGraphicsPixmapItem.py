from math import ceil

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

from MyWidgets.MGraphicsItem import MGraphicsItem


class MGraphicsPixmapItem(QGraphicsPixmapItem, MGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_MGraphicsItem__()
        self.ItemType = 'image'
        
        self.__WW = 2000
        self.__WL = 1000
        self.__func = 'window'


    def update_pixmap(self, img: np.array=None):
        if img is None:
            img = self.img.copy()
        else:
            self.img = img.copy()
        scene = self.scene()
        scene_width = scene.sceneRect().width()
        scene_height = scene.sceneRect().height()
        img = np.clip(img, **self.IDW)
        img = ((img - img.min()) / max(1, img.max() - img.min()))*255
        img = img.astype(np.uint8)
        image = QImage(
            img, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Grayscale8)
        pix_img = QPixmap.fromImage(image)
        scale = min(scene_height/pix_img.height(), scene_width/pix_img.width())
        self.setPixmap(pix_img)
        self.setScale(scale)
        self.setY((scene_height-pix_img.height()*scale)/2)
        self.setX((scene_width-pix_img.width()*scale)/2)

    @property
    def img(self) -> np.array:
        return self.__img

    @img.setter
    def img(self, img: np.array) -> None:
        self.__img = img

    @property
    def WW(self) -> float:
        return self.__WW

    @WW.setter
    def WW(self, ww: float):
        if ww > 30000:
            ww = 30000
        if ww < 2:
            ww = 2
        self.__WW = ww

    @property
    def WL(self) -> float:
        return self.__WL

    @WL.setter
    def WL(self, wl: float) -> None:
        if wl > 30000:
            wl = 30000
        if wl < -1000:
            wl = -1000
        self.__WL = wl

    @property
    def IDW(self) -> dict:
        '''Image Display Window (IDW)'''
        value_min = self.WL - self.WW//2
        value_max = self.WL + self.WW//2
        if value_min < 0:
            value_min = 0
        if value_max > 50000:
            value_max = 50000
        return {'a_min':value_min, 'a_max':value_max}

    def maptoPixmap(self, pos: QPointF=None) -> QPoint:
        if pos is None:
            point = QPoint(0, 0)
        pix_pos = self.mapFromScene(pos)
        x = pix_pos.x()
        y = pix_pos.y()
        x_check = x > 0 and x < self.pixmap().width()
        y_check = y > 0 and y < self.pixmap().height()
        if x_check and y_check: 
            point = QPoint(ceil(x), ceil(y))
        else:
            point = QPoint(0, 0)
        return point

    def maptoSelf(self, pos: QPointF=None) -> QPointF:
        if pos is None:
            return QPointF(0, 0)
        pix_pos = self.mapFromScene(pos)
        x = pix_pos.x()
        y = pix_pos.y()
        return QPointF(ceil(x), ceil(y))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.func == 'window':
                self.x_init = event.scenePos().x()
                self.y_init = event.scenePos().y()
            elif self.func == 'series':
                self.y_init = event.scenePos().y()
            elif self.func == 'move' or self.func == 'zoom':
                self.x_init = event.scenePos().x()
                self.y_init = event.scenePos().y()
                self.item_img_pos = self.scenePos()
            elif self.func == 'point':
                pass

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            if self.func == 'window':
                self.x_end = event.scenePos().x()
                self.y_end = event.scenePos().y()
                x_diff = self.x_end - self.x_init
                y_diff = (self.y_end - self.y_init) * (-1)
                self.WW = (self.WW + 10000 * (x_diff / self.scene().sceneRect().width()))
                self.WL = (self.WL + 10000 * (y_diff / self.scene().sceneRect().height()))
                self.update_pixmap()
                # diff = 'x_diff/y_diff: {}/{}'.format(x_diff, y_diff)
                # window = 'WW/WL: {}/{}'.format(int(self.WW), int(self.WL))
                # self.mainwindow.statusBar().showMessage('{} {}'.format(diff, window))
                self.x_init = self.x_end
                self.y_init = self.y_end
            # elif self.func == 'series':
            #     self.y_end = event.pos().y()
            #     y_diff = (self.y_end - self.y_init)
            #     totalnum = self.dicom_reader.len()
            #     height_per_img = self.scene().sceneRect().height() / totalnum
            #     if abs(y_diff) > height_per_img:
            #         self.y_init = self.y_end
            #         idx = self._check_idx(int(y_diff/abs(y_diff)) + self.idx)
            #         self.set_scene(idx)
    
            elif self.func == 'move' or self.func == 'zoom':
                x_diff = event.scenePos().x() - self.x_init
                y_diff = event.scenePos().y() - self.y_init
                self.item_img_pos.setX(self.item_img_pos.x() + x_diff)
                self.item_img_pos.setY(self.item_img_pos.y() + y_diff)
                self.setPos(self.item_img_pos)
                self.x_init = event.scenePos().x()
                self.y_init = event.scenePos().y()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return None

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        angle = event.delta()
        value = int(angle//120)
        bef_scale = self.scale()
        cur_scale = max(0.2, bef_scale+0.05*value)
        bef_pos = self.pos()
        cursor_pos = event.scenePos()
        cursor_pos_x = cursor_pos.x()
        cursor_pos_y = cursor_pos.y()
        ratio_x = (cursor_pos_x - bef_pos.x())/(self.pixmap().width()*bef_scale)
        ratio_y = (cursor_pos_y - bef_pos.y())/(self.pixmap().height()*bef_scale)
        aft_cursor_pos_x = bef_pos.x() + ratio_x * (self.pixmap().width()*cur_scale)
        aft_cursor_pos_y = bef_pos.y() + ratio_y * (self.pixmap().height()*cur_scale)
        self.setScale(cur_scale)
        self.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
        self.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))


    @property
    def func(self) -> str:
        return self.__func

    @func.setter
    def func(self, func: str) -> None:
        self.__func = func