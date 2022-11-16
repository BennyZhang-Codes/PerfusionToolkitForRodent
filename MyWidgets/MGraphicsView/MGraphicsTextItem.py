from PySide6.QtWidgets import QGraphicsTextItem


class MGraphicsTextItem(QGraphicsTextItem, ):
    def __init__(self):
        super().__init__()
        self._itemtype = 'info'
        
    @property
    def ItemType(self) -> str:
        return self._itemtype