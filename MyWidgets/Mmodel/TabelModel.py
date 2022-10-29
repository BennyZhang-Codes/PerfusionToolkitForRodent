

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import numpy as np

class TimePointsTableModel(QAbstractTableModel):
    def __init__(self, TimePoint, SignalValue, parent=None) -> None:
        super().__init__(parent)
        self.headers = ['Point', 'Time (s)', 'Value']
        self._signalvalue = SignalValue
        self._timepoint = TimePoint
        self._S0 = np.zeros_like(TimePoint).astype(np.bool8)
        self._S0[:5] = np.ones((5)).astype(np.bool8)

        self._Contained = np.ones_like(TimePoint).astype(np.bool8)
        # print(self._S0)

    def rowCount(self, parent) -> int:
        return len(self._timepoint)

    def columnCount(self, parent) -> int:
        return len(self.headers)


    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.headers[section]
        else:
            return str(section + 1)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return index.row()+1
            elif index.column() == 1:
                return float(self.TimePoints[index.row()])
            elif index.column() == 2:
                return float(self.SignalValue[index.row()])
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role == Qt.BackgroundRole:
            if self.Contained[index.row()]:
                if self.S0[index.row()]:
                    return QColor(255,244,23,128)
                else:
                    return QColor(45,167,222,128)
            else:
                return QColor(45,45,45,128)
            # if index.column() == 0:
            #     return QColor(255,244,23,128)
            # elif index.column() == 1:
            #     return QColor(255,244,23,128)
            # elif index.column() == 2:
            #     return QColor(255,244,23,128)

    @property 
    def SignalValue(self) -> np.array:
        return self._signalvalue

    @SignalValue.setter
    def SignalValue(self, sv: np.array) -> None:
        self._signalvalue = sv

    @property 
    def TimePoints(self) -> np.array:
        return self._timepoint

    @TimePoints.setter
    def TimePoints(self, tp: np.array) -> None:
        self._timepoint = tp

    @property 
    def S0(self) -> np.array:
        return self._S0


    @property 
    def Contained(self) -> np.array:
        return self._Contained


