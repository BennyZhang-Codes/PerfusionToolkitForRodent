import numpy as np
from PIL import Image
from pydicom import FileDataset
import matplotlib.pyplot as plt
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from MyWidgets.MGraphicsView.MGraphicsPixmapItem import MGraphicsPixmapItem
from MyWidgets.MGraphicsView.MGraphicsItemGroup import MGraphicsItemGroup
from MyWidgets.MGraphicsView.MGraphicsItem import MGraphicsItem, MRoiItem
from MyWidgets.MGraphicsView.MGraphicsPolygonItem import MGraphicsPolygonItem
from MyWidgets.MGraphicsView.MGraphicsEllipseItem import MGraphicsEllipseItem
from MyWidgets.MGraphicsView.MGraphicsTextItem import MGraphicsTextItem
from modules.dcmreader.read_Dicom import MAbstractDicomReader
from modules.utils.shape import shape_to_mask, get_index_of_mask

class MGraphicsScene(QGraphicsScene):
    ItemType_roi = 'roi'
    ItemType_image = 'image'
    ItemType_info = 'info'
    SceneMode_roi = 'roi'
    SceneMode_image = 'image'
    signal_ROI = Signal(tuple)  # mask np.array  index np.array
    signal_ROI_point = Signal(QPoint)
    signal_ROI_color = Signal(QColor)
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.setup()
        self.__SceneMode = 'image'
        self.__InfoHide = False
        self.__func = 'window'
        self.__roi_type = None
        self.__roi_added = False
        self.__drawing_roi = None

        self.__row = 0
        self.__column = 0
        self.ROI = []

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        point = self.item_img.maptoPixmap(pos)
        if self.drawing:
            self.drawingRoi.mousePressEvent(event)
        else:
            if not self.ROI_added:
                if self.ROI_type == 'ellipse':
                    self.add_Mellipse(pos)
                    self.ROI_added = True
                # if self.ROI_type == 'polygon':
                #     self.add_Mpolygon(pos)
                #     self.ROI_added = True


            if self.SceneMode == self.SceneMode_roi:
                items = self.selectedItems()
                if items:
                    items[0].mousePressEvent(event)
            else:
                self.item_img.func = self.func
                self.item_img.mousePressEvent(event)
                if self.func == 'point':
                    self.signal_ROI_point.emit(point)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)  # hover
        pos = event.scenePos()
        point = self.item_img.maptoPixmap(pos)
        self.column = point
        self.row = point
        self._update_item_info_LeftBottom()

        if self.drawing:
            self.drawingRoi.mouseMoveEvent(event)
        else:
            items = self.selectedItems()
            if items:
                items[0].mouseMoveEvent(event)
                self.SceneMode = self.SceneMode_roi
            else:
                self.SceneMode = self.SceneMode_image
                self.item_img.func = self.func
                self.item_img.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.drawing:
            self.drawingRoi.mouseReleaseEvent(event)
        else:
            if self.SceneMode == self.SceneMode_roi:
                items = self.selectedItems()
                if items:
                    items[0].mouseReleaseEvent(event)
            else:
                self.item_img.func = self.func
                self.item_img.mouseReleaseEvent(event)

    def resizeevent(self) -> None:
        self.InfoHide = self.InfoHide

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        if self.SceneMode == self.SceneMode_roi:
            items = self.selectedItems()
            if items:
                items[0].wheelEvent(event)
        else:
            self.item_img.func == self.func
            self.item_img.wheelEvent(event)
            self._update_item_info_LeftBottom()

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.drawing:
            self.drawingRoi.mouseDoubleClickEvent(event)
        else:
            if self.SceneMode == self.SceneMode_roi:
                items = self.selectedItems()
                if items:
                    items[0].mouseDoubleClickEvent(event)
            else:
                self.item_img.func == self.func
                self.item_img.mouseDoubleClickEvent(event)
                self._update_item_info_LeftBottom()


        # if self.func == 'point':
        #     super().mouseDoubleClickEvent(event)
        # else:
        #     self.set_scene(self.ds)
        return super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.drawing:
            self.drawingRoi.keyPressEvent(event)
        else:
            if self.SceneMode == self.SceneMode_roi:
                items = self.selectedItems()
                if items:
                    items[0].keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.drawing:
            self.drawingRoi.keyReleaseEvent(event)
        else:
            if self.SceneMode == self.SceneMode_roi:
                items = self.selectedItems()
                if items:
                    items[0].keyReleaseEvent(event)

    def add_Mellipse(self, pos: QPointF) -> MGraphicsEllipseItem:
        ellipse = MGraphicsEllipseItem(self.parent())

        ellipse.setPos(pos)
        ellipse.setZValue(1)

        ellipse.signal.ellipse_shape.connect(self.__slot_roi_shape)
        ellipse.signal.item_delete.connect(self.__slot_roi_delete)
        self.__add_roi(ellipse)
        return ellipse

    def __add_roi(self, item: MRoiItem):
        self.addItem(item)
        self.ROI.append(item)

    def __slot_roi_shape(self, painterpath: QPainterPath): 
        w = self.item_img.pixmap().width()
        h = self.item_img.pixmap().height()
        path = self.item_img.mapFromScene(painterpath)
        pix = QPixmap(w, h)
        pix.fill(QColor(0,0,0,0))

        painter = QPainter(pix)
        pen = QPen()
        pen.setWidthF(0)
        pen.setColor(QColor(0,0,0,0))
        painter.setPen(pen)
        painter.setBrush(QColor(0,255,255,100))
        painter.drawPath(path)
        painter.end()
        # self.mask.setPixmap(pix)

        # img = pix.toImage()
        # b = img.bits()
        # img_array = np.frombuffer(b, np.uint8).reshape((h, w, 4))
        # mask = img_array[:,:,-1].astype(bool)
        # plt.imsave('mask.jpg', mask)

        # index = get_index_of_mask(mask)
        self.signal_ROI.emit((path, self.item_img.pixmap()))
    
    def __slot_roi_delete(self, item: QGraphicsItem):
        self.removeItem(item)

    def add_Mpolygon(self) -> MGraphicsPolygonItem: 
        polygon = MGraphicsPolygonItem(self.parent())
        # polygon.setPen(QPen(QColor(0,0,255,255), 1, Qt.SolidLine))
        # polygon.setBrush(QColor(255,0,0,255))
        polygon.setZValue(1)
        polygon.signal.drawing.connect(self.__slot_drawing)
        polygon.signal.drawed.connect(self.__slot_drawed)
        polygon.signal.polygon_shape.connect(self.__slot_roi_shape)
        polygon.signal.item_delete.connect(self.__slot_roi_delete)
        polygon.signal.ROI_color.connect(self.__slot_roi_color)
        self.__add_roi(polygon)
        polygon.signal.drawing.emit(polygon)
        return polygon

    def __slot_roi_color(self, color: QColor) ->None:
        self.signal_ROI_color.emit(color)
        
    def __slot_drawing(self, roi: MRoiItem) ->None:
        self.drawingRoi = roi

    def __slot_drawed(self):
        self.drawingRoi = None

    def itemAt(self, pos: QPointF, deviceTransform: QTransform) -> MGraphicsItem:
        return super().itemAt(pos, deviceTransform)
    
    def selectedItems(self) -> list[MGraphicsItem]:
        return super().selectedItems()

    @property
    def func(self) -> str:
        return self.__func

    @func.setter
    def func(self, func: str) -> None:
        if func in [
            'window',
            'series',
            'move',
            'zoom',
            'roi',
            'info',
            'point',
        ]:
            self.__func = func
        else:
            raise ValueError('Unsupported func: {}'.format(func))

    @property
    def row(self) -> int:
        return self.__row

    @row.setter
    def row(self, point: QPoint) -> None:
        self.__row = point.y()

    @property
    def column(self) -> int:
        return self.__column

    @column.setter
    def column(self, point: QPoint) -> None:
        self.__column = point.x()

    @property 
    def SizeTooSmall(self) -> bool:
        return self.height() < 170 or self.width() < 400

    @property
    def InfoHide(self) -> bool:
        return self.__InfoHide

    @InfoHide.setter
    def InfoHide(self, hide: bool) -> None:
        self.__InfoHide = hide
        if self.SizeTooSmall:
            self.item_info_group.setVisible(False)
        else:
            self.item_info_group.setVisible(not self.__InfoHide)

    @property
    def ROI_type(self) -> str:
        return self.__roi_type

    @ROI_type.setter
    def ROI_type(self, roi_type: str) -> None:
        if roi_type in [
            'ellipse',
            'polygon',
        ]:
            self.__roi_type = roi_type
        else:
            raise ValueError('Unsupported ROI_type: {}'.format(roi_type))
        
    @property
    def ROI_added(self) -> bool:
        return self.__roi_added

    @ROI_added.setter
    def ROI_added(self, added: bool) -> None:
        self.__roi_added = added

    @property
    def SceneMode(self) -> str:
        return self.__SceneMode

    @SceneMode.setter
    def SceneMode(self, SceneMode: str) -> None:
        if SceneMode in [
            self.SceneMode_image,
            self.SceneMode_roi,
        ]:
            self.__SceneMode = SceneMode
        else:
            raise ValueError('Unsupported SceneMode: {}'.format(SceneMode))

    @property
    def drawingRoi(self) -> QGraphicsItem:
        return self.__drawing_roi

    @drawingRoi.setter
    def drawingRoi(self, Roi: QGraphicsItem) -> None:
        self.__drawing_roi = Roi

    @property
    def drawing(self) -> bool:
        if self.__drawing_roi is None:
            draw = False
        else:
            draw = True
        return draw
    
    
    def set_scene(self, ds: FileDataset) -> None:
        self.ds = ds
        self.item_img.update_item(self.ds.pixel_array)
        self._prep_item_info(self.ds)
        self.InfoHide = self.InfoHide
        
    def _prep_item_info(self, ds: FileDataset):
        self._prep_item_info_LeftTop(ds)
        self._prep_item_info_LeftBottom()
        self._prep_item_info_RightTop(ds)
        self._prep_item_info_RightBottom(ds)

    def _prep_item_info_RightTop(self, ds: FileDataset):
        device_mr = '{}\n{}\n{}\n'.format(ds.InstitutionName, ds.ManufacturerModelName, ds.Manufacturer)
        text = device_mr
        self.item_info_RightTop.setPlainText(text)
        self.item_info_RightTop.setX(self.sceneRect().width() - self.item_info_RightTop.boundingRect().width())
        self.item_info_RightTop.setY(0)
        # set AlignRight
        document = self.item_info_RightTop.document()
        opts = document.defaultTextOption()
        opts.setAlignment(Qt.AlignRight)
        document.setDefaultTextOption(opts)
        document.setTextWidth(self.item_info_RightTop.boundingRect().width())
        self.item_info_RightTop.setPlainText(text)

    def _prep_item_info_RightBottom(self, ds: FileDataset):
        acq_date = '{}/{}/{}'.format(ds.AcquisitionDate[0:4], ds.AcquisitionDate[4:6], ds.AcquisitionDate[6:8])
        	
        text = 'Date: {}\nSeries Nb: {}\n{}\nTR: {:.2f}\nTE: {}\nThickness: {:.2f}mm\nLocation: {:.2f}mm'.format(
            acq_date, self._check_ds_info(ds.SeriesNumber), self._check_ds_info(ds.MRAcquisitionType), 
            self._check_ds_info(ds.RepetitionTime), self._check_ds_info(ds.EchoTime), 
            self._check_ds_info(ds.SliceThickness), self._check_ds_info(ds.SliceLocation))
        self.item_info_RightBottom.setPlainText(text)
        self.item_info_RightBottom.setX(self.sceneRect().width() - self.item_info_RightBottom.boundingRect().width())
        self.item_info_RightBottom.setY(self.sceneRect().height() - self.item_info_RightBottom.boundingRect().height())

        # set AlignRight
        document = self.item_info_RightBottom.document()
        opts = document.defaultTextOption()
        opts.setAlignment(Qt.AlignRight)
        document.setDefaultTextOption(opts)
        document.setTextWidth(self.item_info_RightBottom.boundingRect().width())
        self.item_info_RightBottom.setPlainText(text)

    def _prep_item_info_LeftBottom(self):
        zoom = 'Zoom: {:.2f}%'.format(100*self.item_img.scale())
        window = 'WW/WL: {}/{}'.format(int(self.item_img.WW), int(self.item_img.WL))
        matrix = 'Matrix: {}, {}'.format(self.item_img.pixmap().height(), self.item_img.pixmap().width())
        if self.row == 0 or self.column == 0:
            value = 'Voxel value: outside image'
        else:
            value = 'Voxel value: {}, {}, {}'.format(self.item_img.img[self.row-1, self.column-1], self.row, self.column)

        info_LeftBottom = '{}\n{}\n{}\n{}'.format(zoom, window, matrix, value)
        self.item_info_LeftBottom.setPlainText(info_LeftBottom)
        self.item_info_LeftBottom.setX(0)
        self.item_info_LeftBottom.setY(self.sceneRect().height() - self.item_info_LeftBottom.boundingRect().height())

    def _prep_item_info_LeftTop(self, ds: FileDataset):
        PatientBirthDate = '{}/{}/{}'.format(ds.PatientBirthDate[0:4], ds.PatientBirthDate[4:6], ds.PatientBirthDate[6:8])
        info_patient = '{}\n{}\n{}\n{}'.format(ds.PatientName, ds.PatientID, PatientBirthDate, ds.Modality)
        self.item_info_LeftTop.setPlainText(info_patient)

    def _update_item_info_LeftBottom(self):
        zoom = 'Zoom: {:.2f}%'.format(100*self.item_img.scale())
        window = 'WW/WL: {}/{}'.format(int(self.item_img.WW), int(self.item_img.WL))
        matrix = 'Matrix: {}, {}'.format(self.item_img.pixmap().height(), self.item_img.pixmap().width())
        if self.row == 0 or self.column == 0:
            value = 'Voxel value: outside image'
        else:
            value = 'Voxel value: {}, {}, {}'.format(self.item_img.img[self.row-1, self.column-1], self.row, self.column)
        info_LeftBottom = '{}\n{}\n{}\n{}'.format(zoom, window, matrix, value)
        self.item_info_LeftBottom.setPlainText(info_LeftBottom)

    def _check_ds_info(self, ds_info: None):
        if ds_info is None:
            ds_info = 0.0
        return ds_info


    def _action_info(self) -> None:
        self.InfoHide = not self.InfoHide

    def _action_window(self) -> None:
        '''更换鼠标样式？'''
        self.func = 'window'
        self.item_img.func = self.func
    
    def _action_series(self) -> None:
        '''更换鼠标样式？'''
        self.func = 'series'
        self.item_img.func = self.func
    
    def _action_move(self) -> None:
        '''更换鼠标样式？'''
        self.func = 'move'
        self.item_img.func = self.func
    
    def _action_zoom(self) -> None:
        '''更换鼠标样式？'''
        self.func = 'zoom'
        self.item_img.func = self.func
    
    def _action_roi(self) -> None:
        self.func = 'roi'
        self.item_img.func = 'zoom'

    def _action_ellipse(self) -> None:
        self.ROI_added = False
        self.ROI_type = 'ellipse'

    def _action_polygon(self) -> None:
        self.ROI_added = False
        self.ROI_type = 'polygon'
        self.add_Mpolygon()
    
    def _action_point(self) -> None:
        '''更换鼠标样式？'''
        self.func = 'point'

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        if self.SceneMode == self.SceneMode_roi:
            items = self.selectedItems()
            if items:
                items[0].contextMenuEvent(event)
        else:
            self.menu.exec_(QCursor.pos())

    def setup(self) -> None:
        self.item_img = MGraphicsPixmapItem()
        self.mask = MGraphicsPixmapItem()
        self.mask.setParentItem(self.item_img)
        self.item_info_RightTop = MGraphicsTextItem()
        self.item_info_LeftBottom = MGraphicsTextItem()
        self.item_info_LeftTop = MGraphicsTextItem()
        self.item_info_RightBottom = MGraphicsTextItem()
        self.item_info_group = MGraphicsItemGroup()

        self.item_info_LeftBottom.setZValue(-1)
        self.item_info_LeftTop.setZValue(-1)
        self.item_info_RightTop.setZValue(-1)
        self.item_info_RightBottom.setZValue(-1)
        
        self.item_info_RightTop.setGroup(self.item_info_group)
        self.item_info_LeftBottom.setGroup(self.item_info_group)
        self.item_info_LeftTop.setGroup(self.item_info_group)
        self.item_info_RightBottom.setGroup(self.item_info_group)
        self.item_roi_group = MGraphicsItemGroup()
        
        self.item_info_LeftTop.setObjectName('info_LeftTop')
        self.item_info_LeftBottom.setObjectName('info_LeftBottom')
        self.item_info_RightTop.setObjectName('info_RightTop')
        self.item_info_RightBottom.setObjectName('info_RightBottom')

        self.item_info_LeftTop.setDefaultTextColor(QColor(255, 255, 255, 255))
        self.item_info_LeftBottom.setDefaultTextColor(QColor(255, 255, 255, 255))
        self.item_info_RightTop.setDefaultTextColor(QColor(255, 255, 255, 255))
        self.item_info_RightBottom.setDefaultTextColor(QColor(255, 255, 255, 255))

        self.item_img.setZValue(-2)
        self.item_info_group.setZValue(-1)
        self.item_roi_group.setZValue(1)
        self.addItem(self.item_img)
        self.addItem(self.item_info_group)
        self.addItem(self.item_roi_group)

        self._menu = QMenu(self.parent())
        self.setup_menu()

    def setup_menu(self) -> None:
        ROI_menu = QMenu(title='ROI', parent=self.parent())
        action_ellipse = ROI_menu.addAction('add Ellipse')
        action_ellipse.triggered.connect(self._action_ellipse)
        action_polygon = ROI_menu.addAction('add Polygon')
        action_polygon.triggered.connect(self._action_polygon)
        action_point = ROI_menu.addAction('Point')
        action_point.triggered.connect(self._action_point)

        menu = self._menu
        action_window = menu.addAction('Window')
        action_window.triggered.connect(self._action_window)
        menu.addMenu(ROI_menu)
        action_series = menu.addAction('Series Scroll')
        action_series.triggered.connect(self._action_series)
        action_move = menu.addAction('Move')
        action_move.triggered.connect(self._action_move)
        action_zoom = menu.addAction('Zoom')
        action_zoom.triggered.connect(self._action_zoom)
        self.action_info = menu.addAction('Info Hide')
        self.action_info.triggered.connect(self._action_info)

    @property
    def menu(self) -> QMenu:
        return self._menu

########

    def __rotation180(self, img: np.array) -> np.array:
        return np.flipud(np.fliplr(img))


    @property
    def PatientSpeciesDescription(self) -> str:
        return self._PatientSpeciesDescription

    @PatientSpeciesDescription.setter
    def PatientSpeciesDescription(self, psd: str) -> None:
        self._PatientSpeciesDescription = psd