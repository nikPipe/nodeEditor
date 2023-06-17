from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet

class QDMCutLine(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.line_points = []


        self._pen = QPen(QColor("#FF0000"))
        self._pen.setWidth(3)
        self._pen.setDashPattern([1, 4, 5, 4])

        self.setZValue(1000)


    def boundingRect(self):
        '''

        :return:
        '''
        return QRectF(0, 0, 1, 1)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)