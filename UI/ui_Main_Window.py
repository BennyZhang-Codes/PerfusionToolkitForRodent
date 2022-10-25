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
    QToolBar, QWidget)
from UI import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1060, 714)
        icon = QIcon()
        icon.addFile(u":/\u65b0\u524d\u7f00/qrc/GUI_Logo.ico", QSize(), QIcon.Normal, QIcon.On)
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
        icon2.addFile(u":/\u65b0\u524d\u7f00/qrc/Exit.png", QSize(), QIcon.Normal, QIcon.On)
        self.actionEXit.setIcon(icon2)
        self.actionFAIR = QAction(MainWindow)
        self.actionFAIR.setObjectName(u"actionFAIR")
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
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
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1060, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menuBar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menuBar)

        self.toolBar.addAction(self.actionSelect_Dicom_Folder)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionFAIR)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuFile.addAction(self.actionSelect_Dicom_Folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionEXit)
        self.menuTools.addAction(self.actionStart)
        self.menuTools.addAction(self.actionFAIR)

        self.retranslateUi(MainWindow)
        self.actionEXit.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Dicom", None))
#if QT_CONFIG(statustip)
        MainWindow.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.actionSelect_Dicom_Folder.setText(QCoreApplication.translate("MainWindow", u"Select Dicom Folder", None))
        self.actionEXit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionFAIR.setText(QCoreApplication.translate("MainWindow", u"FAIR", None))
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

