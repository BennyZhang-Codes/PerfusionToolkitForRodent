# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget_DSC.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFrame, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QProgressBar,
    QPushButton, QRadioButton, QScrollArea, QScrollBar,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QVBoxLayout, QWidget)

from MyWidgets.MChart.MChart import MChartView
from MyWidgets.MGraphicsView.MGraphicsView_TimeSeries import MGraphicsView_TimeSeries
from MyWidgets.MView.MTableView import MTableView
from MyWidgets.MWidget import (MROI, MResult)

class Ui_Widget_DSC(object):
    def setupUi(self, Widget_DSC):
        if not Widget_DSC.objectName():
            Widget_DSC.setObjectName(u"Widget_DSC")
        Widget_DSC.resize(1065, 966)
        self.verticalLayout_14 = QVBoxLayout(Widget_DSC)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.widget_center = QWidget(Widget_DSC)
        self.widget_center.setObjectName(u"widget_center")
        self.verticalLayout = QVBoxLayout(self.widget_center)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.splitter = QSplitter(self.widget_center)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_8 = QVBoxLayout(self.widget)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.widget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = MGraphicsView_TimeSeries(self.layoutWidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(0, 0))
        self.graphicsView.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_3.addWidget(self.graphicsView)

        self.verticalScrollBar = QScrollBar(self.layoutWidget)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.horizontalLayout_3.addWidget(self.verticalScrollBar)

        self.widget_tools = QWidget(self.layoutWidget)
        self.widget_tools.setObjectName(u"widget_tools")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_tools.sizePolicy().hasHeightForWidth())
        self.widget_tools.setSizePolicy(sizePolicy)
        self.widget_tools.setMinimumSize(QSize(256, 0))
        self.verticalLayout_9 = QVBoxLayout(self.widget_tools)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.widget_tools)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 289, 480))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents_2)
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

        self.radioButton_usecorrected = QRadioButton(self.groupBox)
        self.radioButton_usecorrected.setObjectName(u"radioButton_usecorrected")
        self.radioButton_usecorrected.setChecked(False)

        self.verticalLayout_13.addWidget(self.radioButton_usecorrected)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setSpacing(3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_27.addWidget(self.label_6)

        self.doubleSpinBox_DSC_TR = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_DSC_TR.setObjectName(u"doubleSpinBox_DSC_TR")
        self.doubleSpinBox_DSC_TR.setDecimals(2)
        self.doubleSpinBox_DSC_TR.setMaximum(9000.000000000000000)

        self.horizontalLayout_27.addWidget(self.doubleSpinBox_DSC_TR)


        self.horizontalLayout_18.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_28.addWidget(self.label_13)

        self.doubleSpinBox_DSC_TE = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_DSC_TE.setObjectName(u"doubleSpinBox_DSC_TE")
        self.doubleSpinBox_DSC_TE.setDecimals(2)
        self.doubleSpinBox_DSC_TE.setMaximum(9000.000000000000000)
        self.doubleSpinBox_DSC_TE.setStepType(QAbstractSpinBox.DefaultStepType)
        self.doubleSpinBox_DSC_TE.setValue(0.000000000000000)

        self.horizontalLayout_28.addWidget(self.doubleSpinBox_DSC_TE)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_12)


        self.horizontalLayout_18.addLayout(self.horizontalLayout_28)


        self.verticalLayout_7.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_29.addWidget(self.label_14)

        self.comboBox_DSC_AIF = QComboBox(self.groupBox_2)
        self.comboBox_DSC_AIF.setObjectName(u"comboBox_DSC_AIF")

        self.horizontalLayout_29.addWidget(self.comboBox_DSC_AIF)

        self.pushButton_DSC_set_AIF = QPushButton(self.groupBox_2)
        self.pushButton_DSC_set_AIF.setObjectName(u"pushButton_DSC_set_AIF")

        self.horizontalLayout_29.addWidget(self.pushButton_DSC_set_AIF)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer)


        self.verticalLayout_7.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_15)

        self.progressBar_DSC = QProgressBar(self.groupBox_2)
        self.progressBar_DSC.setObjectName(u"progressBar_DSC")
        self.progressBar_DSC.setValue(24)

        self.horizontalLayout_30.addWidget(self.progressBar_DSC)

        self.pushButton_DSC_run = QPushButton(self.groupBox_2)
        self.pushButton_DSC_run.setObjectName(u"pushButton_DSC_run")

        self.horizontalLayout_30.addWidget(self.pushButton_DSC_run)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_14)


        self.verticalLayout_7.addLayout(self.horizontalLayout_30)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_12.setSpacing(3)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_16 = QLabel(self.groupBox_3)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_33.addWidget(self.label_16)

        self.spinBox_correction = QSpinBox(self.groupBox_3)
        self.spinBox_correction.setObjectName(u"spinBox_correction")

        self.horizontalLayout_33.addWidget(self.spinBox_correction)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_11)


        self.verticalLayout_12.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_32.addWidget(self.label_15)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.checkBox_correction_x = QCheckBox(self.groupBox_3)
        self.checkBox_correction_x.setObjectName(u"checkBox_correction_x")

        self.horizontalLayout_31.addWidget(self.checkBox_correction_x)

        self.checkBox_correction_y = QCheckBox(self.groupBox_3)
        self.checkBox_correction_y.setObjectName(u"checkBox_correction_y")

        self.horizontalLayout_31.addWidget(self.checkBox_correction_y)

        self.checkBox_correction_z = QCheckBox(self.groupBox_3)
        self.checkBox_correction_z.setObjectName(u"checkBox_correction_z")

        self.horizontalLayout_31.addWidget(self.checkBox_correction_z)


        self.horizontalLayout_32.addLayout(self.horizontalLayout_31)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_10)


        self.verticalLayout_12.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_8)

        self.progressBar_correction = QProgressBar(self.groupBox_3)
        self.progressBar_correction.setObjectName(u"progressBar_correction")
        self.progressBar_correction.setMinimumSize(QSize(100, 0))
        self.progressBar_correction.setValue(24)

        self.horizontalLayout_25.addWidget(self.progressBar_correction)

        self.pushButton_correction = QPushButton(self.groupBox_3)
        self.pushButton_correction.setObjectName(u"pushButton_correction")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_correction.sizePolicy().hasHeightForWidth())
        self.pushButton_correction.setSizePolicy(sizePolicy1)
        self.pushButton_correction.setMinimumSize(QSize(50, 30))

        self.horizontalLayout_25.addWidget(self.pushButton_correction)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_9)


        self.verticalLayout_12.addLayout(self.horizontalLayout_25)

        self.scrollArea_correction = QScrollArea(self.groupBox_3)
        self.scrollArea_correction.setObjectName(u"scrollArea_correction")
        self.scrollArea_correction.setMaximumSize(QSize(16777215, 200))
        self.scrollArea_correction.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 286, 268))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.widget_correction_before = QWidget(self.scrollAreaWidgetContents_3)
        self.widget_correction_before.setObjectName(u"widget_correction_before")
        self.verticalLayout_11 = QVBoxLayout(self.widget_correction_before)
        self.verticalLayout_11.setSpacing(3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_7 = QLabel(self.widget_correction_before)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_24.addWidget(self.label_7)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_6)


        self.verticalLayout_11.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setSpacing(6)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_9 = QLabel(self.widget_correction_before)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        self.label_9.setMinimumSize(QSize(80, 0))
        self.label_9.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_19.addWidget(self.label_9)

        self.label_correction_before_row = QLabel(self.widget_correction_before)
        self.label_correction_before_row.setObjectName(u"label_correction_before_row")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_correction_before_row.sizePolicy().hasHeightForWidth())
        self.label_correction_before_row.setSizePolicy(sizePolicy2)
        self.label_correction_before_row.setMinimumSize(QSize(192, 48))
        self.label_correction_before_row.setMaximumSize(QSize(400, 48))
        self.label_correction_before_row.setBaseSize(QSize(0, 0))

        self.horizontalLayout_19.addWidget(self.label_correction_before_row)


        self.verticalLayout_11.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_10 = QLabel(self.widget_correction_before)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)
        self.label_10.setMinimumSize(QSize(80, 0))
        self.label_10.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_21.addWidget(self.label_10)

        self.label_correction_before_col = QLabel(self.widget_correction_before)
        self.label_correction_before_col.setObjectName(u"label_correction_before_col")
        sizePolicy2.setHeightForWidth(self.label_correction_before_col.sizePolicy().hasHeightForWidth())
        self.label_correction_before_col.setSizePolicy(sizePolicy2)
        self.label_correction_before_col.setMinimumSize(QSize(192, 48))
        self.label_correction_before_col.setMaximumSize(QSize(400, 48))

        self.horizontalLayout_21.addWidget(self.label_correction_before_col)


        self.verticalLayout_11.addLayout(self.horizontalLayout_21)


        self.verticalLayout_3.addWidget(self.widget_correction_before)

        self.widget_correction_after = QWidget(self.scrollAreaWidgetContents_3)
        self.widget_correction_after.setObjectName(u"widget_correction_after")
        self.verticalLayout_10 = QVBoxLayout(self.widget_correction_after)
        self.verticalLayout_10.setSpacing(3)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_8 = QLabel(self.widget_correction_after)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_20.addWidget(self.label_8)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_7)


        self.verticalLayout_10.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_11 = QLabel(self.widget_correction_after)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setMinimumSize(QSize(80, 0))
        self.label_11.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_22.addWidget(self.label_11)

        self.label_correction_after_row = QLabel(self.widget_correction_after)
        self.label_correction_after_row.setObjectName(u"label_correction_after_row")
        sizePolicy2.setHeightForWidth(self.label_correction_after_row.sizePolicy().hasHeightForWidth())
        self.label_correction_after_row.setSizePolicy(sizePolicy2)
        self.label_correction_after_row.setMinimumSize(QSize(192, 48))
        self.label_correction_after_row.setMaximumSize(QSize(400, 48))

        self.horizontalLayout_22.addWidget(self.label_correction_after_row)


        self.verticalLayout_10.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_12 = QLabel(self.widget_correction_after)
        self.label_12.setObjectName(u"label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)
        self.label_12.setMinimumSize(QSize(80, 0))
        self.label_12.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_23.addWidget(self.label_12)

        self.label_correction_after_col = QLabel(self.widget_correction_after)
        self.label_correction_after_col.setObjectName(u"label_correction_after_col")
        sizePolicy2.setHeightForWidth(self.label_correction_after_col.sizePolicy().hasHeightForWidth())
        self.label_correction_after_col.setSizePolicy(sizePolicy2)
        self.label_correction_after_col.setMinimumSize(QSize(192, 48))
        self.label_correction_after_col.setMaximumSize(QSize(400, 48))

        self.horizontalLayout_23.addWidget(self.label_correction_after_col)


        self.verticalLayout_10.addLayout(self.horizontalLayout_23)


        self.verticalLayout_3.addWidget(self.widget_correction_after)

        self.verticalSpacer = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea_correction.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_12.addWidget(self.scrollArea_correction)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_9.addWidget(self.scrollArea_2)


        self.horizontalLayout_3.addWidget(self.widget_tools)

        self.horizontalLayout_3.setStretch(0, 5)
        self.splitter_2.addWidget(self.layoutWidget)
        self.widget_chart = QWidget(self.splitter_2)
        self.widget_chart.setObjectName(u"widget_chart")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_chart.sizePolicy().hasHeightForWidth())
        self.widget_chart.setSizePolicy(sizePolicy3)
        self.horizontalLayout_5 = QHBoxLayout(self.widget_chart)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.chartView = MChartView(self.widget_chart)
        self.chartView.setObjectName(u"chartView")
        self.chartView.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_5.addWidget(self.chartView)

        self.splitter_2.addWidget(self.widget_chart)

        self.verticalLayout_8.addWidget(self.splitter_2)

        self.splitter.addWidget(self.widget)
        self.widget_4 = QWidget(self.splitter)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(3, 3, 3, 3)
        self.splitter_3 = QSplitter(self.widget_4)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.groupBox_4 = QGroupBox(self.splitter_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_35.addWidget(self.label_17)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_16)

        self.pushButton_Save_mask = QPushButton(self.groupBox_4)
        self.pushButton_Save_mask.setObjectName(u"pushButton_Save_mask")

        self.horizontalLayout_35.addWidget(self.pushButton_Save_mask)


        self.verticalLayout_5.addLayout(self.horizontalLayout_35)

        self.frame = QFrame(self.groupBox_4)
        self.frame.setObjectName(u"frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy4)
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


        self.verticalLayout_5.addWidget(self.frame)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_18 = QLabel(self.groupBox_4)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_38.addWidget(self.label_18)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_17)

        self.pushButton_Save_overlap = QPushButton(self.groupBox_4)
        self.pushButton_Save_overlap.setObjectName(u"pushButton_Save_overlap")

        self.horizontalLayout_38.addWidget(self.pushButton_Save_overlap)


        self.verticalLayout_5.addLayout(self.horizontalLayout_38)

        self.frame_2 = QFrame(self.groupBox_4)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy4.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy4)
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


        self.verticalLayout_5.addWidget(self.frame_2)

        self.splitter_3.addWidget(self.groupBox_4)
        self.groupBox_5 = QGroupBox(self.splitter_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_10.setSpacing(3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(3, 3, 3, 3)
        self.frame_3 = QFrame(self.groupBox_5)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy4.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy4)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_3)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.widget_mask_3 = MResult(self.frame_3)
        self.widget_mask_3.setObjectName(u"widget_mask_3")
        sizePolicy3.setHeightForWidth(self.widget_mask_3.sizePolicy().hasHeightForWidth())
        self.widget_mask_3.setSizePolicy(sizePolicy3)

        self.verticalLayout_15.addWidget(self.widget_mask_3)


        self.horizontalLayout_10.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.groupBox_5)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy4.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy4)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_4)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.widget_mask_4 = MResult(self.frame_4)
        self.widget_mask_4.setObjectName(u"widget_mask_4")

        self.verticalLayout_16.addWidget(self.widget_mask_4)


        self.horizontalLayout_10.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.groupBox_5)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy4.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy4)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_5)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.widget_mask_5 = MResult(self.frame_5)
        self.widget_mask_5.setObjectName(u"widget_mask_5")

        self.verticalLayout_17.addWidget(self.widget_mask_5)


        self.horizontalLayout_10.addWidget(self.frame_5)

        self.splitter_3.addWidget(self.groupBox_5)

        self.horizontalLayout_11.addWidget(self.splitter_3)

        self.splitter.addWidget(self.widget_4)

        self.horizontalLayout_4.addWidget(self.splitter)

        self.tableView = MTableView(self.widget_center)
        self.tableView.setObjectName(u"tableView")
        sizePolicy3.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy3)
        self.tableView.setMinimumSize(QSize(50, 0))
        self.tableView.setMaximumSize(QSize(200, 16777215))
        self.tableView.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.tableView.setTextElideMode(Qt.ElideMiddle)
        self.tableView.verticalHeader().setVisible(False)

        self.horizontalLayout_4.addWidget(self.tableView)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_14.addWidget(self.widget_center)

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


        self.verticalLayout_14.addWidget(self.widget_load)

        self.verticalLayout_14.setStretch(0, 10)
        self.verticalLayout_14.setStretch(1, 1)

        self.retranslateUi(Widget_DSC)

        self.comboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget_DSC)
    # setupUi

    def retranslateUi(self, Widget_DSC):
        Widget_DSC.setWindowTitle(QCoreApplication.translate("Widget_DSC", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget_DSC", u"Basic", None))
        self.label_5.setText(QCoreApplication.translate("Widget_DSC", u"Group By", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget_DSC", u"Slice", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget_DSC", u"Time point", None))

        self.label.setText(QCoreApplication.translate("Widget_DSC", u"Slice", None))
        self.label_2.setText(QCoreApplication.translate("Widget_DSC", u"Time point", None))
        self.label_WL.setText(QCoreApplication.translate("Widget_DSC", u"WL", None))
        self.label_WW.setText(QCoreApplication.translate("Widget_DSC", u"WW", None))
        self.label_3.setText(QCoreApplication.translate("Widget_DSC", u"Row", None))
        self.label_4.setText(QCoreApplication.translate("Widget_DSC", u"Column", None))
        self.spinBox_column.setSuffix("")
        self.spinBox_column.setPrefix("")
        self.radioButton_usecorrected.setText(QCoreApplication.translate("Widget_DSC", u"use correcred images", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget_DSC", u"DSC", None))
        self.label_6.setText(QCoreApplication.translate("Widget_DSC", u"TR", None))
        self.doubleSpinBox_DSC_TR.setSuffix(QCoreApplication.translate("Widget_DSC", u" ms", None))
        self.label_13.setText(QCoreApplication.translate("Widget_DSC", u"TE", None))
        self.doubleSpinBox_DSC_TE.setSuffix(QCoreApplication.translate("Widget_DSC", u" ms", None))
        self.label_14.setText(QCoreApplication.translate("Widget_DSC", u"AIF", None))
        self.pushButton_DSC_set_AIF.setText(QCoreApplication.translate("Widget_DSC", u"Set AIF", None))
        self.pushButton_DSC_run.setText(QCoreApplication.translate("Widget_DSC", u"Run", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget_DSC", u"Correction", None))
        self.label_16.setText(QCoreApplication.translate("Widget_DSC", u"Set fixed point:", None))
        self.label_15.setText(QCoreApplication.translate("Widget_DSC", u"Translation direction:", None))
#if QT_CONFIG(tooltip)
        self.checkBox_correction_x.setToolTip(QCoreApplication.translate("Widget_DSC", u"Column", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_correction_x.setText(QCoreApplication.translate("Widget_DSC", u"X", None))
#if QT_CONFIG(tooltip)
        self.checkBox_correction_y.setToolTip(QCoreApplication.translate("Widget_DSC", u"Row", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_correction_y.setText(QCoreApplication.translate("Widget_DSC", u"Y", None))
#if QT_CONFIG(tooltip)
        self.checkBox_correction_z.setToolTip(QCoreApplication.translate("Widget_DSC", u"Slice", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_correction_z.setText(QCoreApplication.translate("Widget_DSC", u"Z", None))
        self.pushButton_correction.setText(QCoreApplication.translate("Widget_DSC", u"RUN", None))
        self.label_7.setText(QCoreApplication.translate("Widget_DSC", u"before:", None))
        self.label_9.setText(QCoreApplication.translate("Widget_DSC", u"Center Row", None))
        self.label_correction_before_row.setText("")
        self.label_10.setText(QCoreApplication.translate("Widget_DSC", u"Center Col", None))
        self.label_correction_before_col.setText("")
        self.label_8.setText(QCoreApplication.translate("Widget_DSC", u"after:", None))
        self.label_11.setText(QCoreApplication.translate("Widget_DSC", u"Center Row", None))
        self.label_correction_after_row.setText("")
        self.label_12.setText(QCoreApplication.translate("Widget_DSC", u"Center Col", None))
        self.label_correction_after_col.setText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("Widget_DSC", u"ROI", None))
        self.label_17.setText(QCoreApplication.translate("Widget_DSC", u"Mask", None))
        self.pushButton_Save_mask.setText(QCoreApplication.translate("Widget_DSC", u"Save", None))
        self.label_18.setText(QCoreApplication.translate("Widget_DSC", u"Overlap", None))
        self.pushButton_Save_overlap.setText(QCoreApplication.translate("Widget_DSC", u"Save", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Widget_DSC", u"Results", None))
        self.load_label.setText(QCoreApplication.translate("Widget_DSC", u"TextLabel", None))
    # retranslateUi

