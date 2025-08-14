import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt, QPoint

# 그림판 UI
class PaintCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 600)
        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.white)
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = Qt.black
        self.pen_width = 3  # 선 굵기 옵션 추가 가능

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

# 메인 UI
class PaintApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("자유 그림판 (색상 선택 가능)")
        self.setGeometry(100, 100, 900, 600)

        layout = QHBoxLayout()
        self.setLayout(layout)

        # 그림판
        self.canvas = PaintCanvas()
        layout.addWidget(self.canvas)

        # 색상 선택 버튼 레이아웃
        color_layout = QVBoxLayout()
        layout.addLayout(color_layout)

        # 기본 색상 버튼
        self.colors = [Qt.black, Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.magenta]
        for color in self.colors:
            btn = QPushButton()
            btn.setStyleSheet(f"background-color: {QColor(color).name()}")
            btn.setFixedSize(50, 50)
            # 외부에서 호출 가능하도록 버튼 클릭 시 PaintCanvas 메서드 사용
            btn.clicked.connect(lambda checked, col=color: self.canvas.change_color(col))
            color_layout.addWidget(btn)

        color_layout.addStretch()

# main 블록 (main 브랜치에서만 실행)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec_())
