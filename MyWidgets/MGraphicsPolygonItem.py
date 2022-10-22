import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal, QLine, QObject, QRectF
from PySide6.QtGui import QImage, QPixmap, QIcon, QResizeEvent, QMouseEvent, QCursor, QColor, QWheelEvent
from PySide6.QtGui import QPainter, QPainterPath, QPen, QPolygon, QPolygonF, QBrush, QTransform

from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsSceneMoveEvent, QGraphicsSceneWheelEvent, QGraphicsSceneHoverEvent
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMenu, QScrollBar, QColorDialog
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsPixmapItem
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem
from PySide6.QtWidgets import QGraphicsSceneContextMenuEvent
from pyparsing import line

from MyWidgets.MGraphicsItem import MRoiItem

class MNodeItem_Signal(QObject):
    item_delete = Signal(QGraphicsItem)
    node_selected = Signal(bool)
    node_moved = Signal()
    node_remove = Signal(QGraphicsPathItem)
    def __init__(self) -> None:
        super().__init__()

class MLineItem_Signal(QObject):
    item_delete = Signal(QGraphicsItem)
    line_selected = Signal(bool)
    line_moved = Signal(QPointF)
    line_remove = Signal(QGraphicsPathItem)
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

class MPolylItem_Signal(QObject):
    polygon_shape = Signal(QPainterPath)
    drawing = Signal(MRoiItem)
    drawed = Signal()
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

