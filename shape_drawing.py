import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint


class ShapeDrawingFunctions:
    """도형 그리기 기능만 담당하는 클래스"""
    
    def __init__(self, canvas_widget):
        """
        초기화
        canvas_widget: 그리기할 캔버스 위젯
        """
        self.canvas = canvas_widget
        self.current_shape = "사각형"  # 현재 선택된 도형
        self.is_drawing = False        # 그리기 중인지 여부
        self.start_x = 0               # 시작점 X 좌표
        self.start_y = 0               # 시작점 Y 좌표
        self.end_x = 0                 # 끝점 X 좌표
        self.end_y = 0                 # 끝점 Y 좌표
        
        # 캔버스 이미지 초기화
        self.canvas_image = QPixmap(self.canvas.size())
        self.canvas_image.fill(Qt.white)
    
    def set_shape(self, shape_name):
        """도형 종류 설정"""
        self.current_shape = shape_name
    
    def start_drawing(self, x, y):
        """그리기 시작"""
        self.is_drawing = True
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
    
    def update_drawing(self, x, y):
        """그리기 업데이트 (미리보기용)"""
        if self.is_drawing:
            self.end_x = x
            self.end_y = y
            self.canvas.update()
    
    def finish_drawing(self, x, y):
        """그리기 완료"""
        if self.is_drawing:
            self.end_x = x
            self.end_y = y
            self.draw_shape()
            self.is_drawing = False
    
    def draw_shape(self):
        """도형 그리기"""
        painter = QPainter(self.canvas_image)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        
        if self.current_shape == "사각형":
            self.draw_rectangle(painter)
        elif self.current_shape == "원":
            self.draw_circle(painter)
        elif self.current_shape == "삼각형":
            self.draw_triangle(painter)
        elif self.current_shape == "직선":
            self.draw_line(painter)
        
        self.canvas.update()
    
    def draw_rectangle(self, painter):
        """사각형 그리기"""
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        painter.drawRect(left, top, width, height)
    
    def draw_circle(self, painter):
        """원 그리기"""
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        painter.drawEllipse(left, top, width, height)
    
    def draw_triangle(self, painter):
        """삼각형 그리기"""
        # 삼각형의 세 점 계산
        center_x = (self.start_x + self.end_x) // 2
        top_x = center_x
        top_y = self.start_y
        left_x = self.start_x
        left_y = self.end_y
        right_x = self.end_x
        right_y = self.end_y
        
        # 삼각형 그리기
        painter.drawLine(top_x, top_y, left_x, left_y)
        painter.drawLine(left_x, left_y, right_x, right_y)
        painter.drawLine(right_x, right_y, top_x, top_y)
    
    def draw_line(self, painter):
        """직선 그리기"""
        painter.drawLine(self.start_x, self.start_y, self.end_x, self.end_y)
    
    def draw_preview(self, painter):
        """미리보기 그리기"""
        if self.is_drawing:
            painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
            
            if self.current_shape == "사각형":
                self.draw_rectangle_preview(painter)
            elif self.current_shape == "원":
                self.draw_circle_preview(painter)
            elif self.current_shape == "삼각형":
                self.draw_triangle_preview(painter)
            elif self.current_shape == "직선":
                self.draw_line_preview(painter)
    
    def draw_rectangle_preview(self, painter):
        """사각형 미리보기"""
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        painter.drawRect(left, top, width, height)
    
    def draw_circle_preview(self, painter):
        """원 미리보기"""
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        painter.drawEllipse(left, top, width, height)
    
    def draw_triangle_preview(self, painter):
        """삼각형 미리보기"""
        center_x = (self.start_x + self.end_x) // 2
        top_x = center_x
        top_y = self.start_y
        left_x = self.start_x
        left_y = self.end_y
        right_x = self.end_x
        right_y = self.end_y
        
        painter.drawLine(top_x, top_y, left_x, left_y)
        painter.drawLine(left_x, left_y, right_x, right_y)
        painter.drawLine(right_x, right_y, top_x, top_y)
    
    def draw_line_preview(self, painter):
        """직선 미리보기"""
        painter.drawLine(self.start_x, self.start_y, self.end_x, self.end_y)
    
    def clear_canvas(self):
        """캔버스 지우기"""
        self.canvas_image.fill(Qt.white)
        self.canvas.update()
    
    def get_canvas_image(self):
        """캔버스 이미지 반환"""
        return self.canvas_image
    
    def set_canvas_image(self, pixmap):
        """캔버스 이미지 설정"""
        self.canvas_image = pixmap
        self.canvas.update()
