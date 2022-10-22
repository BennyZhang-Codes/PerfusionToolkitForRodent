# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Status_progressbar.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QProgressBar,
    QSizePolicy, QWidget)

class Ui_status_progressbar(object):
    def setupUi(self, status_progressbar):
        if not status_progressbar.objectName():
            status_progressbar.setObjectName(u"status_progressbar")
        status_progressbar.resize(209, 16)
        self.horizontalLayout = QHBoxLayout(status_progressbar)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(status_progressbar)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(status_progressbar)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QSize(150, 5))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.horizontalLayout.addWidget(self.progressBar)


        self.retranslateUi(status_progressbar)

        QMetaObject.connectSlotsByName(status_progressbar)
    # setupUi

    def retranslateUi(self, status_progressbar):
        status_progressbar.setWindowTitle(QCoreApplication.translate("status_progressbar", u"Form", None))
        self.label.setText(QCoreApplication.translate("status_progressbar", u"TextLabel", None))
    # retranslateUi

