import math

from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_socket import *

EDGE_CP_ROUNDNESS = 100

class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.edge = edge
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")


        self._pen = QPen(self._color)
        self._pen.setWidthF(2.0)

        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)

        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen_dragging.setWidthF(2.0)


        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)


        self.posSource = [0, 0]
        self.posDestination = [200, 100]

        self.setZValue(-1)


    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]



    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        self.setPath(self.calcPath())

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:


            if self.isSelected():
                painter.setPen(self._pen_selected)
            else:painter.setPen(self._pen)

        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())



    def calcPath(self):
        '''
        will handle drawing QPainterPath from Point A to B
        :return:
        '''
        raise NotImplemented("This method has to be overriden in a child class")

    def intersectsWith(self, p1, p2):
        '''

        :param p1:
        :param p2:
        :return:
        '''
        cutpath = QPainterPath(p1)
        cutpath.lineTo(p2)
        path = self.calcPath()
        return cutpath.intersects(path)


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        return path



class QDMGraphicsEdgeBasier(QDMGraphicsEdge):
    def calcPath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        #if s[0] > d[0]:dist *= -1


        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0
        sspos = self.edge.start_socket.position

        if (s[0] > d[0] and sspos in [RIGHT_TOP, RIGHT_BOTTOM]) or (s[0] < d[0] and sspos in [LEFT_TOP, LEFT_BOTTOM]):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = (
                (s[1] - d[1]) / math.fabs(
                        s[1] - d[1] if s[1] - d[1] != 0 else 0.00001
                    )
                    ) * EDGE_CP_ROUNDNESS

            cpy_s = (
                (d[1] - s[1]) / math.fabs(
                        d[1] - s[1] if d[1] - s[1] != 0 else 0.00001
                    )
                    ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))

        path.cubicTo(
            s[0] + cpx_s, s[1] + cpy_s,
            d[0] + cpx_d, d[1] + cpy_d,
            self.posDestination[0], self.posDestination[1],
        )

        return path















