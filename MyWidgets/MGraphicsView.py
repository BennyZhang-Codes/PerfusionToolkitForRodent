from math import ceil

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal
from PySide6.QtGui import QImage, QPixmap, QIcon, QCursor, QColor, QPen
from PySide6.QtGui import QMouseEvent, QWheelEvent, QResizeEvent

from PySide6.QtWidgets import QWidget, QGraphicsScene, QMenu, QScrollBar, QGraphicsTextItem
from PySide6.QtWidgets import  QGraphicsView, QLabel, QSizePolicy, QFrame
from PySide6.QtWidgets import QGraphicsTextItem
from pydicom import FileDataset

from modules.dcmreader.Read_dcm import MAbstractDicomReader
from modules.dcmreader.read_Dicom import read_Dicom_folder
from MyWidgets.MWidget import MWidget
from MyWidgets.MGraphicsScene import MGraphicsScene

class MGraphicsView(QGraphicsView, MWidget):
    _idx_changed = Signal(int)
    _location = Signal(tuple)

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.idx = 0
        self.setMouseTracking(True)
        self.__setup_scene()

    def set_dicom_reader(self, dicom_reader: MAbstractDicomReader) -> None:
        self.dicom_reader = dicom_reader
        self._setupUI()

    def set_mainwindow(self, mainwindow) -> None:
        self.mainwindow = mainwindow
        
    def _setupUI(self) -> None:
        self.setStyleSheet('''MGraphicsView{background-color: rgb(0, 0, 0);}''')
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        self.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.icon_move = QPixmap(u"qrc/move.png")
        self.icon_move = self.icon_move.scaled(29, 29, mode=Qt.SmoothTransformation)
        self.icon_zoom_in = QPixmap(u"qrc/zoom_in.png")
        self.icon_zoom_in = self.icon_zoom_in.scaled(29, 29, mode=Qt.SmoothTransformation)
        self.icon_zoom_out = QPixmap(u"qrc/zoom_out.png")
        self.icon_zoom_out = self.icon_zoom_out.scaled(29, 29, mode=Qt.SmoothTransformation)
        
    def __setup_scene(self):
        self.mscene = MGraphicsScene(self)
        self.mscene._mask.connect(self.__mask)
        self.mscene._ds_idxchange.connect(self.__ds_idx_change)
        self.setScene(self.mscene)

    def __mask(self, index):
        pass
        # print('get mask')

    def __ds_idx_change(self, idx: int) -> None:
        idx = self.idx + idx
        idx = self._check_idx(idx)
        self.set_scene(idx)
        self.idx = idx


    def set_scene(self, idx: int) -> None:
        ds = self.dicom_reader.get_ds(idx)
        self.mscene.set_scene(ds)


    def _check_idx(self, idx: int) -> int:
        if idx < self.dicom_reader.min_idx():
            idx = self.dicom_reader.min_idx()
        if idx > self.dicom_reader.max_idx():
            idx = self.dicom_reader.max_idx()
        return idx

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.scene().setSceneRect(self.geometry())
        self.set_scene(self.idx)
        # if hasattr(self, 'mainwindow'):
        #     self.mainwindow.statusBar().showMessage('MGraphicsView::Resize GraphicsView: {}/{}, Scene: {}/{} '.format(
        #         self.height(), self.width(), self.scene().height(), self.scene().width()))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        return super().mouseMoveEvent(event)
 
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)

if __name__ == '__main__':
    mGraphicView = MGraphicsView()