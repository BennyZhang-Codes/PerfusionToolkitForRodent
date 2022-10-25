import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtCore import Qt, Slot, QSize, QModelIndex, QEvent
from PySide6.QtGui import QImage, QPixmap, QIcon, QResizeEvent, QMouseEvent, QCursor, QColor, QWheelEvent

from PySide6.QtWidgets import QWidget, QGraphicsPixmapItem, QGraphicsScene, QMenu, QHBoxLayout
from PySide6.QtWidgets import QListWidgetItem, QListWidget, QGraphicsView, QLabel

from UI.ui_Widget_FAIR import Ui_Widget_FAIR
from modules.dcmreader.read_FAIR import read_FAIR_folder
from modules.threads.FAIR_CBF import Thread_FAIR_CBF_Calc
from modules.FAIR_CBF import _fig_FAIR_Images, _fig_Fitting, _fig_Results, Msel, Msel_abs
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class MyFigure(FigureCanvas):
    def __init__(self, figure=None):
        super().__init__(figure)

class Widget_FAIR(QWidget, Ui_Widget_FAIR):
    def __init__(self, dicom_dir, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.root = dicom_dir
        self.dicom = read_FAIR_folder(self.root)
        self.setupUi(self)
        self._setupUI()

    def _setupUI(self):
        self.graphicsView.set_root(self.root)
        self.graphicsView.set_mainwindow(self.mainwindow)
        self.graphicsView._location.connect(self._slot_location)
        self.graphicsView.dicom_reader = read_FAIR_folder(self.root)

    def _setup(self):
        self.slices = 0

    def _slot_location(self, pos):
        dss_sel, dss_non = self.dicom.dss
        img_sel = []
        img_non = []
        xdata = []
        for ds_sel, ds_non in zip(dss_sel, dss_non):
            xdata.append(ds_sel.InversionTime)
            img_sel.append(np.expand_dims(ds_sel.pixel_array, axis=2))
            img_non.append(np.expand_dims(ds_non.pixel_array, axis=2))
        img_sel = np.concatenate(img_sel, axis=2)
        img_non = np.concatenate(img_non, axis=2)
        xdata = np.array(xdata)

        x = pos[0] - 1
        y = pos[1] - 1
        fig = plt.figure(figsize=(5,5), facecolor='black')
        ax = plt.subplot(111)
        fig.canvas.manager.set_window_title('Fitting')
        ydata_sel = img_sel[x, y]
        ydata_non = img_non[x, y]
        popt_sel, pcov_sel = curve_fit(Msel_abs, xdata, ydata_sel, p0=(1500,10000))
        T1app, M0 = popt_sel
        def Mnon(TI, f):
            T1b = 2800
            Ms = Msel(TI, T1app, M0)
            M_diff = 2*M0*f/0.9 * ((np.exp(-TI/T1app)- np.exp(-TI/T1b))/(1/T1b-1/T1app))
            return np.abs(Ms - M_diff)

        popt_non, pcov_non = curve_fit(Mnon, xdata, ydata_non, p0=(1/60000), bounds=(0, 2000/60000/100))
        f = popt_non*60000*100

        ax.plot(np.arange(0,10000, 2), Msel_abs(np.arange(0, 10000, 2), T1app, M0), color='red', label='Sel', linewidth=1)
        ax.plot(np.arange(0,10000, 2), Mnon(np.arange(0, 10000, 2), f/60000/100), color='yellow', label='Non', linestyle='--', linewidth=1)
        ax.plot(xdata, img_sel[x, y], '*', color='red', label='measured Sel')
        ax.plot(xdata, img_non[x, y], '*', color='yellow', label='measured Non')
        ax.legend(loc='lower right', fontsize=7, labelcolor='w', facecolor='black', frameon=False)

        ax.tick_params('both', colors='w', labelsize=8)
        ax.set_facecolor('black')
        for i in ['top', 'bottom', 'left', 'right']:
            ax.spines[i].set_color('w')
        fig.tight_layout(w_pad=0)
        self.fig_curve = MyFigure(fig)
        for i in range(self.verticalLayout_curve.count()): 
            self.verticalLayout_curve.removeWidget(self.verticalLayout_curve.itemAt(i).widget())
        self.verticalLayout_curve.addWidget(self.fig_curve)

    @Slot()
    def on_pushButton_run_clicked(self):
        self.pushButton_run.setEnabled(False)
        dss = self.dicom.dss

        self.thread_FAIR_CBF_Calc = Thread_FAIR_CBF_Calc(self, dss)
        self.thread_FAIR_CBF_Calc.processing_signal.connect(self._slot_processing)
        self.thread_FAIR_CBF_Calc.processed_signal.connect(self._slot_processed)
        self.thread_FAIR_CBF_Calc.start()

        Fig_FAIR_Images = _fig_FAIR_Images(dss)
        Fig_images = MyFigure(Fig_FAIR_Images)
        Fig_FAIR_Images


    def _slot_processing(self, idx):
        progressBar = self.mainwindow._Status_progressBar
        progressBar.progressBar.setValue(idx)        

    def _slot_processed(self, res: tuple):
        self.img_sel, self.img_non, xdata, T1app_map, M0_map, cbf_map = res
        Fig_Results = _fig_Results(T1app_map.copy(), M0_map.copy(), cbf_map.copy())
        self.verticalLayout_results.addWidget(MyFigure(Fig_Results))
        progressBar = self.mainwindow._Status_progressBar
        progressBar.label.setText('Processed!')
        progressBar.progressBar.setHidden(True)
        self.pushButton_run.setEnabled(True)


        