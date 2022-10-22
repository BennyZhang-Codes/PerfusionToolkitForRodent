# -*- coding: utf-8 -*-
from PySide6.QtCore import Signal, QThread

class ThreadIconlist(QThread):
    loading_signal = Signal(int)
    loaded_signal = Signal()
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    def run(self):
        self.parent.listWidget.clear()
        
        for idx in range(self.parent.dicom_reader.len()):
            self.parent.iconlist(idx)
            self.loading_signal.emit(idx)
        self.loaded_signal.emit()

