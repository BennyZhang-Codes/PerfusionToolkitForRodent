import os
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import CenterWidgets.Browse as Browse
import CenterWidgets.DSC as DSC
import CenterWidgets.FAIR as FAIR

from UI.ui_DockWidget_Start import Ui_DockWidget_Start

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
        self.mainwindow.tabWidget.addTab(FAIR.Widget_FAIR(current_path, self.mainwindow), '(FAIR) {}'.format(os.path.basename(current_path)))

    def _action_dsc(self):
        current_path = self.filesystem_model.filePath(self.treeView.currentIndex())
        self.mainwindow.tabWidget.addTab(DSC.Widget_DSC(current_path, self.mainwindow), '(DSC) {}'.format(os.path.basename(current_path)))

    def _action_opendicomfolder(self):
        current_path = self.filesystem_model.filePath(self.treeView.currentIndex())
        self.mainwindow.tabWidget.addTab(Browse.Widget_Browse(current_path, self.mainwindow), '(Viewer) {}'.format(os.path.basename(current_path)))

    @Slot(QModelIndex)
    def on_treeView_clicked(self, Qmodelidx):
        self.mainwindow.statusBar().showMessage(self.filesystem_model.filePath(Qmodelidx))

