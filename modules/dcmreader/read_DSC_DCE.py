# -*- coding: utf-8 -*-
import re
import glob
import numpy as np
from pydicom.filereader import dcmread
from pydicom.dataset import FileDataset

from PySide6.QtCore import Signal, QObject

from modules.dcmreader.Read_dcm import MAbstractDicomReader
from modules.threads.thread_load_dicom import Thread_load_DSC_DCE

class read_DSC_DCE_folder(MAbstractDicomReader):
    _loadstart = Signal(bool)
    _loading = Signal(int)
    _loaded = Signal(bool)

    '''Bruker 11.7 DSC/DCE'''
    def __init__(self, dicom_dir: str=None) -> None:
        super().__init__()
        if dicom_dir:
            self.set_root(dicom_dir)

    def set_root(self, new_dicom_dir: str):
        self.root = new_dicom_dir
        self.acqp_path = '{}/acqp'.format(self.root)
        self.dicom_path = self.root + r'\pdata\1\dicom'
        self._slice_num, self._time_points_num, self._time_points = self.__read_acqp(self.acqp_path)
        self._dcm_list = self.__load_dcm_list()
        self.Thread_loader = Thread_load_DSC_DCE(self)
        self.Thread_loader._loadstart.connect(self.__loadstart)
        self.Thread_loader._loading.connect(self.__loading)
        self.Thread_loader._loaded.connect(self.__loaded)
        self.Thread_loader.start()
        


    def set_slice(self, idx: int):
        idx = self.__check_slice(idx)
        
        self._current_slice = idx + 1

        self._imgs_curSlice = self.__imgs_all[idx]
        self._dss_curSlice = self.__dss_all[idx]

        # if hasattr(self, '__imgs_all') and hasattr(self, '__dss_all') :
        #     self.__imgs_curSlice = self.__imgs_all[idx]
        #     self.__dss_curSlice = self.__dss_all[idx]
        # else:
        #     self.__imgs_curSlice, self.__dss_curSlice = self.__load_slice(idx)
        
    def __read_acqp(self, acqp_path: str) -> tuple:
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
            print('check number of times points')
        return slice_num, time_points_num, time_points

    def __load_dcm_list(self) -> list:
        DCM_list = glob.glob('*.dcm', root_dir=self.dicom_path)
        IMA_list = glob.glob('*.IMA', root_dir=self.dicom_path)
        dcm_list = DCM_list + IMA_list
        dcm_list.sort()
        return dcm_list

    def __load_slice(self, idx: int) -> np.array:
        dcms = self.DicomList[idx::self.SliceNum]
        ds_perSlice = [dcmread(self.dicom_path + '/' + dcm) for dcm in dcms]
        imgs_perSlice = [ds.pixel_array for ds in ds_perSlice]
        return np.array(imgs_perSlice), np.array(ds_perSlice)

    def __load_all(self) -> np.array:
        '''QThread'''
        res = [self.__load_slice(idx) for idx in range(self.SliceNum)]
        imgs_all = [r[0] for r in res]
        dss_all = [r[1] for r in res]
        return np.array(imgs_all), np.array(dss_all)
        
    def thread(self):
        self.__imgs_all, self.__dss_all = self.__load_all()

    def get_pixel_array(self, index: int) -> np.array:
        ds = self.get_ds(index)
        return ds.pixel_array

    def get_ds(self, index: int) -> FileDataset:
        index = self.__check_time_point(index)
        return self.dss_curSlice[index]

    def get_ds_and_array(self, index: int) -> tuple:
        ds = self.get_ds(index)
        return ds, ds.pixel_array
         

    @property
    def len(self) -> int:
        return self.TimePointsNum
        
    def min_idx(self) -> int:
        return 0

    def max_idx(self) -> int:
        return self.len - 1

    def __check_time_point(self, idx: int) -> int:
        return self.__check_index(idx, self.min_idx(), self.max_idx())

    def __check_slice(self, idx: int) -> int:
        return self.__check_index(idx, 0, self._slice_num-1)

    @staticmethod
    def __check_index(para: int, min: int, max: int) -> int:
        if para < min:
            para  = min
        elif para >= max:
            para = max
        return para


    @property
    def SliceNum(self) -> int:
        return self._slice_num

    @property
    def TimePointsNum(self) -> int:
        return self._time_points_num

    @property
    def TimePoints(self) -> np.array:
        return self._time_points

    @property
    def CurrentSlice(self) -> int:
        return self._current_slice

    @property
    def imgs_curSlice(self) -> np.array:
        return self._imgs_curSlice

    @property 
    def dss_curSlice(self) -> np.array:
        return self._dss_curSlice

    @property
    def DicomList(self) -> list:
        return self._dcm_list

    def __loadstart(self, start: bool):
        self._loadstart.emit(start)

    def __loading(self, value: int):
        self._loading.emit(value)

    def __loaded(self, data: tuple):
        self.__imgs_all, self.__dss_all = data
        self._row, self._col = self.__imgs_all[0,0,:,:].shape
        self._loaded.emit(True)

    @property
    def RowNum(self) -> int:
        return self._row

    @property
    def ColNum(self) -> int:
        return self._col
        

