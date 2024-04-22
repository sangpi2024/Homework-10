from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QRectF, Qt


class SpringItem(QGraphicsItem):
    """
    Custom QGraphicsItem to represent a spring.
    """

    def __init__(self, x, y, width, height, coils=5, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.coils = coils

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawLine(self.x + self.width / 2, self.y, self.x + self.width / 2,
                         self.y + self.height / (2 * self.coils))
        for i in range(self.coils):
            rect = QRectF(self.x, self.y + (self.height / self.coils) * i, self.width, self.height / self.coils)
            if i % 2 == 0:
                painter.drawArc(rect, 0, 180 * 16)
            else:
                painter.drawArc(rect, 180 * 16, 180 * 16)
        painter.drawLine(self.x + self.width / 2, self.y + self.height, self.x + self.width / 2,
                         self.y + self.height - self.height / (2 * self.coils))


class DashpotItem(QGraphicsItem):
    """
    Custom QGraphicsItem to represent a dashpot (damper).
    """

    def __init__(self, x, y, width, height, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawRect(self.x, self.y, self.width, self.height)
        painter.drawLine(self.x + self.width / 2, self.y, self.x + self.width / 2, self.y + self.height)


# Example usage in CarView.buildScene():
def buildScene(self):
    # ... existing code ...
    # Assume we have self.x_center, self.y_base, etc. as the center position to place the items.

    # Create and add a spring to the scene
    spring = SpringItem(self.x_center - 15, self.y_base - 100, 30, 100)
    self.scene.addItem(spring)

    # Create and add a dashpot to the scene
    dashpot = DashpotItem(self.x_center + 15, self.y_base - 100, 30, 100)
    self.scene.addItem(dashpot)

    # ... rest of the buildScene code ...
