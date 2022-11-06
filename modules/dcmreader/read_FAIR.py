# -*- coding: utf-8 -*-
import os
import glob
import numpy as np
from pydicom.filereader import dcmread
from pydicom.dataset import FileDataset
from PySide6.QtCore import Signal
from modules.dcmreader.Read_dcm import MAbstractDicomReader

class read_FAIR_folder(MAbstractDicomReader):
    '''Bruker 11.7 Perfusion of FAIR'''
    signal_loadstart = Signal(bool)
    signal_loading = Signal(int)
    signal_loaded = Signal(bool)

    GroupByTime = 'Time'
    GroupBySlice = 'Slice'
    def __init__(self, dicom_dir: str=None) -> None:
        super().__init__()
        self.setDicomRoot(dicom_dir)

    def setDicomRoot(self, dicom_dir: str) -> None:
        self.DicomRoot = dicom_dir
        self.setup()

    def setup(self) -> None:
        self._group_mode = self.GroupByTime 
        self._current_slice = 0
        self._current_timepoint = 0
        # self._img_all: np.array = None
        # self._dss_all: np.array = None

    def get_data(self, idx: int) -> tuple:
        """obtain data

        Input
        -------
        idx : int

        Output
        --------
        ds : FileDataset
        img: ndarray
        """
        if self.GroupBy == self.GroupByTime:
            self.CurrentSlice = idx
            ds = self.dss_GroupByTime[self.CurrentSlice]
            img = self.img_GroupByTime[self.CurrentSlice]
        elif self.GroupBy == self.GroupBySlice:
            self.CurrentTimePoint = idx
            ds = self.dss_GroupBySlice[self.CurrentTimePoint]
            img = self.img_GroupBySlice[self.CurrentTimePoint]
        return ds, img

    @property
    def RowNum(self) -> int:
        return self._row

    @property
    def ColNum(self) -> int:
        return self._col

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
    def DicomRoot(self) -> str:
        return self._dicom_root

    @DicomRoot.setter
    def DicomRoot(self, root: str) -> None:
        if not os.path.exists(root):
            raise FileNotFoundError('Dicom root does not exist: {}'.format(root))
        else:
            self._dicom_root = root
            self.__read_FAIR_dicom(root)
            self._slice_num = len(self._SliceLocation)
            self._time_points_num = len(self._InversionTime)
            self._time_points = self._InversionTime
            self._row, self._col = self._img_all[0,:,:].shape

            self._sel_img_all = self._img_all[0::2]
            self._non_img_all = self._img_all[1::2]

            # self.Thread_loader = Thread_load_Bruker_TimeSeries(self)
            # self.Thread_loader._loadstart.connect(self.__slot_loadstart)
            # self.Thread_loader._loading.connect(self.__slot_loading)
            # self.Thread_loader._loaded.connect(self.__slot_loaded)
            # self.Thread_loader.start()

    def __read_FAIR_dicom(self, root: str) -> tuple:
        '''Bruker 11.7T: read Dicom images of Perfusion_FAIR '''
        DCM_list = glob.glob('*.dcm', root_dir=root)
        IMA_list = glob.glob('*.IMA', root_dir=root)
        dcm_list = DCM_list + IMA_list
        dcm_list.sort()

        self.total_num = len(dcm_list)
        SliceLocation = set()
        InversionTime = set()
        # check number of slices
        img = []
        dss = []
        for dcm_name in dcm_list:
            dcm_path = self.DicomRoot + '\\' + dcm_name
            ds = dcmread(dcm_path)
            SliceLocation.add(ds.SliceLocation)
            InversionTime.add(ds.InversionTime)
            print(InversionTime)
            dss.append(ds)
            img.append(ds.pixel_array)

        SliceLocation = [float(Location) for Location in SliceLocation]
        SliceLocation.sort()
        InversionTime = [float(time) for time in InversionTime]
        InversionTime.sort()

        self._img_all = np.array(img)
        self._dss_all = np.array(dss)
        self._SliceLocation = SliceLocation
        self._InversionTime = InversionTime

    @property
    def img_GroupBySlice(self) -> np.array:
        return self.imgAll[self.CurrentSlice::self.SliceNum]
        
    @property 
    def dss_GroupBySlice(self) -> np.array:
        return self.dssAll[self.CurrentSlice::self.SliceNum]

    @property
    def img_GroupByTime(self) -> np.array:
        return self.imgAll[self.SliceNum * self.CurrentTimePoint : self.SliceNum * (self.CurrentTimePoint+1)]
        
    @property 
    def dss_GroupByTime(self) -> np.array:
        return self.dssAll[self.SliceNum * self.CurrentTimePoint : self.SliceNum * (self.CurrentTimePoint+1)]
    
    @property
    def imgAll(self) -> np.array:
        return self._sel_img_all

    @property
    def dssAll(self) -> np.array:
        return self._dss_all



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
        self._current_slice = self.__check_index(idx, 0, self.SliceNum-1)

    @property
    def CurrentTimePoint(self) -> int:
        return self._current_timepoint

    @CurrentTimePoint.setter
    def CurrentTimePoint(self, idx: int) -> None:
        self._current_timepoint = self.__check_index(idx, 0, self.TimePointsNum-1)

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

    @staticmethod
    def __check_index(para: int, min: int, max: int) -> int:
        if para < min:
            para  = min
        elif para >= max:
            para = max
        return para



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