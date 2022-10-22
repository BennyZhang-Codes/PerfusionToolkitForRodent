from PySide6.QtCore import Qt, Slot, QSize, QModelIndex, QEvent, qDebug
from PySide6.QtGui import QImage, QPixmap, QIcon, QResizeEvent, QMouseEvent, QCursor, QColor, QWheelEvent

from PySide6.QtWidgets import QWidget, QGraphicsPixmapItem, QGraphicsScene, QMenu, QHBoxLayout
from PySide6.QtWidgets import QListWidgetItem, QListWidget, QGraphicsView, QLabel
from PySide6.QtGui import QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QScatterSeries

from UI.ui_Widget_DSC import Ui_Widget_DSC
from modules.dcmreader.read_DSC_DCE import read_DSC_DCE_folder

class Widget_DSC(QWidget, Ui_Widget_DSC):
    def __init__(self, dicom_dir, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.root = dicom_dir
        self.dicom_reader = read_DSC_DCE_folder(self.root)
        self.dicom_reader._loadstart.connect(self.__slot_loadstart)
        self.dicom_reader._loading.connect(self.__slot_loading)
        self.dicom_reader._loaded.connect(self.__slot_loaded)
        self.setupUi(self)
        

    def _setupUI(self):
        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.legend().hide()
        
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chartView.setChart(self.chart)

        self.graphicsView.set_mainwindow(self.mainwindow)
        self.graphicsView.set_dicom_reader(self.dicom_reader)
        self.graphicsView._slice.connect(self.__slot_graphicsView_slice)
        self.graphicsView._idx_changed.connect(self.__slot_graphicsView_idx_changed)
        self.graphicsView._location.connect(self.__slot_graphicsView_location)
        
        

        self.spinBox_timepoint.setMaximum(self.dicom_reader.max_idx() + 1)
        self.spinBox_timepoint.setMinimum(self.dicom_reader.min_idx() + 1)
        self.spinBox_timepoint.setValue(self.graphicsView.idx + 1)
        self.verticalScrollBar.setMaximum(self.dicom_reader.max_idx() + 1)
        self.verticalScrollBar.setMinimum(self.dicom_reader.min_idx() + 1)
        self.verticalScrollBar.setValue(self.graphicsView.idx + 1)

        self.spinBox_slice.setMaximum(self.dicom_reader.get_slice_num())
        self.spinBox_slice.setMinimum(1)
        self.spinBox_slice.setValue(self.dicom_reader.get_current_slice())

        self.spinBox_row.setMaximum(self.dicom_reader.get_row())
        self.spinBox_row.setMinimum(1)

        self.spinBox_column.setMaximum(self.dicom_reader.get_column())
        self.spinBox_column.setMinimum(1)

    def __item_img(self, event: QMouseEvent):
        print('clicked')

    def __slot_graphicsView_slice(self, idx: int):
        self.dicom_reader.set_slice(idx)
        self.graphicsView.set_scene(self.graphicsView.idx)
        self.spinBox_slice.setValue(idx+1)

    def __slot_graphicsView_idx_changed(self, idx: int):
        self.verticalScrollBar.setValue(idx+1)


    @Slot(int)
    def on_spinBox_timepoint_valueChanged(self, value: int):
        self.graphicsView.set_scene(value-1)
        self.verticalScrollBar.setValue(value)

    @Slot(int)
    def on_spinBox_slice_valueChanged(self, value: int):
        self.dicom_reader.set_slice(value - 1)
        self.graphicsView.set_scene(self.graphicsView.idx)
        self.__curve(self.spinBox_row.value(), self.spinBox_column.value())

    @Slot(int)
    def on_verticalScrollBar_valueChanged(self, value: int):
        self.spinBox_timepoint.setValue(value)

    @Slot(int)
    def on_spinBox_row_valueChanged(self, value: int):
        self.__curve(value, self.spinBox_column.value())

    @Slot(int)
    def on_spinBox_column_valueChanged(self, value: int):
        self.__curve(self.spinBox_row.value(), value)

    def __slot_graphicsView_location(self, pos: tuple):
        row, col = pos
        self.spinBox_row.setValue(row)
        self.spinBox_column.setValue(col)
        self.__curve(row, col)

    def __curve(self, row: int, col: int) -> None:
        ydata = self.dicom_reader.get_imgs_curSlice()[:, row - 1, col - 1]
        self.chart.removeAllSeries()
        series = QLineSeries()
        for time_point, value in zip(self.dicom_reader.get_time_points(), ydata):
            series.append(time_point, value)
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
            slice_num = self.dicom_reader.get_slice_num()
            timepoints_num = self.dicom_reader.get_time_points_num()
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
            self.dicom_reader.set_slice(0)

            self._setupUI()
            self.graphicsView.item_img.mouseDoubleClickEvent = self.__item_img
            
      


        