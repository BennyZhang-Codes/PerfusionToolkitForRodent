from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
import numpy as np

class MChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.Antialiasing)


    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update()
        return super().resizeEvent(event)
        
    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     print('View press')
    #     return super().mousePressEvent(event)

    # def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    #     print('View release')
    #     return super().mouseReleaseEvent(event)

    # def mouseMoveEvent(self, event: QMouseEvent) -> None:
    #     # print('View Mouse move')
    #     # print(event.pos())
        
    #     # item = self.itemAt(event.pos())
    #     # if isinstance(item, QGraphicsEllipseItem):
    #     #     # item.setBrush(QColor(123,34,99,255))
    #     #     print(item.pos())
    #     return super().mouseMoveEvent(event)

    # def contextMenuEvent(self, event: QContextMenuEvent) -> None:
    #     return super().contextMenuEvent(event)

    # def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    #     print('View double')
    #     return super().mouseDoubleClickEvent(event)

    # def wheelEvent(self, event: QWheelEvent) -> None:
    #     print('View wheel')
    #     return super().wheelEvent(event)


class MPoint(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(parent)


class MChart(QChart):
    selected_point = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTheme(QChart.ChartThemeDark)
        self.legend().hide()
        self.setAnimationOptions(QChart.SeriesAnimations)
        self.setAcceptHoverEvents(True)
        self.init_series()

        self.idx = 0

    def set_data(self, xdata: np.array, ydata: np.array) -> None:
        self.xdata = xdata
        self.ydata = ydata
        self.LineSeries.clear()
        self.ScatterSeries.clear()
        self.ScatterSeries_up.clear()
        for x, y in zip(self.xdata, self.ydata):
            self.ScatterSeries.append(x, y)
            
            self.LineSeries.append(x, y)

        self.createDefaultAxes()
        self.axes(Qt.Horizontal)[0].setRange(-10, xdata.max())
        self.axes(Qt.Vertical)[0].setRange(-10, ydata.max())

    def set_S0(self, s0: np.array) -> None:
        conf = QXYSeries.PointConfiguration()
        for idx in range(len(s0)):
            if s0[idx]:
                self.ScatterSeries.setPointConfiguration(idx, conf.Color, QColor(128, 99,222, 255))

        
    def init_series(self) -> None:
        self.ScatterSeries = QScatterSeries()
        self.ScatterSeries.setMarkerSize(15)
        self.ScatterSeries.hovered.connect(self._slot_hovered)
        self.ScatterSeries.pressed.connect(self._slot_pressed)
        

        self.ScatterSeries_up = QScatterSeries()
        self.ScatterSeries_up.setMarkerSize(20)
        self.ScatterSeries_up.setColor(QColor(12,255,97,255))
        self.ScatterSeries_up.pressed.connect(self._slot_pressed)

        self.LineSeries = QLineSeries()

        self.addSeries(self.LineSeries)
        self.addSeries(self.ScatterSeries)
        self.addSeries(self.ScatterSeries_up)
        

    def _slot_hovered(self, point: QPointF, state: bool):
        idx = self.get_index(point)

        if state:
            self.ScatterSeries_up.clear()
            self.ScatterSeries_up.append(self.xdata[idx], self.ydata[idx])

            # conf = QXYSeries.PointConfiguration()
            # self.ScatterSeries.clearPointConfiguration(self.idx,conf.Color)
            # self.ScatterSeries.clearPointConfiguration(self.idx,conf.Size)
            # self.ScatterSeries.setPointConfiguration(idx, conf.Size, 20)
            # self.ScatterSeries.setPointConfiguration(idx, conf.Color, QColor(128, 99,222, 255))

    def _slot_pressed(self, point: QPointF) -> None:
        idx = self.get_index(point)
        self.selected_point.emit(idx)
        print('pressed', idx)

    def _slot_clicked(self, point: QPointF) -> None:
        idx = np.argwhere(self.xdata == point.x()).squeeze()
        print('clicked', idx)
        self.selected_point.emit(idx)


    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print('chart leave')
        self.ScatterSeries_up.clear()
        return super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('chart press')
        return super().mousePressEvent(event)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        return super().contextMenuEvent(event)

    def get_index(self, point: QPointF) -> int:
        return int(np.argwhere(self.xdata == point.x()).squeeze())