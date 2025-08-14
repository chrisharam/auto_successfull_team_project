import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

from canvas_core import CanvasCore
from paint_canvas import PaintCanvas
from shape_drawing import ShapeDrawingFunctions

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("통합 그림판 & 도형 테스트")
        self.setGeometry(100, 100, 1200, 700)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Free Paint Canvas
        self.free_paint_canvas = PaintCanvas()
        main_layout.addWidget(self.free_paint_canvas)

        # Shape & Color Layout
        color_layout = QVBoxLayout()
        main_layout.addLayout(color_layout)

        colors = [Qt.black, Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.magenta]
        for color in colors:
            btn = QPushButton()
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(f"background-color: {QColor(color).name()}")
            btn.clicked.connect(lambda checked, col=color: self.free_paint_canvas.change_color(col))
            color_layout.addWidget(btn)
        color_layout.addStretch()

        # Shape Canvas
        self.shape_label = QLabel("도형 그리기 영역")
        color_layout.addWidget(self.shape_label)
        self.shape_canvas_widget = QWidget()
        self.shape_canvas_widget.setFixedSize(400, 400)
        self.shape_canvas_widget.setStyleSheet("background-color: white;")
        color_layout.addWidget(self.shape_canvas_widget)

        self.shape_drawer = ShapeDrawingFunctions(self.shape_canvas_widget)
        self.shape_canvas_widget.paintEvent = self.shape_paint_event
        self.shape_canvas_widget.mousePressEvent = lambda e: self.shape_drawer.start_drawing(e.x(), e.y()) if e.button()==Qt.LeftButton else None
        self.shape_canvas_widget.mouseMoveEvent = lambda e: self.shape_drawer.update_drawing(e.x(), e.y())
        self.shape_canvas_widget.mouseReleaseEvent = lambda e: self.shape_drawer.finish_drawing(e.x(), e.y()) if e.button()==Qt.LeftButton else None

        for shape in ["사각형", "원", "삼각형", "직선"]:
            btn = QPushButton(shape)
            btn.clicked.connect(lambda checked, s=shape: self.shape_drawer.set_shape(s))
            color_layout.addWidget(btn)

        # CanvasCore test
        self.canvas_core = CanvasCore(width=400, height=400, bg="white")
        main_layout.addWidget(QLabel("CanvasCore 영역 (오프스크린 도형)"))
        self.canvas_core.add_rect((50, 50), (150, 150), stroke="red", width=3, fill="yellow")
        self.canvas_core.add_ellipse((200, 50), (300, 150), stroke="blue", width=2, fill="green")
        self.canvas_core.add_line((50, 200), (300, 300), stroke="black", width=4)
        self.canvas_core.render()
        self.canvas_core.image.save("canvas_core_test.png")

    def shape_paint_event(self, event):
        painter = QPainter(self.shape_canvas_widget)
        painter.drawPixmap(0, 0, self.shape_drawer.get_canvas_image())
        self.shape_drawer.draw_preview(painter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
