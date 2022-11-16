
import numpy as np
import matplotlib.pyplot as plt

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from UI.ui_Widget_TimePoints import Ui_Widget_TimePoints

class Widget_area_TimePoints(QWidget, Ui_Widget_TimePoints):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.setupUi(self)


    def _setup(self):
        self.tableView.setModel(model)
        self.chartView.chart().setModel(model)
        self.chart.selected_point.connect(self.tableView_points.selectRow)
        self.tableView_points.changed_rows.connect(self.chart._slot_update_pointConf)
        self.tableView_points.selected_row.connect(self.chart._update_focus_point)



    def setData(self, xdata: np.array, ydata: np.array) -> None:
        


        pass


    

      


        