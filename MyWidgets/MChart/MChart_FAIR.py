
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
import numpy as np

from scipy.optimize import curve_fit

class MChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        # self.


    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update()
        return super().resizeEvent(event)

        

class MChart_FAIR(QChart):
    selected_point = Signal(int)
    Color_Focus = QColor(31, 243, 116, 255)
    Color_Non = QColor.fromRgbF(0.921569, 0.533333, 0.090196, 1.000000)
    Color_Sel = QColor.fromRgbF(0.219608, 0.678431, 0.419608, 1.000000)
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
        self.axes(Qt.Vertical)[0].setRange(0, y_max)
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
        self.addSeries(QLineSeries())
        self.addSeries(self.LineSeries_Non)

        self.addSeries(self.ScatterSeries_Sel)
        self.addSeries(self.ScatterSeries_Non)

        self.addSeries(self.ScatterSeries_up)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.markers()[0].setVisible(False)
        legend.markers()[1].setVisible(False)
        legend.markers()[2].setVisible(False)
        legend.markers()[5].setVisible(False)
        
    def _slot_Non_hovered(self, point: QPointF, state: bool):
        idx = self.get_index(point)
        if state:
            self.ScatterSeries_up.clear()
            self.ScatterSeries_up.append(self.xdata[idx], self.non_ydata[idx])

    def _slot_Non_pressed(self, point: QPointF) -> None:
        idx = self.get_index(point)
        self.selectPoint(idx)

    def _slot_Non_clicked(self, point: QPointF) -> None:
        idx = np.argwhere(self.xdata == point.x()).squeeze()
        self.selectPoint(idx)

    def _slot_Sel_hovered(self, point: QPointF, state: bool):
        idx = self.get_index(point)
        if state:
            self.ScatterSeries_up.clear()
            self.ScatterSeries_up.append(self.xdata[idx], self.sel_ydata[idx])

    def _slot_Sel_pressed(self, point: QPointF) -> None:
        idx = self.get_index(point)
        self.selectPoint(idx)

    def _slot_Sel_clicked(self, point: QPointF) -> None:
        idx = np.argwhere(self.xdata == point.x()).squeeze()
        self.selectPoint(idx)

    def _update_all(self) -> None:
        self.LineSeries_Sel.clear()
        self.ScatterSeries_Sel.clear()

        self.LineSeries_Non.clear()
        self.ScatterSeries_Non.clear()

        self.ScatterSeries_up.clear()

        # Msel model
        def Msel_abs(TI: float, T1app: float, M0: float) -> float:
            return np.abs(M0*(1-2*np.exp(-TI/T1app)))

        popt_sel, pcov_sel = curve_fit(Msel_abs, self.xdata, self.sel_ydata, p0=(1500,10000))
        T1app_sel, M0_sel = popt_sel

        popt_sel, pcov_sel = curve_fit(Msel_abs, self.xdata, self.non_ydata, p0=(1500,10000))
        T1app_non, M0_non = popt_sel

        fit_xdata = np.arange(self.xdata[0], self.xdata[-1], 10)
        fit_sel_ydata = Msel_abs(fit_xdata, T1app_sel, M0_sel)
        fit_non_ydata = Msel_abs(fit_xdata, T1app_non, M0_non)
        for x, sel_y, non_y in zip(fit_xdata, fit_sel_ydata, fit_non_ydata):
            self.LineSeries_Sel.append(x, sel_y)
            self.LineSeries_Non.append(x, non_y)

        for x, sel_y, non_y in zip(self.xdata, self.sel_ydata, self.non_ydata):
            # self.LineSeries_Sel.append(x, sel_y)
            self.ScatterSeries_Sel.append(x, sel_y)
            # self.LineSeries_Non.append(x, non_y)
            self.ScatterSeries_Non.append(x, non_y)

    def selectPoint(self, idx: int) -> None:
        self.selected_point.emit(idx+1)

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

    def wheelEvent(self, event: QWheelEvent) -> None:
        pass