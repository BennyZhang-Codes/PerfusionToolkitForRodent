
import sys
import math
from PySide6 import QtCore, QtDataVisualization
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from jupyter_client import BlockingKernelClient
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
        scatter = InteractScatterChart()

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
        scatter.Mchart.set_data(xdata, ydata)
        


        model = TimePointsTableModel(xdata, ydata)
        tableview.setModel(model)
        scatter.Mchart.set_S0(model._S0)

        tableview.verticalHeader().setVisible(False)
        # self.tableView_points.selected_row.connect(series._slot)
        
        scatter.Mchart.selected_point.connect(tableview.selectRow)
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