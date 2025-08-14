from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt

class ShapeDrawingFunctions:
    def __init__(self, canvas_widget: QWidget):
        self.canvas = canvas_widget
        self.current_shape = "사각형"
        self.is_drawing = False
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.canvas_image = QPixmap(self.canvas.size())
        self.canvas_image.fill(Qt.white)

    def set_shape(self, shape_name: str):
        self.current_shape = shape_name

    def start_drawing(self, x: int, y: int):
        self.is_drawing = True
        self.start_x, self.start_y = x, y
        self.end_x, self.end_y = x, y

    def update_drawing(self, x: int, y: int):
        if self.is_drawing:
            self.end_x, self.end_y = x, y
            self.canvas.update()

    def finish_drawing(self, x: int, y: int):
        if self.is_drawing:
            self.end_x, self.end_y = x, y
            self.draw_shape()
            self.is_drawing = False

    def draw_shape(self):
        painter = QPainter(self.canvas_image)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        if self.current_shape == "사각형":
            self._draw_rectangle(painter)
        elif self.current_shape == "원":
            self._draw_circle(painter)
        elif self.current_shape == "삼각형":
            self._draw_triangle(painter)
        elif self.current_shape == "직선":
            self._draw_line(painter)
        self.canvas.update()

    def _draw_rectangle(self, painter):
        left, top = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        width, height = abs(self.end_x - self.start_x), abs(self.end_y - self.start_y)
        painter.drawRect(left, top, width, height)

    def _draw_circle(self, painter):
        left, top = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        width, height = abs(self.end_x - self.start_x), abs(self.end_y - self.start_y)
        painter.drawEllipse(left, top, width, height)

    def _draw_triangle(self, painter):
        center_x = (self.start_x + self.end_x) // 2
        painter.drawLine(center_x, self.start_y, self.start_x, self.end_y)
        painter.drawLine(self.start_x, self.end_y, self.end_x, self.end_y)
        painter.drawLine(self.end_x, self.end_y, center_x, self.start_y)

    def _draw_line(self, painter):
        painter.drawLine(self.start_x, self.start_y, self.end_x, self.end_y)

    def draw_preview(self, painter):
        if not self.is_drawing:
            return
        painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
        if self.current_shape == "사각형":
            self._draw_rectangle(painter)
        elif self.current_shape == "원":
            self._draw_circle(painter)
        elif self.current_shape == "삼각형":
            self._draw_triangle(painter)
        elif self.current_shape == "직선":
            self._draw_line(painter)

    def clear_canvas(self):
        self.canvas_image.fill(Qt.white)
        self.canvas.update()

    def get_canvas_image(self):
        return self.canvas_image
