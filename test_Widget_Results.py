import sys
from pydicom import dcmread
import numpy as np
import matplotlib.pyplot as plt

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from UI.ui_Widget_Results import Ui_Widget_Results
from modules.utils.colormap import MColorMap
from ToolWidgets.Widget_Results import Widget_Results


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = QWidget()
        layout = QVBoxLayout()
        self.w.setLayout(layout)
        w = Widget_Results(self)
        ds = dcmread(r'E:\A30\DSC\Im00008.dcm')
        w.setImageArray(ds.pixel_array)
        layout.addWidget(w)
        self.setCentralWidget(self.w)
        self.resize(500, 300)
        self.setWindowTitle('Color')

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

main()