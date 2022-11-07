# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.optimize import curve_fit
from PySide6.QtCore import Signal, QThread

from modules.dcmreader.read_FAIR import read_FAIR_folder
from modules.utils.shape import get_index_of_mask

class Thread_FAIR_CBF(QThread):
    signal_start = Signal(bool)
    signal_processing = Signal(int)
    signal_end = Signal(tuple)
    def __init__(self):
        super().__init__()

        self._DicomReader = None
        self._t1blood = None
        self._maskIndex = None

    def run(self):
        T1blood = self.T1blood
        img_sel = self.DicomReader.imgAll_Sel
        img_non = self.DicomReader.imgAll_Non
        xdata = self.DicomReader.TimePoints
        x = self.DicomReader.RowNum
        y = self.DicomReader.ColNum
        if T1blood != 0:
            self.signal_start.emit(True)
            cbf_map = np.zeros((x, y), dtype=np.float32)
            for idx in range(len(self.maskIndex)):
                self.signal_processing.emit(idx+1)
                row_idx, col_idx = self.maskIndex[idx]
                ydata_sel = img_sel[:, row_idx, col_idx]
                ydata_non = img_non[:, row_idx, col_idx]
                popt_sel, pcov_sel = curve_fit(self.Msel_abs, xdata, ydata_sel, p0=(1500,10000))
                T1app, M0 = popt_sel
                def Mnon(TI, f):
                    T1b = T1blood
                    Ms = self.Msel(TI, T1app, M0)
                    M_diff = 2*M0*f/0.9 * ((np.exp(-TI/T1app)- np.exp(-TI/T1b))/(1/T1b-1/T1app))
                    return np.abs(Ms - M_diff)
                popt_non, pcov_non = curve_fit(Mnon, xdata, ydata_non, p0=(1/60000), bounds=(0, 2000/60000/100))
                cbf_map[row_idx, col_idx] = popt_non*60000*100

            self.signal_end.emit((cbf_map,))


    @property
    def DicomReader(self) -> read_FAIR_folder:
        return self._DicomReader

    @DicomReader.setter
    def DicomReader(self, reader) -> None:
        self._DicomReader = reader

    @property
    def T1blood(self) -> float:
        return self._t1blood

    @T1blood.setter
    def T1blood(self, t1b: float) -> None:
        self._t1blood = t1b

    @property
    def maskIndex(self) -> np.array:
        if self._maskIndex is None:
            row = self.DicomReader.RowNum
            col = self.DicomReader.ColNum
            self._maskIndex = get_index_of_mask(np.ones((row, col)))
        return self._maskIndex

    @maskIndex.setter
    def maskIndex(self, maskindex: np.array) -> None:
        self._maskIndex = maskindex

    @staticmethod
    def Msel_abs(TI: float, T1app: float, M0: float) -> float:
        '''Msel model'''
        return np.abs(M0*(1-2*np.exp(-TI/T1app)))

    @staticmethod
    def Msel(TI: float, T1app: float, M0: float) -> float:
        '''Msel model'''
        return M0*(1-2*np.exp(-TI/T1app))