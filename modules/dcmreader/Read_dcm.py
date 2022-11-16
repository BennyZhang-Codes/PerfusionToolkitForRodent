# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, ABCMeta
import numpy as np
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget


class MAbstractDicomReader(QObject):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def set_root(self, new_dicom_dir: str) -> None:
        '''set dicom directory'''

    @abstractmethod
    def get_pixel_array(self, index: int) -> np.array:
        '''obtain array of image by index'''

    @abstractmethod
    def get_ds(self, index: int) -> np.array:
        '''obtain ds by index'''

    @abstractmethod
    def len(self) -> int:
        '''number of Dicom files'''

    @abstractmethod    
    def min_idx(self) -> int:
        '''minimum index'''

    @abstractmethod
    def max_idx(self) -> int:
        '''maximum index'''


# if __name__ == '__main__':
#     path = r'E:\A30\19\pdata\1\dicom'
#     dcm = read_Dicom_folder(dicom_dir=path)
#     print(dcm.dcm_list)
#     a = glob.glob('*.dcm', root_dir=path)
#     b = glob.glob('*.IMA', root_dir=path)
#     print(dcm.len())