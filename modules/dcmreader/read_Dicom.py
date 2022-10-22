# -*- coding: utf-8 -*-
import glob
import numpy as np
from pydicom.filereader import dcmread
from pydicom.dataset import FileDataset
from modules.dcmreader.Read_dcm import MAbstractDicomReader

class read_Dicom_folder(MAbstractDicomReader):
    def __init__(self, dicom_dir: str=None) -> None:
        super().__init__()
        if dicom_dir:
            self.set_root(dicom_dir)

    def set_root(self, new_dicom_dir: str):
        self.root = new_dicom_dir
        self.dcm_list = self._get_dcm_list(self.root)

    @staticmethod
    def _get_dcm_list(root: str) -> tuple:
        DCM_list = glob.glob('*.dcm', root_dir=root)
        IMA_list = glob.glob('*.IMA', root_dir=root)
        dcm_list = DCM_list + IMA_list
        dcm_list.sort()
        return dcm_list

    def _get_path(self, index: int) -> str:
        dcm_name = self.dcm_list[index]
        dcm_path = self.root + '\\' + dcm_name
        return dcm_path

    def get_pixel_array(self, index: int) -> np.array:
        ds = self.get_ds(index)
        return ds.pixel_array

    def get_ds(self, index: int) -> FileDataset:
        dcm_path = self._get_path(index)
        return dcmread(dcm_path)

    def get_ds_and_array(self, index: int) -> tuple:
        ds = self.get_ds(index)
        return ds, ds.pixel_array
         
    def len(self) -> int:
        return len(self.dcm_list)
        
    def min_idx(self) -> int:
        return 0

    def max_idx(self) -> int:
        return self.len() - 1
