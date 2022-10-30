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
    Color_Focus = QColor(31, 243, 116, 255)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTheme(QChart.ChartThemeDark)
        self.legend().hide()
        self.setAnimationOptions(QChart.SeriesAnimations)
        self.setAcceptHoverEvents(True)
        self.init_series()

    def setModel(self, model: TimePointsTableModel) -> None:
        self._model = model
        self.xdata = self._model.TimePoints
        self.ydata = self._model.SignalValue
    
        self._update_all()

        self.createDefaultAxes()
        self.axes(Qt.Horizontal)[0].setRange(self.xdata.min()*0.9, self.xdata.max()*1.1)
        self.axes(Qt.Vertical)[0].setRange(self.ydata.min()*0.9, self.ydata.max()*1.1)

    def init_series(self) -> None:
        self.ScatterSeries = QScatterSeries()
        self.ScatterSeries.setMarkerSize(8)
        self.ScatterSeries.hovered.connect(self._slot_hovered)
        self.ScatterSeries.pressed.connect(self._slot_pressed)
        
        self.ScatterSeries_up = QScatterSeries()
        self.ScatterSeries_up.setMarkerSize(12)
        self.ScatterSeries_up.setColor(self.Color_Focus)
        self.ScatterSeries_up.pressed.connect(self._slot_pressed)

        self.LineSeries = QLineSeries()

        self.addSeries(self.LineSeries)
        self.addSeries(self.ScatterSeries)
        self.addSeries(self.ScatterSeries_up)
        
    def _slot_hovered(self, point: QPointF, state: bool):
        idx = self.get_index(point)
        if state:
            self._update_focus_point(idx)

    def _update_focus_point(self, idx: int) -> None:
        self.ScatterSeries_up.clear()
        self.ScatterSeries_up.append(self.xdata[idx], self.ydata[idx])

    def _slot_pressed(self, point: QPointF) -> None:
        idx = self.get_index(point)
        self.selected_point.emit(idx)

    def _slot_clicked(self, point: QPointF) -> None:
        idx = np.argwhere(self.xdata == point.x()).squeeze()
        self.selected_point.emit(idx)

    def _slot_update_pointConf(self, rows: list) -> None:
        self._update_all()
        # conf = QXYSeries.PointConfiguration()
        # for row in rows:
        #     self.ScatterSeries.setPointConfiguration(row, conf.Color, self.Model.getColor(row))

    def _update_all(self) -> None:
        self.LineSeries.clear()
        self.ScatterSeries.clear()
        self.ScatterSeries_up.clear()
        conf = QXYSeries.PointConfiguration()
        for idx in range(len(self.xdata)):
            x = self.xdata[idx]
            y = self.ydata[idx]
            c = bool(self.Model.Contained[idx])
            if c:
                self.LineSeries.append(x, y)
            self.ScatterSeries.append(x, y)
            self.ScatterSeries.setPointConfiguration(idx, conf.Color, self.Model.getColor(idx))
            self.ScatterSeries.setPointConfiguration(idx, conf.Visibility, c)


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

    @property
    def Model(self) -> TimePointsTableModel:
        return self._model