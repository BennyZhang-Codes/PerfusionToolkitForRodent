from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from MyWidgets.Mmodel.TabelModel import *

class MTableView(QTableView):
    selected_row = Signal(int)
    changed_rows = Signal(list)  # rows[list]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # self.setFocusPolicy(Qt.NoFocus)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._menu = QMenu(self)
        self.setup_menu()
        self.setStyleSheet('''
        QHeaderView::down-arrow {
            border: none;
            height: 0px;
            width: 0px;
            padding-left: 0px;
            padding-right: 0px;
        }
        ''')
    

    def resizeEvent(self, event) -> None:
        self.resizeColumnToContents(0)
        width = (self.viewport().width() - self.columnWidth(0))//2
        self.setColumnWidth(1, width)
        self.setColumnWidth(2, (self.viewport().width() - self.columnWidth(0)) - width)
        return super().resizeEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        v = self.horizontalHeader()
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        row = self._selectedRows()[0]
        self.selected_row.emit(row)
        return super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, arg__1: QContextMenuEvent) -> None:
        self.Menu.exec_(QCursor.pos())


    def setup_menu(self) -> None:
        action_select_s0 = self.Menu.addAction('Select as S0')
        action_select_s0.triggered.connect(self._action_select_s0)

        action_deselect_s0 = self.Menu.addAction('Deselect as S0')
        action_deselect_s0.triggered.connect(self._action_deselect_s0)

        # action_delete = self.Menu.addAction('Delete')
        # action_delete.triggered.connect(self._action_delete)

        # action_delete_cancel = self.Menu.addAction('Delete cancel')
        # action_delete_cancel.triggered.connect(self._action_delete_cancel)
        
    def _action_select_s0(self) -> None:
        rows = self._selectedRows()
        self.model().set_S0(rows, True)
        self.changed_rows.emit(rows)
        

    def _action_deselect_s0(self) -> None:
        rows = self._selectedRows()
        self.model().set_S0(rows, False)
        self.changed_rows.emit(rows)

    def _action_delete(self) -> None:
        rows = self._selectedRows()
        self.model().set_delete(rows, False)
        self.changed_rows.emit(rows)

    def _action_delete_cancel(self) -> None:
        rows = self._selectedRows()
        self.model().set_delete(rows, True)
        self.changed_rows.emit(rows)

    def _selectedRows(self) -> list:
        rows = set()
        for Index in self.selectedIndexes():
            rows.add(Index.row())
        rows = list(rows)
        rows.sort()
        return rows
    def model(self) -> TimePointsTableModel:
        return super().model()

    @property
    def Menu(self) -> QMenu:
        return self._menu