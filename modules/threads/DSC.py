# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.optimize import curve_fit
from PySide6.QtCore import Signal, QThread

from modules.dcmreader.read_DSC_DCE import Read_Bruker_TimeSeries
from MyWidgets.Mmodel.TabelModel import TimePointsTableModel

from modules.utils.shape import shape_to_mask, get_index_of_mask


class Thread_DSC(QThread):
    signal_start = Signal(bool)
    signal_processing = Signal(int)
    signal_end = Signal(tuple)
    def __init__(self):
        super().__init__()

        self._DicomReader = None
        self._TR = None
        self._TE = None
        self._Model = None
        self._maskIndex = None


    def set_DicomReader(self, dicomreader: Read_Bruker_TimeSeries) -> None:
        self.DicomReader = dicomreader

    def set_model(self, model: TimePointsTableModel) -> None:
        self.Model = model

    def set_maskIndex(self, roi: np.array) -> None:
        self.maskIndex = roi

    def set_AIF(self, aif: np.array) -> None:
        self.AIF = aif

    def set_TR(self, tr: float) -> None:
        self.TR = tr

    def set_TE(self, te: float) -> None:
        self.TE = te
        
    def setup(self):
        pass


    def run(self):
        self.signal_start.emit(True)

        row = self.DicomReader.RowNum
        col = self.DicomReader.ColNum
        img = self.DicomReader.img_GroupBySlice
        nt = self.DicomReader.TimePointsNum
        nt = 200   ###

        S0 = self.Model.S0

        CBF = np.zeros((row, col))
        CBV = np.zeros((row, col))
        MTT = np.zeros((row, col))

        if self.maskIndex is None:
            self.maskIndex = get_index_of_mask(np.ones((row, col)))


        # print(self.TR, np.arange(0, self.TR * nt, self.TR)[1])
        # self.AIF = self.preclinicalAIF(5, np.arange(0, self.TR * nt, self.TR))
        self.AIF = self.AIF[:200]   ###
        S0 = S0[:200]      ###

        x_data = np.arange(0, self.TR * nt, self.TR)

        dR2s_AIF = self.Sig2Conc(signal=self.AIF, S0=np.sum(S0 * self.AIF) / max(1, np.sum(S0)), TE=self.TE)
        dR2s_AIF = self.AIF_fit(x_data, dR2s_AIF, shift=11)

        A_mtx = self.AIF2matrix(dR2s_AIF, nt, self.TR)
        U,S,V = np.linalg.svd(A_mtx)

        for idx in range(len(self.maskIndex)):

            self.signal_processing.emit(idx+1)
            row_idx, col_idx = self.maskIndex[idx]
            sig = img[:200, row_idx, col_idx]             ###

            baseline_sig = np.sum(S0 * sig) / max(1, np.sum(S0))
            dR2s_TIS = self.Sig2Conc(signal=sig, S0=baseline_sig, TE=self.TE)
            dR2s_TIS = self.to_smoothed(x_data, dR2s_TIS, shift=11)
            
            CBF[row_idx, col_idx], CBV[row_idx, col_idx], MTT[row_idx, col_idx] = self.DSC(dR2s_TIS, dR2s_AIF, self.TR, A_mtx, U, S, V, nt)

        self.signal_end.emit((CBF, CBV, MTT))

    @staticmethod
    def Sig2Conc(signal: np.array, S0: np.array, TE: float) -> np.array:
        """Estimate R2* change.

        Input
        -------
        signal : ndarray
            1D array of signals.
        S0 : ndarray
            baseline signals.
        TE : float
            Echo time (s).

        Output
        --------
        delta_R2s : ndarray
            1D array of R2* changes (s^-1).
        """
        S0 = np.mean(S0)
        delta_R2s = -(1/TE) * np.log(signal/S0)
        return delta_R2s
    
    @staticmethod
    def AIF2matrix(dR2s_AIF: np.array, nt: int, TR: float) -> np.array:
        """Discretize the AIF.

        Input
        -------
        dR2s_AIF : ndarray
            1D array of delta R2 star of AIF.
        nt : int
            number of time points.
        TR : float
            intervel time (s).

        Output
        --------
        A_mtx : ndarray
            matrix form of AIF.
        """
        A_mtx = np.zeros([nt,nt])
        for i in range(nt):
            for j in range(nt):
                if j == 0 and i != 0:
                    A_mtx[i,j] = (2 * dR2s_AIF[i] + dR2s_AIF[i-1])/6.
                elif i == j:
                    A_mtx[i,j] = (2 * dR2s_AIF[0] + dR2s_AIF[1])/6.
                elif 0<j and j<i:
                    A_mtx[i,j] = ((2 * dR2s_AIF[i-j] + dR2s_AIF[i-j-1])/6) +((2 * dR2s_AIF[i-j] + dR2s_AIF[i-j+1])/6)
            else:
                A_mtx[i,j] = 0.
        return TR * A_mtx
    
    @staticmethod
    def DSCResults(ResidualFunction: np.array, dR2s_TIS: np.array, dR2s_AIF: np.array, TR: float) -> tuple:
        """Extract DSC parameters from residual function.

        Input
        -------
        ResidualFunction : ndarray
        dR2s_TIS : ndarray
        dR2s_AIF : ndarray
        TR : float

        Output
        -------
        CBF : mL/100 mL/min
        CBV : mL/100 mL
        MTT : s
        """
        CBF = np.amax(ResidualFunction) / TR * 60 * 100           # mL/100 mL/min
        CBV = np.trapz(dR2s_TIS) / np.trapz(dR2s_AIF) * 100       # mL/100 mL
        MTT = CBV / CBF * 60                                      # s
        return CBF, CBV, MTT 
    
    @staticmethod
    def lcurvereg(A_mtx, B, U, S):
        umax = 10.
        umin = 10E-10
        nu = 400
        k = np.arange(nu)
        u = np.amax(S) * umin * np.power((umax/umin),((k-1)/(nu-1)))

        l_0 = np.zeros([nu,A_mtx[:,0].size])
        l_1 = np.zeros([nu,A_mtx[:,0].size])
        l_2 = np.zeros([nu,A_mtx[:,0].size])
        L = np.zeros([nu,A_mtx[:,0].size,3])
        for x in range(nu):
            for y in range(A_mtx[:,0].size):
                l_0[x,y] = np.power((np.power(u[x],2) / (np.power(S[y],2) + np.power(u[x],2))),2)
                l_1[x,y] = np.power((S[y] / (np.power(S[y],2) + np.power(u[x],2))),2)
                l_2[x,y] = ((-4)*u[x]*np.power(S[y],2)) / np.power((np.power(S[y],2) + np.power(u[x],2)),3)

        L[:,:,0] = l_0
        L[:,:,1] = l_1
        L[:,:,2] = l_2

        # Start LCCOPTIMIZE
        k = (nu - 1)-1
        m = np.zeros([nu,3])
        product = np.zeros(A_mtx[:,0].size)
        L_curve = np.zeros(nu)

        for x in range(A_mtx[:,0].size):
            U_i = U[:,x]
            product[x] = np.power((np.transpose(U_i) @ B),2)

        for x in range(3):
            l_tmp = L[:,:,x]
            m[:,x] = np.sum(l_tmp,axis=1)*np.sum(product)

        for x in range(nu):
            L_curve[x] = 2 * (m[x,1] * m[x,0] / m[x,2]) * ((np.power(u[x],2) * m[x,2] * m[x,0] + 2 * u[x] * m[x,1] *m[x,0] + 
                                                            np.power(u[x],4) * m[x,1] * m[x,2]) / np.power((np.power(u[x],4) * 
                                                            np.power(m[x,1],2) + np.power(m[x,0],2)),(3/2)));

        L_minus1 = L_curve[k-2]
        L_0 = L_curve[k-1]
        L_1 = L_curve[k]

        while L_0 >= L_minus1 or L_0 >= L_1:
            k = k - 1
            if k == 0:
                mu_opt = umax
                break

            L_1 = L_0
            L_0 = L_minus1
            L_minus1 = L_curve[k-1]
            mu_opt = u[k-1]
        return mu_opt
    
    def DSC(self, dR2s_TIS: np.array, dR2s_AIF: np.array, TR: float, A_mtx, U, S, V, nt: int=None) -> tuple:
        if nt is None:
            nt = len(dR2s_TIS)

        B = np.transpose(U) @ dR2s_TIS
        mu_opt = self.lcurvereg(A_mtx, B, U, S)
        Bpi = np.multiply(np.divide(S,(np.power(S,2) + np.power(mu_opt,2))),B)
        residualFunction = np.transpose(V) @ Bpi
        CBF, CBV, MTT = self.DSCResults(residualFunction, dR2s_TIS, dR2s_AIF, TR)
        return CBF, CBV, MTT


    def arr_shift(self, A,n):
        shift = np.zeros(n)
        A_shifted = np.insert(A,0,shift)
        A_new = A_shifted[0:len(A)]
        return(A_new)


    def preclinicalAIF(self, t0, t):
        # Model B - parameter values defined in table 1 (McGrath MRM 2009)
        A1 = 3.4
        A2 = 1.81
        k1 = 0.045
        k2 = 0.0015
        t1 = 7
        
        # Eq. 5 (McGrath MRM 2009)     
        Ca = [A1*(i/t1)+A2*(i/t1) if i<=t1 else A1*np.exp(-k1*(i-t1))+A2*np.exp(-k2*(i-t1)) for i in t]
        # baseline shift
        Ca = self.arr_shift(Ca,int(t0/t[1])-1)
        return(Ca)  


    def AIF_fit(self, x_data, y_data, shift):
        def smooth(points, scale, t1):
            A1 = 3.4
            A2 = 1.81
            k1 = 0.045
            k2 = 0.0015
            Ca = np.zeros_like(points)
            index = np.where(points<t1)
            for i in range(len(Ca)):
                if i in list(index[0]):
                    Ca[i] = A1*(points[i]/t1)+A2*(points[i]/t1)
                else:
                    Ca[i] = A1*np.exp(-k1*(points[i]-t1))+A2*np.exp(-k2*(points[i]-t1))
    
            Ca = Ca+(0-min(Ca))  # limitation of non-negative
            Ca = Ca*(max(y_data) / max(Ca))
            return self.arr_shift(Ca, shift)
        popt_non, pcov_non = curve_fit(smooth, xdata=x_data, ydata=y_data, bounds=(0, [100, 5]))
        smoothed = smooth(x_data,popt_non[0],popt_non[1])
        return smoothed



    def to_smoothed(self, x_data, y_data, shift) -> np.array:
        def smooth(points, scale, A1, A2, k1, k2, t1):
            Ca = np.zeros_like(points)
            index = np.where(points<t1)
            for i in range(len(Ca)):
                if i in list(index[0]):
                    Ca[i] = A1*(points[i]/t1)+A2*(points[i]/t1)
                else:
                    Ca[i] = A1*np.exp(-k1*(points[i]-t1))+A2*np.exp(-k2*(points[i]-t1))
    
            Ca = Ca+(0-min(Ca))  # limitation of non-negative
            return self.arr_shift(Ca*scale, shift)
        popt_non, pcov_non = curve_fit(smooth, xdata=x_data, ydata=y_data, bounds=(0, [1000, 1000, 1000, 1, 1, 5]))
        smoothed = smooth(x_data,popt_non[0],popt_non[1],popt_non[2],popt_non[3],popt_non[4], popt_non[5])
        return smoothed