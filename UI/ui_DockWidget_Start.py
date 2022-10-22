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
    QHBoxLayout, QHeaderView, QListWidget, QListWidgetItem,
    QSizePolicy, QTabWidget, QTreeView, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_DockWidget_Start(object):
    def setupUi(self, DockWidget_Start):
        if not DockWidget_Start.objectName():
            DockWidget_Start.setObjectName(u"DockWidget_Start")
        DockWidget_Start.resize(461, 714)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.horizontalLayout = QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tab_Browse = QWidget()
        self.tab_Browse.setObjectName(u"tab_Browse")
        self.verticalLayout = QVBoxLayout(self.tab_Browse)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.treeView = QTreeView(self.tab_Browse)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setFrameShape(QFrame.NoFrame)
        self.treeView.setFrameShadow(QFrame.Plain)
        self.treeView.setLineWidth(0)
        self.treeView.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.treeView.setExpandsOnDoubleClick(True)

        self.verticalLayout.addWidget(self.treeView)

        self.tabWidget.addTab(self.tab_Browse, "")
        self.tab_Thumbnail = QWidget()
        self.tab_Thumbnail.setObjectName(u"tab_Thumbnail")
        self.verticalLayout_2 = QVBoxLayout(self.tab_Thumbnail)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.tab_Thumbnail)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setFrameShape(QFrame.NoFrame)
        self.listWidget.setFrameShadow(QFrame.Plain)
        self.listWidget.setLineWidth(0)

        self.verticalLayout_2.addWidget(self.listWidget)

        self.tabWidget.addTab(self.tab_Thumbnail, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        DockWidget_Start.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_Start)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DockWidget_Start)
    # setupUi

    def retranslateUi(self, DockWidget_Start):
        DockWidget_Start.setWindowTitle(QCoreApplication.translate("DockWidget_Start", u"Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Browse), QCoreApplication.translate("DockWidget_Start", u"Browse", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Thumbnail), QCoreApplication.translate("DockWidget_Start", u"Thumbnail", None))
    # retranslateUi

