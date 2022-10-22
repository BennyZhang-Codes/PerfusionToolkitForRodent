# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DockWidget_FAIR.ui'
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
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTreeView, QVBoxLayout,
    QWidget)

class Ui_DockWidget_FAIR(object):
    def setupUi(self, DockWidget_FAIR):
        if not DockWidget_FAIR.objectName():
            DockWidget_FAIR.setObjectName(u"DockWidget_FAIR")
        DockWidget_FAIR.resize(461, 736)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.dockWidgetContents)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 100))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_Slices = QLabel(self.frame)
        self.label_Slices.setObjectName(u"label_Slices")
        sizePolicy.setHeightForWidth(self.label_Slices.sizePolicy().hasHeightForWidth())
        self.label_Slices.setSizePolicy(sizePolicy)
        self.label_Slices.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_3.addWidget(self.label_Slices)

        self.label_numofSlices = QLabel(self.frame)
        self.label_numofSlices.setObjectName(u"label_numofSlices")
        sizePolicy.setHeightForWidth(self.label_numofSlices.sizePolicy().hasHeightForWidth())
        self.label_numofSlices.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_numofSlices)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_TIs = QLabel(self.frame)
        self.label_TIs.setObjectName(u"label_TIs")
        self.label_TIs.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_2.addWidget(self.label_TIs)

        self.label_numofTIs = QLabel(self.frame)
        self.label_numofTIs.setObjectName(u"label_numofTIs")

        self.horizontalLayout_2.addWidget(self.label_numofTIs)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.pushButton_RUN = QPushButton(self.frame)
        self.pushButton_RUN.setObjectName(u"pushButton_RUN")
        self.pushButton_RUN.setMaximumSize(QSize(50, 16777215))
        font = QFont()
        font.setFamilies([u"Tw Cen MT"])
        font.setPointSize(10)
        self.pushButton_RUN.setFont(font)
        self.pushButton_RUN.setCheckable(False)
        self.pushButton_RUN.setAutoDefault(False)
        self.pushButton_RUN.setFlat(False)

        self.horizontalLayout_4.addWidget(self.pushButton_RUN)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.frame)

        self.tabWidget = QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.treeView = QTreeView(self.tab_3)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEnabled(True)

        self.verticalLayout_4.addWidget(self.treeView)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)

        DockWidget_FAIR.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_FAIR)

        self.pushButton_RUN.setDefault(False)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DockWidget_FAIR)
    # setupUi

    def retranslateUi(self, DockWidget_FAIR):
        DockWidget_FAIR.setWindowTitle(QCoreApplication.translate("DockWidget_FAIR", u"FAIR", None))
        self.label_Slices.setText(QCoreApplication.translate("DockWidget_FAIR", u"Slices", None))
        self.label_numofSlices.setText(QCoreApplication.translate("DockWidget_FAIR", u"0", None))
        self.label_TIs.setText(QCoreApplication.translate("DockWidget_FAIR", u"TIs", None))
        self.label_numofTIs.setText(QCoreApplication.translate("DockWidget_FAIR", u"0", None))
        self.pushButton_RUN.setText(QCoreApplication.translate("DockWidget_FAIR", u"RUN", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("DockWidget_FAIR", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("DockWidget_FAIR", u"Tab 2", None))
    # retranslateUi

