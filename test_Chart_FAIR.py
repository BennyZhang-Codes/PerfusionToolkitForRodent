
import sys
import math
from PySide6 import QtCore, QtDataVisualization
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *

import numpy as np



from MyWidgets.MChart.MChart_FAIR import MChartView, MChart_FAIR
from MyWidgets.Mmodel.TabelModel import TimePointsTableModel


class InteractScatterChart(MChartView):
    def __init__(self):
        super().__init__()
        self.Mchart = MChart_FAIR()
        self.setChart(self.Mchart)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setMinimumHeight(500)
        # self.setMinimumWidth(1200)
        self.scatter = InteractScatterChart()
        scatter = self.scatter


        self.w = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(scatter)
        layout.setStretch(0,2)

        self.w.setLayout(layout)


        xdata = np.arange(20)
        ydata = np.arange(20)**2
        line = QLineSeries()

        for x, y in zip(xdata, ydata):
            line.append(QPointF(x, y))


        scatter.Mchart.setData(xdata, ydata, ydata+10)

        # scatter.Mchart.removeAllSeries()
        # scatter.Mchart.addSeries(line)
        self.setCentralWidget(self.w)
        # self.resize(500, 300)
        self.setWindowTitle('InteractScatterChart')
        print(scatter.Mchart.LineSeries_Non.color())
        print(scatter.Mchart.LineSeries_Sel.color())

        

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
        main()