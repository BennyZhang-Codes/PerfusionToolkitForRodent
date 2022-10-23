import sys
import os
import numpy as np

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QImage, QPixmap, QIcon

import qdarkstyle

from ui_Main_Window import Ui_MainWindow
from DockWidgets import DockWidget_Start, DockWidget_FAIR
from Widget_Browse import Widget_Browse
from Widget_FAIR import Widget_FAIR
from Widget_DSC import Widget_DSC
from MyWidgets.Status import Status_progressBar

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        # themeFile = 'themes/py_dracula_light.qss'
        # self.sheet = open(themeFile, 'r').read()
        self.setupUi(self)
        self.add_dockWidgets()
        self._setup()
        self.statusBar().showMessage('Ready')
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        # self.setStyleSheet('''MGraphicsView{background-color: rgb(0, 0, 0); padding: 0px; border: 0px}''')

    def _setup(self):
        self._Status_progressBar = Status_progressBar(self.statusBar())
        self._Status_progressBar.setHidden(True)
        self.statusBar().addPermanentWidget(self._Status_progressBar)
        root = r'E:\PySide6\examplefiles\E7_DCE_FLASH'
        self.tabWidget.addTab(Widget_DSC(root, self), root)
        root = r'E:\PySide6\examplefiles'
        self.tabWidget.addTab(Widget_Browse(root, self), root)
        # root = r'E:\A30\FAIR\19\pdata\1\dicom'
        # self.tabWidget.addTab(Widget_FAIR(root, self), root)

    @Slot(int)
    def on_tabWidget_tabCloseRequested(self, idx):
        '''删除部件？'''
        self.tabWidget.removeTab(idx)

    def add_dockWidgets(self):
        self.dockWidget_Start = DockWidget_Start(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget_Start)

        self.dockWidget_FAIR = DockWidget_FAIR(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget_FAIR)
        self.dockWidget_FAIR.hide()

    @Slot()
    def on_actionStart_triggered(self):
        self.dockWidget_Start.show()
        

    @Slot()
    def on_actionFAIR_triggered(self):
        self.dockWidget_FAIR.show()

    @Slot()
    def on_actionSelect_Dicom_Folder_triggered(self):
        self.root = QFileDialog.getExistingDirectory(self,"Choose Folder",r"C:\Users\Administrator\Desktop\\")

        subwindow = Widget_Browse(self.root, self)
        self.tabWidget.addTab(Widget_Browse(self.root, self), self.root)

app = QApplication(sys.argv)
window = MainWindow()
# window.setWindowFlags(Qt.FramelessWindowHint)

# window.showMaximized()'
window.show()



sys.exit(app.exec())