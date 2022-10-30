
from signal import SIG_DFL
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *



class MTableView(QTableView):
    selected_row = Signal(int)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.verticalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._menu = QMenu(self)
        self.setup_menu()

    def resizeEvent(self, event) -> None:
        self.resizeColumnToContents(0)
        width = (self.viewport().width() - self.columnWidth(0))//2
        self.setColumnWidth(1, width)
        self.setColumnWidth(2, (self.viewport().width() - self.columnWidth(0)) - width)
        return super().resizeEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(event)
        print(self.selectedIndexes())
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        return super().mouseDoubleClickEvent(event)


    def contextMenuEvent(self, arg__1: QContextMenuEvent) -> None:
        self.Menu.exec_(QCursor.pos())
        print(QCursor.pos())


    def setup_menu(self) -> None:
        self._menu.addAction('Select as S0')
        self._menu.addAction('Delete this Point')



    @property
    def Menu(self) -> QMenu:
        return self._menu