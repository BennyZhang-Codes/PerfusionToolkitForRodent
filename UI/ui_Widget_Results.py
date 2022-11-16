# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget_Results.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from MyWidgets.MComboBox.ColorMap import MColorMapComboBox
from MyWidgets.MWidget import (MColorBar, MResult)

class Ui_Widget_Results(object):
    def setupUi(self, Widget_Results):
        if not Widget_Results.objectName():
            Widget_Results.setObjectName(u"Widget_Results")
        Widget_Results.resize(464, 591)
        self.verticalLayout = QVBoxLayout(Widget_Results)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(Widget_Results)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_min = QHBoxLayout()
        self.horizontalLayout_min.setObjectName(u"horizontalLayout_min")
        self.label_min = QLabel(Widget_Results)
        self.label_min.setObjectName(u"label_min")

        self.horizontalLayout_min.addWidget(self.label_min)

        self.doubleSpinBox_min = QDoubleSpinBox(Widget_Results)
        self.doubleSpinBox_min.setObjectName(u"doubleSpinBox_min")
        self.doubleSpinBox_min.setMinimum(-90000.000000000000000)
        self.doubleSpinBox_min.setMaximum(90000.000000000000000)

        self.horizontalLayout_min.addWidget(self.doubleSpinBox_min)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_min)

        self.horizontalLayout_max = QHBoxLayout()
        self.horizontalLayout_max.setObjectName(u"horizontalLayout_max")
        self.label_max = QLabel(Widget_Results)
        self.label_max.setObjectName(u"label_max")

        self.horizontalLayout_max.addWidget(self.label_max)

        self.doubleSpinBox_max = QDoubleSpinBox(Widget_Results)
        self.doubleSpinBox_max.setObjectName(u"doubleSpinBox_max")
        self.doubleSpinBox_max.setMinimum(-90000.000000000000000)
        self.doubleSpinBox_max.setMaximum(90000.000000000000000)

        self.horizontalLayout_max.addWidget(self.doubleSpinBox_max)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_max)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_colormap = QLabel(Widget_Results)
        self.label_colormap.setObjectName(u"label_colormap")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_colormap.sizePolicy().hasHeightForWidth())
        self.label_colormap.setSizePolicy(sizePolicy)
        self.label_colormap.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_2.addWidget(self.label_colormap)

        self.comboBox_colormap = MColorMapComboBox(Widget_Results)
        self.comboBox_colormap.setObjectName(u"comboBox_colormap")

        self.horizontalLayout_2.addWidget(self.comboBox_colormap)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.pushButton_Save = QPushButton(Widget_Results)
        self.pushButton_Save.setObjectName(u"pushButton_Save")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_Save.sizePolicy().hasHeightForWidth())
        self.pushButton_Save.setSizePolicy(sizePolicy1)
        self.pushButton_Save.setMinimumSize(QSize(40, 28))

        self.horizontalLayout_3.addWidget(self.pushButton_Save)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_result = MResult(Widget_Results)
        self.widget_result.setObjectName(u"widget_result")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_result.sizePolicy().hasHeightForWidth())
        self.widget_result.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.widget_result)

        self.widget_colorbar = MColorBar(Widget_Results)
        self.widget_colorbar.setObjectName(u"widget_colorbar")
        sizePolicy2.setHeightForWidth(self.widget_colorbar.sizePolicy().hasHeightForWidth())
        self.widget_colorbar.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.widget_colorbar)

        self.horizontalLayout.setStretch(0, 12)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Widget_Results)

        QMetaObject.connectSlotsByName(Widget_Results)
    # setupUi

    def retranslateUi(self, Widget_Results):
        Widget_Results.setWindowTitle(QCoreApplication.translate("Widget_Results", u"Form", None))
        self.label.setText(QCoreApplication.translate("Widget_Results", u"TextLabel", None))
        self.label_min.setText(QCoreApplication.translate("Widget_Results", u"Min", None))
        self.label_max.setText(QCoreApplication.translate("Widget_Results", u"Max", None))
        self.label_colormap.setText(QCoreApplication.translate("Widget_Results", u"colormap", None))
        self.pushButton_Save.setText(QCoreApplication.translate("Widget_Results", u"Save", None))
    # retranslateUi

