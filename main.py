import sys
import os

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from UI.ui_Main_Window import Ui_MainWindow
import qdarkstyle

from DockWidgets.Start import DockWidget_Start
import CenterWidgets.Browse as Browse
import CenterWidgets.DSC as DSC
import CenterWidgets.FAIR as FAIR

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)

        self.add_dockWidgets()
        self._setup()
        self.statusBar().showMessage('Ready')

        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        # self.theme()

    def theme(self):
        themeFile = 'dark.qss'
        self.sheet = open(themeFile, 'r').read()
        str = open(themeFile, 'r').read()
        self.setStyleSheet(str)
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        # self.setStyleSheet('''MGraphicsView{background-color: rgb(0, 0, 0); padding: 0px; border: 0px}''')

    def _setup(self):

        # root = r'E:\ISMRM2023\Example\Example_mice_DSC'
        # self.tabWidget.addTab(DSC.Widget_DSC(root, self), '(DSC) {}'.format(os.path.basename(root)))

        # root = r'E:\PySide6\examplefiles\E7_DCE_FLASH'
        # self.tabWidget.addTab(DSC.Widget_DSC(root, self), '(DSC) {}'.format(os.path.basename(root)))

        # root = r'E:\ISMRM2023\Example\Example_mice_T2'
        # self.tabWidget.addTab(Browse.Widget_Browse(root, self), '(Viewer) {}'.format(os.path.basename(root)))

        root = r'E:\ISMRM2023\Example\Example_mice_FAIR\pdata\1\dicom'
        self.tabWidget.addTab(FAIR.Widget_FAIR(root, self), '(FAIR) {}'.format(os.path.basename(root)))

    @Slot(int)
    def on_tabWidget_tabCloseRequested(self, idx):
        '''删除部件？'''
        self.tabWidget.removeTab(idx)

    def add_dockWidgets(self):
        self.dockWidget_Start = DockWidget_Start(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget_Start)

    @Slot()
    def on_actionStart_triggered(self):
        self.dockWidget_Start.show()
        

    @Slot()
    def on_actionSelect_Dicom_Folder_triggered(self):
        self.root = QFileDialog.getExistingDirectory(self,"Choose Folder",r"C:\Users\Administrator\Desktop\\")

        subwindow = Browse.Widget_Browse(self.root, self)
        self.tabWidget.addTab(Browse.Widget_Browse(self.root, self), self.root)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.setWindowFlags(Qt.FramelessWindowHint)
    # window.showMaximized()'
    window.show()
    sys.exit(app.exec())