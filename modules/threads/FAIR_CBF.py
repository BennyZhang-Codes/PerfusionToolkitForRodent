# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.optimize import curve_fit
from PySide6.QtCore import Signal, QThread

class Thread_FAIR_CBF_Calc(QThread):
    processing_signal = Signal(int)
    processed_signal = Signal(tuple)
    def __init__(self, parent, dss: tuple):
        '''dss tuple(dss_selective, dss_non-selective)'''
        super().__init__()
        self.parent = parent
        self.dss = dss
        
    def setup(self):
        x, y, _ = self.img_sel.shape
        progressBar = self.parent.mainwindow._Status_progressBar
        progressBar.setHidden(False)
        progressBar.progressBar.setHidden(False)
        progressBar.progressBar.setMinimum(1)
        progressBar.progressBar.setMaximum(x*y)
        progressBar.label.setText('Processing')
        
    @staticmethod
    def Msel_abs(TI: float, T1app: float, M0: float) -> float:
        '''Msel model'''
        return np.abs(M0*(1-2*np.exp(-TI/T1app)))

    @staticmethod
    def Msel(TI: float, T1app: float, M0: float) -> float:
        '''Msel model'''
        return M0*(1-2*np.exp(-TI/T1app))

    def prepare(self, dss):
        '''extract image array and TIs'''
        dss_sel, dss_non = dss
        img_sel = []
        img_non = []
        xdata = []
        for ds_sel, ds_non in zip(dss_sel, dss_non):
            xdata.append(ds_sel.InversionTime)
            img_sel.append(np.expand_dims(ds_sel.pixel_array, axis=2))
            img_non.append(np.expand_dims(ds_non.pixel_array, axis=2))
        self.img_sel = np.concatenate(img_sel, axis=2)
        self.img_non = np.concatenate(img_non, axis=2)
        self.xdata = np.array(xdata)

    def run(self):
        self.prepare(self.dss)
        self.setup()
        x, y, _ = self.img_sel.shape
        cbf_map = np.zeros((x, y), dtype=np.float32)
        T1app_map = np.zeros((x, y), dtype=np.float32)
        M0_map = np.zeros((x, y), dtype=np.float32)
        for i in range(x):
            for j in range(y):
                self.processing_signal.emit(i*y+j+1)
                ydata_sel = self.img_sel[i, j]
                ydata_non = self.img_non[i, j]
                popt_sel, pcov_sel = curve_fit(self.Msel_abs, self.xdata, ydata_sel, p0=(1500,10000))
                T1app, M0 = popt_sel
                M0_map[i, j] = M0
                if M0 < 3000:
                    cbf_map[i, j] = 0
                    T1app_map[i, j] = 0
                    continue

                def Mnon(TI, f):
                    T1b = 2800
                    Ms = self.Msel(TI, T1app, M0)
                    M_diff = 2*M0*f/0.9 * ((np.exp(-TI/T1app)- np.exp(-TI/T1b))/(1/T1b-1/T1app))
                    return np.abs(Ms - M_diff)
                popt_non, pcov_non = curve_fit(Mnon, self.xdata, ydata_non, p0=(1/60000), bounds=(0, 2000/60000/100))
                cbf_map[i, j] = popt_non*60000*100
                T1app_map[i, j] = T1app
        self.processed_signal.emit((self.img_sel, self.img_non, self.xdata, T1app_map, M0_map, cbf_map))