class MLineItem(QGraphicsPathItem, MRoiItem):
    signal = MLineItem_Signal()
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.__init_MRoiItem__()
        self.setup()
        self.hoverEnter = False
        self.setZValue(0)

        self._start_node = None
        self._end_node = None
        self.linepath = QPainterPath()

    def update_line(self):
        self.linepath.clear()
        self.linepath.moveTo(self.startPoint)
        self.linepath.lineTo(self.endPoint)
        # self.update()

    def setup(self):
        self.init_pen = QPen()
        self.init_pen.setWidthF(3)
        self.init_pen.setColor(QColor(49, 200, 10, 255))
        
        self.selected_pen = QPen()
        self.selected_pen.setWidthF(5)
        self.selected_pen.setColor(QColor(20, 216, 230, 255))
        self.setPen(self.init_pen)

    def paint(self, painter: QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        if self.hoverEnter:
            self.setPen(self.selected_pen)
            self.setPath(self.linepath)
        else:
            self.setPen(self.init_pen)
            self.setPath(self.linepath)
        return super().paint(painter, option, widget)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        pos = event.scenePos()
        self._initScenePos = pos
        
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pass
        # pos = event.scenePos()
        # if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
        #     x_diff = pos.x() - self.initScenePos.x()
        #     y_diff = pos.y() - self.initScenePos.y()
        #     self.setX(self.x() + x_diff)
        #     self.setY(self.y() + y_diff)
        #     self.initScenePos = pos
        #     self.signal.line_moved.emit(pos)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = True
        self.setSelected(self.hoverEnter)
        self.signal.line_selected.emit(self.hoverEnter)

        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.update()
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(self.hoverEnter)
        self.signal.line_selected.emit(self.hoverEnter)
        return super().hoverLeaveEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.signal.line_remove.emit(self)
        return super().mouseDoubleClickEvent(event)

    def sceneEvent(self, event: QEvent) -> bool:
        return super().sceneEvent(event)

    @property
    def initScenePos(self) -> QPointF:
        return self._initScenePos

    @initScenePos.setter
    def initScenePos(self, pos: QPointF) -> None:
        self._initScenePos = pos

    @property
    def startPoint(self) -> QPointF:
        return self.startNode.pos()

    @property
    def endPoint(self) -> QPointF:
        return self.endNode.pos()

    @property
    def startNode(self):
        return self._start_node

    @startNode.setter
    def startNode(self, node):
        # node.signal.node_moved.connect(self.update_line)
        self._start_node = node

    @property
    def endNode(self):
        return self._end_node

    @endNode.setter
    def endNode(self, node):
        # node.signal.node_moved.connect(self.update_line)
        self._end_node = node

class MNodeItem(QGraphicsPathItem, MRoiItem):
    name = 'node'
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.__init_MRoiItem__()
        self.setup()
        self.setZValue(1)
        self.hoverEnter = False
        self._next_node = None
        self._prev_node = None
        self._next_Line = None
        self._prev_Line = None
        self.signal = MNodeItem_Signal()

    def setup(self):
        self.init_pen = QPen()
        self.init_pen.setWidthF(0)
        self.init_pen.setColor(QColor(23, 178, 90, 255))
        
        self.init_brush = QBrush()
        self.init_brush.setStyle(Qt.SolidPattern)
        self.init_brush.setColor(QColor(23, 178, 90, 255))

        self.init_path = QPainterPath()
        self.init_path.addEllipse(-4,-4,8,8)

        self.selected_pen = QPen()
        self.selected_pen.setWidthF(3)
        self.selected_pen.setColor(QColor(23, 178, 90, 255))
        
        self.selected_brush = QBrush()
        self.selected_brush.setStyle(Qt.SolidPattern)
        self.selected_brush.setColor(QColor(255, 255, 255, 255))

        self.selected_path = QPainterPath()
        self.selected_path.addEllipse(-8,-8,16,16)

        self.setBrush(self.init_brush)
        self.setPen(self.init_pen)
        self.setPath(self.init_path)
   
    def paint(self, painter: QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        if self.hoverEnter:
            self.setBrush(self.selected_brush)
            self.setPen(self.selected_pen)
            self.setPath(self.selected_path)
        else:
            self.setBrush(self.init_brush)
            self.setPen(self.init_pen)
            self.setPath(self.init_path)
        return super().paint(painter, option, widget)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        pos = event.scenePos()
        self._initScenePos = pos
        
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> tuple:
        pos = event.scenePos()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            x_diff = pos.x() - self.initScenePos.x()
            y_diff = pos.y() - self.initScenePos.y()
            self.setX(self.x() + x_diff)
            self.setY(self.y() + y_diff)
            self.initScenePos = pos
            self.update_line()
            self.signal.node_moved.emit()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = True
        self.setSelected(self.hoverEnter)
        # self.prevNode.setSelected(self.hoverEnter)
        # self.nextNode.setSelected(self.hoverEnter)
        self.setSelected(self.hoverEnter)
        self.signal.node_selected.emit(self.hoverEnter)

        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.update()
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(self.hoverEnter)
        # self.prevNode.setSelected(self.hoverEnter)
        # self.nextNode.setSelected(self.hoverEnter)

        self.signal.node_selected.emit(self.hoverEnter)
        return super().hoverLeaveEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.remove()
        # self.signal.node_remove.emit(self)

    def sceneEvent(self, event: QEvent) -> bool:
        return super().sceneEvent(event)


    def remove(self):
        # print(self.prevNode)
        # print(self.nextNode)
        self.prevLine.endNode = self.nextNode
        self.nextLine.startNode = self.prevNode
        self.nextNode.prevLine = self.prevLine
        self.prevLine.update_line()

        # 删除当前node和next line

    def update_line(self):
        if self.prevLine:
            self.prevLine.update_line()
        if self.nextLine:
            self.nextLine.update_line()

    @property
    def initScenePos(self) -> QPointF:
        return self._initScenePos

    @initScenePos.setter
    def initScenePos(self, pos: QPointF) -> None:
        self._initScenePos = pos

    @property
    def nextNode(self):
        return self._next_node

    @nextNode.setter
    def nextNode(self, node):
        self._next_node = node

    @property
    def prevNode(self):
        return self._prev_node

    @prevNode.setter
    def prevNode(self, node):
        self._prev_node = node

    @property
    def nextLine(self):
        return self._next_Line

    @nextLine.setter
    def nextLine(self, Line):
        self._next_Line = Line

    @property
    def prevLine(self):
        return self._prev_Line

    @prevLine.setter
    def prevLine(self, Line):
        self._prev_Line = Line
    
class MGraphicsPolygonItem(QGraphicsPathItem, MRoiItem):
    signal = MPolylItem_Signal()
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.__init_MRoiItem__()
        self.poly_path = QPainterPath()
        self.prev_node = MNodeItem()
        self.curr_node = MNodeItem()
        self.next_node = MNodeItem()
        self.head_node = MNodeItem()
        self.tail_node = MNodeItem()

        self._drawed = False

    def add_node(self, pos: QPoint):
        node = MNodeItem()
        node.signal.node_selected.connect(self._slot_node_selected)
        node.signal.node_moved.connect(self._slot_node_move)
        node.signal.node_remove.connect(self._slot_node_remove)
        node.setParentItem(self)
        node.setPos(pos)
        if self.nodesNum == 0:
            self.head_node.nextNode = node
        else:
            line = MLineItem()
            line.setParentItem(self)
            line.signal.line_selected.connect(self._slot_line_selected)

            line.startNode = self.tail_node.nextNode
            line.endNode = node
            line.update_line()

            self.tail_node.nextNode.nextLine = line
            node.prevLine = line
            self.tail_node.nextNode.nextNode = node
            node.prevNode = self.tail_node.nextNode
        self.tail_node.nextNode = node
        self.update_nodes()
            
    def del_node(self):
        pass

    def line_move(self):
        pass

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        polygon_pos = self.mapFromScene(pos)
        if not self.Drawed:
            self.add_node(polygon_pos.toPoint())
        self._initScenePos = pos

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            x_diff = pos.x() - self.initScenePos.x()
            y_diff = pos.y() - self.initScenePos.y()
            self.setX(self.x() + x_diff)
            self.setY(self.y() + y_diff)
            self.initScenePos = pos

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.signal.polygon_shape.emit(self.mapToScene(self.shape()))
        return super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.Drawed = not self.Drawed
        # self.close()

        print(self.closed)
        if self.Drawed:
            self.signal.drawed.emit()
        else:
            self.signal.drawing.emit(self)
        
        return super().mouseDoubleClickEvent(event)
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = True
        self.setSelected(True)
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.update()
        # print('move')
        # for item in self.childItems():
        #     pos = item.mapFromParent(self.mapFromScene(event.scenePos()))
        #     item.contains(pos)
        # print(self.contains(event.scenePos()))
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(False)
        # print('leave')
        return super().hoverLeaveEvent(event)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        # angle = event.delta()
        # value = int(angle//120)

        # bef_scale = self.scale()
        # cur_scale = bef_scale + 0.1 * value
        # rect = self.boundingRect()
        # bef_pos = self.pos()
        # cursor_pos = event.scenePos()
        # cursor_pos_x = cursor_pos.x()
        # cursor_pos_y = cursor_pos.y()
        # ratio_x = (cursor_pos_x - bef_pos.x())/(rect.width()*bef_scale)
        # ratio_y = (cursor_pos_y - bef_pos.y())/(rect.height()*bef_scale)
        # aft_cursor_pos_x = bef_pos.x() + ratio_x * (rect.width()*cur_scale)
        # aft_cursor_pos_y = bef_pos.y() + ratio_y * (rect.height()*cur_scale)
        # self.setScale(cur_scale)
        # self.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
        # self.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))
        return super().wheelEvent(event)
    
    def sceneEvent(self, event: QEvent) -> bool:
        return super().sceneEvent(event)
    
    def _slot_node_selected(self, selected: bool) -> None:
        if selected:
            self.setSelected(False)
        else:
            self.setSelected(self.hoverEnter)

    def _slot_line_selected(self, selected: bool) -> None:
        if selected:
            self.setSelected(False)
        else:
            self.setSelected(self.hoverEnter)
    
    def _slot_node_move(self):
        self.update_nodes()

    def _slot_node_remove(self, node: MNodeItem) -> None:
        # if node == self.tail_node.nextNode:
        #     pass

        print('///')
        # print(node)
        # print(node.prevLine)
        # print(node.prevLine.startNode)
        # print(node.prevLine.endNode)

        # print(node.nextLine)
        # print(node.nextLine.startNode)
        # print(node.nextLine.endNode)
        # print(self.tail_node.nextNode)

        # print(node.prevLine.endNode)
        # print(node.nextNode)
        # node.prevLine.endNode = node.nextNode
        # node.prevLine.update_line()

        # print(node.prevLine.endNode)
        

        # node.prevNode.nextNode = node.nextNode
        # node.nextNode.prevNode = node.prevNode

        # self.scene().removeItem(node.nextLine)
        # self.scene().removeItem(node)

        # self.update_nodes()

    def update_nodes(self):
        self.poly_path.clear()
        poly = QPolygonF()
        head_node = self.head_node.nextNode

        while True:
            point = head_node.pos()
            poly.append(QPoint(int(point.x()), int(point.y())))
            if head_node.nextNode is None:
                break
            else:
                head_node = head_node.nextNode

        self.poly_path.addPolygon(poly)

    def close(self):


        start_node = self.head_node.nextNode
        end_node = self.tail_node.nextNode
        

        start_node.prevNode = end_node
        end_node.nextNode = start_node

        line = MLineItem()
        line.setParentItem(self)
        line.signal.line_selected.connect(self._slot_line_selected)

        line.startNode = start_node
        line.endNode = end_node
        line.update_line()

        start_node.prevLine = line
        end_node.nextLine = line

        self.tail_node.nextNode = self.head_node.nextNode





    @property
    def initScenePos(self) -> QPointF:
        return self._initScenePos

    @initScenePos.setter
    def initScenePos(self, pos: QPointF) -> None:
        self._initScenePos = pos

    @property 
    def closed(self) -> bool:
        return self.head_node.nextNode == self.tail_node.nextNode

    @property
    def nodesNum(self) -> int:
        if self.head_node.nextNode is None:
            num = 0
        else:
            node = self.head_node.nextNode
            num = 1

            while True:
                if node.nextNode is None:
                    break
                else:
                    num = num + 1
                    node = node.nextNode
        return num

    @property
    def Drawed(self) -> bool:
        return self._drawed

    @Drawed.setter
    def Drawed(self, drawed: bool) -> None:
        self._drawed = drawed


    def paint(self, painter: QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = self.pen()
        pen.setWidthF(0)
        self.setPen(pen)
        if self.hoverEnter:
            # self.setBrush(self.selected_brush)
            # self.setPen(self.selected_pen)

            self.setPath(self.poly_path)
        else:
            # self.setBrush(self.init_brush)
            # self.setPen(self.init_pen)
            self.setPath(self.poly_path)
        return super().paint(painter, option, widget)
