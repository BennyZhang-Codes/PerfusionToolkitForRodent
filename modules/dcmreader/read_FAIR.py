# -*- coding: utf-8 -*-
import glob
import numpy as np
from pydicom.filereader import dcmread
from pydicom.dataset import FileDataset
from modules.dcmreader.Read_dcm import MAbstractDicomReader

class read_FAIR_folder(MAbstractDicomReader):
    '''Bruker 11.7 Perfusion of FAIR'''
    def __init__(self, dicom_dir: str=None) -> None:
        super().__init__()
        if dicom_dir:
            self.set_root(dicom_dir)

    def set_root(self, new_dicom_dir: str):
        self.root = new_dicom_dir
        self.dss_all, self.slice_num = self.__read_dicom_folder(self.root)
        self.current_slice = 1
        self.dss_slice = self.dss_all[self.current_slice-1]
        self.dss = (self.dss_slice[0::2], self.dss_slice[1::2])
        self.dss_sel = self.dss_slice[0::2]
        self.dss_non = self.dss_slice[1::2]

    def __read_dicom_folder(self, root: str) -> tuple:
        '''Bruker 11.7T: read Dicom images of Perfusion_FAIR '''
        DCM_list = glob.glob('*.dcm', root_dir=root)
        IMA_list = glob.glob('*.IMA', root_dir=root)
        dcm_list = DCM_list + IMA_list
        dcm_list.sort()
        self.total_num = len(dcm_list)
        SliceLocation = []
        # check number of slices
        for dcm_name in dcm_list:
            dcm_path = self.__get_path(dcm_name)
            ds = dcmread(dcm_path)
            if ds.SliceLocation not in SliceLocation:
                SliceLocation.append(ds.SliceLocation)
        # read dicom files
        slice_num = SliceLocation.__len__()
        dss_slices = []
        for slice in range(slice_num):
            dss = []
            dcm_files_perslice = dcm_list[slice::slice_num]
            for dcm_name in dcm_files_perslice:
                dcm_path = self.__get_path(dcm_name)
                ds = dcmread(dcm_path)
                dss.append(ds)
            dss_slices.append(dss)
        return dss_slices, slice_num

    def __get_path(self, dcm_name: str) -> str:
        return self.root + '\\' + dcm_name

    def get_pixel_array(self, index: int) -> np.array:
        ds = self.get_ds(index)
        return ds.pixel_array

    def get_ds(self, index: int) -> FileDataset:
        return self.dss_slice[index]

    def get_ds_and_array(self, index: int) -> tuple:
        ds = self.get_ds(index)
        return ds, ds.pixel_array
         
    def len(self) -> int:
        return len(self.dss_slice)
        
    def min_idx(self) -> int:
        return 0

    def max_idx(self) -> int:
        return self.len() - 1

