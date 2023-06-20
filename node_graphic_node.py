from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet


class QDmGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        '''

        :param node:
        :param title:
        '''
        super().__init__(parent)
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()


        self.node = node
        self.content = self.node.content
        self._title = self.node.title

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24.0
        self._padding = 20.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.initTitle()
        self.title = self.node.title

        #INIT SOCKET
        self.initSockets()

        #INIT CONTENT
        self.initContent()

        self.initUI()
        self.wasMoved = False

    def boundingRect(self):
        '''

        :return:
        '''
        return QRectF(0, 0,
                      (self.width),
                      (self.height)).normalized()

    def initTitle(self):
        '''

        :return:
        '''
        self.title_item = QGraphicsTextItem(self.title, self)
        self.title_item.node = self.node
        self.title_item.setFont(self._title_font)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self._padding)

    def initContent(self):
        '''

        :return:
        '''
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(self.edge_size),
                                 int(self.title_height + self.edge_size),
                                 int(self.width - 2 * self.edge_size),
                                 int(self.height - 2 * self.edge_size - self.title_height))
        self.grContent.setWidget(self.content)

    def initSockets(self):
        pass

    def initUI(self):
        '''

        :return:
        '''
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)



    def mouseMoveEvent(self, event):
        '''

        :param event:
        :return:
        '''
        super().mouseMoveEvent(event)
        #self.node.updateConnectedEdges()
        #TODO: update this selection nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()

                self.node.scene.hasBeenModified = True


        self.wasMoved = True

    def mouseReleaseEvent(self, event):
        '''

        :param event:
        :return:
        '''
        super().mouseReleaseEvent(event)
        if self.wasMoved:
            self.wasMoved = False
            self.node.scene.history.storeHistory("Node moved")


    @property
    def title(self):
        '''

        :return:
        '''
        return self._title

    @title.setter
    def title(self, value):
        '''

        :param value:
        :return:
        '''
        self._title = value
        self.title_item.setPlainText(self._title)


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        #Title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        #CONTENT

        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        #OUTLINE
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        if self.isSelected():
            painter.setPen(self._pen_selected)
        else:
            painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())





















