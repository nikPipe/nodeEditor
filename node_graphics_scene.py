
from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
import math





class QDMGraphicScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.scene = scene

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")
        self._grid_size = 20
        self._grid_squares = 5

        # light pen
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        # dark pen
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)


        self.setBackgroundBrush(self._color_background)


    def setGrScene(self, width, height):
        '''
        Set the size of the scene
        :param width:
        :param height:
        :return:
        '''
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        '''

        :param painter:
        :param rect:
        :return:
        '''
        super().drawBackground(painter, rect)
        # Draw Grid
        left = int(math.floor(rect.left()))
        top = int(math.floor(rect.top()))
        right = int(math.ceil(rect.right()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self._grid_size)
        first_top = top - (top % self._grid_size)

        # COMPUTE GRID SIZE
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self._grid_size):
            if (x % (self._grid_size * self._grid_squares)) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self._grid_size):
            if (y % (self._grid_squares * self._grid_size)) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # DRAW GRID
        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)





















