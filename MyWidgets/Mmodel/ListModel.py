from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import Qt, QModelIndex
import numpy as np



class TimePointListModel(QAbstractListModel):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)


    def data(self, index: QModelIndex, role: int):
        return super().data(index, role)

    def rowCount(self, parent: QModelIndex) -> int:
        return super().rowCount(parent)