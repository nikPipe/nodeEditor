from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet


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


        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)


        self.posSource = [0, 0]
        self.posDestination = [200, 100]

        self.setZValue(-1)


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        self.updatePath()
        if self.isSelected():
            painter.setPen(self._pen_selected)
        else:painter.setPen(self._pen)

        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())



    def updatePath(self):
        '''
        will handle drawing QPainterPath from Point A to B
        :return:
        '''
        raise NotImplemented("This method has to be overriden in a child class")


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)



class QDMGraphicsEdgeBasier(QDMGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]:dist *= -1




        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(
            s[0] + dist, s[1],
            d[0] - dist, d[1],
            self.posDestination[0], self.posDestination[1],
        )
        self.setPath(path)















