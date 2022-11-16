# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DockWidget_Start.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDockWidget, QFrame,
    QHeaderView, QSizePolicy, QTreeView, QVBoxLayout,
    QWidget)
import UI.icons_rc

class Ui_DockWidget_Start(object):
    def setupUi(self, DockWidget_Start):
        if not DockWidget_Start.objectName():
            DockWidget_Start.setObjectName(u"DockWidget_Start")
        DockWidget_Start.resize(461, 714)
        DockWidget_Start.setMinimumSize(QSize(100, 110))
        icon = QIcon()
        icon.addFile(u":/\u65b0\u524d\u7f00/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        DockWidget_Start.setWindowIcon(icon)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeView = QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setFrameShape(QFrame.NoFrame)
        self.treeView.setFrameShadow(QFrame.Plain)
        self.treeView.setLineWidth(0)
        self.treeView.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.treeView.setExpandsOnDoubleClick(True)

        self.verticalLayout.addWidget(self.treeView)

        DockWidget_Start.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_Start)

        QMetaObject.connectSlotsByName(DockWidget_Start)
    # setupUi

    def retranslateUi(self, DockWidget_Start):
        DockWidget_Start.setWindowTitle(QCoreApplication.translate("DockWidget_Start", u"Select Folder", None))
    # retranslateUi

