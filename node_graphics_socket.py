
from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent=None,  socket_type=True, socket=None):
        super().__init__(parent=parent)

        self.socket = socket
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()
        self.color =[
            QColor("#FFFF7700"),
            QColor("#FF52e220"),
            QColor("#FF0056a6"),
            QColor("#FFb51d14"),
            QColor("#FFdeb500"),
            QColor("#FF9500b5"),
            QColor("#FF00c9b5")]

        self.radius = 6
        self.outline_width = 1

        self._color_background = self.color[socket_type]
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)

        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        #PAINTING CIRCLE
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)


    def boundingRect(self):

        return QRectF(
            -self.radius - self.outline_width,
            -self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )






