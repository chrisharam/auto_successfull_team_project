# PyQt 도형 그리기 기능 모듈

PyQt5를 활용한 도형 그리기 기능만 담당하는 모듈입니다. UI 컴포넌트 없이 순수한 도형 그리기 기능만 제공하여 다른 프로젝트에 쉽게 통합할 수 있습니다.

## 주요 기능

### 🔷 도형 그리기 기능
- **사각형**: 드래그하여 사각형 그리기
- **원**: 드래그하여 원 그리기  
- **삼각형**: 드래그하여 삼각형 그리기
- **직선**: 드래그하여 직선 그리기
- 실시간 미리보기 기능

### 🎯 핵심 특징
- **순수 기능 모듈**: UI 컴포넌트 없이 기능만 제공
- **쉬운 통합**: 다른 프로젝트에 간단히 import 가능
- **간단한 API**: 직관적인 메서드명과 사용법

## 클래스 구조

### ShapeDrawingFunctions 클래스
```python
class ShapeDrawingFunctions:
    - __init__(canvas_widget): 캔버스 위젯으로 초기화
    - set_shape(shape_name): 도형 종류 설정
    - start_drawing(x, y): 그리기 시작
    - update_drawing(x, y): 그리기 업데이트 (미리보기)
    - finish_drawing(x, y): 그리기 완료
    - draw_preview(painter): 미리보기 그리기
    - clear_canvas(): 캔버스 지우기
    - get_canvas_image(): 캔버스 이미지 반환
    - set_canvas_image(pixmap): 캔버스 이미지 설정
```

## 설치 및 실행

### 1. 필요한 패키지 설치
```bash
pip install PyQt5
```

### 2. 모듈 사용
```python
from shape_drawing import ShapeDrawingFunctions
```

## 사용법

### 기본 사용법
```python
# 다른 프로젝트에서 사용할 때
from shape_drawing import ShapeDrawingFunctions

# 캔버스 위젯에 도형 기능 추가
shape_drawer = ShapeDrawingFunctions(your_canvas_widget)

# 도형 선택
shape_drawer.set_shape("사각형")

# 마우스 이벤트에서 호출
def mousePressEvent(self, event):
    shape_drawer.start_drawing(event.x(), event.y())

def mouseMoveEvent(self, event):
    shape_drawer.update_drawing(event.x(), event.y())

def mouseReleaseEvent(self, event):
    shape_drawer.finish_drawing(event.x(), event.y())

def paintEvent(self, event):
    painter = QPainter(self)
    painter.drawPixmap(0, 0, shape_drawer.get_canvas_image())
    shape_drawer.draw_preview(painter)
```

### 핵심 메서드
- `set_shape(shape_name)` - 도형 종류 설정 ("사각형", "원", "삼각형", "직선")
- `start_drawing(x, y)` - 그리기 시작
- `update_drawing(x, y)` - 그리기 업데이트 (미리보기)
- `finish_drawing(x, y)` - 그리기 완료
- `draw_preview(painter)` - 미리보기 그리기
- `clear_canvas()` - 캔버스 지우기
- `get_canvas_image()` - 캔버스 이미지 반환

## 기술적 특징

### 객체지향 설계
- 단일 책임 원칙: 도형 그리기 기능만 담당
- 캡슐화: 내부 구현은 숨기고 필요한 인터페이스만 제공
- 재사용성: 다양한 프로젝트에서 활용 가능

### 이벤트 처리
- 마우스 이벤트를 통한 직관적인 도형 그리기
- 실시간 미리보기 기능
- 드래그 앤 드롭 방식

### 확장성
- 새로운 도형 추가 용이
- 색상, 선 두께 등 추가 기능 확장 가능
- 다른 UI 프레임워크와도 호환 가능

## 파일 구조
```
auto_successfull_team_project/
├── shape_drawing.py   # 도형 그리기 기능 모듈
└── README.md          # 프로젝트 설명서
```

## 시스템 요구사항
- Python 3.6 이상
- PyQt5
- Windows/macOS/Linux 지원

## 협업 프로젝트에서의 활용

이 모듈은 협업 프로젝트에서 도형 그리기 기능을 담당하는 부분입니다. 다른 팀원들이 다음과 같은 기능들을 추가할 수 있습니다:

- **색상 선택 기능**
- **브러시 크기 조절**
- **이미지 저장 기능**
- **자유 그리기 기능**
- **UI 컴포넌트**

## 라이선스
이 프로젝트는 교육 목적으로 제작되었습니다.
