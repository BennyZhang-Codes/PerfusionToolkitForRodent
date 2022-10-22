from math import ceil

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Slot, QSize, QEvent, QPoint, QPointF, Signal
from PySide6.QtGui import QImage, QPixmap, QIcon, QCursor, QColor, QPen
from PySide6.QtGui import QMouseEvent, QWheelEvent, QResizeEvent

from PySide6.QtWidgets import QWidget, QGraphicsScene, QMenu, QScrollBar, QGraphicsTextItem
from PySide6.QtWidgets import  QGraphicsView, QLabel, QSizePolicy, QFrame
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsEllipseItem
from pydicom import FileDataset

from modules.dcmreader.Read_dcm import MAbstractDicomReader
from modules.dcmreader.read_Dicom import read_Dicom_folder
from MyWidgets.MWidget import MWidget
from MyWidgets.MGraphicsItem import MGraphicsPixmapItem, MGraphicsEllipseItem
from MyWidgets.MGraphicsScene import MGraphicsScene
from MyWidgets.MGraphicsItemGroup import MGraphicsItemGroup

class MyGraphicsView(QGraphicsView, MWidget):
    _idx_changed = Signal(int)
    _location = Signal(tuple)

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.idx = 0
        self._textHide = False
        self._sizeTooSmall = False
        self.cursor_func = 'window'
        self._setupUI()
        self.dicom_reader = read_Dicom_folder()
    
    def set_mainwindow(self, mainwindow) -> None:
        self.mainwindow = mainwindow

    def set_root(self, root: str) -> None:
        self.root = root
        self.dicom_reader.set_root(root)
        self.WL = 10000
        self.WW = 10000
        self.idw = self._set_IDW()
        
    def _setupUI(self) -> None:
        self.setStyleSheet('''MGraphicsView{background-color: rgb(0, 0, 0);}''')
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        self.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setScene(QGraphicsScene())
        self.scene().mouseDoubleClickEvent = self._mouseDoubleClickEvent
        self.resizeEvent = self._resizeEvent
        self.mousePressEvent = self._mouseEvent
        self.mouseMoveEvent = self._mouseEvent
        self.mouseReleaseEvent = self._mouseEvent
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._pop_menu)
        self.wheelEvent = self._wheelEvent

        self.icon_move = QPixmap(u"E:/PySide6/K216_FAIR/qrc/move.png")
        self.icon_move = self.icon_move.scaled(29, 29, mode=Qt.SmoothTransformation)
        self.icon_zoom_in = QPixmap(u"E:/PySide6/K216_FAIR/qrc/zoom_in.png")
        self.icon_zoom_in = self.icon_zoom_in.scaled(29, 29, mode=Qt.SmoothTransformation)
        self.icon_zoom_out = QPixmap(u"E:/PySide6/K216_FAIR/qrc/zoom_out.png")
        self.icon_zoom_out = self.icon_zoom_out.scaled(29, 29, mode=Qt.SmoothTransformation)
        
    def set_scene(self, idx: int) -> None:
        if idx != self.idx:
            self._idx_changed.emit(idx)
        self.idx = idx
         
        self.scene().clear()
        scene = self.scene()
        scene.setSceneRect(self.geometry()) 
        scene = self._prep_item_img(self.idx, scene)
        scene = self._prep_item_info(self.idx, scene)
        self._set_textHidden(self._textHide)

        self.setScene(scene)
    
    def _pop_menu(self) -> None:
        menu = QMenu(self)
        action_window = menu.addAction('Window')
        action_window.triggered.connect(self._action_window)
        action_series = menu.addAction('Series Scroll')
        action_series.triggered.connect(self._action_series)
        action_move = menu.addAction('Move')
        action_move.triggered.connect(self._action_move)
        action_zoom = menu.addAction('Zoom')
        action_zoom.triggered.connect(self._action_zoom)

        action_point = menu.addAction('Point')
        action_point.triggered.connect(self._action_point)
        self.action_info = menu.addAction('info')
        self.action_info.triggered.connect(self._action_info)
        menu.exec_(QCursor.pos())
        self.mainwindow.statusBar().showMessage('{}::pop_menu: cursor: {}/{}'.format(self.objectName(), QCursor.pos().x(), QCursor.pos().y()))
    
    def _action_info(self) -> None:
        if self._textHide:
            self._set_textHidden(False)
            self._textHide = False
        else:
            self._set_textHidden(True)
            self._textHide = True

    def _action_window(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'window'
    
    def _action_series(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'series'
    
    def _action_move(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'move'
    
    def _action_zoom(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'zoom'
    
    def _action_point(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'point'

    def _prep_item_img(self, idx: int, scene: QGraphicsScene) -> QGraphicsScene:
        scene_width = scene.sceneRect().width()
        scene_height = scene.sceneRect().height()
        self.img = self.dicom_reader.get_pixel_array(idx)
        img = self.img.copy()
        img = np.clip(img, **self.idw)
        img = ((img - img.min()) / max(1, img.max() - img.min()))*255
        img = img.astype(np.int8)
        image = QImage(
            img, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Grayscale8)
        pix_img = QPixmap.fromImage(image)
        scale = min(scene_height/pix_img.height(), scene_width/pix_img.width())
        self.item_img = scene.addPixmap(pix_img)
        self.item_img.setScale(scale)
        self.item_img.setY((scene_height-pix_img.height()*scale)/2)
        self.item_img.setX((scene_width-pix_img.width()*scale)/2)

        self._col, self._row = self._maptoimg()
        return scene
        
    def _prep_item_info(self, idx: int, scene: QGraphicsScene) -> QGraphicsScene:
        ds = self.dicom_reader.get_ds(idx)
        scene = self._prep_item_info_LeftTop(ds, scene)
        scene = self._prep_item_info_LeftBottom(scene)
        scene = self._prep_item_info_RightTop(ds, scene)
        scene = self._prep_item_info_RightBottom(ds, scene)
        return scene

    def _prep_item_info_RightTop(self, ds: FileDataset, scene: QGraphicsScene) -> QGraphicsScene:
        device_mr = '{}\n{}\n{}\n'.format(ds.InstitutionName, ds.ManufacturerModelName, ds.Manufacturer)
        text = device_mr
        item_info_RightTop = scene.addText(text)
        item_info_RightTop.setObjectName('info_RightTop')
        item_info_RightTop.setDefaultTextColor(QColor(255, 255, 255, 255))
        item_info_RightTop.setX(scene.sceneRect().width() - item_info_RightTop.boundingRect().width())
        item_info_RightTop.setY(0)
        # set AlignRight
        document = item_info_RightTop.document()
        opts = document.defaultTextOption()
        opts.setAlignment(Qt.AlignRight)
        document.setDefaultTextOption(opts)
        document.setTextWidth(item_info_RightTop.boundingRect().width())

        item_info_RightTop.setPlainText(text)
        return scene

    def _prep_item_info_RightBottom(self, ds: FileDataset, scene: QGraphicsScene) -> QGraphicsScene:
        acq_date = '{}/{}/{}'.format(ds.AcquisitionDate[0:4], ds.AcquisitionDate[4:6], ds.AcquisitionDate[6:8])
        	
        text = 'Date: {}\nSeries Nb: {}\n{}\nTR: {:.2f}\nTE: {}\nThickness: {:.2f}mm\nLocation: {:.2f}mm'.format(
            acq_date, self._check_ds_info(ds.SeriesNumber), self._check_ds_info(ds.MRAcquisitionType), 
            self._check_ds_info(ds.RepetitionTime), self._check_ds_info(ds.EchoTime), 
            self._check_ds_info(ds.SliceThickness), self._check_ds_info(ds.SliceLocation))
        item_info_RightBottom = scene.addText(text)
        item_info_RightBottom.setObjectName('info_RightBottom')
        item_info_RightBottom.setDefaultTextColor(QColor(255, 255, 255, 255))
        item_info_RightBottom.setX(scene.sceneRect().width() - item_info_RightBottom.boundingRect().width())
        item_info_RightBottom.setY(scene.sceneRect().height() - item_info_RightBottom.boundingRect().height())

        # set AlignRight
        document = item_info_RightBottom.document()
        opts = document.defaultTextOption()
        opts.setAlignment(Qt.AlignRight)
        document.setDefaultTextOption(opts)
        document.setTextWidth(item_info_RightBottom.boundingRect().width())

        item_info_RightBottom.setPlainText(text)
        return scene

    def _prep_item_info_LeftBottom(self, scene: QGraphicsScene) -> QGraphicsScene:
        zoom = 'Zoom: {:.2f}%'.format(100*self.item_img.scale())
        window = 'WW/WL: {}/{}'.format(int(self.WW), int(self.WL))
        matrix = 'Matrix: {}, {}'.format(self.item_img.pixmap().height(), self.item_img.pixmap().width())
        if self._row == 0 or self._col == 0:
            value = 'Voxel value: outside image'
        else:
            value = 'Voxel value: {}, {}, {}'.format(self.img[self._row-1, self._col-1], self._row, self._col)

        info_LeftBottom = '{}\n{}\n{}\n{}'.format(zoom, window, matrix, value)
        item_info_LeftBottom = scene.addText(info_LeftBottom)
        item_info_LeftBottom.setObjectName('info_LeftBottom')
        item_info_LeftBottom.setDefaultTextColor(QColor(255, 255, 255, 255))
        item_info_LeftBottom.setX(0)
        item_info_LeftBottom.setY(scene.sceneRect().height() - item_info_LeftBottom.boundingRect().height())
        return scene

    def dsinfo(self,ds):
        acq_num = '{}\n{}'.format(ds.AcquisitionNumber, ds.InstanceNumber)
        return acq_num
     
    def _prep_item_info_LeftTop(self, ds: FileDataset, scene: QGraphicsScene) -> QGraphicsScene:
        PatientBirthDate = '{}/{}/{}'.format(ds.PatientBirthDate[0:4], ds.PatientBirthDate[4:6], ds.PatientBirthDate[6:8])
        info_patient = '{}\n{}\n{}\n{}'.format(ds.PatientName, ds.PatientID, PatientBirthDate, ds.Modality)
        item_info_LeftTop = scene.addText(info_patient)
        item_info_LeftTop.setObjectName('info_LeftTop')
        item_info_LeftTop.setDefaultTextColor(QColor(255, 255, 255, 255))
        return scene
    
    def _check_ds_info(self, ds_info: None):
        if ds_info is None:
            ds_info = 0.0
        return ds_info

    def _set_WW(self, WW: float) -> None:
        if WW > 30000:
            WW = 30000
        if WW < 2:
            WW = 2
        self.WW = WW
        self.idw = self._set_IDW()
    
    def _set_WL(self, WL: float) -> None:
        if WL > 30000:
            WL = 30000
        if WL < -1000:
            WL = -1000
        self.WL = WL
        self.idw = self._set_IDW()
    
    def _set_IDW(self) -> dict:
        '''Image Display Window (IDW)'''
        self.value_min = self.WL - self.WW//2
        self.value_max = self.WL + self.WW//2
        if self.value_min < 0:
            self.value_min = 0
        if self.value_max > 50000:
            self.value_max = 50000
        idw = {'a_min':self.value_min, 'a_max':self.value_max}
        return idw
    
    def _resizeEvent(self, event: QResizeEvent) -> None:
        if hasattr(self, 'root'): 
            self.set_scene(self.idx)
    
        self._sizeTooSmall =  self.height() < 170 or self.width() < 400
        self._set_textHidden(self._textHide)

        if hasattr(self, 'mainwindow'):
            self.mainwindow.statusBar().showMessage('MGraphicsView::Resize GraphicsView: {}/{}, Scene: {}/{} '.format(
                self.height(), self.width(), self.scene().height(), self.scene().width()))

    def _mouseEvent(self, event: QMouseEvent) -> None:
        pos = event.position()
        self._col, self._row = self._maptoimg(pos)
        self.mainwindow.statusBar().showMessage('Location:: scene: {}/{}, image: {}/{}'.format(
            pos.x(), pos.y(), self._col, self._row))
        self._update_item_info_LeftBottom()

        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.cursor_func == 'window':
                    self.x_init = event.pos().x()
                    self.y_init = event.pos().y()
                elif self.cursor_func == 'series':
                    self.y_init = event.pos().y()
                elif self.cursor_func == 'move' or self.cursor_func == 'zoom':
                    self.x_init = event.pos().x()
                    self.y_init = event.pos().y()
                    self.item_img_pos = self.item_img.pos()
                elif self.cursor_func == 'point':
                    self._location.emit((self._row, self._col))

        elif event.type() == QEvent.Type.MouseMove:
            if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
                if self.cursor_func == 'window':
                    self.x_end = event.pos().x()
                    self.y_end = event.pos().y()
                    x_diff = self.x_end - self.x_init
                    y_diff = (self.y_end - self.y_init) * (-1)
                    self._set_WW(self.WW + 10000 * (x_diff / self.geometry().width()))
                    self._set_WL(self.WL + 10000 * (y_diff / self.geometry().height()))
                    self.set_scene(self.idx)
                    diff = 'x_diff/y_diff: {}/{}'.format(x_diff, y_diff)
                    window = 'WW/WL: {}/{}'.format(int(self.WW), int(self.WL))
                    # self.mainwindow.statusBar().showMessage('{} {}'.format(diff, window))
                    self.x_init = self.x_end
                    self.y_init = self.y_end
                elif self.cursor_func == 'series':
                    self.y_end = event.pos().y()
                    y_diff = (self.y_end - self.y_init)
                    totalnum = self.dicom_reader.len()
                    height_per_img = self.geometry().height() / totalnum
                    if abs(y_diff) > height_per_img:
                        self.y_init = self.y_end
                        idx = self._check_idx(int(y_diff/abs(y_diff)) + self.idx)
                        self.set_scene(idx)
                    self.mainwindow.statusBar().showMessage('{}:: current:{} diff:{}/{}'.format(self.objectName(), self.idx, y_diff, int(y_diff/max(1, abs(y_diff)))))
                elif self.cursor_func == 'move' or self.cursor_func == 'zoom':
                    self.setCursor(QCursor(self.icon_move))
                    x_diff = event.pos().x() - self.x_init
                    y_diff = event.pos().y() - self.y_init
                    # self.mainwindow.statusBar().showMessage('Move: x:{}, y:{}'.format(x_diff, y_diff))
                    self.item_img_pos.setX(self.item_img_pos.x() + x_diff)
                    self.item_img_pos.setY(self.item_img_pos.y() + y_diff)
                    self.item_img.setPos(self.item_img_pos)

                    self.x_init = event.pos().x()
                    self.y_init = event.pos().y()
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.setCursor(QCursor())
        else:
            self.setCursor(QCursor())

    def _wheelEvent(self, event: QWheelEvent) -> None:
        angle = event.angleDelta().y()
        value = int(angle//120)
        if self.cursor_func == 'zoom':
            if value > 0:
                self.setCursor(QCursor(self.icon_zoom_in, hotX=15, hotY=15))
            else:
                self.setCursor(QCursor(self.icon_zoom_out, hotX=15, hotY=15))
            bef_scale = self.item_img.scale()
            cur_scale = max(0.2, bef_scale+0.05*value)
            bef_pos = self.item_img.pos()
            cursor_pos = self.mapFromGlobal(event.globalPosition())
            cursor_pos_x = cursor_pos.x()
            cursor_pos_y = cursor_pos.y()
            ratio_x = (cursor_pos_x - bef_pos.x())/(self.item_img.pixmap().width()*bef_scale)
            ratio_y = (cursor_pos_y - bef_pos.y())/(self.item_img.pixmap().height()*bef_scale)
            aft_cursor_pos_x = bef_pos.x() + ratio_x * (self.item_img.pixmap().width()*cur_scale)
            aft_cursor_pos_y = bef_pos.y() + ratio_y * (self.item_img.pixmap().height()*cur_scale)
            self.item_img.setScale(cur_scale)
            self.item_img.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
            self.item_img.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))
            self._update_item_info_LeftBottom()
            self.mainwindow.statusBar().showMessage('{}::Zoom::Wheel: {}/{}, scale: {}, cursor: {}/{}'.format(self.objectName(), angle, value, cur_scale, cursor_pos_x, cursor_pos_y))
        else:
            idx = self._check_idx(self.idx-1*value)
            self.set_scene(idx)
            self._update_item_info_LeftBottom()
            self.mainwindow.statusBar().showMessage('{}::ScrollBar:Wheel: {}/{}, Current Index: {}'.format(self.objectName(), angle, value, self.idx))

    def _mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.cursor_func == 'window':
            max_value = np.max(self.img)
            min_value = np.min(self.img)
            self._set_WL((max_value+min_value)/2)
            self._set_WW(max(0, max_value-min_value))
        self.set_scene(self.idx)

    def _maptoimg(self, pos: QPointF=None) -> tuple:
        if pos is None:
            pos = self.mapFromGlobal(QCursor.pos())
        cur_scale = self.item_img.scale()
        display_width = self.item_img.pixmap().width()*cur_scale
        display_height = self.item_img.pixmap().height()*cur_scale
        diff_x = pos.x() - self.item_img.x()
        diff_y = pos.y() - self.item_img.y()
        x_check = diff_x > 0 and diff_x < display_width
        y_check = diff_y > 0 and diff_y < display_height    
        if x_check and y_check:
            return ceil(diff_x/cur_scale), ceil(diff_y/cur_scale)
        else:
            return 0, 0

    def _update_item_info_LeftBottom(self):
        zoom = 'Zoom: {:.2f}%'.format(100*self.item_img.scale())
        window = 'WW/WL: {}/{}'.format(int(self.WW), int(self.WL))
        matrix = 'Matrix: {}, {}'.format(self.item_img.pixmap().height(), self.item_img.pixmap().width())
        if self._row == 0 or self._col == 0:
            value = 'Voxel value: outside image'
        else:
            value = 'Voxel value: {}, {}, {}'.format(self.img[self._row-1, self._col-1], self._row, self._col)
        info_LeftBottom = '{}\n{}\n{}\n{}'.format(zoom, window, matrix, value)
        for item in self.items():
            if isinstance(item, QGraphicsTextItem):
                if item.objectName() == 'info_LeftBottom':
                    item.setPlainText(info_LeftBottom)

    def _check_idx(self, idx: int) -> int:
        if idx < self.dicom_reader.min_idx():
            idx = self.dicom_reader.min_idx()
        if idx > self.dicom_reader.max_idx():
            idx = self.dicom_reader.max_idx()
        return idx

    def _set_textHidden(self, hidden: bool):
        text_items = [item for item in self.items() if isinstance(item, QGraphicsTextItem)]
        if self._sizeTooSmall:
            hidden = True
        for item in text_items:
            item.setVisible(not hidden)


class MGraphicsView(QGraphicsView, MWidget):
    _idx_changed = Signal(int)
    _location = Signal(tuple)

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.idx = 0
        self._textHide = False
        self._sizeTooSmall = False
        self.cursor_func = 'window'
        self.mscene = MGraphicsScene(self)
        self.mscene._mask.connect(self.__mask)
        self.item_img = self.mscene.item_img
        self.item_info_RightTop = self.mscene.item_info_RightTop
        self.item_info_LeftBottom = self.mscene.item_info_LeftBottom
        self.item_info_LeftTop = self.mscene.item_info_LeftTop
        self.item_info_RightBottom = self.mscene.item_info_RightBottom
        self.item_info_group = self.mscene.item_info_group
        self.item_roi_group = self.mscene.item_roi_group
        self.item_rois = []
        self.setMouseTracking(True)
        print('mouse tracking',self.hasMouseTracking())

    def __mask(self, index):
        print('get mask')
        # print(mask)
    def set_dicom_reader(self, dicom_reader: MAbstractDicomReader) -> None:
        self.dicom_reader = dicom_reader
        self.WL = 10000
        self.WW = 10000
        self.idw = self._set_IDW()
        self._setupUI()

    def set_mainwindow(self, mainwindow) -> None:
        self.mainwindow = mainwindow
        
    def _setupUI(self) -> None:
        self.setStyleSheet('''MGraphicsView{background-color: rgb(0, 0, 0);}''')
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        self.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setScene(self.mscene)

        self.icon_move = QPixmap(u"E:/PySide6/K216_FAIR/qrc/move.png")
        self.icon_move = self.icon_move.scaled(29, 29, mode=Qt.SmoothTransformation)
        self.icon_zoom_in = QPixmap(u"E:/PySide6/K216_FAIR/qrc/zoom_in.png")
        self.icon_zoom_in = self.icon_zoom_in.scaled(29, 29, mode=Qt.SmoothTransformation)
        self.icon_zoom_out = QPixmap(u"E:/PySide6/K216_FAIR/qrc/zoom_out.png")
        self.icon_zoom_out = self.icon_zoom_out.scaled(29, 29, mode=Qt.SmoothTransformation)
        
    def set_scene(self, idx: int) -> None:
        if idx != self.idx:
            self._idx_changed.emit(idx)
        self.idx = idx
        
        scene = self.scene()
        scene.setSceneRect(self.geometry()) 
        self._prep_item_img(self.idx)
        self._prep_item_info(self.idx)
        self._set_textHidden(self._textHide)

        # self.setScene(scene)
    
    def _roi_menu(self) -> QMenu:
        menu = QMenu('ROI')
        action_ellipse = menu.addAction('Ellipse')
        action_ellipse.triggered.connect(self._action_ellipse)
        action_point = menu.addAction('Point')
        action_point.triggered.connect(self._action_point)
        return menu
    
    def _pop_menu(self) -> None:
        menu = QMenu(self)
        action_window = menu.addAction('Window')
        action_window.triggered.connect(self._action_window)
        menu.addMenu(self._roi_menu())
        action_series = menu.addAction('Series Scroll')
        action_series.triggered.connect(self._action_series)
        action_move = menu.addAction('Move')
        action_move.triggered.connect(self._action_move)
        action_zoom = menu.addAction('Zoom')
        action_zoom.triggered.connect(self._action_zoom)
        self.action_info = menu.addAction('info')
        self.action_info.triggered.connect(self._action_info)
        menu.exec_(QCursor.pos())
        self.mainwindow.statusBar().showMessage('{}::pop_menu: cursor: {}/{}'.format(self.objectName(), QCursor.pos().x(), QCursor.pos().y()))
    
    def _action_info(self) -> None:
        if self._textHide:
            self._set_textHidden(False)
            self._textHide = False
        else:
            self._set_textHidden(True)
            self._textHide = True

    def _action_window(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'window'
    
    def _action_series(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'series'
    
    def _action_move(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'move'
    
    def _action_zoom(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'zoom'
    
    def _action_ellipse(self) -> None:
        ellipse = self.scene().add_Mellipse()
        self.cursor_func = 'ellipse'
        self.item_rois.append(ellipse)

    def _action_point(self) -> None:
        '''更换鼠标样式？'''
        self.cursor_func = 'point'

    def _prep_item_img(self, idx: int):
        scene = self.scene()
        scene_width = scene.sceneRect().width()
        scene_height = scene.sceneRect().height()
        self.img = self.dicom_reader.get_pixel_array(idx)
        img = self.img.copy()
        img = np.clip(img, **self.idw)
        img = ((img - img.min()) / max(1, img.max() - img.min()))*255
        img = img.astype(np.int8)
        image = QImage(
            img, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Grayscale8)
        pix_img = QPixmap.fromImage(image)
        scale = min(scene_height/pix_img.height(), scene_width/pix_img.width())
        self.item_img.setPixmap(pix_img)
        self.item_img.setScale(scale)
        self.item_img.setY((scene_height-pix_img.height()*scale)/2)
        self.item_img.setX((scene_width-pix_img.width()*scale)/2)

        self._col, self._row = self._maptoimg()
        
    def _prep_item_info(self, idx: int):
        ds = self.dicom_reader.get_ds(idx)
        self._prep_item_info_LeftTop(ds)
        self._prep_item_info_LeftBottom()
        self._prep_item_info_RightTop(ds)
        self._prep_item_info_RightBottom(ds)

    def _prep_item_info_RightTop(self, ds: FileDataset):
        scene = self.scene()
        device_mr = '{}\n{}\n{}\n'.format(ds.InstitutionName, ds.ManufacturerModelName, ds.Manufacturer)
        text = device_mr
        self.item_info_RightTop.setPlainText(text)
        item_info_RightTop = self.item_info_RightTop
        item_info_RightTop.setObjectName('info_RightTop')
        item_info_RightTop.setDefaultTextColor(QColor(255, 255, 255, 255))
        item_info_RightTop.setX(scene.sceneRect().width() - item_info_RightTop.boundingRect().width())
        item_info_RightTop.setY(0)
        # set AlignRight
        document = item_info_RightTop.document()
        opts = document.defaultTextOption()
        opts.setAlignment(Qt.AlignRight)
        document.setDefaultTextOption(opts)
        document.setTextWidth(item_info_RightTop.boundingRect().width())
        item_info_RightTop.setPlainText(text)

    def _prep_item_info_RightBottom(self, ds: FileDataset):
        scene = self.scene()
        acq_date = '{}/{}/{}'.format(ds.AcquisitionDate[0:4], ds.AcquisitionDate[4:6], ds.AcquisitionDate[6:8])
        	
        text = 'Date: {}\nSeries Nb: {}\n{}\nTR: {:.2f}\nTE: {}\nThickness: {:.2f}mm\nLocation: {:.2f}mm'.format(
            acq_date, self._check_ds_info(ds.SeriesNumber), self._check_ds_info(ds.MRAcquisitionType), 
            self._check_ds_info(ds.RepetitionTime), self._check_ds_info(ds.EchoTime), 
            self._check_ds_info(ds.SliceThickness), self._check_ds_info(ds.SliceLocation))
        self.item_info_RightBottom.setPlainText(text)
        item_info_RightBottom = self.item_info_RightBottom
        item_info_RightBottom.setObjectName('info_RightBottom')
        item_info_RightBottom.setDefaultTextColor(QColor(255, 255, 255, 255))
        item_info_RightBottom.setX(scene.sceneRect().width() - item_info_RightBottom.boundingRect().width())
        item_info_RightBottom.setY(scene.sceneRect().height() - item_info_RightBottom.boundingRect().height())

        # set AlignRight
        document = item_info_RightBottom.document()
        opts = document.defaultTextOption()
        opts.setAlignment(Qt.AlignRight)
        document.setDefaultTextOption(opts)
        document.setTextWidth(item_info_RightBottom.boundingRect().width())

        item_info_RightBottom.setPlainText(text)

    def _prep_item_info_LeftBottom(self):
        scene = self.scene()
        zoom = 'Zoom: {:.2f}%'.format(100*self.item_img.scale())
        window = 'WW/WL: {}/{}'.format(int(self.WW), int(self.WL))
        matrix = 'Matrix: {}, {}'.format(self.item_img.pixmap().height(), self.item_img.pixmap().width())
        if self._row == 0 or self._col == 0:
            value = 'Voxel value: outside image'
        else:
            value = 'Voxel value: {}, {}, {}'.format(self.img[self._row-1, self._col-1], self._row, self._col)

        info_LeftBottom = '{}\n{}\n{}\n{}'.format(zoom, window, matrix, value)
        self.item_info_LeftBottom.setPlainText(info_LeftBottom)
        item_info_LeftBottom = self.item_info_LeftBottom
        item_info_LeftBottom.setObjectName('info_LeftBottom')
        item_info_LeftBottom.setDefaultTextColor(QColor(255, 255, 255, 255))
        item_info_LeftBottom.setX(0)
        item_info_LeftBottom.setY(scene.sceneRect().height() - item_info_LeftBottom.boundingRect().height())

    def dsinfo(self,ds):
        acq_num = '{}\n{}'.format(ds.AcquisitionNumber, ds.InstanceNumber)
        return acq_num
     
    def _prep_item_info_LeftTop(self, ds: FileDataset):
        PatientBirthDate = '{}/{}/{}'.format(ds.PatientBirthDate[0:4], ds.PatientBirthDate[4:6], ds.PatientBirthDate[6:8])
        info_patient = '{}\n{}\n{}\n{}'.format(ds.PatientName, ds.PatientID, PatientBirthDate, ds.Modality)
        self.item_info_LeftTop.setPlainText(info_patient)
        item_info_LeftTop = self.item_info_LeftTop
        item_info_LeftTop.setObjectName('info_LeftTop')
        item_info_LeftTop.setDefaultTextColor(QColor(255, 255, 255, 255))
    
    def _check_ds_info(self, ds_info: None):
        if ds_info is None:
            ds_info = 0.0
        return ds_info

    def _set_WW(self, WW: float) -> None:
        if WW > 30000:
            WW = 30000
        if WW < 2:
            WW = 2
        self.WW = WW
        self.idw = self._set_IDW()
    
    def _set_WL(self, WL: float) -> None:
        if WL > 30000:
            WL = 30000
        if WL < -1000:
            WL = -1000
        self.WL = WL
        self.idw = self._set_IDW()
    
    def _set_IDW(self) -> dict:
        '''Image Display Window (IDW)'''
        self.value_min = self.WL - self.WW//2
        self.value_max = self.WL + self.WW//2
        if self.value_min < 0:
            self.value_min = 0
        if self.value_max > 50000:
            self.value_max = 50000
        idw = {'a_min':self.value_min, 'a_max':self.value_max}
        return idw
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.set_scene(self.idx)
        self._sizeTooSmall =  self.height() < 170 or self.width() < 400
        self._set_textHidden(self._textHide)

        if hasattr(self, 'mainwindow'):
            self.mainwindow.statusBar().showMessage('MGraphicsView::Resize GraphicsView: {}/{}, Scene: {}/{} '.format(
                self.height(), self.width(), self.scene().height(), self.scene().width()))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.cursor_func == 'window':
                self.x_init = event.pos().x()
                self.y_init = event.pos().y()
            elif self.cursor_func == 'series':
                self.y_init = event.pos().y()
            elif self.cursor_func == 'move' or self.cursor_func == 'zoom':
                self.x_init = event.pos().x()
                self.y_init = event.pos().y()
                self.item_img_pos = self.item_img.pos()
            elif self.cursor_func == 'point':
                self._location.emit((self._row, self._col))
            elif self.cursor_func == 'ellipse':
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.position()
        self._col, self._row = self._maptoimg(pos)
        self.mainwindow.statusBar().showMessage('Location:: scene: {}/{}, image: {}/{}'.format(
            pos.x(), pos.y(), self._col, self._row))
        self._update_item_info_LeftBottom()
        if event.buttons() == Qt.LeftButton | event.button() == Qt.MouseButton.LeftButton:
            if self.cursor_func == 'window':
                self.x_end = event.pos().x()
                self.y_end = event.pos().y()
                x_diff = self.x_end - self.x_init
                y_diff = (self.y_end - self.y_init) * (-1)
                self._set_WW(self.WW + 10000 * (x_diff / self.geometry().width()))
                self._set_WL(self.WL + 10000 * (y_diff / self.geometry().height()))
                self.set_scene(self.idx)
                diff = 'x_diff/y_diff: {}/{}'.format(x_diff, y_diff)
                window = 'WW/WL: {}/{}'.format(int(self.WW), int(self.WL))
                # self.mainwindow.statusBar().showMessage('{} {}'.format(diff, window))
                self.x_init = self.x_end
                self.y_init = self.y_end
            elif self.cursor_func == 'series':
                self.y_end = event.pos().y()
                y_diff = (self.y_end - self.y_init)
                totalnum = self.dicom_reader.len()
                height_per_img = self.geometry().height() / totalnum
                if abs(y_diff) > height_per_img:
                    self.y_init = self.y_end
                    idx = self._check_idx(int(y_diff/abs(y_diff)) + self.idx)
                    self.set_scene(idx)
                self.mainwindow.statusBar().showMessage('{}:: current:{} diff:{}/{}'.format(self.objectName(), self.idx, y_diff, int(y_diff/max(1, abs(y_diff)))))
            elif self.cursor_func == 'move' or self.cursor_func == 'zoom':
                self.setCursor(QCursor(self.icon_move))
                x_diff = event.pos().x() - self.x_init
                y_diff = event.pos().y() - self.y_init
                # self.mainwindow.statusBar().showMessage('Move: x:{}, y:{}'.format(x_diff, y_diff))
                self.item_img_pos.setX(self.item_img_pos.x() + x_diff)
                self.item_img_pos.setY(self.item_img_pos.y() + y_diff)
                self.item_img.setPos(self.item_img_pos)

                self.x_init = event.pos().x()
                self.y_init = event.pos().y()
            elif self.cursor_func == 'ellipse':
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.cursor_func == 'ellipse':
            super().mouseReleaseEvent(event)
        self.setCursor(QCursor())

    def wheelEvent(self, event: QWheelEvent) -> None:
        angle = event.angleDelta().y()
        value = int(angle//120)

        
        if self.cursor_func == 'zoom':
            if value > 0:
                self.setCursor(QCursor(self.icon_zoom_in, hotX=15, hotY=15))
            else:
                self.setCursor(QCursor(self.icon_zoom_out, hotX=15, hotY=15))
            bef_scale = self.item_img.scale()
            cur_scale = max(0.2, bef_scale+0.05*value)
            bef_pos = self.item_img.pos()
            cursor_pos = self.mapFromGlobal(event.globalPosition())
            cursor_pos_x = cursor_pos.x()
            cursor_pos_y = cursor_pos.y()
            ratio_x = (cursor_pos_x - bef_pos.x())/(self.item_img.pixmap().width()*bef_scale)
            ratio_y = (cursor_pos_y - bef_pos.y())/(self.item_img.pixmap().height()*bef_scale)
            aft_cursor_pos_x = bef_pos.x() + ratio_x * (self.item_img.pixmap().width()*cur_scale)
            aft_cursor_pos_y = bef_pos.y() + ratio_y * (self.item_img.pixmap().height()*cur_scale)
            self.item_img.setScale(cur_scale)
            self.item_img.setX(bef_pos.x() - (aft_cursor_pos_x - cursor_pos_x))
            self.item_img.setY(bef_pos.y() - (aft_cursor_pos_y - cursor_pos_y))
            self._update_item_info_LeftBottom()
            self.mainwindow.statusBar().showMessage('{}::Zoom::Wheel: {}/{}, scale: {}, cursor: {}/{}'.format(self.objectName(), angle, value, cur_scale, cursor_pos_x, cursor_pos_y))
        elif self.cursor_func == 'ellipse':
            super().wheelEvent(event)
        else:
            idx = self._check_idx(self.idx-1*value)
            self.set_scene(idx)
            self._update_item_info_LeftBottom()
            self.mainwindow.statusBar().showMessage('{}::ScrollBar:Wheel: {}/{}, Current Index: {}'.format(self.objectName(), angle, value, self.idx))

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.cursor_func == 'window':
            max_value = np.max(self.img)
            min_value = np.min(self.img)
            self._set_WL((max_value+min_value)/2)
            self._set_WW(max(0, max_value-min_value))

        if self.cursor_func == 'point':
            super().mouseMoveEvent(event)
        else:
            self.set_scene(self.idx)

    def _maptoimg(self, pos: QPointF=None) -> tuple:
        if pos is None:
            pos = self.mapFromGlobal(QCursor.pos())
        cur_scale = self.item_img.scale()
        display_width = self.item_img.pixmap().width()*cur_scale
        display_height = self.item_img.pixmap().height()*cur_scale
        diff_x = pos.x() - self.item_img.x()
        diff_y = pos.y() - self.item_img.y()
        x_check = diff_x > 0 and diff_x < display_width
        y_check = diff_y > 0 and diff_y < display_height    
        if x_check and y_check:
            return ceil(diff_x/cur_scale), ceil(diff_y/cur_scale)
        else:
            return 0, 0

    def _update_item_info_LeftBottom(self):
        zoom = 'Zoom: {:.2f}%'.format(100*self.item_img.scale())
        window = 'WW/WL: {}/{}'.format(int(self.WW), int(self.WL))
        matrix = 'Matrix: {}, {}'.format(self.item_img.pixmap().height(), self.item_img.pixmap().width())
        if self._row == 0 or self._col == 0:
            value = 'Voxel value: outside image'
        else:
            value = 'Voxel value: {}, {}, {}'.format(self.img[self._row-1, self._col-1], self._row, self._col)
        info_LeftBottom = '{}\n{}\n{}\n{}'.format(zoom, window, matrix, value)
        self.item_info_LeftBottom.setPlainText(info_LeftBottom)

    def _check_idx(self, idx: int) -> int:
        if idx < self.dicom_reader.min_idx():
            idx = self.dicom_reader.min_idx()
        if idx > self.dicom_reader.max_idx():
            idx = self.dicom_reader.max_idx()
        return idx

    def _set_textHidden(self, hidden: bool):
        if self._sizeTooSmall:
            hidden = True
        self.item_info_group.setVisible(not hidden)
    
    def contextMenuEvent(self, event):
        self._pop_menu()
        super().contextMenuEvent(event)

if __name__ == '__main__':
    mGraphicView = MyGraphicsView()