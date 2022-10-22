# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget_FAIR.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from MyWidgets.MGraphicsView import MGraphicsView

class Ui_Widget_FAIR(object):
    def setupUi(self, Widget_FAIR):
        if not Widget_FAIR.objectName():
            Widget_FAIR.setObjectName(u"Widget_FAIR")
        Widget_FAIR.resize(1120, 499)
        self.verticalLayout_2 = QVBoxLayout(Widget_FAIR)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Widget_FAIR)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_browse = QWidget(self.widget)
        self.widget_browse.setObjectName(u"widget_browse")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_browse.sizePolicy().hasHeightForWidth())
        self.widget_browse.setSizePolicy(sizePolicy)
        self.widget_browse.setMinimumSize(QSize(0, 0))
        self.widget_browse.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_browse)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = MGraphicsView(self.widget_browse)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy1)
        self.graphicsView.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_2.addWidget(self.graphicsView)

        self.widget_curve = QWidget(self.widget_browse)
        self.widget_curve.setObjectName(u"widget_curve")
        self.verticalLayout_curve = QVBoxLayout(self.widget_curve)
        self.verticalLayout_curve.setSpacing(0)
        self.verticalLayout_curve.setObjectName(u"verticalLayout_curve")
        self.verticalLayout_curve.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(self.widget_curve)

        self.widget_2 = QWidget(self.widget_browse)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")

        self.horizontalLayout.addWidget(self.widget_4)

        self.pushButton_run = QPushButton(self.widget_2)
        self.pushButton_run.setObjectName(u"pushButton_run")

        self.horizontalLayout.addWidget(self.pushButton_run)


        self.horizontalLayout_2.addWidget(self.widget_2)


        self.verticalLayout_4.addWidget(self.widget_browse)


        self.verticalLayout.addWidget(self.widget)

        self.widget_results = QWidget(Widget_FAIR)
        self.widget_results.setObjectName(u"widget_results")
        self.widget_results.setMinimumSize(QSize(0, 200))
        self.verticalLayout_results = QVBoxLayout(self.widget_results)
        self.verticalLayout_results.setSpacing(0)
        self.verticalLayout_results.setObjectName(u"verticalLayout_results")
        self.verticalLayout_results.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.widget_results)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Widget_FAIR)

        QMetaObject.connectSlotsByName(Widget_FAIR)
    # setupUi

    def retranslateUi(self, Widget_FAIR):
        Widget_FAIR.setWindowTitle(QCoreApplication.translate("Widget_FAIR", u"Form", None))
        self.pushButton_run.setText(QCoreApplication.translate("Widget_FAIR", u"PushButton", None))
    # retranslateUi

