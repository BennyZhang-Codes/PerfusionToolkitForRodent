
import numpy as np
import matplotlib.pyplot as plt

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QScatterSeries, QVXYModelMapper

from UI.ui_Widget_DSC import Ui_Widget_DSC
from modules.dcmreader.read_DSC_DCE import Read_Bruker_TimeSeries

from modules.utils.shape import shape_to_mask, get_index_of_mask
from MyWidgets.Mmodel.TabelModel import TimePointsTableModel
from MyWidgets.MChart.MChart import MChart

class Widget_DSC(QWidget, Ui_Widget_DSC):

    def __init__(self, dicom_dir, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.root = dicom_dir
        self.setupUi(self)
        
        self.dicom_reader = Read_Bruker_TimeSeries(self.root)
        if self.comboBox.currentText() == 'Slice':
            self.dicom_reader.GroupBy = 'Slice'

        self.dicom_reader.signal_loadstart.connect(self.__slot_loadstart)
        self.dicom_reader.signal_loading.connect(self.__slot_loading)
        self.dicom_reader.signal_loaded.connect(self.__slot_loaded)
        
        self._ROI_color = QColor(118,185,172,196)
        

    def _setupUI(self):
        self.chart = MChart()
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.legend().hide()
        
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chartView.setChart(self.chart)

        self.graphicsView.set_mainwindow(self.mainwindow)
        self.graphicsView.DicomReader = self.dicom_reader
        self.graphicsView._idx_changed.connect(self.__slot_graphicsView_idx_changed)
        self.graphicsView.mscene.signal_ROI_point.connect(self.__slot_ROI_point)
        self.graphicsView.mscene.signal_ROI.connect(self.__slot_ROI)
        self.graphicsView.mscene.signal_ROI_color.connect(self.__slot_ROI_color)
        

        self.spinBox_timepoint.setMaximum(self.dicom_reader.max_idx + 1)
        self.spinBox_timepoint.setMinimum(self.dicom_reader.min_idx + 1)
        self.spinBox_timepoint.setValue(self.graphicsView.idx + 1)
        self.verticalScrollBar.setMaximum(self.dicom_reader.max_idx + 1)
        self.verticalScrollBar.setMinimum(self.dicom_reader.min_idx + 1)
        self.verticalScrollBar.setValue(self.graphicsView.idx + 1)

        self.spinBox_slice.setMaximum(self.dicom_reader.SliceNum)
        self.spinBox_slice.setMinimum(1)
        self.spinBox_slice.setValue(self.dicom_reader.CurrentSlice)

        self.spinBox_row.setMaximum(self.dicom_reader.RowNum)
        self.spinBox_row.setMinimum(1)

        self.spinBox_column.setMaximum(self.dicom_reader.ColNum)
        self.spinBox_column.setMinimum(1)

    def __slot_ROI(self, data: tuple):
        path, item_pix = data
        w = item_pix.width()
        h = item_pix.height()
        pix = QPixmap(w, h)
        pix.fill(QColor(0,0,0,255))

        
        pen = QPen()
        pen.setWidthF(0)
        pen.setColor(QColor(0,0,0,0))

        painter_item_pix = QPainter(item_pix)
        painter_item_pix.setPen(pen)
        painter_item_pix.setBrush(self.ROI_color)
        painter_item_pix.drawPath(path)
        painter_item_pix.end()

        painter_pix = QPainter(pix)
        painter_pix.setPen(pen)
        painter_pix.setBrush(QColor(255,255,255,255))
        painter_pix.drawPath(path)
        painter_pix.end()


        img = pix.toImage()
        b = img.bits()
        img_array = np.frombuffer(b, np.uint8).reshape((pix.height(), pix.width(), 4))
        mask = img_array[:,:,-2].astype(bool)
        plt.imsave('mask.jpg', mask, cmap='gray')

        index = get_index_of_mask(mask)
        ydata = []
        for idx in index:
            ydata.append(self.dicom_reader.img_GroupBySlice[:, idx[0], idx[1]])

        ydata = np.array(ydata)
        xdata = self.dicom_reader.TimePoints
        self.__curve(xdata, np.mean(ydata, axis=0))

        self.label_mask.setPixmap(pix.scaled(512,512, Qt.KeepAspectRatio, Qt.FastTransformation))

        self.label_mask_img.setPixmap(item_pix.scaled(512,512, Qt.KeepAspectRatio, Qt.FastTransformation))
        # self.label_mask_img.setScaledContents(True)
    def __slot_ROI_color(self, color: QColor) -> None:
        self.ROI_color = color
        
    def __slot_graphicsView_idx_changed(self, idx: int):
        self.verticalScrollBar.setValue(idx+1)


    @Slot(int)
    def on_spinBox_timepoint_valueChanged(self, value: int):
        self.graphicsView.set_scene(value-1)
        self.verticalScrollBar.setValue(value)

    @Slot(int)
    def on_spinBox_slice_valueChanged(self, value: int):
        self.dicom_reader.CurrentSlice = value - 1
        self.graphicsView.set_scene(self.graphicsView.idx)
        row = self.spinBox_row.value()
        col = self.spinBox_column.value()
        ydata = self.dicom_reader.img_GroupBySlice[:, row - 1, col - 1]
        xdata = self.dicom_reader.TimePoints
        self.__curve(xdata, ydata)

    @Slot(int)
    def on_verticalScrollBar_valueChanged(self, value: int):
        self.spinBox_timepoint.setValue(value)

    @Slot(int)
    def on_spinBox_row_valueChanged(self, value: int):
        row = value
        col = self.spinBox_column.value()
        ydata = self.dicom_reader.img_GroupBySlice[:, row - 1, col - 1]
        xdata = self.dicom_reader.TimePoints
        self.__curve(xdata, ydata)

    @Slot(int)
    def on_spinBox_column_valueChanged(self, value: int):
        row = self.spinBox_row.value()
        col = value
        ydata = self.dicom_reader.img_GroupBySlice[:, row - 1, col - 1]
        xdata = self.dicom_reader.TimePoints
        self.__curve(xdata, ydata)

    def __slot_ROI_point(self, pos: QPoint):
        row = pos.y()
        col = pos.x()
        self.spinBox_row.setValue(row)
        self.spinBox_column.setValue(col)

        ydata = self.dicom_reader.img_GroupBySlice[:, row - 1, col - 1]
        xdata = self.dicom_reader.TimePoints
        self.__curve(xdata, ydata)

    def __curve(self, xdata: np.array, ydata: np.array) -> None:
        self.chart.removeAllSeries()
        series = QLineSeries()
        # series = QScatterSeries()





        model = TimePointsTableModel(xdata, ydata)
        self.mapper = QVXYModelMapper(self)
        self.mapper.setXColumn(1)
        self.mapper.setYColumn(2)
        self.mapper.setSeries(series)
        self.mapper.setModel(model)
        self.tableView_points.setModel(model)

        series.setPointsVisible(True)
        series.setMarkerSize(4)
        self.chart.addSeries(series)
        self.chart.createDefaultAxes()

    def _setup(self):
        self.slices = 0

    def __slot_loadstart(self, start: bool):
        if start:
            self.widget_center.setEnabled(False)
            self.widget_center.setVisible(False)
            self.widget_load.setEnabled(True)
            self.widget_load.setVisible(True)

            self.load_progressBar.setMinimum(1)
            slice_num = self.dicom_reader.SliceNum
            timepoints_num = self.dicom_reader.TimePointsNum
            self.load_progressBar.setMaximum(slice_num*timepoints_num)
            self.load_label.setText('Loading ...')

    def __slot_loading(self, value: int):
        self.load_progressBar.setValue(value)

    def __slot_loaded(self, loaded: bool):
        if loaded:
            self.load_label.setText('Loaded')
            self.widget_center.setEnabled(True)
            self.widget_center.setVisible(True)
            self.widget_load.setEnabled(False)
            self.widget_load.setVisible(False)

            self._setupUI()



    @property
    def ROI_color(self) -> QColor:
        return self._ROI_color

    @ROI_color.setter
    def ROI_color(self, color: QColor) -> None:
        self._ROI_color = color
            
      


        