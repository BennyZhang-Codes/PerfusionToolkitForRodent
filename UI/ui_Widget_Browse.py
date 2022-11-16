# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget_Browse.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QListView, QListWidget, QListWidgetItem, QScrollBar,
    QSizePolicy, QSplitter, QWidget)

from MyWidgets.MGraphicsView.MGraphicsView import MGraphicsView

class Ui_Widget_Browse(object):
    def setupUi(self, Widget_Browse):
        if not Widget_Browse.objectName():
            Widget_Browse.setObjectName(u"Widget_Browse")
        Widget_Browse.resize(960, 602)
        self.horizontalLayout_2 = QHBoxLayout(Widget_Browse)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Widget_Browse)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.listWidget = QListWidget(self.splitter)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setBaseSize(QSize(0, 0))
        self.listWidget.setFrameShape(QFrame.NoFrame)
        self.listWidget.setFrameShadow(QFrame.Plain)
        self.listWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listWidget.setIconSize(QSize(0, 0))
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.listWidget.setMovement(QListView.Static)
        self.listWidget.setFlow(QListView.LeftToRight)
        self.listWidget.setResizeMode(QListView.Adjust)
        self.listWidget.setLayoutMode(QListView.SinglePass)
        self.listWidget.setSpacing(0)
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setItemAlignment(Qt.AlignCenter)
        self.listWidget.setSortingEnabled(False)
        self.splitter.addWidget(self.listWidget)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = MGraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setFrameShape(QFrame.NoFrame)
        self.graphicsView.setFrameShadow(QFrame.Plain)
        self.graphicsView.setLineWidth(0)
        self.graphicsView.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.graphicsView)

        self.verticalScrollBar_Image = QScrollBar(self.layoutWidget)
        self.verticalScrollBar_Image.setObjectName(u"verticalScrollBar_Image")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(10)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.verticalScrollBar_Image.sizePolicy().hasHeightForWidth())
        self.verticalScrollBar_Image.setSizePolicy(sizePolicy1)
        self.verticalScrollBar_Image.setOrientation(Qt.Vertical)

        self.horizontalLayout.addWidget(self.verticalScrollBar_Image)

        self.splitter.addWidget(self.layoutWidget)

        self.horizontalLayout_2.addWidget(self.splitter)


        self.retranslateUi(Widget_Browse)

        QMetaObject.connectSlotsByName(Widget_Browse)
    # setupUi

    def retranslateUi(self, Widget_Browse):
        Widget_Browse.setWindowTitle(QCoreApplication.translate("Widget_Browse", u"Form", None))
    # retranslateUi

