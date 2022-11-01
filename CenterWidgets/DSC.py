import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from UI.ui_Widget_DSC import Ui_Widget_DSC
from modules.dcmreader.read_DSC_DCE import Read_Bruker_TimeSeries

from modules.utils.shape import shape_to_mask, get_index_of_mask
from MyWidgets.Mmodel.TabelModel import TimePointsTableModel
from MyWidgets.MChart.MChart import MChart
from modules.threads.TimeSeries_correction import Thread_TimeSeries_correction
from modules.threads.DSC import Thread_DSC



class Widget_DSC(QWidget, Ui_Widget_DSC):
    GroupSlice = 'Slice'
    GroupTime = 'Time'
    def __init__(self, dicom_dir, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.root = dicom_dir
        self.setupUi(self)
        
        self.dicom_reader = Read_Bruker_TimeSeries(self.root)
        if self.comboBox.currentText() == 'Slice':
            self.dicom_reader.GroupBy = 'Slice'
            self._groupby = 'Slice'

        self.dicom_reader.signal_loadstart.connect(self.__slot_loadstart)
        self.dicom_reader.signal_loading.connect(self.__slot_loading)
        self.dicom_reader.signal_loaded.connect(self.__slot_loaded)
        
        self._ROI_color = QColor(118,185,172,196)
        
    def _setupUI(self):
        # DSC
        self.progressBar_DSC.setVisible(False)


        
        self.chart = MChart()
        self.chartView.setChart(self.chart)

        self.graphicsView.set_mainwindow(self.mainwindow)
        self.graphicsView.DicomReader = self.dicom_reader
        self.graphicsView.update_scene_Rect()
        item_img = self.graphicsView.mscene.item_img
        item_img.signal.WW_changed.connect(self.spinBox_WW.setValue)
        item_img.signal.WL_changed.connect(self.spinBox_WL.setValue)
        self.graphicsView._idx_changed.connect(self.__slot_graphicsView_idx_changed)
        self.graphicsView.mscene.signal_ROI_point.connect(self.__slot_ROI_point)
        self.graphicsView.mscene.signal_ROI.connect(self.__slot_ROI)
        self.graphicsView.mscene.signal_ROI_color.connect(self.__slot_ROI_color)
        

        # Basic
        self.spinBox_timepoint.setMaximum(self.dicom_reader.len)
        self.spinBox_timepoint.setMinimum(1)
        self.spinBox_timepoint.setValue(self.graphicsView.idx + 1)
        self.verticalScrollBar.setMaximum(self.dicom_reader.len)
        self.verticalScrollBar.setMinimum(1)
        self.verticalScrollBar.setValue(self.graphicsView.idx + 1)

        self.spinBox_slice.setMaximum(self.dicom_reader.SliceNum)
        self.spinBox_slice.setMinimum(1)
        self.spinBox_slice.setValue(self.dicom_reader.CurrentSlice)

        self.spinBox_row.setMaximum(self.dicom_reader.RowNum)
        self.spinBox_row.setMinimum(1)

        self.spinBox_column.setMaximum(self.dicom_reader.ColNum)
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
        center_slice = self.dicom_reader.SliceNum//2
        self.spinBox_row.setValue(center_row)
        self.spinBox_column.setValue(center_col)

        imgall = self.dicom_reader.imgAll[center_slice::self.dicom_reader.SliceNum]
        img_qc = imgall[:,:,center_col].T

        img = img_qc
        img = ((img - img.min()) / max(1, img.max() - img.min()))*255
        img = img.astype(np.uint8)
        image = Image.fromarray(img)
        pix = image.toqpixmap()
        self.label_correction_before_col.setPixmap(pix)
        self.label_correction_before_col.setScaledContents(True)

        img_qc = imgall[:,center_row,:].T

        img = img_qc
        img = ((img - img.min()) / max(1, img.max() - img.min()))*255
        img = img.astype(np.uint8)
        image = Image.fromarray(img)
        pix = image.toqpixmap()
        self.label_correction_before_row.setPixmap(pix)
        self.label_correction_before_row.setScaledContents(True)



        # correction
        self.widget_correction_after.setVisible(False)
        self.widget_correction_after.setEnabled(False)
        self.progressBar_correction.setVisible(False)
        self.radioButton_usecorrected.setEnabled(False)
        self.spinBox_correction.setValue(self.dicom_reader.TimePointsNum//2)
        self.spinBox_correction.setMinimum(1)
        self.spinBox_correction.setMaximum(self.dicom_reader.TimePointsNum)




    def __curve(self, xdata: np.array, ydata: np.array) -> None:
        self.xdata = xdata
        self.ydata = ydata
        model = TimePointsTableModel(xdata, ydata)
        self.tableView.setModel(model)
        self.chart.setModel(model)
        self.chart.selected_point.connect(self.tableView.selectRow)
        self.tableView.changed_rows.connect(self.chart._slot_update_pointConf)
        self.tableView.selected_row.connect(self.chart._update_focus_point)
        
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

      
    ### Basic
    def __slot_graphicsView_idx_changed(self, idx: int):
        self.verticalScrollBar.setValue(idx+1)

    @Slot(int)
    def on_spinBox_timepoint_valueChanged(self, value: int):
        self.dicom_reader.CurrentTimePoint = value - 1 
        if self.GroupBy == self.GroupSlice:
            self.verticalScrollBar.setValue(value)
            self.graphicsView.set_scene(value-1)
        elif self.GroupBy == self.GroupTime:
            self.graphicsView.set_scene(self.graphicsView.idx)
        
    @Slot(int)
    def on_spinBox_slice_valueChanged(self, value: int):
        self.dicom_reader.CurrentSlice = value - 1
        if self.GroupBy == self.GroupTime:
            self.verticalScrollBar.setValue(value)
            self.graphicsView.set_scene(value - 1)
        if self.GroupBy == self.GroupSlice:
            self.graphicsView.set_scene(self.graphicsView.idx)
        
    @Slot(int)
    def on_verticalScrollBar_valueChanged(self, value: int):
        if self.GroupBy == self.GroupSlice:
            self.spinBox_timepoint.setValue(value)
        elif self.GroupBy == self.GroupTime:
            self.spinBox_slice.setValue(value)

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
        self.GroupBy = value

    def update_graphicsView(self) -> None:
        if self.GroupBy == self.GroupSlice:
            self.graphicsView.set_scene(self.spinBox_timepoint.value()-1)
        elif self.GroupBy == self.GroupTime:
            self.graphicsView.set_scene(self.spinBox_slice.value()-1)

    @property
    def GroupBy(self) -> str:
        return self._groupby

    @GroupBy.setter
    def GroupBy(self, value: int) -> None:
        if value == 0:
            self._groupby = 'Slice'
        if value == 1:
            self._groupby = 'Time'

        CurrentSlice = self.dicom_reader.CurrentSlice
        CurrentTimePoint = self.dicom_reader.CurrentTimePoint

        self.dicom_reader.GroupBy = self._groupby
        self.verticalScrollBar.setMaximum(self.dicom_reader.len)
        self.verticalScrollBar.setMinimum(1)
        if self._groupby == self.GroupSlice:
            self.verticalScrollBar.setValue(CurrentTimePoint+1)
        elif self._groupby == self.GroupTime:
            self.verticalScrollBar.setValue(CurrentSlice+1)
        
### ROI
    def __slot_ROI_point(self, pos: QPoint):
        row = pos.y()
        col = pos.x()
        self.spinBox_row.setValue(row)
        self.spinBox_column.setValue(col)

        ydata = self.dicom_reader.img_GroupBySlice[:, row - 1, col - 1]
        xdata = self.dicom_reader.TimePoints
        self.__curve(xdata, ydata)
    @property
    def ROI_color(self) -> QColor:
        return self._ROI_color

    @ROI_color.setter
    def ROI_color(self, color: QColor) -> None:
        self._ROI_color = color

    @property
    def maskIndex(self) -> np.array:
        return self._mask_index

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

        self._mask_index = get_index_of_mask(mask)
        ydata = []
        for idx in self._mask_index:
            ydata.append(self.dicom_reader.img_GroupBySlice[:, idx[0], idx[1]])

        ydata = np.array(ydata)
        xdata = self.dicom_reader.TimePoints
        self.__curve(xdata, np.mean(ydata, axis=0))

        self.widget_mask.setPixmap(pix)
        self.widget_mask_img.setPixmap(item_pix)

    def __slot_ROI_color(self, color: QColor) -> None:
        self.ROI_color = color
  
### Correction
    @Slot()
    def on_pushButton_correction_clicked(self) -> None:
        x = self.checkBox_correction_x.isChecked()
        y = self.checkBox_correction_y.isChecked()
        z = self.checkBox_correction_z.isChecked()
        fixedpoint = self.spinBox_correction.value()

        if x or y or z:
            self.Thread_correction = Thread_TimeSeries_correction()
            self.Thread_correction.TimeSeries_registration.x = x
            self.Thread_correction.TimeSeries_registration.y = y
            self.Thread_correction.TimeSeries_registration.z = z

            self.Thread_correction.set_FixedPoint(fixedpoint)
            self.Thread_correction.set_DicomReader(self.dicom_reader)
            self.Thread_correction.signal_start.connect(self.__slot_correction_start)
            self.Thread_correction.signal_processing.connect(self.__slot_correction_processing)
            self.Thread_correction.signal_end.connect(self.__slot_correction_end)
            self.Thread_correction.start()

    def __slot_correction_start(self, start: bool) -> None:
        if start:
            self.progressBar_correction.setMinimum(0)
            self.progressBar_correction.setMaximum(self.dicom_reader.TimePointsNum)
            self.progressBar_correction.setVisible(True)
            self.progressBar_correction.setEnabled(True)
            self.pushButton_correction.setEnabled(False)
            self.pushButton_correction.setVisible(False)

    def __slot_correction_processing(self, value: int) -> None:
        self.progressBar_correction.setValue(value)

    def __slot_correction_end(self, end: bool) -> None:
        if end:
            self.progressBar_correction.setVisible(False)
            self.progressBar_correction.setEnabled(False)
            self.pushButton_correction.setEnabled(True)
            self.pushButton_correction.setVisible(True)

            self.radioButton_usecorrected.setEnabled(True)

            row, col = self.graphicsView.mscene.item_img.img.shape
            center_row = row//2
            center_col = col//2
            center_slice = self.dicom_reader.SliceNum//2

            imgall = self.dicom_reader._img_corrected[center_slice::self.dicom_reader.SliceNum]
            
            img_qc = imgall[:,:,center_col].T
            img = img_qc
            img = ((img - img.min()) / max(1, img.max() - img.min()))*255
            img = img.astype(np.uint8)
            image = Image.fromarray(img)
            pix = image.toqpixmap()
            self.label_correction_after_col.setPixmap(pix)
            self.label_correction_after_col.setScaledContents(True)

            img_qc = imgall[:,center_row,:].T
            img = img_qc
            img = ((img - img.min()) / max(1, img.max() - img.min()))*255
            img = img.astype(np.uint8)
            image = Image.fromarray(img)
            pix = image.toqpixmap()
            self.label_correction_after_row.setPixmap(pix)
            self.label_correction_after_row.setScaledContents(True)

            self.widget_correction_after.setVisible(True)
            self.widget_correction_after.setEnabled(True)


    @Slot(bool)
    def on_radioButton_usecorrected_clicked(self, clicked: bool) -> None:
        self.dicom_reader.ShowCorrected = self.radioButton_usecorrected.isChecked()
        


### DSC
    @Slot()
    def on_pushButton_DSC_set_AIF_clicked(self) -> None:
        self.AIF = self.ydata

    @Slot(float)
    def on_doubleSpinBox_DSC_TR_valueChanged(self, value: float) -> None:
        self.TR = self.doubleSpinBox_DSC_TR.value() / 1000
        print(self.TR)

    @Slot(float)
    def on_doubleSpinBox_DSC_TE_valueChanged(self, value: float) -> None:
        self.TE = self.doubleSpinBox_DSC_TE.value() / 1000
        print(self.TE)

    @Slot()
    def on_pushButton_DSC_run_clicked(self) -> None:
        self.Thread_DSC = Thread_DSC()

        self.Thread_DSC.signal_start.connect(self.__slot_DSC_start)
        self.Thread_DSC.signal_processing.connect(self.__slot_DSC_processing)
        self.Thread_DSC.signal_end.connect(self.__slot_DSC_end)



    def __slot_DSC_start(self, start: bool) -> None:
        if start:
            self.progressBar_DSC.setMinimum(0)
            # self.progressBar_DSC.setMaximum(self.dicom_reader.TimePointsNum)
            self.progressBar_DSC.setVisible(True)
            self.progressBar_DSC.setEnabled(True)
            self.pushButton_DSC_run.setEnabled(False)
            self.pushButton_DSC_run.setVisible(False)

    def __slot_DSC_processing(self, value: int) -> None:
        self.progressBar_DSC.setValue(value)

    def __slot_DSC_end(self, end: bool) -> None:
        if end:
            self.progressBar_DSC.setVisible(False)
            self.progressBar_DSC.setEnabled(False)
            self.pushButton_DSC_run.setEnabled(True)
            self.pushButton_DSC_run.setVisible(True)

    

    

