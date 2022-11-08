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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QScrollArea, QScrollBar,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from MyWidgets.MChart.MChart import MChartView
from MyWidgets.MGraphicsView.MGraphicsView import MGraphicsView
from MyWidgets.MWidget import MROI
from ToolWidgets.Widget_Results import Widget_Results

class Ui_Widget_FAIR(object):
    def setupUi(self, Widget_FAIR):
        if not Widget_FAIR.objectName():
            Widget_FAIR.setObjectName(u"Widget_FAIR")
        Widget_FAIR.resize(1007, 706)
        self.verticalLayout_5 = QVBoxLayout(Widget_FAIR)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.graphicsView = MGraphicsView(Widget_FAIR)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_5.addWidget(self.graphicsView)

        self.verticalScrollBar = QScrollBar(Widget_FAIR)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.horizontalLayout_5.addWidget(self.verticalScrollBar)

        self.horizontalLayout_5.setStretch(0, 10)

        self.horizontalLayout_9.addLayout(self.horizontalLayout_5)

        self.scrollArea = QScrollArea(Widget_FAIR)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(250, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 287, 346))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox)
        self.verticalLayout_13.setSpacing(3)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_8.addWidget(self.label_5)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_8.addWidget(self.comboBox)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_13)


        self.verticalLayout_13.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.spinBox_slice = QSpinBox(self.groupBox)
        self.spinBox_slice.setObjectName(u"spinBox_slice")
        self.spinBox_slice.setValue(1)

        self.horizontalLayout_2.addWidget(self.spinBox_slice)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_timepoint = QSpinBox(self.groupBox)
        self.spinBox_timepoint.setObjectName(u"spinBox_timepoint")
        self.spinBox_timepoint.setValue(1)

        self.horizontalLayout.addWidget(self.spinBox_timepoint)


        self.horizontalLayout_15.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_WL = QLabel(self.groupBox)
        self.label_WL.setObjectName(u"label_WL")

        self.horizontalLayout_13.addWidget(self.label_WL)

        self.spinBox_WW = QSpinBox(self.groupBox)
        self.spinBox_WW.setObjectName(u"spinBox_WW")
        self.spinBox_WW.setSingleStep(50)

        self.horizontalLayout_13.addWidget(self.spinBox_WW)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_WW = QLabel(self.groupBox)
        self.label_WW.setObjectName(u"label_WW")

        self.horizontalLayout_14.addWidget(self.label_WW)

        self.spinBox_WL = QSpinBox(self.groupBox)
        self.spinBox_WL.setObjectName(u"spinBox_WL")
        self.spinBox_WL.setSingleStep(50)

        self.horizontalLayout_14.addWidget(self.spinBox_WL)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_14)


        self.verticalLayout_2.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.spinBox_row = QSpinBox(self.groupBox)
        self.spinBox_row.setObjectName(u"spinBox_row")
        self.spinBox_row.setValue(1)

        self.horizontalLayout_6.addWidget(self.spinBox_row)


        self.horizontalLayout_17.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.spinBox_column = QSpinBox(self.groupBox)
        self.spinBox_column.setObjectName(u"spinBox_column")
        self.spinBox_column.setFrame(True)
        self.spinBox_column.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_column.setValue(1)

        self.horizontalLayout_7.addWidget(self.spinBox_column)


        self.horizontalLayout_17.addLayout(self.horizontalLayout_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_17)


        self.horizontalLayout_34.addLayout(self.verticalLayout_2)


        self.verticalLayout_13.addLayout(self.horizontalLayout_34)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.groupBox_FAIR = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_FAIR.setObjectName(u"groupBox_FAIR")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_FAIR)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_T1blood = QLabel(self.groupBox_FAIR)
        self.label_T1blood.setObjectName(u"label_T1blood")

        self.horizontalLayout_11.addWidget(self.label_T1blood)

        self.doubleSpinBox_T1blood = QDoubleSpinBox(self.groupBox_FAIR)
        self.doubleSpinBox_T1blood.setObjectName(u"doubleSpinBox_T1blood")
        self.doubleSpinBox_T1blood.setMaximum(10000.000000000000000)
        self.doubleSpinBox_T1blood.setSingleStep(10.000000000000000)

        self.horizontalLayout_11.addWidget(self.doubleSpinBox_T1blood)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_2)

        self.progressBar_FAIR = QProgressBar(self.groupBox_FAIR)
        self.progressBar_FAIR.setObjectName(u"progressBar_FAIR")
        self.progressBar_FAIR.setValue(0)

        self.horizontalLayout_10.addWidget(self.progressBar_FAIR)

        self.pushButton_FAIR_run = QPushButton(self.groupBox_FAIR)
        self.pushButton_FAIR_run.setObjectName(u"pushButton_FAIR_run")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_FAIR_run.sizePolicy().hasHeightForWidth())
        self.pushButton_FAIR_run.setSizePolicy(sizePolicy1)
        self.pushButton_FAIR_run.setMinimumSize(QSize(50, 28))

        self.horizontalLayout_10.addWidget(self.pushButton_FAIR_run)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)


        self.verticalLayout_6.addWidget(self.groupBox_FAIR)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_9.addWidget(self.scrollArea)

        self.chartView = MChartView(Widget_FAIR)
        self.chartView.setObjectName(u"chartView")
        self.chartView.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_9.addWidget(self.chartView)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(2, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(6, 6, 6, 6)
        self.groupBox_ROI = QGroupBox(Widget_FAIR)
        self.groupBox_ROI.setObjectName(u"groupBox_ROI")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_ROI)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, -1, 5)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.label_17 = QLabel(self.groupBox_ROI)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_35.addWidget(self.label_17)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_16)

        self.pushButton_Save_mask = QPushButton(self.groupBox_ROI)
        self.pushButton_Save_mask.setObjectName(u"pushButton_Save_mask")
        sizePolicy1.setHeightForWidth(self.pushButton_Save_mask.sizePolicy().hasHeightForWidth())
        self.pushButton_Save_mask.setSizePolicy(sizePolicy1)
        self.pushButton_Save_mask.setMinimumSize(QSize(35, 28))

        self.horizontalLayout_35.addWidget(self.pushButton_Save_mask)


        self.verticalLayout_3.addLayout(self.horizontalLayout_35)

        self.frame = QFrame(self.groupBox_ROI)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame)
        self.horizontalLayout_36.setSpacing(0)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.widget_mask = MROI(self.frame)
        self.widget_mask.setObjectName(u"widget_mask")
        self.widget_mask.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.horizontalLayout_36.addWidget(self.widget_mask)


        self.verticalLayout_3.addWidget(self.frame)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_18 = QLabel(self.groupBox_ROI)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_38.addWidget(self.label_18)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_17)

        self.pushButton_Save_overlap = QPushButton(self.groupBox_ROI)
        self.pushButton_Save_overlap.setObjectName(u"pushButton_Save_overlap")
        sizePolicy1.setHeightForWidth(self.pushButton_Save_overlap.sizePolicy().hasHeightForWidth())
        self.pushButton_Save_overlap.setSizePolicy(sizePolicy1)
        self.pushButton_Save_overlap.setMinimumSize(QSize(35, 28))

        self.horizontalLayout_38.addWidget(self.pushButton_Save_overlap)


        self.verticalLayout.addLayout(self.horizontalLayout_38)

        self.frame_2 = QFrame(self.groupBox_ROI)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_37.setSpacing(0)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.widget_mask_img = MROI(self.frame_2)
        self.widget_mask_img.setObjectName(u"widget_mask_img")
        self.widget_mask_img.setAutoFillBackground(False)
        self.widget_mask_img.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.horizontalLayout_37.addWidget(self.widget_mask_img)


        self.verticalLayout.addWidget(self.frame_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout)


        self.horizontalLayout_12.addWidget(self.groupBox_ROI)

        self.groupBox_Results = QGroupBox(Widget_FAIR)
        self.groupBox_Results.setObjectName(u"groupBox_Results")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_Results)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.frame_3 = QFrame(self.groupBox_Results)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy2.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy2)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_3)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.widget_result_CBF = Widget_Results(self.frame_3)
        self.widget_result_CBF.setObjectName(u"widget_result_CBF")
        sizePolicy.setHeightForWidth(self.widget_result_CBF.sizePolicy().hasHeightForWidth())
        self.widget_result_CBF.setSizePolicy(sizePolicy)

        self.verticalLayout_15.addWidget(self.widget_result_CBF)


        self.horizontalLayout_4.addWidget(self.frame_3)


        self.horizontalLayout_12.addWidget(self.groupBox_Results)


        self.verticalLayout_5.addLayout(self.horizontalLayout_12)


        self.retranslateUi(Widget_FAIR)

        self.comboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget_FAIR)
    # setupUi

    def retranslateUi(self, Widget_FAIR):
        Widget_FAIR.setWindowTitle(QCoreApplication.translate("Widget_FAIR", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget_FAIR", u"Basic", None))
        self.label_5.setText(QCoreApplication.translate("Widget_FAIR", u"show", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget_FAIR", u"Selective Inversion", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget_FAIR", u"Non-Selective Inversion", None))

        self.label.setText(QCoreApplication.translate("Widget_FAIR", u"Slice", None))
        self.label_2.setText(QCoreApplication.translate("Widget_FAIR", u"Time point", None))
        self.label_WL.setText(QCoreApplication.translate("Widget_FAIR", u"WW", None))
        self.label_WW.setText(QCoreApplication.translate("Widget_FAIR", u"WL", None))
        self.label_3.setText(QCoreApplication.translate("Widget_FAIR", u"Row", None))
        self.label_4.setText(QCoreApplication.translate("Widget_FAIR", u"Column", None))
        self.spinBox_column.setSuffix("")
        self.spinBox_column.setPrefix("")
        self.groupBox_FAIR.setTitle(QCoreApplication.translate("Widget_FAIR", u"FAIR", None))
        self.label_T1blood.setText(QCoreApplication.translate("Widget_FAIR", u"T1 of blood", None))
        self.doubleSpinBox_T1blood.setSuffix(QCoreApplication.translate("Widget_FAIR", u" ms", None))
        self.pushButton_FAIR_run.setText(QCoreApplication.translate("Widget_FAIR", u"Run", None))
        self.groupBox_ROI.setTitle(QCoreApplication.translate("Widget_FAIR", u"ROI", None))
        self.label_17.setText(QCoreApplication.translate("Widget_FAIR", u"Mask", None))
        self.pushButton_Save_mask.setText(QCoreApplication.translate("Widget_FAIR", u"Save", None))
        self.label_18.setText(QCoreApplication.translate("Widget_FAIR", u"Overlap", None))
        self.pushButton_Save_overlap.setText(QCoreApplication.translate("Widget_FAIR", u"Save", None))
        self.groupBox_Results.setTitle(QCoreApplication.translate("Widget_FAIR", u"Results", None))
    # retranslateUi

