# -*- coding: utf-8 -*-
import numpy as np
from pydicom import dcmread
from PySide6.QtCore import Signal, QThread

class Thread_load_Bruker_TimeSeries(QThread):
    _loadstart = Signal(bool)
    _loading = Signal(int)
    _loaded = Signal(bool)
    def __init__(self, parent):
        super().__init__()
        self.DicomReader = parent

    def run(self):
        self._loadstart.emit(True)
        img = []
        dss = []
        for idx in range(len(self.DicomReader.DicomList)):
            self._loading.emit(idx)
            ds = dcmread(self.DicomReader.dicom_path + '/' + self.DicomReader.DicomList[idx])
            dss.append(ds)
            img.append(ds.pixel_array)

        self.DicomReader._img_all = np.array(img)
        self.DicomReader._dss_all = np.array(dss)

        self._loaded.emit(True)

