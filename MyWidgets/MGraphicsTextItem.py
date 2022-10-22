from PySide6.QtWidgets import QGraphicsTextItem
from MyWidgets.MGraphicsItem import MGraphicsItem



class MTextItem(MGraphicsItem):
    def __init_MTextItem__(self) -> None:
        super().__init_MGraphicsItem__()
        self.ItemType = 'info'

class MGraphicsTextItem(QGraphicsTextItem, MTextItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_MTextItem__()