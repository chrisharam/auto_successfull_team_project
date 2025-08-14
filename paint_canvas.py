# paint_canvas.py
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt, QPoint

class PaintCanvas(QWidget):
    def __init__(self, width=700, height=600):
        super().__init__()
        self.setFixedSize(width, height)
        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.white)
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = Qt.black
        self.pen_width = 3

    def change_color(self, color):
        self.pen_color = color

    def change_width(self, width):
        self.pen_width = width

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.canvas)
            pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
