import numpy as np
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from UI.ui_Widget_Browse import Ui_Widget_Browse

from modules.dcmreader.read_Dicom import read_Dicom_folder
from modules.threads.Iconlist import ThreadIconlist



class Widget_Browse(QWidget, Ui_Widget_Browse):
    def __init__(self, dicom_dir, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.root = dicom_dir
        self.dicom_reader = read_Dicom_folder(self.root)
        self.setupUi(self)
        self._setupUI()
        self._setup()

    def set_root(self, root: str):
        self.root = root
        self.dicom_reader = read_Dicom_folder(self.root)
        self._setup()
        
    def _setupUI(self):
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 7)

        self.listWidget.resizeEvent = self._listWidget_resizeEvent
        self.graphicsView.DicomReader = self.dicom_reader
        self.graphicsView.set_mainwindow(self.mainwindow)
        self.graphicsView._idx_changed.connect(self._slot_idx)

    def _setup(self):
        self.WL = 10000
        self.WW = 10000
        self.idw = self._set_IDW()
        self.verticalScrollBar_Image.setMaximum(self.dicom_reader.len())
        self.verticalScrollBar_Image.setMinimum(self.graphicsView.DicomReader.min_idx+1)
        self.verticalScrollBar_Image.setValue(self.graphicsView.DicomReader.min_idx+1)
        self.threadiconlist = ThreadIconlist(self)
        self.threadiconlist.loading_signal.connect(self._slot_loading)
        self.threadiconlist.loaded_signal.connect(self._slot_loaded)
        self.threadiconlist.start()

    def _slot_loaded(self):
        self.mainwindow._Status_progressBar.label.setText('Loaded')
    def _slot_loading(self, idx):
        progressBar = self.mainwindow._Status_progressBar
        if idx == 0:
            progressBar.setHidden(False)
            progressBar.progressBar.setMinimum(1)
            progressBar.progressBar.setMaximum(self.dicom_reader.len())
            progressBar.label.setText('Loading')
        progressBar.progressBar.setValue(idx+1)

    def _slot_idx(self, idx):
        self.verticalScrollBar_Image.setValue(idx+1)
        
    @Slot(int)
    def on_verticalScrollBar_Image_valueChanged(self, value):
        self.graphicsView.set_scene(value-1)

    @Slot()
    def on_listWidget_itemClicked(self):
        item = self.listWidget.selectedItems()[0]
        idx = int(item.text())
        self.verticalScrollBar_Image.setValue(idx)
        self.graphicsView.set_scene(idx-1)

    def iconlist(self, idx):
        ds, img = self.dicom_reader.get_ds_and_array(idx)
        try:
            img = np.clip(img, a_min=ds.SmallestImagePixelValue, a_max=ds.LargestImagePixelValue)
        except:
            img = np.clip(img, **self.idw)
        img = ((img-img.min())/(img.max()-img.min()))*255
        img = img.astype(np.int8)
        image = QImage(img, img.shape[1], img.shape[0], img.shape[1],
                                QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(image)
        pix = pix.scaled(img.shape[0],img.shape[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        item = QListWidgetItem()
        item.setIcon(QIcon(pix))
        item.setText(str(idx+1))
        
        item.setToolTip('{}\n{}x{}'.format(ds.ProtocolName, ds.Rows, ds.Columns))
        self.listWidget.addItem(item)

    def _set_WW(self, WW):
        if WW > 30000:
            WW = 30000
        if WW < 2:
            WW = 2
        self.WW = WW
        self.idw = self._set_IDW()
    
    def _set_WL(self, WL):
        if WL > 30000:
            WL = 30000
        if WL < 0:
            WL = 0
        self.WL = WL
        self.idw = self._set_IDW()
    
    def _set_IDW(self):
        '''Image Display Window (IDW)'''
        self.value_min = self.WL - self.WW//2
        self.value_max = self.WL + self.WW//2
        if self.value_min < 0:
            self.value_min = 0
        if self.value_max > 50000:
            self.value_max = 50000
        idw = {'a_min':self.value_min, 'a_max':self.value_max}
        return idw

    def _listWidget_resizeEvent(self, event: QResizeEvent):
        width = self.listWidget.geometry().width()//4
        self.listWidget.setIconSize(QSize(width, width))
        self.mainwindow.statusBar().showMessage('{}:: {}'.format(self.listWidget.objectName(), self.listWidget.geometry()))
