from math import sqrt

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from MyWidgets.MGraphicsView.MGraphicsItem import MRoiItem

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
    line_moved = Signal()
    line_remove = Signal(QGraphicsPathItem)
    add_node = Signal(QGraphicsItem)
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

class MPolylItem_Signal(QObject):
    polygon_shape = Signal(QPainterPath)
    drawing = Signal(MRoiItem)
    drawed = Signal()
    item_delete = Signal(QGraphicsItem)
    ROI_color = Signal(QColor)
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

class MLineItem(QGraphicsPathItem, MRoiItem):
    Hover_addnode = 'addNode'
    Hover_move = 'move'
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)  
        self.__init_MRoiItem__()
        self.setup()
        self.hoverEnter = False
        self.setZValue(0)
        self.signal = MLineItem_Signal()
        self._start_node = None
        self._end_node = None
        self._hovermode = self.Hover_addnode
        self.linepath = QPainterPath()

    def setup(self):
        self.init_pen = QPen()
        self.init_pen.setWidthF(2.5)
        self.init_pen.setColor(QColor(49, 200, 10, 255))
        
        self.selected_pen = QPen()
        self.selected_pen.setWidthF(4)
        self.selected_pen.setColor(QColor(20, 216, 230, 255))

        self.point_brush = QBrush()
        self.point_brush.setStyle(Qt.SolidPattern)
        self.point_brush.setColor(QColor(20, 216, 230, 255))
        self.setPen(self.init_pen)

    def update_line(self):
        self.linepath.clear()
        self.setPos(self.startPoint)
        self.linepath.lineTo(self.endPoint)

        self.setBrush(self.point_brush)
        if self.hoverEnter:
            self.setPen(self.selected_pen)
            if self.parentItem().closed:
                if self.HoverMode == self.Hover_addnode:
                    self.linepath.addEllipse(self._point(self.hoverPos), 4,4)
            self.setPath(self.linepath)
        else:
            self.setPen(self.init_pen)
            self.setPath(self.linepath)

    def paint(self, painter: QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        option.state = QtWidgets.QStyle.State_None
        return super().paint(painter, option, widget)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        pos = event.scenePos()
        self._initScenePos = pos
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            if self.HoverMode == self.Hover_addnode:
                self.newPoint = self.mapToScene(self._point(self.hoverPos))
                self.hoverEnter = False
                self.setSelected(self.hoverEnter)
                self.update_line()
                self.signal.add_node.emit(self)
        
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            if self.HoverMode == self.Hover_move:
                x_diff = pos.x() - self.initScenePos.x()
                y_diff = pos.y() - self.initScenePos.y()
                self.initScenePos = pos
                self.signal.line_moved.emit()
                self.update_bothNode(x_diff, y_diff)
            elif self.HoverMode == self.Hover_addnode:
                pass

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = True
        self.setSelected(self.hoverEnter)
        self.signal.line_selected.emit(self.hoverEnter)

    def _point(self, pos: QPointF) -> QPointF:
        length_pos_start = sqrt(pos.x() ** 2 + pos.y() ** 2)
        length_end_start = sqrt(self.endPoint.x() ** 2 + self.endPoint.y() ** 2)
        ratio = length_pos_start / length_end_start
        point = QPointF()
        point.setX(ratio * self.endPoint.x())
        point.setY(ratio * self.endPoint.y())
        return point

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        pos = event.scenePos()
        self.hoverPos = self.mapFromScene(pos)
        self.update_line()
        
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(self.hoverEnter)
        self.update_line()
        self.signal.line_selected.emit(self.hoverEnter)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            self.HoverMode = self.Hover_move
            self.update_line()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        print(event)
        if event.key() == Qt.Key_Control:
            self.HoverMode = self.Hover_addnode
            self.update_line()

    def update_bothNode(self, dx: float, dy: float) -> None:
        self.update_startNode(dx, dy)
        self.update_endNode(dx, dy)
        self.update_line()

    def update_startNode(self, dx: float, dy: float) -> None:
        new_startpoint = QPointF(self.startPoint.x() + dx, self.startPoint.y() + dy)
        self.startNode.setPos(new_startpoint)
        self.startNode.update_prevLine()

    def update_endNode(self, dx: float, dy: float) -> None:
        endPoint = self.endNode.pos()
        new_endpoint = QPointF(endPoint.x() + dx, endPoint.y() + dy)
        self.endNode.setPos(new_endpoint)
        self.endNode.update_nextLine()

    @property
    def HoverMode(self) -> str:
        return self._hovermode
   
    @HoverMode.setter
    def HoverMode(self, mode: str) -> None:
        if mode in [
            self.Hover_addnode,
            self.Hover_move,
        ]:
            self._hovermode = mode
        else:
            raise ValueError('Unsupported HoverMode: {}'.format(mode))

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
        endpoint = QPointF()
        endpoint.setX(self.endNode.pos().x() - self.startPoint.x())
        endpoint.setY(self.endNode.pos().y() - self.startPoint.y())
        return endpoint

    @property
    def startNode(self):
        return self._start_node

    @startNode.setter
    def startNode(self, node):
        self._start_node = node

    @property
    def endNode(self):
        return self._end_node

    @endNode.setter
    def endNode(self, node):
        self._end_node = node


class MNodeItem(QGraphicsPathItem, MRoiItem):
    name = 'node'

    DEFAULT_COLOR = QColor(31, 243, 116, 255)
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
        self._delete = False

    def setup(self):
        self.init_pen = QPen()
        self.init_pen.setWidthF(0)
        self.init_pen.setColor(self.DEFAULT_COLOR)
        
        self.init_brush = QBrush()
        self.init_brush.setStyle(Qt.SolidPattern)
        self.init_brush.setColor(self.DEFAULT_COLOR)

        self.init_path = QPainterPath()
        self.init_path.addEllipse(-4,-4,8,8)

        self.selected_pen = QPen()
        self.selected_pen.setWidthF(3.5)
        self.selected_pen.setColor(self.DEFAULT_COLOR)
        
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
        option.state = QtWidgets.QStyle.State_None
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
            self.update_bothLine()
            self.signal.node_moved.emit()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = True
        self.setSelected(self.hoverEnter)
        self.signal.node_selected.emit(self.hoverEnter)
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.update()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hoverEnter = False
        self.setSelected(self.hoverEnter)
        self.signal.node_selected.emit(self.hoverEnter)
        return super().hoverLeaveEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            self.Delete = True

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            if self.Delete:
                self.remove()

    def remove(self):
        self.signal.node_remove.emit(self)

    def update_bothLine(self) -> None:
        self.update_prevLine()
        self.update_nextLine()

    def update_prevLine(self) -> None:
        if self.prevLine:
            self.prevLine.update_line()

    def update_nextLine(self) -> None:
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
    
    @property
    def Delete(self) -> bool:
        return self._delete

    @Delete.setter
    def Delete(self, delete: bool) -> None:
        self._delete = delete


class MGraphicsPolygonItem(QGraphicsPathItem, MRoiItem):
    DEFAULT_COLOR = QColor(118,185,172,128)
    def __init__(self, parent) -> None:
        super().__init__()  
        self.__init_MRoiItem__(parent)
        self.signal = MPolylItem_Signal()
        self.poly_path = QPainterPath()
        self.prev_node = MNodeItem()
        self.curr_node = MNodeItem()
        self.next_node = MNodeItem()
        self.head_node = MNodeItem()
        self.tail_node = MNodeItem()
        self._drawed = False
        self._closed = False
        self._delete = False

        # self.setup_menu()
        # self.mouseTrackNode = None

    def setMouseTrack(self, track: bool):
        if track:
            self.mouseTrackNode = self.NewNode
            self.mouseTrackNode.setAcceptHoverEvents(False)
            self.mouseTrackNode.setZValue(2)
            
            self.mouseTrackLine = self.NewLine
            self.mouseTrackLine.setZValue(2)
            self.mouseTrackLine.setAcceptHoverEvents(False)

            self.mouseTrackLine.endNode = self.mouseTrackNode
            # self.mouseTrackLine.startNode = self.tail_node
            self.mouseTrackNode.prevLine = self.mouseTrackLine
        # else:
        #     self.mouseTrackLine = None
        #     self.mouseTrackNode = None

    def add_node(self, pos: QPointF):
        node = self.NewNode
        node.setPos(pos)
        if self.nodesNum == 0:
            self.head_node.nextNode = node
        else:
            line = self.NewLine

            line.startNode = self.tail_node.nextNode
            line.endNode = node
            line.update_line()

            self.tail_node.nextNode.nextLine = line
            node.prevLine = line
            self.tail_node.nextNode.nextNode = node
            node.prevNode = self.tail_node.nextNode
        self.tail_node.nextNode = node

        # self.mouseTrackLine.startNode = self.tail_node.nextNode

        self.update()
            
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        polygon_pos = self.mapFromScene(pos)

        if not self.closed:
            if self.head_node.nextNode is None:
                self.add_node(polygon_pos.toPoint())
            else:
                if self.head_node.nextNode.contains(self.head_node.nextNode.mapFromScene(pos)):
                    self.close()
                else: 
                    self.add_node(polygon_pos.toPoint())
        self._initScenePos = pos

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()

        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            if self.closed:
                x_diff = pos.x() - self.initScenePos.x()
                y_diff = pos.y() - self.initScenePos.y()
                self.setX(self.x() + x_diff)
                self.setY(self.y() + y_diff)
                self.initScenePos = pos


        # self.mouseTrackNode.setPos(self.mapFromScene(pos))
        # self.mouseTrackNode.update_prevLine()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.closed:
            self.signal.polygon_shape.emit(self.mapToScene(self.shape()))
        return super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pass
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverLeaveEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Return:
            self.close()


    def _slot_node_selected(self, selected: bool) -> None:
        if selected:
            self.setSelected(False)
        else:
            self.setSelected(self.hoverEnter)

    def _slot_node_moved(self):
        self.update()

    def _slot_node_remove(self, node: MNodeItem) -> None:
        if node == self.tail_node.nextNode:
            self.tail_node.nextNode = node.prevNode
        elif node == self.head_node.nextNode:
            self.head_node.nextNode = node.nextNode
        node.prevLine.endNode = node.nextNode
        node.nextLine.startNode = node.prevNode
        node.nextNode.prevLine = node.prevLine
        node.prevNode.nextNode = node.nextNode
        node.nextNode.prevNode = node.prevNode

        node.prevLine.update_line()
        self.scene().removeItem(node.nextLine)
        self.scene().removeItem(node)

    def _slot_line_selected(self, selected: bool) -> None:
        if selected:
            self.setSelected(False)
        else:
            self.setSelected(self.hoverEnter)
    
    def _slot_line_moved(self) -> None:
        self.update()

    def _slot_line_add_node(self, line: MLineItem) -> None:
        newnode = self.NewNode
        newline = self.NewLine
        newnode.nextNode = line.endNode
        newnode.nextLine = newline
        newnode.prevNode = line.startNode
        newnode.prevLine = line

        newline.startNode = newnode
        newline.endNode = line.endNode

        line.endNode.prevNode = newnode
        line.endNode.prevLine = newline

        line.startNode.nextNode = newnode
        line.endNode = newnode

        newnode.setPos(self.mapFromScene(line.newPoint))
        newnode.update_bothLine()
        newnode.initScenePos = line.newPoint
        newnode.hoverEnter = True
        newnode.setSelected(self.hoverEnter)

        self.head_node.nextNode = newnode
        self.tail_node.nextNode = newnode.prevNode

        self.update()

    def close(self):
        start_node = self.tail_node.nextNode
        end_node = self.head_node.nextNode
        
        start_node.nextNode = end_node
        end_node.prevNode = start_node

        line = self.NewLine

        line.startNode = start_node
        line.endNode = end_node
        
        start_node.nextLine = line
        end_node.prevLine = line

        line.update_line()

        self.closed = True
        self.Drawed = True
        self.signal.drawed.emit()
        self.update()

    @property
    def NewNode(self) -> MNodeItem:
        node = MNodeItem()
        node.signal.node_selected.connect(self._slot_node_selected)
        node.signal.node_moved.connect(self._slot_node_moved)
        node.signal.node_remove.connect(self._slot_node_remove)
        self.scene().addItem(node)
        node.setParentItem(self)

        return node

    @property
    def NewLine(self) -> MLineItem:
        line = MLineItem()
        self.scene().addItem(line)
        line.setParentItem(self)
        line.signal.line_selected.connect(self._slot_line_selected)
        line.signal.line_moved.connect(self._slot_line_moved)
        line.signal.add_node.connect(self._slot_line_add_node)
        return line

    @property
    def initScenePos(self) -> QPointF:
        return self._initScenePos

    @initScenePos.setter
    def initScenePos(self, pos: QPointF) -> None:
        self._initScenePos = pos

    @property 
    def closed(self) -> bool:
        return self._closed

    @closed.setter
    def closed(self, close: bool) -> None:
        self._closed = close

    @property
    def nodesNum(self) -> int:
        node = self.head_node.nextNode
        num = 0
        while True:
            if node is None:
                break
            else:
                num = num + 1
                node = node.nextNode
                if node == self.tail_node.nextNode:
                    num = num + 1
                    break
        return num

    @property
    def Drawed(self) -> bool:
        return self._drawed

    @Drawed.setter
    def Drawed(self, drawed: bool) -> None:
        self._drawed = drawed

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        self.menu.exec_(QCursor.pos())

    def __action_color(self) -> None:
        cd = self.ColorDialog
        cd.setMouseTracking(False)
        cd.setCurrentColor(self.brush().color())
        cd.setOption(cd.ShowAlphaChannel)
        cd.setOption(cd.DontUseNativeDialog)
        cd.exec()
        color = cd.selectedColor()
        self.DEFAULT_COLOR = color

        self.signal.ROI_color.emit(color)

        self.update()

    def __action_delete(self) -> None:
        self.signal.item_delete.emit(self)

    def paint(self, painter: QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        option.state = QtWidgets.QStyle.State_None
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        pen.setWidthF(0)
        self.setPen(pen)

        brush = self.brush()
        if self.closed:
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            brush.setColor(self.DEFAULT_COLOR)
            self.setBrush(brush)
        else:
            brush.setStyle(Qt.BrushStyle.NoBrush)
            self.setBrush(brush)

        self.__update_nodes()
        self.setPath(self.poly_path)
        return super().paint(painter, option, widget)

    def __update_nodes(self):
        self.poly_path.clear()
        poly = QPolygonF()
        node = self.head_node.nextNode
        for idx in range(self.nodesNum):
            poly.append(node.pos().toPoint())
            node = node.nextNode

        self.poly_path.addPolygon(poly)



    def setup_menu(self) -> None:
        menu = self.menu
        action_color = menu.addAction('Color')
        action_color.triggered.connect(self.__action_color)
        action_delete = menu.addAction('Delete')
        action_delete.triggered.connect(self.__action_delete)