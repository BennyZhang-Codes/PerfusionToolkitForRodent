from operator import mod
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
import numpy as np

from MyWidgets.Mmodel.TabelModel import TimePointsTableModel

class MChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.Antialiasing)


    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update()
        return super().resizeEvent(event)
        

class MChart_FAIR(QChart):
    selected_point = Signal(int)
    Color_Focus = QColor(31, 243, 116, 255)
    Color_Non = QColor.fromRgbF(0.921569, 0.533333, 0.090196, 1.000000)
    Color_Sel = QColor.fromRgbF(0.219608, 0.678431, 0.419608, 1.000000)
    

    # Color_Sel = QColor(235, 136, 23)
    # Color_Non = QColor(47, 136, 88)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTheme(QChart.ChartThemeDark)

        self.setAnimationOptions(QChart.SeriesAnimations)
        self.setAcceptHoverEvents(True)
        self.init_series()

    def setData(self, xdata, sel_ydata, non_ydata) -> None:
        self.xdata = xdata
        self.sel_ydata = sel_ydata
        self.non_ydata = non_ydata
        self._update_all()
        self.createDefaultAxes()

        y_min = min(self.sel_ydata.min(), self.non_ydata.min())*0.9
        y_max = max(self.sel_ydata.max(), self.non_ydata.max())*1.1
        self.axes(Qt.Vertical)[0].setRange(y_min, y_max)
        self.axes(Qt.Horizontal)[0].setRange(0, self.xdata.max()*1.1)
        
    def init_series(self) -> None:
        self.ScatterSeries_up = QScatterSeries()
        self.ScatterSeries_up.setMarkerSize(12)
        self.ScatterSeries_up.setColor(self.Color_Focus)
        self.ScatterSeries_up.pressed.connect(self._slot_Sel_pressed)


        self.ScatterSeries_Sel = QScatterSeries()
        self.ScatterSeries_Sel.setName('Selective Inversion')
        self.ScatterSeries_Sel.setMarkerSize(8)
        self.ScatterSeries_Sel.setColor(self.Color_Sel)
        self.ScatterSeries_Sel.hovered.connect(self._slot_Sel_hovered)
        self.ScatterSeries_Sel.pressed.connect(self._slot_Sel_pressed)
        
        self.LineSeries_Sel = QLineSeries()

        self.ScatterSeries_Non = QScatterSeries()
        self.ScatterSeries_Non.setName('Non-Selective Inversion')
        self.ScatterSeries_Non.setMarkerSize(8)
        self.ScatterSeries_Non.setColor(self.Color_Non)
        self.ScatterSeries_Non.hovered.connect(self._slot_Non_hovered)
        self.ScatterSeries_Non.pressed.connect(self._slot_Non_pressed)

        self.LineSeries_Non = QLineSeries()

        self.addSeries(self.LineSeries_Sel)
        self.addSeries(self.ScatterSeries_Sel)

        self.addSeries(self.LineSeries_Non)
        self.addSeries(self.ScatterSeries_Non)

        self.addSeries(self.ScatterSeries_up)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.markers()[0].setVisible(False)
        legend.markers()[2].setVisible(False)
        legend.markers()[4].setVisible(False)
        
    def _slot_Non_hovered(self, point: QPointF, state: bool):
        idx = self.get_index(point)
        if state:
            self.ScatterSeries_up.clear()
            self.ScatterSeries_up.append(self.xdata[idx], self.non_ydata[idx])

    def _slot_Non_pressed(self, point: QPointF) -> None:
        idx = self.get_index(point)
        self.selected_point.emit(idx)

    def _slot_Non_clicked(self, point: QPointF) -> None:
        idx = np.argwhere(self.xdata == point.x()).squeeze()
        self.selected_point.emit(idx)

    def _slot_Sel_hovered(self, point: QPointF, state: bool):
        idx = self.get_index(point)
        if state:
            self.ScatterSeries_up.clear()
            self.ScatterSeries_up.append(self.xdata[idx], self.sel_ydata[idx])

    def _slot_Sel_pressed(self, point: QPointF) -> None:
        idx = self.get_index(point)
        self.selected_point.emit(idx)

    def _slot_Sel_clicked(self, point: QPointF) -> None:
        idx = np.argwhere(self.xdata == point.x()).squeeze()
        self.selected_point.emit(idx)

    def _slot_update_pointConf(self, rows: list) -> None:
        self._update_all()
        # conf = QXYSeries.PointConfiguration()
        # for row in rows:
        #     self.ScatterSeries.setPointConfiguration(row, conf.Color, self.Model.getColor(row))

    def _update_all(self) -> None:
        self.LineSeries_Sel.clear()
        self.ScatterSeries_Sel.clear()

        self.LineSeries_Non.clear()
        self.ScatterSeries_Non.clear()

        self.ScatterSeries_up.clear()

        conf = QXYSeries.PointConfiguration()
        for x, sel_y, non_y in zip(self.xdata, self.sel_ydata, self.non_ydata):
            self.LineSeries_Sel.append(x, sel_y)
            self.ScatterSeries_Sel.append(x, sel_y)
            self.LineSeries_Non.append(x, non_y)
            self.ScatterSeries_Non.append(x, non_y)


    def get_index(self, point: QPointF) -> int:
        return int(np.argwhere(self.xdata == point.x()).squeeze())

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mousePressEvent(event)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        return super().contextMenuEvent(event)
