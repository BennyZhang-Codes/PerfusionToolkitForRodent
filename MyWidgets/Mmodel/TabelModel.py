

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import numpy as np

class TimePointsTableModel(QAbstractTableModel):
    Color_Background_Default = QColor(0,82,157,255)
    Color_Background_S0 = QColor(186,42,23,255)
    Color_Background_Delete = QColor(151,153,151,255)

    Color_chart_Default = QColor(0,82,157,255)
    Color_chart_S0 = QColor(186,42,23,255)
    Color_chart_Delete = QColor(151,153,151,255)
    def __init__(self, TimePoint, SignalValue, parent=None) -> None:
        super().__init__(parent)
        self.headers = ['Point', 'Time (s)', 'Value']
        self._signalvalue = SignalValue
        self._timepoint = TimePoint
        self._S0 = np.zeros_like(TimePoint).astype(np.bool8)
        self._Contained = np.ones_like(TimePoint).astype(np.bool8)

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
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        elif role == Qt.BackgroundRole:
            if self.Contained[index.row()]:
                if self.S0[index.row()]:
                    return self.Color_Background_S0
                else:
                    return self.Color_Background_Default
            else:
                return self.Color_Background_Delete

    def getColor(self, row: int) -> QColor:
        if self.Contained[row]:
            if self.S0[row]:
                return self.Color_chart_S0
            else:
                return self.Color_chart_Default
        else:
            return self.Color_chart_Delete

    def set_S0(self, indexes: np.array, select: bool) -> None:
        for idx in indexes:
            self.S0[idx] = select

    def set_delete(self, indexes: np.array, delete: bool) -> None:
        for idx in indexes:
            self.Contained[idx] = delete

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


