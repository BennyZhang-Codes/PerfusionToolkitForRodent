# -*- coding: utf-8 -*-
import os
import re
import glob
import numpy as np
from pydicom.filereader import dcmread
from pydicom.dataset import FileDataset

from PySide6.QtCore import Signal, QObject

from modules.dcmreader.Read_dcm import MAbstractDicomReader
from modules.threads.load_dicom import Thread_load_Bruker_TimeSeries

class Read_Bruker_TimeSeries(MAbstractDicomReader):
    '''Bruker 11.7 DSC/DCE like time series images in Dicom format.'''
    signal_loadstart = Signal(bool)
    signal_loading = Signal(int)
    signal_loaded = Signal(bool)

    GroupByTime = 'Time'
    GroupBySlice = 'Slice'
    def __init__(self, dicom_dir: str) -> None:
        super().__init__()
        self.setDicomRoot(dicom_dir)

    def setDicomRoot(self, dicom_dir: str) -> None:
        self.DicomRoot = dicom_dir
        self.setup()

    def setup(self) -> None:
        self._group_mode = self.GroupByTime 
        self._current_slice = 0
        self._current_timepoint = 0
        self._img_all: np.array = None
        self._dss_all: np.array = None
        
    def __get_dcm_list(self) -> list:
        DCM_list = glob.glob('*.dcm', root_dir=self.dicom_path)
        IMA_list = glob.glob('*.IMA', root_dir=self.dicom_path)
        dcm_list = DCM_list + IMA_list
        dcm_list.sort()
        return dcm_list

    def get_ds(self, idx: int) -> FileDataset:
        '''get ds::FileDataset'''
        if self.GroupBy == self.GroupByTime:
            self.CurrentSlice = idx
            ds = self.dss_GroupByTime[self.CurrentSlice]
        elif self.GroupBy == self.GroupBySlice:
            self.CurrentTimePoint = idx
            ds = self.dss_GroupBySlice[self.CurrentTimePoint]
        return ds

    def get_array(self, index: int) -> np.array:
        ds = self.get_ds(index)
        return ds.pixel_array

    @property
    def len(self) -> int:
        if self.GroupBy == self.GroupBySlice:
            number = self.TimePointsNum
        elif self.GroupBy == self.GroupByTime:
            number = self.SliceNum
        return number
        
    @property
    def min_idx(self) -> int:
        return 0

    @property
    def max_idx(self) -> int:
        return self.len - 1

    @property
    def CurrentSlice(self) -> int:
        return self._current_slice

    @CurrentSlice.setter
    def CurrentSlice(self, idx: int) -> None:
        self._current_slice = self.__check_index(idx, 0, self.SliceNum)

    @property
    def CurrentTimePoint(self) -> int:
        return self._current_timepoint

    @CurrentTimePoint.setter
    def CurrentTimePoint(self, idx: int) -> None:
        self._current_timepoint = self.__check_index(idx, 0, self.TimePointsNum)

    @property
    def DicomList(self) -> list:
        return self._dcm_list

    @property
    def RowNum(self) -> int:
        return self._row

    @property
    def ColNum(self) -> int:
        return self._col

    @property
    def imgAll(self) -> int:
        return self._img_all

    @property
    def dssAll(self) -> int:
        return self._dss_all

    @property
    def DicomRoot(self) -> str:
        return self._dicom_root

    @DicomRoot.setter
    def DicomRoot(self, root: str) -> None:
        if not os.path.exists(root):
            raise FileNotFoundError('Dicom root does not exist: {}'.format(root))
        else:
            self._dicom_root = root
            self.acqp_path = '{}/acqp'.format(root)
            self.dicom_path = root + r'\pdata\1\dicom'
            self._slice_num, self._time_points_num, self._time_points = self.__read_acqp(self.acqp_path)
            self._dcm_list = self.__get_dcm_list()
            self.Thread_loader = Thread_load_Bruker_TimeSeries(self)
            self.Thread_loader._loadstart.connect(self.__slot_loadstart)
            self.Thread_loader._loading.connect(self.__slot_loading)
            self.Thread_loader._loaded.connect(self.__slot_loaded)
            self.Thread_loader.start()
        
    def __slot_loadstart(self, start: bool):
        '''Slot function for dicom read thread'''
        self.signal_loadstart.emit(start)

    def __slot_loading(self, value: int):
        '''Slot function for dicom read thread'''
        self.signal_loading.emit(value)

    def __slot_loaded(self, loaded: bool):
        '''Slot function for dicom read thread'''
        self._row, self._col = self._img_all[0,:,:].shape
        self.signal_loaded.emit(True)

    @property
    def img_GroupBySlice(self) -> np.array:
        return self.imgAll[self.CurrentSlice::self.SliceNum]
        
    @property 
    def dss_GroupBySlice(self) -> np.array:
        return self.dssAll[self.CurrentSlice::self.SliceNum]

    @property
    def img_GroupByTime(self) -> np.array:
        return self.imgAll[self.CurrentTimePoint::self.TimePointsNum]
        
    @property 
    def dss_GroupByTime(self) -> np.array:
        return self.dssAll[self.CurrentTimePoint::self.TimePointsNum]

    @property
    def SliceNum(self) -> int:
        return self._slice_num

    @property
    def TimePointsNum(self) -> int:
        return self.TimePoints.__len__()

    @property
    def TimePoints(self) -> np.array:
        return self._time_points

    @property
    def GroupBy(self) -> str:
        return self._group_mode

    @GroupBy.setter
    def GroupBy(self, mode: str) -> None:
        if mode in [
            self.GroupByTime,
            self.GroupBySlice,
        ]:
            self._group_mode = mode
        else:
            raise ValueError('Unsupported Group mode: {}'.format(mode))

    def __read_acqp(self, acqp_path: str) -> tuple:
        '''Read Bruker acqp file, and get infomation of Time Points and number of Slice'''
        with open(acqp_path, mode='r', encoding='UTF-8') as f:
            file = f.read()
        Re = re.compile(r'[##$]NSLICES=(.*)\n')
        slice = Re.findall(file)
        slice_num = int(slice[0])
        Re = re.compile(r'[##$]ACQ_time_points=[(] (.\d+) [)](.*?)#', flags=re.DOTALL)
        res = Re.findall(file)
        time_points_num = int(res[0][0])
        time_points = res[0][1]
        time_points = (time_points.strip()).replace('\n', '').split(' ')
        time_points = np.array([float(time)*1000 for time in time_points])
        if time_points_num != time_points.__len__():
            raise ValueError('Times points number not match!')
        return slice_num, time_points_num, time_points

    @staticmethod
    def __check_index(para: int, min: int, max: int) -> int:
        if para < min:
            para  = min
        elif para >= max:
            para = max
        return para