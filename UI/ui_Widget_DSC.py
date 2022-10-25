# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget_DSC.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QScrollArea, QScrollBar, QSizePolicy,
    QSpacerItem, QSpinBox, QSplitter, QTabWidget,
    QToolBox, QVBoxLayout, QWidget)

from MyWidgets.MGraphicsView_timeseries import MGraphicsView_timeseries

class Ui_Widget_DSC(object):
    def setupUi(self, Widget_DSC):
        if not Widget_DSC.objectName():
            Widget_DSC.setObjectName(u"Widget_DSC")
        Widget_DSC.resize(1065, 795)
        self.verticalLayout_5 = QVBoxLayout(Widget_DSC)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_center = QWidget(Widget_DSC)
        self.widget_center.setObjectName(u"widget_center")
        self.verticalLayout = QVBoxLayout(self.widget_center)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter_3 = QSplitter(self.widget_center)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Vertical)
        self.widget = QWidget(self.splitter_3)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_8 = QVBoxLayout(self.widget)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.widget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.widget1 = QWidget(self.splitter_2)
        self.widget1.setObjectName(u"widget1")
        self.horizontalLayout_3 = QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = MGraphicsView_timeseries(self.widget1)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout_3.addWidget(self.graphicsView)

        self.verticalScrollBar = QScrollBar(self.widget1)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.horizontalLayout_3.addWidget(self.verticalScrollBar)

        self.widget_tools = QWidget(self.widget1)
        self.widget_tools.setObjectName(u"widget_tools")
        self.verticalLayout_7 = QVBoxLayout(self.widget_tools)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 5, 5, 5)
        self.splitter = QSplitter(self.widget_tools)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.widget2 = QWidget(self.splitter)
        self.widget2.setObjectName(u"widget2")
        self.horizontalLayout_18 = QHBoxLayout(self.widget2)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(self.widget2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_8.addWidget(self.label_5)

        self.comboBox = QComboBox(self.widget2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_8.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.widget2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.spinBox_slice = QSpinBox(self.widget2)
        self.spinBox_slice.setObjectName(u"spinBox_slice")
        self.spinBox_slice.setValue(1)

        self.horizontalLayout_2.addWidget(self.spinBox_slice)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.widget2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_timepoint = QSpinBox(self.widget2)
        self.spinBox_timepoint.setObjectName(u"spinBox_timepoint")
        self.spinBox_timepoint.setValue(1)

        self.horizontalLayout.addWidget(self.spinBox_timepoint)


        self.horizontalLayout_15.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_6 = QLabel(self.widget2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_13.addWidget(self.label_6)

        self.spinBox = QSpinBox(self.widget2)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_13.addWidget(self.spinBox)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_7 = QLabel(self.widget2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_14.addWidget(self.label_7)

        self.spinBox_2 = QSpinBox(self.widget2)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.horizontalLayout_14.addWidget(self.spinBox_2)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_14)


        self.verticalLayout_2.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.widget2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.spinBox_row = QSpinBox(self.widget2)
        self.spinBox_row.setObjectName(u"spinBox_row")
        self.spinBox_row.setValue(1)

        self.horizontalLayout_6.addWidget(self.spinBox_row)


        self.horizontalLayout_17.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.widget2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.spinBox_column = QSpinBox(self.widget2)
        self.spinBox_column.setObjectName(u"spinBox_column")
        self.spinBox_column.setFrame(True)
        self.spinBox_column.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_column.setValue(1)

        self.horizontalLayout_7.addWidget(self.spinBox_column)


        self.horizontalLayout_17.addLayout(self.horizontalLayout_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_17)


        self.horizontalLayout_18.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer)

        self.splitter.addWidget(self.widget2)
        self.toolBox = QToolBox(self.splitter)
        self.toolBox.setObjectName(u"toolBox")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 265, 123))
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.page)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_4.addWidget(self.listWidget)

        self.verticalLayout_4.setStretch(0, 5)
        self.toolBox.addItem(self.page, u"ROI")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 265, 123))
        self.pushButton = QPushButton(self.page_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 50, 75, 24))
        self.toolBox.addItem(self.page_2, u"Correction")
        self.splitter.addWidget(self.toolBox)

        self.verticalLayout_7.addWidget(self.splitter)


        self.horizontalLayout_3.addWidget(self.widget_tools)

        self.horizontalLayout_3.setStretch(0, 10)
        self.horizontalLayout_3.setStretch(2, 5)
        self.splitter_2.addWidget(self.widget1)
        self.widget_chart = QWidget(self.splitter_2)
        self.widget_chart.setObjectName(u"widget_chart")
        self.verticalLayout_3 = QVBoxLayout(self.widget_chart)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.chartView = QChartView(self.widget_chart)
        self.chartView.setObjectName(u"chartView")

        self.verticalLayout_3.addWidget(self.chartView)

        self.splitter_2.addWidget(self.widget_chart)

        self.verticalLayout_8.addWidget(self.splitter_2)

        self.splitter_3.addWidget(self.widget)
        self.tabWidget = QTabWidget(self.splitter_3)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 50))
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName(u"tabWidgetPage1")
        self.horizontalLayout_4 = QHBoxLayout(self.tabWidgetPage1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.tabWidgetPage1)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.widget_4)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1030, 512))
        self.horizontalLayout_11 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_mask = QLabel(self.scrollAreaWidgetContents)
        self.label_mask.setObjectName(u"label_mask")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_mask.sizePolicy().hasHeightForWidth())
        self.label_mask.setSizePolicy(sizePolicy)
        self.label_mask.setMinimumSize(QSize(512, 512))
        self.label_mask.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_mask)

        self.label_mask_img = QLabel(self.scrollAreaWidgetContents)
        self.label_mask_img.setObjectName(u"label_mask_img")
        sizePolicy.setHeightForWidth(self.label_mask_img.sizePolicy().hasHeightForWidth())
        self.label_mask_img.setSizePolicy(sizePolicy)
        self.label_mask_img.setMinimumSize(QSize(512, 512))
        self.label_mask_img.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_mask_img)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_10.addWidget(self.scrollArea)


        self.horizontalLayout_4.addWidget(self.widget_4)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.splitter_3.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.splitter_3)


        self.verticalLayout_5.addWidget(self.widget_center)

        self.widget_load = QWidget(Widget_DSC)
        self.widget_load.setObjectName(u"widget_load")
        self.verticalLayout_6 = QVBoxLayout(self.widget_load)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_2 = QSpacerItem(20, 93, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)

        self.load_label = QLabel(self.widget_load)
        self.load_label.setObjectName(u"load_label")

        self.horizontalLayout_9.addWidget(self.load_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_5)

        self.load_progressBar = QProgressBar(self.widget_load)
        self.load_progressBar.setObjectName(u"load_progressBar")
        self.load_progressBar.setValue(24)

        self.horizontalLayout_12.addWidget(self.load_progressBar)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_12.setStretch(0, 1)
        self.horizontalLayout_12.setStretch(1, 2)
        self.horizontalLayout_12.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.verticalSpacer_3 = QSpacerItem(20, 93, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)


        self.verticalLayout_5.addWidget(self.widget_load)


        self.retranslateUi(Widget_DSC)

        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget_DSC)
    # setupUi

    def retranslateUi(self, Widget_DSC):
        Widget_DSC.setWindowTitle(QCoreApplication.translate("Widget_DSC", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("Widget_DSC", u"Group By", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget_DSC", u"Slice", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget_DSC", u"Time point", None))

        self.label.setText(QCoreApplication.translate("Widget_DSC", u"Slice", None))
        self.label_2.setText(QCoreApplication.translate("Widget_DSC", u"Time point", None))
        self.label_6.setText(QCoreApplication.translate("Widget_DSC", u"Window level", None))
        self.label_7.setText(QCoreApplication.translate("Widget_DSC", u"Window width", None))
        self.label_3.setText(QCoreApplication.translate("Widget_DSC", u"Row", None))
        self.label_4.setText(QCoreApplication.translate("Widget_DSC", u"Column", None))
        self.spinBox_column.setSuffix("")
        self.spinBox_column.setPrefix("")
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("Widget_DSC", u"ROI", None))
        self.pushButton.setText(QCoreApplication.translate("Widget_DSC", u"PushButton", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("Widget_DSC", u"Correction", None))
        self.label_mask.setText("")
        self.label_mask_img.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QCoreApplication.translate("Widget_DSC", u"ROI", None))
        self.load_label.setText(QCoreApplication.translate("Widget_DSC", u"TextLabel", None))
    # retranslateUi

