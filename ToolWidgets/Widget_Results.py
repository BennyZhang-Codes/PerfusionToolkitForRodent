import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from UI.ui_Widget_Results import Ui_Widget_Results
from modules.utils.colormap import MColorMap

class Widget_Results(QWidget, Ui_Widget_Results):
    value = Signal(float)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.ColorMap = MColorMap()
        self.setEnabled(False)
        self.setup()

    def setup(self) -> None:
        self.widget_colorbar.setPixmap(self.PixColorBar)
        self.widget_result.ColorMap = self.ColorMap
        self.widget_result.Vmax.connect(self.doubleSpinBox_max.setValue)
        self.widget_result.Vmin.connect(self.doubleSpinBox_min.setValue)
        self.doubleSpinBox_max.valueChanged.connect(self.widget_result.setVmax)
        self.doubleSpinBox_min.valueChanged.connect(self.widget_result.setVmin)

    def setImageArray(self, img: np.array) -> None:
        self.widget_result.setImgArray(img)
        self.img = img
        self.setEnabled(True)

    @Slot(int)
    def on_comboBox_colormap_currentIndexChanged(self, idx: int) -> None:
        self.ColorMap.idx = idx
        self.widget_colorbar.setPixmap(self.PixColorBar)
        self.widget_result.update_PixImage()
        self.widget_result.update()

    @Slot()
    def on_pushButton_Save_clicked(self) -> None:
        dialog = QFileDialog(self, 'Save File')
        dialog.setMimeTypeFilters(['image/png', 'image/jpeg', 'image/bmp', 'image/tiff'])
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("png")
        dialog.setDirectory(
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        )
        if dialog.exec() == QFileDialog.Accepted:
            a = dialog.selectedFiles()[0]
            self.widget_result.PixImage.save(a)


        


    @property
    def PixColorBar(self) -> QPixmap:
        a = np.expand_dims(np.flipud(np.arange(256)), axis=0)
        cb = [a for i in range(50)]
        cb = np.concatenate(cb, axis=0).astype(np.uint8).T
        cb = self.ColorMap.applyColorMap(cb)
        cb = Image.fromarray(cb)
        return cb.toqpixmap()