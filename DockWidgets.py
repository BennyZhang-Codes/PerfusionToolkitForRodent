import os
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QDockWidget, QFileSystemModel, QMenu
from PySide6.QtCore import Slot, QDir, QModelIndex, Qt
from PySide6.QtGui import QCursor
from Widget_DSC import Widget_DSC
from Widget_FAIR import Widget_FAIR

from UI.ui_DockWidget_Start import Ui_DockWidget_Start
from UI.ui_DockWidget_FAIR import Ui_DockWidget_FAIR
from Widget_Browse import Widget_Browse

class DockWidget_Start(QDockWidget, Ui_DockWidget_Start):
    def __init__(self, mainwindow) -> None:
        super().__init__()
        self.mainwindow = mainwindow
        self.setupUi(self)
        self._setup()
        
    def _setup(self):
        self.filesystem_model = QFileSystemModel()
        self.filesystem_model.setRootPath('')
        self.filesystem_model.setFilter(QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot)
        self.treeView.setModel(self.filesystem_model)
        self.treeView.setHeaderHidden(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.treeview_pop_menu)
        for col in range(1, 4):
            self.treeView.setColumnHidden(col, True)
    
    def treeview_pop_menu(self, pos):
        menu = QMenu(self.treeView)
        action_open = menu.addAction('Open as DICOM folder')
        action_open.triggered.connect(self._action_opendicomfolder)
        action_fair = menu.addAction('FAIR')
        action_fair.triggered.connect(self._action_fair)
        action_dsc = menu.addAction('DSC')
        action_dsc.triggered.connect(self._action_dsc)
        menu.exec_(QCursor.pos())

    def _action_fair(self):
        current_path = self.filesystem_model.filePath(self.treeView.currentIndex())
        self.mainwindow.tabWidget.addTab(Widget_FAIR(current_path, self.mainwindow), current_path)

    def _action_dsc(self):
        current_path = self.filesystem_model.filePath(self.treeView.currentIndex())
        self.mainwindow.tabWidget.addTab(Widget_DSC(current_path, self.mainwindow), current_path)

    def _action_opendicomfolder(self):
        '''添加tab'''
        current_path = self.filesystem_model.filePath(self.treeView.currentIndex())
        self.mainwindow.tabWidget.addTab(Widget_Browse(current_path, self.mainwindow), current_path)

    @Slot(QModelIndex)
    def on_treeView_clicked(self, Qmodelidx):
        self.mainwindow.statusBar().showMessage(self.filesystem_model.filePath(Qmodelidx))


class DockWidget_FAIR(QDockWidget, Ui_DockWidget_FAIR):
    def __init__(self, mainwindow) -> None:
        super().__init__()
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.dcm_path = r'E:\A30\19\pdata\1\dicom'

    @Slot()
    def on_pushButton_RUN_clicked(self):
        print('FAIR_pushButton_RUN')