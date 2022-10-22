# -*- coding: utf-8 -*-
import numpy as np
from pydicom import dcmread
from PySide6.QtCore import Signal, QThread

class Thread_load_DSC_DCE(QThread):
    _loadstart = Signal(bool)
    _loading = Signal(int)
    _loaded = Signal(tuple)
    def __init__(self, parent):
        super().__init__()
        self.parent = parent


    def run(self):
        self._loadstart.emit(True)
        imgs_all = []
        dss_all = []
        for slice_idx in range(self.parent.get_slice_num()):
            dcms = self.parent.get_dcm_list()[slice_idx::self.parent.get_slice_num()]
            ds_perSlice = []
            imgs_perSlice = []
            for point_idx in range(self.parent.get_time_points_num()):

                self._loading.emit(slice_idx*self.parent.get_time_points_num() + point_idx + 1)

                ds = dcmread(self.parent.dicom_path + '/' + dcms[point_idx])
                ds_perSlice.append(ds)
                imgs_perSlice.append(ds.pixel_array)
            imgs_all.append(np.array(imgs_perSlice))
            dss_all.append(np.array(ds_perSlice))

        imgs_all = np.array(imgs_all)
        dss_all = np.array(dss_all)

        self._loaded.emit((imgs_all, dss_all))
