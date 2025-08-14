from __future__ import annotations
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass, field
import math

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush, QColor

ColorLike = Union[str, Tuple[int, int, int], QColor]

def _to_qcolor(c: Optional[ColorLike]) -> Optional[QColor]:
    if c is None:
        return None
    if isinstance(c, QColor):
        return QColor(c)
    if isinstance(c, tuple) and len(c) == 3:
        r, g, b = c
        return QColor(int(r), int(g), int(b))
    return QColor(str(c))

_id_seed = 0
def _next_id() -> int:
    global _id_seed
    _id_seed += 1
    return _id_seed

@dataclass
class Shape:
    id: int
    stroke: QColor
    width: int
    fill: Optional[QColor] = None

    def draw(self, p: QPainter) -> None:
        raise NotImplementedError

    def contains(self, pt: QPoint) -> bool:
        raise NotImplementedError

    def set_fill(self, color: Optional[ColorLike]) -> None:
        self.fill = _to_qcolor(color)

@dataclass
class LineShape(Shape):
    p1: QPoint = field(default_factory=QPoint)
    p2: QPoint = field(default_factory=QPoint)

    def draw(self, p: QPainter) -> None:
        p.setPen(QPen(self.stroke, self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        p.setBrush(Qt.NoBrush)
        p.drawLine(self.p1, self.p2)

    def contains(self, pt: QPoint) -> bool:
        x, y = pt.x(), pt.y()  # <- pt.y() 추가
        x1, y1 = self.p1.x(), self.p1.y()
        x2, y2 = self.p2.x(), self.p2.y()
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            dist = math.hypot(x - x1, y - y1)
        else:
            t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / float(dx*dx + dy*dy)))
            projx, projy = x1 + t*dx, y1 + t*dy
            dist = math.hypot(x - projx, y - projy)
        return dist <= max(3.0, self.width/2 + 1.5)

@dataclass
class RectShape(Shape):
    rect: QRect = field(default_factory=QRect)

    def draw(self, p: QPainter) -> None:
        p.setPen(QPen(self.stroke, self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        p.setBrush(QBrush(self.fill) if self.fill is not None else Qt.NoBrush)
        p.drawRect(self.rect)

    def contains(self, pt: QPoint) -> bool:
        return self.rect.contains(pt)

@dataclass
class EllipseShape(Shape):
    rect: QRect = field(default_factory=QRect)

    def draw(self, p: QPainter) -> None:
        p.setPen(QPen(self.stroke, self.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        p.setBrush(QBrush(self.fill) if self.fill is not None else Qt.NoBrush)
        p.drawEllipse(self.rect)

    def contains(self, pt: QPoint) -> bool:
        if self.rect.width() == 0 or self.rect.height() == 0:
            return False
        cx = self.rect.x() + self.rect.width()/2.0
        cy = self.rect.y() + self.rect.height()/2.0
        rx = self.rect.width()/2.0
        ry = self.rect.height()/2.0
        nx = (pt.x() - cx)/rx
        ny = (pt.y() - cy)/ry
        return nx*nx + ny*ny <= 1.0

class CanvasCore:
    def __init__(self, width:int=800, height:int=500, bg:ColorLike="white") -> None:
        self._bg = _to_qcolor(bg) or QColor(Qt.white)
        self.image = QImage(width, height, QImage.Format_RGB32)
        self.shapes: List[Shape] = []
        self._clear_image()

    def add_line(self, p1:Tuple[int,int], p2:Tuple[int,int], stroke:ColorLike="black", width:int=3) -> int:
        s = LineShape(id=_next_id(), stroke=_to_qcolor(stroke) or QColor(Qt.black),
                      width=max(1,width), fill=None, p1=QPoint(*p1), p2=QPoint(*p2))
        self.shapes.append(s)
        return s.id

    def add_rect(self, p1:Tuple[int,int], p2:Tuple[int,int], stroke:ColorLike="black",
                 width:int=3, fill:Optional[ColorLike]=None) -> int:
        rect = _make_rect(p1,p2)
        s = RectShape(id=_next_id(), stroke=_to_qcolor(stroke) or QColor(Qt.black),
                      width=max(1,width), fill=_to_qcolor(fill), rect=rect)
        self.shapes.append(s)
        return s.id

    def add_ellipse(self, p1:Tuple[int,int], p2:Tuple[int,int], stroke:ColorLike="black",
                    width:int=3, fill:Optional[ColorLike]=None) -> int:
        rect = _make_rect(p1,p2)
        s = EllipseShape(id=_next_id(), stroke=_to_qcolor(stroke) or QColor(Qt.black),
                         width=max(1,width), fill=_to_qcolor(fill), rect=rect)
        self.shapes.append(s)
        return s.id

    def set_fill_by_id(self, shape_id:int, color:Optional[ColorLike]) -> bool:
        shp = self._find(shape_id)
        if not shp: return False
        if isinstance(shp, LineShape):
            shp.set_fill(None)
            return True
        shp.set_fill(color)
        return True

    def set_fill_at_point(self, xy:Tuple[int,int], color:Optional[ColorLike]) -> Optional[int]:
        pt = QPoint(*xy)
        for shp in reversed(self.shapes):
            if isinstance(shp, LineShape): continue
            if shp.contains(pt):
                shp.set_fill(color)
                return shp.id
        return None

    def render(self) -> None:
        self._clear_image()
        p = QPainter(self.image)
        p.setRenderHint(QPainter.Antialiasing, True)
        for shp in self.shapes:
            shp.draw(p)
        p.end()

    def save_image(self, path:str) -> bool:
        self.render()
        return self.image.save(path)

    def clear(self) -> None:
        self.shapes.clear()
        self._clear_image()

    def _clear_image(self) -> None:
        self.image.fill(self._bg)

    def _find(self, shape_id:int) -> Optional[Shape]:
        return next((s for s in self.shapes if s.id==shape_id), None)

def _make_rect(p1:Tuple[int,int], p2:Tuple[int,int]) -> QRect:
    x1,y1 = p1
    x2,y2 = p2
    return QRect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
