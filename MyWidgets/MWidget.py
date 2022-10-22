from abc import ABC, abstractmethod


from PySide6.QtWidgets import QWidget
import PySide6.QtWidgets
import PySide6.QtCore
import PySide6.QtGui

from typing import Optional

class MWidget(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

    @abstractmethod
    def set_mainwindow(self) -> None:
        '''set mainwindow'''
