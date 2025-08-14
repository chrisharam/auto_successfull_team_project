import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QColorDialog, QSlider, 
                             QLabel, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QRect


class ShapeCanvas(QWidget):
    """도형을 그릴 수 있는 캔버스 클래스"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_canvas()
    
    def init_canvas(self):
        """캔버스 초기화"""
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: white; border: 2px solid gray;")
        
        # 도형 그리기 관련 변수들
        self.drawing_mode = "rectangle"  # rectangle, circle, triangle, line
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_drawing_shape = False
        
        # 브러시 설정
        self.brush_color = QColor(0, 0, 0)  # 기본 검은색
        self.brush_size = 3  # 기본 브러시 크기
        
        # 캔버스 초기화
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.white)
    
    def paintEvent(self, event):
        """캔버스 그리기 이벤트"""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        
        # 도형 그리기 중일 때 미리보기 표시
        if self.is_drawing_shape:
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            
            if self.drawing_mode == "rectangle":
                rect = self.get_rect_from_points()
                painter.drawRect(rect)
            elif self.drawing_mode == "circle":
                rect = self.get_rect_from_points()
                painter.drawEllipse(rect)
            elif self.drawing_mode == "triangle":
                self.draw_triangle_preview(painter)
            elif self.drawing_mode == "line":
                painter.drawLine(self.start_point, self.end_point)
    
    def draw_triangle_preview(self, painter):
        """삼각형 미리보기 그리기"""
        # 삼각형의 세 점 계산
        center_x = (self.start_point.x() + self.end_point.x()) // 2
        
        # 삼각형의 세 점
        top_point = QPoint(center_x, self.start_point.y())
        left_point = QPoint(self.start_point.x(), self.end_point.y())
        right_point = QPoint(self.end_point.x(), self.end_point.y())
        
        # 삼각형 그리기
        path = QPainterPath()
        path.moveTo(top_point)
        path.lineTo(left_point)
        path.lineTo(right_point)
        path.lineTo(top_point)
        
        painter.drawPath(path)
    
    def mousePressEvent(self, event):
        """마우스 클릭 이벤트"""
        if event.button() == Qt.LeftButton:
            self.is_drawing_shape = True
            self.start_point = event.pos()
            self.end_point = event.pos()
    
    def mouseMoveEvent(self, event):
        """마우스 이동 이벤트"""
        if self.is_drawing_shape and event.buttons() & Qt.LeftButton:
            self.end_point = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        """마우스 릴리즈 이벤트"""
        if event.button() == Qt.LeftButton and self.is_drawing_shape:
            self.end_point = event.pos()
            self.draw_shape()
            self.is_drawing_shape = False
    
    def resizeEvent(self, event):
        """캔버스 크기 변경 이벤트"""
        if self.width() > 0 and self.height() > 0:
            new_pixmap = QPixmap(self.size())
            new_pixmap.fill(Qt.white)
            painter = QPainter(new_pixmap)
            painter.drawPixmap(0, 0, self.pixmap)
            self.pixmap = new_pixmap
    
    def clear_canvas(self):
        """캔버스 지우기"""
        self.pixmap.fill(Qt.white)
        self.update()
    
    def set_brush_color(self, color):
        """브러시 색상 설정"""
        self.brush_color = color
    
    def set_brush_size(self, size):
        """브러시 크기 설정"""
        self.brush_size = size
    
    def set_drawing_mode(self, mode):
        """그리기 모드 설정"""
        self.drawing_mode = mode
    
    def draw_shape(self):
        """도형 그리기"""
        if self.drawing_mode == "rectangle":
            self.draw_rectangle()
        elif self.drawing_mode == "circle":
            self.draw_circle()
        elif self.drawing_mode == "triangle":
            self.draw_triangle()
        elif self.drawing_mode == "line":
            self.draw_line()
    
    def draw_rectangle(self):
        """사각형 그리기"""
        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        
        rect = self.get_rect_from_points()
        painter.drawRect(rect)
        self.update()
    
    def draw_circle(self):
        """원 그리기"""
        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        
        rect = self.get_rect_from_points()
        painter.drawEllipse(rect)
        self.update()
    
    def draw_triangle(self):
        """삼각형 그리기"""
        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        
        # 삼각형의 세 점 계산
        center_x = (self.start_point.x() + self.end_point.x()) // 2
        
        # 삼각형의 세 점
        top_point = QPoint(center_x, self.start_point.y())
        left_point = QPoint(self.start_point.x(), self.end_point.y())
        right_point = QPoint(self.end_point.x(), self.end_point.y())
        
        # 삼각형 그리기
        path = QPainterPath()
        path.moveTo(top_point)
        path.lineTo(left_point)
        path.lineTo(right_point)
        path.lineTo(top_point)
        
        painter.drawPath(path)
        self.update()
    
    def draw_line(self):
        """직선 그리기"""
        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, 
                           Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.start_point, self.end_point)
        self.update()
    
    def get_rect_from_points(self):
        """두 점으로부터 사각형 생성"""
        return QRect(
            min(self.start_point.x(), self.end_point.x()),
            min(self.start_point.y(), self.end_point.y()),
            abs(self.end_point.x() - self.start_point.x()),
            abs(self.end_point.y() - self.start_point.y())
        )
    
    def save_image(self, file_path):
        """이미지 저장"""
        return self.pixmap.save(file_path)


class ShapeDrawingApp(QMainWindow):
    """도형 그리기 애플리케이션 클래스"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("도형 그리기 도구")
        self.setGeometry(100, 100, 1000, 700)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QHBoxLayout(central_widget)
        
        # 캔버스 생성
        self.canvas = ShapeCanvas()
        main_layout.addWidget(self.canvas, stretch=4)
        
        # 컨트롤 패널 생성
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel, stretch=1)
    
    def create_control_panel(self):
        """컨트롤 패널 생성"""
        panel = QWidget()
        panel.setMaximumWidth(200)
        panel.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 제목
        title_label = QLabel("도형 그리기 도구")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # 색상 선택 버튼
        color_label = QLabel("선 색상:")
        layout.addWidget(color_label)
        
        self.color_button = QPushButton("색상 선택")
        self.color_button.clicked.connect(self.choose_color)
        layout.addWidget(self.color_button)
        
        # 현재 색상 표시
        self.current_color_label = QLabel("현재 색상: 검은색")
        self.current_color_label.setStyleSheet("padding: 5px; border: 1px solid #ccc; background-color: white;")
        layout.addWidget(self.current_color_label)
        
        # 선 두께 조절
        size_label = QLabel("선 두께:")
        layout.addWidget(size_label)
        
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(20)
        self.size_slider.setValue(3)
        self.size_slider.valueChanged.connect(self.change_brush_size)
        layout.addWidget(self.size_slider)
        
        self.size_label = QLabel("두께: 3")
        layout.addWidget(self.size_label)
        
        # 도형 도구 섹션
        shape_label = QLabel("도형 도구:")
        layout.addWidget(shape_label)
        
        # 사각형 버튼
        self.rectangle_button = QPushButton("사각형")
        self.rectangle_button.setStyleSheet("background-color: #FF9800;")
        self.rectangle_button.clicked.connect(lambda: self.set_drawing_mode("rectangle"))
        layout.addWidget(self.rectangle_button)
        
        # 원 버튼
        self.circle_button = QPushButton("원")
        self.circle_button.clicked.connect(lambda: self.set_drawing_mode("circle"))
        layout.addWidget(self.circle_button)
        
        # 삼각형 버튼
        self.triangle_button = QPushButton("삼각형")
        self.triangle_button.clicked.connect(lambda: self.set_drawing_mode("triangle"))
        layout.addWidget(self.triangle_button)
        
        # 직선 버튼
        self.line_button = QPushButton("직선")
        self.line_button.clicked.connect(lambda: self.set_drawing_mode("line"))
        layout.addWidget(self.line_button)
        
        # 기타 도구들
        tools_label = QLabel("기타 도구:")
        layout.addWidget(tools_label)
        
        clear_button = QPushButton("캔버스 지우기")
        clear_button.clicked.connect(self.canvas.clear_canvas)
        layout.addWidget(clear_button)
        
        save_button = QPushButton("이미지 저장")
        save_button.clicked.connect(self.save_image)
        layout.addWidget(save_button)
        
        # 빈 공간 추가
        layout.addStretch()
        
        return panel
    
    def choose_color(self):
        """색상 선택 다이얼로그"""
        color = QColorDialog.getColor(self.canvas.brush_color, self, "선 색상 선택")
        if color.isValid():
            self.canvas.set_brush_color(color)
            self.update_color_display(color)
    
    def update_color_display(self, color):
        """색상 표시 업데이트"""
        color_name = self.get_color_name(color)
        self.current_color_label.setText(f"현재 색상: {color_name}")
        self.current_color_label.setStyleSheet(
            f"padding: 5px; border: 1px solid #ccc; background-color: {color.name()}; color: {'white' if color.lightness() < 128 else 'black'};"
        )
    
    def get_color_name(self, color):
        """색상 이름 반환"""
        color_names = {
            (0, 0, 0): "검은색",
            (255, 255, 255): "흰색",
            (255, 0, 0): "빨간색",
            (0, 255, 0): "초록색",
            (0, 0, 255): "파란색",
            (255, 255, 0): "노란색",
            (255, 0, 255): "마젠타",
            (0, 255, 255): "시안",
            (128, 128, 128): "회색"
        }
        
        rgb = (color.red(), color.green(), color.blue())
        return color_names.get(rgb, f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")
    
    def change_brush_size(self, value):
        """선 두께 변경"""
        self.canvas.set_brush_size(value)
        self.size_label.setText(f"두께: {value}")
    
    def set_drawing_mode(self, mode):
        """그리기 모드 설정"""
        self.canvas.set_drawing_mode(mode)
        self.update_button_styles(mode)
    
    def update_button_styles(self, active_mode):
        """버튼 스타일 업데이트 (선택된 도구 강조)"""
        # 모든 도형 버튼 스타일 초기화
        default_style = "background-color: #4CAF50; color: white; border: none; padding: 8px; border-radius: 4px; font-weight: bold;"
        active_style = "background-color: #FF9800; color: white; border: none; padding: 8px; border-radius: 4px; font-weight: bold;"
        
        self.rectangle_button.setStyleSheet(active_style if active_mode == "rectangle" else default_style)
        self.circle_button.setStyleSheet(active_style if active_mode == "circle" else default_style)
        self.triangle_button.setStyleSheet(active_style if active_mode == "triangle" else default_style)
        self.line_button.setStyleSheet(active_style if active_mode == "line" else default_style)
    
    def save_image(self):
        """이미지 저장"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "이미지 저장", "", 
            "PNG 파일 (*.png);;JPEG 파일 (*.jpg);;모든 파일 (*)"
        )
        
        if file_path:
            try:
                if self.canvas.save_image(file_path):
                    QMessageBox.information(self, "성공", f"이미지가 저장되었습니다:\n{file_path}")
                else:
                    QMessageBox.warning(self, "오류", "이미지 저장에 실패했습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"저장 중 오류가 발생했습니다:\n{str(e)}")


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 애플리케이션 스타일 설정
    app.setStyle('Fusion')
    
    # 메인 윈도우 생성 및 표시
    window = ShapeDrawingApp()
    window.show()
    
    # 이벤트 루프 시작
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
