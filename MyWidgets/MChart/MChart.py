from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *

class MChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # print(event.pos())
        
        item = self.itemAt(event.pos())
        print(item.parentItem())
        if isinstance(item, QGraphicsEllipseItem):
            item.setBrush(QColor(123,34,99,255))
        return super().mouseMoveEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        return super().contextMenuEvent(event)


class MPoint(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(parent)


class MChart(QChart):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mousePressEvent(event)

    def addSeries(self, series: QAbstractSeries) -> None:
        # if isinstance(series, QLineSeries):
        #     for point in series.points():
        #         print(456)
        #         p = MPoint()
        #         p.setPos(point)
        #         p.setRect(-3,-3,6,6)
        #         p.setParentItem(self)
        #         p.setBrush(QColor(123,45,78,255))
        #         self.scene().addItem(p)

        return super().addSeries(series)

class MLineSeries(QLineSeries):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
    def event(self, event: QEvent) -> bool:
        print(event)
        return super().event(event)