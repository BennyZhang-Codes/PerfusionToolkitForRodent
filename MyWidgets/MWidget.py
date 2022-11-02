
import numpy as np
import cv2
from PIL import Image

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *

from modules.utils.colormap import MColorMap

class MROI(QWidget):
    Func_Window = 'window'
    Func_Move = 'move'
    Func_ColorMap = 'colormap'
    Func_Save = 'save'
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        # self.setEnabled(False)

        self.x_diff = 0
        self.y_diff = 0

        self._pix_image = None
        self.ColorMap = MColorMap()
        self.ColorMap.idx = 0

    def setPixmap(self, pix: QPixmap) -> None:
        self.PixImage = pix

    @property
    def PixImage(self) -> QPixmap:
        return self._pix_image

    @PixImage.setter
    def PixImage(self, pix: QPixmap) -> None:
        self._pix_image = pix
        self.update()
        self.setEnabled(True)

    def paintEvent(self, event: QPaintEvent) -> None:
        img = self.PixImage
        if img is not None:
            
            img = img.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
            x = (self.width() - img.width()) // 2 + self.x_diff
            y = (self.height() - img.height()) // 2 + self.y_diff
            painter = QPainter()
            painter.begin(self)
            painter.drawPixmap(x, y, img)
            painter.end()
        return super().paintEvent(event)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.x_init = event.position().x()
            self.y_init = event.position().y()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = event.position()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            x_diff = pos.x() - self.x_init
            y_diff = pos.y() - self.y_init
            self.x_diff = self.x_diff + x_diff
            self.y_diff = self.y_diff + y_diff
            self.x_init = pos.x()
            self.y_init = pos.y()
            self.update()
        return super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.x_diff = 0
        self.y_diff = 0
        self.update()
        return super().mouseDoubleClickEvent(event)
    

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update()
        return super().resizeEvent(event)

class MColorBar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setEnabled(False)
        self.ColorMap = MColorMap()
        self._pix_image = None

    def setPixmap(self, pix: QPixmap) -> None:
        self.PixImage = pix
        self.setEnabled(True)
        self.update()

    @property
    def PixImage(self) -> QPixmap:
        return self._pix_image

    @PixImage.setter
    def PixImage(self, pix: QPixmap) -> None:
        self._pix_image = pix


    def paintEvent(self, event: QPaintEvent) -> None:
        img = self.PixImage
        if img is not None and self.isEnabled():
            cb = img.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
            x_cb = self.width() - cb.width()
            y_cb = (self.height() - cb.height()) // 2
            painter = QPainter()
            painter.begin(self)
            painter.drawPixmap(x_cb, y_cb, cb)
            l1, l2, l3, l4 = self.linsofcolorbar(x_cb, y_cb, cb)
            painter.drawLine(l1)
            painter.drawLine(l2)
            painter.drawLine(l3)
            painter.drawLine(l4)
            painter.end()
        return super().paintEvent(event)

    def linsofcolorbar(self, x: float, y: float, cb: QPixmap) -> tuple:
        l1 = QLine()
        l1.setLine(x, y, x, y+ cb.height()-1)
        l2 = QLine()
        l2.setLine(x, y, x+cb.width()-1, y)
        l3 = QLine()
        l3.setLine(x+cb.width()-1, y, x+cb.width()-1, y+ cb.height()-1)
        l4 = QLine()
        l4.setLine(x, y+ cb.height()-1, x+cb.width()-1, y+ cb.height()-1)
        return l1, l2, l3, l4

    def resizeEvent(self, event: QResizeEvent) -> None:
        return super().resizeEvent(event)

