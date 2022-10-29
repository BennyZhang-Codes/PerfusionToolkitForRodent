from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *

class MChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
    def mousePressEvent(self, event: QMouseEvent) -> None:
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # print(event.pos())
        
        # item = self.itemAt(event.pos())
        # if isinstance(item, QGraphicsEllipseItem):
        #     # item.setBrush(QColor(123,34,99,255))
        #     print(item.pos())
        return super().mouseMoveEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        return super().contextMenuEvent(event)


class MPoint(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(parent)


class MChart(QChart):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print('enter')
        self.series()[0].event(event)
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print('move')
        return super().hoverMoveEvent(event)
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print('leave')
        return super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('press')
        return super().mousePressEvent(event)
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('mouse move')
        return super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('release')
        return super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('double click')
        return super().mouseDoubleClickEvent(event)

    def addSeries(self, series: QAbstractSeries) -> None:
        return super().addSeries(series)

class MLineSeries(QLineSeries):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        
    def event(self, event: QEvent) -> bool:
        print(event)
        return super().event(event)

    def _slot(self, idx: int):
        self.setSelectedColor(QColor(123,22,155,255))
        self.selectPoint(idx)