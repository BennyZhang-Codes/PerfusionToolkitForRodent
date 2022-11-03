# -*- coding: utf-8 -*-
import numpy as np
import SimpleITK as sitk
from PySide6.QtCore import Signal, QThread

from modules.dcmreader.read_DSC_DCE import Read_Bruker_TimeSeries


class DSC_Registration:
    def __init__(self) -> None:
        self._R = sitk.ImageRegistrationMethod()
        self._R.SetMetricAsMeanSquares()
        self._R.SetOptimizerAsRegularStepGradientDescent(4.0, 0.01, 500)
        self._R.SetInitialTransform(sitk.TranslationTransform(3))
        self._R.SetInterpolator(sitk.sitkLinear)

        self._resampler = sitk.ResampleImageFilter()
        self._resampler.SetInterpolator(sitk.sitkLinear)
        self._resampler.SetDefaultPixelValue(0)

        self.x = True
        self.y = True
        self.z = True

        self.four = False

    def Execute(self, moving: np.array) -> np.array:
        moving = self.array_to_sitk(moving)
        outTx = self.R.Execute(self.fixed, moving)
        offset = outTx.GetOffset()
        offset = tuple(np.array(offset) * self.Translation_Direction)
        outTx.SetOffset(offset)
        self.resampler.SetTransform(outTx)
        out = self.resampler.Execute(moving)
        return self.sitk_to_array(out)

    def array_to_sitk(self, img: np.array) -> sitk.Image:
        self.axis0 = img.shape[0]
        if  self.axis0 < 4:
            img = np.concatenate([img, img, img, img], axis=0)
            self.four = True
        return sitk.GetImageFromArray(img.astype(np.float32))


    def sitk_to_array(self, image: sitk.Image) -> np.array:
        img = sitk.GetArrayFromImage(image).astype(np.int16)
        if self.four:
            img = img[:self.axis0]
        return img

    @property
    def R(self) -> sitk.ImageRegistrationMethod:
        return self._R

    @property
    def resampler(self) -> sitk.ResampleImageFilter:
        return self._resampler

    @property
    def fixed(self) -> sitk.Image:
        return self._fixed

    @fixed.setter
    def fixed(self, img: np.array) -> None:
        self._fixed = self.array_to_sitk(img)
        self._resampler.SetReferenceImage(self._fixed)

    @property
    def Translation_Direction(self) -> np.array:
        return np.array([self.x, self.y, self.z])

class Thread_TimeSeries_correction(QThread):
    signal_start = Signal(bool)
    signal_processing = Signal(int)
    signal_end = Signal(bool)
    def __init__(self, ):
        super().__init__()
        self.TimeSeries_registration  = DSC_Registration()

    def set_DicomReader(self, DicomReader: Read_Bruker_TimeSeries) -> None:
        self.DicomReader = DicomReader
        self.imgAll = self.DicomReader.imgAll

    def set_FixedPoint(self, point: int) -> None:
        self.fixedpoint = point - 1
        
    def run(self):
        self.signal_start.emit(True)
        SliceNum = self.DicomReader.SliceNum
        TimePointsNum = self.DicomReader.TimePointsNum

        self.TimeSeries_registration.fixed = self.imgAll[SliceNum * self.fixedpoint : SliceNum * (self.fixedpoint+1)]


        res = np.zeros_like(self.imgAll)
        for idx in range(TimePointsNum):
            self.signal_processing.emit(idx+1)
            out = self.TimeSeries_registration.Execute(self.imgAll[SliceNum * idx : SliceNum * (idx+1)])
            res[SliceNum * idx : SliceNum * (idx+1)] = out

        self.DicomReader._img_corrected = res
        self.signal_end.emit(True)
