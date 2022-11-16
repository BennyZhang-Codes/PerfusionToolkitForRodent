# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget_TimePoints.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QSizePolicy, QWidget)

from MyWidgets.MChart.MChart import MChartView
from MyWidgets.MView.MTableView import MTableView

class Ui_Widget_TimePoints(object):
    def setupUi(self, Widget_TimePoints):
        if not Widget_TimePoints.objectName():
            Widget_TimePoints.setObjectName(u"Widget_TimePoints")
        Widget_TimePoints.resize(400, 229)
        self.horizontalLayout = QHBoxLayout(Widget_TimePoints)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tableView = MTableView(Widget_TimePoints)
        self.tableView.setObjectName(u"tableView")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QSize(0, 0))
        self.tableView.setMaximumSize(QSize(200, 16777215))
        self.tableView.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.tableView.setTextElideMode(Qt.ElideMiddle)
        self.tableView.verticalHeader().setVisible(False)

        self.horizontalLayout.addWidget(self.tableView)

        self.chartView = MChartView(Widget_TimePoints)
        self.chartView.setObjectName(u"chartView")
        self.chartView.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.chartView)


        self.retranslateUi(Widget_TimePoints)

        QMetaObject.connectSlotsByName(Widget_TimePoints)
    # setupUi

    def retranslateUi(self, Widget_TimePoints):
        Widget_TimePoints.setWindowTitle(QCoreApplication.translate("Widget_TimePoints", u"Form", None))
    # retranslateUi