class MResult(QWidget):
    Vmax = Signal(float)
    Vmin = Signal(float)

    Func_Window = 'window'
    Func_Move = 'move'
    Func_ColorMap = 'colormap'
    Func_Save = 'save'
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.__func = self.Func_Window
        self.setEnabled(False)

        self._WW = 2000
        self._WL = 1000
        self._WW_min = 2
        self._WW_max = 60000
        self._WL_max = 30000
        self._WL_min = -30000
        self._x_diff = 0
        self._y_diff = 0
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self._pix_image = None

        self.ColorMap = MColorMap()
        self.ColorMap.idx = 0

    def setImgArray(self, img: np.array) -> None:
        self.img = img
        self.vmin = img.min()
        self.vmax = img.max()
        self.WW = self.vmax - self.vmin
        self.WL = (self.vmax - self.vmin) // 2 + self.vmin
        self.update_PixImage()
        self.setEnabled(True)

    def update_PixImage(self) -> QPixmap:
        img = self.img.copy()
        img = np.clip(img, **self.IDW)
        img = ((img - img.min()) / max(1, img.max() - img.min()))*255
        img = img.astype(np.uint8)

        a = self.ColorMap.applyColorMap(img)
        img = Image.fromarray(a)
        img = img.toqpixmap()
        self.PixImage = img

    @property
    def PixImage(self) -> QPixmap:
        return self._pix_image

    @PixImage.setter
    def PixImage(self, pix: QPixmap) -> None:
        self._pix_image = pix


    def paintEvent(self, event: QPaintEvent) -> None:
        img = self.PixImage
        if img is not None:
            img = img.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.FastTransformation)

            x = (self.width() - img.width()) // 2 + self._x_diff
            y = (self.height() - img.height()) // 2 + self._y_diff

            painter = QPainter()
            painter.begin(self)
            painter.drawPixmap(x, y, img)
            painter.end()
        return super().paintEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.x_init = event.position().x()
            self.y_init = event.position().y()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = event.position()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            if self.func == self.Func_Window:
                self.x_end = event.position().x()
                self.y_end = event.position().y()
                x_diff = self.x_end - self.x_init
                y_diff = (self.y_end - self.y_init) * (-1)
                self.WW = (self.WW + 1000 * (x_diff / self.width()))
                self.WL = (self.WL + 1000 * (y_diff / self.height()))
                self.x_init = self.x_end
                self.y_init = self.y_end
                self.update_PixImage()
            elif self.func == self.Func_Move:
                x_diff = pos.x() - self.x_init
                y_diff = pos.y() - self.y_init
                self._x_diff = self._x_diff + x_diff
                self._y_diff = self._y_diff + y_diff
                self.x_init = pos.x()
                self.y_init = pos.y()
            self.update()
                
        return super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.func == self.Func_Window:
            vmin = self.img.min()
            vmax = self.img.max()
            self.WW = vmax - vmin
            self.WL = (vmax - vmin) // 2 + vmin
            self.update_PixImage()
        if self.func == self.Func_Move:
            self._x_diff = 0
            self._y_diff = 0
        self.update()
        return super().mouseDoubleClickEvent(event)
    
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        return super().contextMenuEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self.func != self.Func_Move:
            self.update()
        return super().resizeEvent(event)

    @property
    def WW(self) -> float:
        return self._WW

    @WW.setter
    def WW(self, ww: float):
        if ww > self._WW_max:
            ww = self._WW_max
        if ww < self._WW_min:
            ww = self._WW_min
        self._WW = ww
        self.emit_ValueRange()

    @property
    def WL(self) -> float:
        return self._WL

    @WL.setter
    def WL(self, wl: float) -> None:
        if wl > self._WL_max:
            wl = self._WL_max
        if wl < self._WL_min:
            wl = self._WL_min
        self._WL = wl
        self.emit_ValueRange()


    def setVmin(self, vmin: float) -> None:
        self.vmin = vmin
        self._WW = self.vmax - self.vmin
        self._WL = (self.vmax - self.vmin) // 2 + self.vmin
        self.update_PixImage()
        self.update()

    def setVmax(self, vmax: float) -> None:
        self.vmax = vmax
        self._WW = self.vmax - self.vmin
        self._WL = (self.vmax - self.vmin) // 2 + self.vmin
        self.update_PixImage()
        self.update()

    def emit_ValueRange(self) -> None:
        vmax = self.WL + self.WW / 2 
        vmin = self.WL - self.WW / 2
        self.Vmax.emit(vmax)
        self.Vmin.emit(vmin)

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

    @property
    def func(self) -> str:
        return self.__func

    @func.setter
    def func(self, func: str) -> None:
        self.__func = func


    def show_context_menu(self) -> None:
        menu = QMenu(self)
        Window = menu.addAction('Window')
        Window.triggered.connect(self._action_Window)
        Move = menu.addAction('Move')
        Move.triggered.connect(self._action_Move)
        ColorMap = menu.addAction('Color map')
        ColorMap.triggered.connect(self._action_ColorMap)
        Save = menu.addAction('Save')
        Save.triggered.connect(self._action_Save)
        menu.exec_(QCursor.pos())

    def _action_Window(self) -> None:
        self.func = self.Func_Window
    
    def _action_ColorMap(self) -> None:
        self.func = self.Func_ColorMap
    
    def _action_Move(self) -> None:
        self.func = self.Func_Move

    def _action_Save(self) -> None:
        self.func = self.Func_Save
