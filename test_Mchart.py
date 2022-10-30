
import sys
import math
from PySide6 import QtCore, QtDataVisualization
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from jupyter_client import BlockingKernelClient
from matplotlib.pyplot import scatter
import numpy as np



from MyWidgets.MChart.MChart import MChartView, MChart
from MyWidgets.MView.MTableView import MTableView
from MyWidgets.Mmodel.TabelModel import TimePointsTableModel


class InteractScatterChart(MChartView):
    def __init__(self):
        super().__init__()
        self.Mchart = MChart()
        self.setChart(self.Mchart)

        self.setRenderHint(QPainter.Antialiasing)




class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(500)
        self.setMinimumWidth(1200)
        self.scatter = InteractScatterChart()
        scatter = self.scatter

        tableview = MTableView()


        self.w = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(tableview)
        layout.addWidget(scatter)
        layout.setStretch(0,2)
        layout.setStretch(1,5)
        self.w.setLayout(layout)


        xdata = np.arange(20)
        ydata = np.arange(20)**2
        
        


        self.model = TimePointsTableModel(xdata, ydata)
        tableview.setModel(self.model)
        scatter.Mchart.setModel(self.model)
        scatter.Mchart.selected_point.connect(tableview.selectRow)
        tableview.changed_rows.connect(scatter.Mchart._slot_update_pointConf)
        tableview.selected_row.connect(scatter.Mchart._update_focus_point)

        self.setCentralWidget(self.w)
        self.resize(500, 300)
        self.setWindowTitle('InteractScatterChart')

        

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
        main()