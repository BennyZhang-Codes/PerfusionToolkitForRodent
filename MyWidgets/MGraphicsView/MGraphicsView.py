from math import ceil

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from pydicom import FileDataset

from modules.dcmreader.Read_dcm import MAbstractDicomReader
from modules.dcmreader.read_Dicom import read_Dicom_folder
from MyWidgets.MGraphicsView.MGraphicsScene import MGraphicsScene

class MGraphicsView(QGraphicsView):
    _idx_changed = Signal(int)
    _location = Signal(tuple)

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.idx = 0
        self.setMouseTracking(True)
        self._mainwindow = None
        self._dicom_reader = None
        self.__setup_scene()
        self._setupUI()

    @property
    def DicomReader(self) -> MAbstractDicomReader:
        return self._dicom_reader

    @DicomReader.setter
    def DicomReader(self, dr: MAbstractDicomReader) -> None:
        self._dicom_reader = dr

    def set_mainwindow(self, mainwindow) -> None:
        self.MainWindow = mainwindow
        
    def _setupUI(self) -> None:
        self.setStyleSheet('''MGraphicsView{background-color: rgb(0, 0, 0); padding: 0px; border: 0px}''')
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        self.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.icon_move = QPixmap(u"qrc/move.png")
        # self.icon_move = self.icon_move.scaled(29, 29, mode=Qt.SmoothTransformation)
        # self.icon_zoom_in = QPixmap(u"qrc/zoom_in.png")
        # self.icon_zoom_in = self.icon_zoom_in.scaled(29, 29, mode=Qt.SmoothTransformation)
        # self.icon_zoom_out = QPixmap(u"qrc/zoom_out.png")
        # self.icon_zoom_out = self.icon_zoom_out.scaled(29, 29, mode=Qt.SmoothTransformation)
        
    def __setup_scene(self):
        self.mscene = MGraphicsScene(self)
        self.mscene.signal_ROI.connect(self.__mask)
        self.mscene._ds_idxchange.connect(self.__ds_idx_change)
        self.setScene(self.mscene)

    def __mask(self, index):
        pass

    def __ds_idx_change(self, idx: int) -> None:
        idx = self.idx + idx
        idx = self._check_idx(idx)
        self.set_scene(idx)
        self.idx = idx


    def set_scene(self, idx: int) -> None:
        ds = self.DicomReader.get_ds(idx)
        self.mscene.set_scene(ds)


    def _check_idx(self, idx: int) -> int:
        if idx < self.DicomReader.min_idx():
            idx = self.DicomReader.min_idx()
        if idx > self.DicomReader.max_idx():
            idx = self.DicomReader.max_idx()
        return idx

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self.DicomReader is not None:
            self.mscene.setSceneRect(self.geometry())
            self.set_scene(self.idx)
            self.mscene.resizeevent()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        return super().mouseMoveEvent(event)
 
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)

    @property
    def MainWindow(self) -> QMainWindow:
        return self._mainwindow

    @MainWindow.setter
    def MainWindow(self, mainwindow: QMainWindow) -> None:
        self._mainwindow = mainwindow

if __name__ == '__main__':
    mGraphicView = MGraphicsView()