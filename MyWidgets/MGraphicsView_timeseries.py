import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal
from PySide6.QtGui import QImage, QPixmap, QResizeEvent, QMouseEvent, QColor

from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGraphicsView, QFrame

from modules.dcmreader.Read_dcm import MAbstractDicomReader
from modules.dcmreader.read_DSC_DCE import Read_Bruker_TimeSeries
from MyWidgets.MWidget import MWidget
from MyWidgets.MGraphicsScene import MGraphicsScene

class MGraphicsView_timeseries(QGraphicsView, MWidget):
    _idx_changed = Signal(int)
    _slice = Signal(int)

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.idx = 0
        self.setMouseTracking(True)
        self._dicom_reader = None
        self.__setup_scene()

    @property
    def DicomReader(self) -> MAbstractDicomReader:
        return self._dicom_reader

    @DicomReader.setter
    def DicomReader(self, dr: MAbstractDicomReader) -> None:
        self._dicom_reader = dr
        self._setupUI()
    
    def set_mainwindow(self, mainwindow) -> None:
        self.mainwindow = mainwindow

        
    def _setupUI(self) -> None:
        self.setStyleSheet('''MGraphicsView_timeseries{background-color: rgb(0, 0, 0); padding: 0px; border: 0px}''')
        # self.setBackgroundBrush(QColor(0,0,0,255))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        self.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __setup_scene(self):
        self.mscene = MGraphicsScene(self)
        self.mscene.signal_ROI.connect(self.__mask)
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
            self.scene().setSceneRect(self.geometry())
            self.set_scene(self.idx)
        return super().resizeEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        return super().mouseMoveEvent(event)
 
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
if __name__ == '__main__':
    mGraphicView = MGraphicsView_timeseries()