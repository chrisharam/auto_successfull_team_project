# auto_successfull_team_project
SW CAMP PROJECT
import sys
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QBrush, QImage, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QColorDialog,
    QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLabel, QCheckBox
)

class PaintCanvas(QWidget):
    """
    최소 개념:
    - 내부 QImage(800x500 고정)에 그리고, paintEvent에서 화면에 보여줌
    - brush는 즉시 QImage에, 도형(line/rect/ellipse)은 드래그 중 오버레이 → 릴리즈 시 QImage에 확정
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage(800, 500, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.setFixedSize(800, 500)

        # 상태
        self.drawing = False
        self.tool = "brush"          # brush | line | rect | ellipse
        self.pen_width = 5
        self.stroke_color = QColor(0, 0, 0)
        self.fill_enabled = False
        self.fill_color = QColor(255, 255, 255)

        # 포인트
        self.start_point = QPoint()
        self.last_point = QPoint()
        self.temp_point = QPoint()

    # ---- 외부에서 호출할 간단 API ----
    def set_tool(self, tool): self.tool = tool
    def set_pen_width(self, w): self.pen_width = max(1, int(w))
    def set_stroke_color(self, c): self.stroke_color = QColor(c)
    def set_fill_color(self, c): self.fill_color = QColor(c)
    def set_fill_enabled(self, enabled): self.fill_enabled = bool(enabled)

    def clear_canvas(self):
        self.image.fill(Qt.white)
        self.update()

    def save_image(self, path):
        return self.image.save(path)

    # ---- 입력 이벤트 ----
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = e.pos()
            self.last_point = e.pos()
            self.temp_point = e.pos()
            if self.tool == "brush":
                self._draw_line_on_image(self.last_point, e.pos())
                self.update()

    def mouseMoveEvent(self, e):
        if self.drawing and (e.buttons() & Qt.LeftButton):
            self.temp_point = e.pos()
            if self.tool == "brush":
                self._draw_line_on_image(self.last_point, self.temp_point)
                self.last_point = self.temp_point
                self.update()
            else:
                # 도형은 오버레이 미리보기만
                self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            end = e.pos()
            if self.tool == "brush":
                self._draw_line_on_image(self.last_point, end)
            elif self.tool == "line":
                self._draw_line_shape(self.start_point, end)
            elif self.tool == "rect":
                self._draw_rect_shape(self.start_point, end)
            elif self.tool == "ellipse":
                self._draw_ellipse_shape(self.start_point, end)
            self.update()

    # ---- 그리기 ----
    def paintEvent(self, _):
        # 1) 실제 이미지
        p = QPainter(self)
        p.drawImage(0, 0, self.image)
        p.end()

        # 2) 도형 미리보기(드래그 중)
        if self.drawing and self.tool in ("line", "rect", "ellipse"):
            view = QPainter(self)
            view.setRenderHint(QPainter.Antialiasing, True)
            pen = QPen(self.stroke_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            view.setPen(pen)
            view.setBrush(QBrush(self.fill_color if self.fill_enabled else Qt.NoBrush))

            r = self._rect_from_points(self.start_point, self.temp_point)
            if self.tool == "line":
                view.drawLine(self.start_point, self.temp_point)
            elif self.tool == "rect":
                view.drawRect(r)
            elif self.tool == "ellipse":
                view.drawEllipse(r)
            view.end()

    # ---- 내부 유틸리티 ----
    def _rect_from_points(self, p1, p2):
        return QRect(min(p1.x(), p2.x()), min(p1.y(), p2.y()),
                     abs(p1.x() - p2.x()), abs(p1.y() - p2.y()))

    def _make_pen(self):
        pen = QPen(self.stroke_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        return pen

    def _draw_line_on_image(self, p1, p2):
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self._make_pen())
        painter.drawLine(p1, p2)
        painter.end()

    def _draw_line_shape(self, p1, p2):
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self._make_pen())
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(p1, p2)
        painter.end()

    def _draw_rect_shape(self, p1, p2):
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self._make_pen())
        painter.setBrush(QBrush(self.fill_color if self.fill_enabled else Qt.NoBrush))
        painter.drawRect(self._rect_from_points(p1, p2))
        painter.end()

    def _draw_ellipse_shape(self, p1, p2):
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self._make_pen())
        painter.setBrush(QBrush(self.fill_color if self.fill_enabled else Qt.NoBrush))
        painter.drawEllipse(self._rect_from_points(p1, p2))
        painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("초간단 PyQt 그림판 (도형 + 채우기)")
        self.canvas = PaintCanvas()

        # 도구 버튼
        btn_brush = QPushButton("브러시")
        btn_line = QPushButton("직선")
        btn_rect = QPushButton("사각형")
        btn_ellipse = QPushButton("원")
        btn_brush.clicked.connect(lambda: self.canvas.set_tool("brush"))
        btn_line.clicked.connect(lambda: self.canvas.set_tool("line"))
        btn_rect.clicked.connect(lambda: self.canvas.set_tool("rect"))
        btn_ellipse.clicked.connect(lambda: self.canvas.set_tool("ellipse"))

        # 색상/채우기/굵기
        btn_stroke = QPushButton("윤곽선 색")
        btn_fill = QPushButton("면색")
        chk_fill = QCheckBox("채우기")
        chk_fill.stateChanged.connect(lambda s: self.canvas.set_fill_enabled(s == Qt.Checked))

        lbl_width = QLabel("굵기")
        sld_width = QSlider(Qt.Horizontal)
        sld_width.setRange(1, 30)
        sld_width.setValue(5)
        sld_width.setFixedWidth(150)
        sld_width.valueChanged.connect(self.canvas.set_pen_width)

        btn_stroke.clicked.connect(self.pick_stroke)
        btn_fill.clicked.connect(self.pick_fill)

        # 지우기/저장
        btn_clear = QPushButton("전체 지우기")
        btn_save = QPushButton("저장")
        btn_clear.clicked.connect(self.canvas.clear_canvas)
        btn_save.clicked.connect(self.save_image)

        # 배치
        tools = QHBoxLayout()
        tools.setSpacing(8)
        for w in (btn_brush, btn_line, btn_rect, btn_ellipse,
                  btn_stroke, btn_fill, chk_fill, lbl_width, sld_width,
                  btn_clear, btn_save):
            tools.addWidget(w)
        tools.addStretch()

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addLayout(tools)
        layout.addWidget(self.canvas)

        self.setCentralWidget(root)
        self.resize(900, 620)

    def pick_stroke(self):
        c = QColorDialog.getColor(self.canvas.stroke_color, self, "윤곽선 색")
        if c.isValid():
            self.canvas.set_stroke_color(c)

    def pick_fill(self):
        c = QColorDialog.getColor(self.canvas.fill_color, self, "면색")
        if c.isValid():
            self.canvas.set_fill_color(c)

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "이미지 저장", "drawing.png",
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp)"
        )
        if path:
            self.canvas.save_image(path)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
