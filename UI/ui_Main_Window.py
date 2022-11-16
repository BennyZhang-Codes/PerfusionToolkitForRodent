# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_Window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QWidget)
import UI.icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1044, 707)
        font = QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/\u65b0\u524d\u7f00/GUI_Logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QSize(30, 30))
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.actionSelect_Dicom_Folder = QAction(MainWindow)
        self.actionSelect_Dicom_Folder.setObjectName(u"actionSelect_Dicom_Folder")
        self.actionSelect_Dicom_Folder.setEnabled(True)
        icon1 = QIcon()
        iconThemeName = u"accessories-calculator"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u":/\u65b0\u524d\u7f00/qrc/folder.png", QSize(), QIcon.Normal, QIcon.On)
        
        self.actionSelect_Dicom_Folder.setIcon(icon1)
        self.actionEXit = QAction(MainWindow)
        self.actionEXit.setObjectName(u"actionEXit")
        icon2 = QIcon()
        icon2.addFile(u":/\u65b0\u524d\u7f00/Exit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionEXit.setIcon(icon2)
        self.actionFAIR = QAction(MainWindow)
        self.actionFAIR.setObjectName(u"actionFAIR")
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
        icon3 = QIcon()
        icon3.addFile(u":/\u65b0\u524d\u7f00/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStart.setIcon(icon3)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1044, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionStart)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionEXit)

        self.retranslateUi(MainWindow)
        self.actionEXit.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Perfusion Toolkit For Rodent", None))
#if QT_CONFIG(statustip)
        MainWindow.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.actionSelect_Dicom_Folder.setText(QCoreApplication.translate("MainWindow", u"Select Dicom Folder", None))
        self.actionEXit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionFAIR.setText(QCoreApplication.translate("MainWindow", u"FAIR", None))
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Folder Browser", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

