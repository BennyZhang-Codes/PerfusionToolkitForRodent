import numpy as np

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCharts import *
from UI.ui_Widget_FAIR import Ui_Widget_FAIR
from modules.dcmreader.read_FAIR import read_FAIR_folder
from modules.threads.FAIR import Thread_FAIR_CBF
from MyWidgets.MChart.MChart_FAIR import MChart_FAIR

from modules.utils.shape import get_index_of_mask

class Widget_FAIR(QWidget, Ui_Widget_FAIR):
    ShowSel = 'Selective'
    ShowNon = 'Non-Selective'
    def __init__(self, dicom_dir, mainwindow):
        super().__init__()
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.root = dicom_dir
        self.DicomReader = read_FAIR_folder(self.root)
        self._mask_index: np.array = None
        self._setupUI()
        self._ROI_color = QColor(118,185,172,196)

    def _setupUI(self):
        self.groupBox_ROI.setEnabled(False)
        self.groupBox_Results.setEnabled(False)
    
        self.chart = MChart_FAIR()


        self.chartView.setChart(self.chart)
        self.graphicsView.set_mainwindow(self.mainwindow)
        self.graphicsView.DicomReader = self.DicomReader
        self.graphicsView.update_scene_Rect()
        item_img = self.graphicsView.mscene.item_img
        item_img.signal.WW_changed.connect(self.spinBox_WW.setValue)
        item_img.signal.WL_changed.connect(self.spinBox_WL.setValue)
        self.graphicsView._idx_changed.connect(self.__slot_graphicsView_idx_changed)
        self.graphicsView.mscene.signal_ROI_point.connect(self.__slot_ROI_point)
        self.graphicsView.mscene.signal_ROI.connect(self.__slot_ROI)
        self.graphicsView.mscene.signal_ROI_color.connect(self.__slot_ROI_color)

        # Basic
        self.spinBox_timepoint.setMaximum(self.DicomReader.len)
        self.spinBox_timepoint.setMinimum(1)
        self.spinBox_timepoint.setValue(self.graphicsView.idx + 1)
        self.verticalScrollBar.setMaximum(self.DicomReader.len)
        self.verticalScrollBar.setMinimum(1)
        self.verticalScrollBar.setValue(self.graphicsView.idx + 1)

        self.spinBox_slice.setMaximum(self.DicomReader.SliceNum)
        self.spinBox_slice.setMinimum(1)
        self.spinBox_slice.setValue(self.DicomReader.CurrentSlice)

        self.spinBox_row.setMaximum(self.DicomReader.RowNum)
        self.spinBox_row.setMinimum(1)

        self.spinBox_column.setMaximum(self.DicomReader.ColNum)
        self.spinBox_column.setMinimum(1)

        img = item_img.img
        max_value = np.max(img)
        min_value = np.min(img)
        WL = (max_value+min_value)/2
        WW = max(0, max_value-min_value)
        self.spinBox_WW.setMaximum(item_img.WW_max)
        self.spinBox_WW.setMinimum(item_img.WW_min)
        self.spinBox_WW.setValue(WW)

        self.spinBox_WL.setMaximum(item_img.WL_max)
        self.spinBox_WL.setMinimum(item_img.WL_min)
        self.spinBox_WL.setValue(WL)

        row, col = img.shape
        center_row = row//2
        center_col = col//2
        center_slice = self.DicomReader.SliceNum//2
        self.spinBox_row.setValue(center_row)
        self.spinBox_column.setValue(center_col)

        # FAIR
        self.progressBar_FAIR.setVisible(False)

        # results
        self.widget_result_CBF.label.setText('CBF')



    # FAIR
    @Slot()
    def on_pushButton_FAIR_run_clicked(self):

        self.thread_CBF = Thread_FAIR_CBF()
        self.thread_CBF.DicomReader = self.DicomReader
        self.thread_CBF.maskIndex = self.maskIndex
        self.thread_CBF.T1blood = self._check_T1blood()
        self.thread_CBF.signal_start.connect(self.__slot_FAIR_start)
        self.thread_CBF.signal_processing.connect(self.__slot_FAIR_processing)
        self.thread_CBF.signal_end.connect(self.__slot_FAIR_end)
        self.thread_CBF.start()


    def __slot_FAIR_start(self, start: bool) -> None:
        if start:
            self.progressBar_FAIR.setMinimum(1)
            self.progressBar_FAIR.setMaximum(len(self.maskIndex))
            
            self.progressBar_FAIR.setEnabled(True)
            self.progressBar_FAIR.setVisible(True)
            self.pushButton_FAIR_run.setEnabled(False)
            self.pushButton_FAIR_run.setVisible(False)

    def __slot_FAIR_processing(self, value: int) -> None:
        self.progressBar_FAIR.setValue(value)

    def __slot_FAIR_end(self, CBF: tuple) -> None:
        self.progressBar_FAIR.setVisible(False)
        self.progressBar_FAIR.setEnabled(False)
        self.pushButton_FAIR_run.setEnabled(True)
        self.pushButton_FAIR_run.setVisible(True)

        self.groupBox_Results.setEnabled(True)

        self.widget_result_CBF.setImageArray(CBF[0])

    # @Slot(float)
    # def on_doubleSpinBox_T1blood_valueChanged(self, value: float):
    #     print(self.doubleSpinBox_T1blood.value())
    def _check_T1blood(self) -> float:
        t1b = self.doubleSpinBox_T1blood.value()
        if t1b == 0:
            print(123)
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle('Warning')
            msgBox.setText('T1 of blood should not be 0!')

            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.exec()
        return t1b


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


    # mscene
    def __slot_ROI(self, data: tuple):
        path, item_pix = data
        self.groupBox_ROI.setEnabled(True)

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
        self.maskIndex = get_index_of_mask(mask)
        sel_ydata = []
        non_ydata = []
        for idx in self.maskIndex:
            sel_ydata.append(self.DicomReader._sel_img_all[:, idx[0], idx[1]])
            non_ydata.append(self.DicomReader._non_img_all[:, idx[0], idx[1]])

        sel_ydata = np.array(sel_ydata)
        non_ydata = np.array(non_ydata)
        xdata = self.DicomReader.TimePoints
        self.__curve(xdata, np.mean(sel_ydata, axis=0), np.mean(non_ydata, axis=0))

        self.widget_mask.setPixmap(pix)
        self.widget_mask_img.setPixmap(item_pix)

    def __slot_ROI_point(self, pos: QPoint):
        row = pos.y()
        col = pos.x()
        self.spinBox_row.setValue(row)
        self.spinBox_column.setValue(col)

        sel_ydata = self.DicomReader._sel_img_all[:, row - 1, col - 1]
        non_ydata = self.DicomReader._non_img_all[:, row - 1, col - 1]
        xdata = self.DicomReader.TimePoints
        self.__curve(xdata, sel_ydata, non_ydata)

    def __slot_ROI_color(self, color: QColor) -> None:
        self.ROI_color = color
    
    @property
    def maskIndex(self) -> np.array:
        if self._mask_index is None:
            row = self.DicomReader.RowNum
            col = self.DicomReader.ColNum
            self._mask_index = get_index_of_mask(np.ones((row, col)))
        return self._mask_index

    @maskIndex.setter
    def maskIndex(self, index: np.array) -> None:
        self._mask_index = index

    @property
    def ROI_color(self) -> QColor:
        return self._ROI_color

    @ROI_color.setter
    def ROI_color(self, color: QColor) -> None:
        self._ROI_color = color

    ### Basic
    def __slot_graphicsView_idx_changed(self, idx: int):
        self.verticalScrollBar.setValue(idx+1)

    @Slot(int)
    def on_spinBox_timepoint_valueChanged(self, value: int):
        self.DicomReader.CurrentTimePoint = value - 1 
        self.verticalScrollBar.setValue(value)
        self.graphicsView.set_scene(value-1)

    @Slot(int)
    def on_spinBox_slice_valueChanged(self, value: int):
        self.DicomReader.CurrentSlice = value - 1
        self.graphicsView.set_scene(self.graphicsView.idx)
        
    @Slot(int)
    def on_verticalScrollBar_valueChanged(self, value: int):
        self.spinBox_timepoint.setValue(value)

    @Slot(int)
    def on_spinBox_row_valueChanged(self, value: int):
        row = value
        col = self.spinBox_column.value()
        sel_ydata = self.DicomReader._sel_img_all[:, row - 1, col - 1]
        non_ydata = self.DicomReader._non_img_all[:, row - 1, col - 1]
        xdata = self.DicomReader.TimePoints
        self.__curve(xdata, sel_ydata, non_ydata)

    @Slot(int)
    def on_spinBox_column_valueChanged(self, value: int):
        row = self.spinBox_row.value()
        col = value
        sel_ydata = self.DicomReader._sel_img_all[:, row - 1, col - 1]
        non_ydata = self.DicomReader._non_img_all[:, row - 1, col - 1]
        xdata = self.DicomReader.TimePoints
        self.__curve(xdata, sel_ydata, non_ydata)

    @Slot(int)
    def on_spinBox_WL_valueChanged(self, value: int):
        self.graphicsView.mscene.item_img.WL = value
        self.update_graphicsView()

    @Slot(int)
    def on_spinBox_WW_valueChanged(self, value: int):
        self.graphicsView.mscene.item_img.WW = value
        self.update_graphicsView()

    @Slot(int)
    def on_comboBox_currentIndexChanged(self, value: int) -> None:
        print(value)

        if value == 0:
            self.DicomReader.ShowMode = self.DicomReader.ShowSel
        elif value == 1:
            self.DicomReader.ShowMode = self.DicomReader.ShowNon
        self.update_graphicsView()

    def update_graphicsView(self) -> None:
        self.graphicsView.set_scene(self.spinBox_timepoint.value()-1)

    def __curve(self, xdata, sel_ydata, non_ydata) -> None:
        self.chart.setData(xdata, sel_ydata, non_ydata)
        
        # sel_scatter = QScatterSeries()
        # non_scatter = QScatterSeries()

        # for x, sel, non in zip(xdata, sel_ydata, non_ydata):
        #     sel_scatter.append(QPointF(x, sel))
        #     non_scatter.append(QPointF(x, non))

        # self.chart.removeAllSeries()
        # self.chart.addSeries(sel_scatter)
        # self.chart.addSeries(non_scatter)
        # self.chart.createDefaultAxes()
    


