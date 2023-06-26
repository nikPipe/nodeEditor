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
        self._was_moved = False
        self._last_selected_state = False

        self._title = self.node.title


        self.initSize()
        self.initAssets()
        self.initUI()


    def initUI(self):
        '''

        :return:
        '''
        self.initTitle()
        self.initContent()
        self.title = self.node.title


        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initSize(self):
        '''

        :return:
        '''
        self.width = 180
        self.height = 240
        self.edge_roundness = 10.0
        self.edge_padding = 10.0
        self.title_height = 24.0
        self._title_horizontal_padding = 20.0
        self._title_vertical_padding = 4.0
    def initAssets(self):
        '''

        :return:
        '''
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

    def onSelected(self):
        #print("node_graphic_node.py onSelected")
        self.node.scene.grScene.itemSelected.emit()

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
        self.title_item.setPos(self._title_horizontal_padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self._title_horizontal_padding)

    def initContent(self):
        '''

        :return:
        '''
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(self.edge_padding),
                                 int(self.title_height + self.edge_padding),
                                 int(self.width - 2 * self.edge_padding),
                                 int(self.height - 2 * self.edge_padding - self.title_height))
        self.grContent.setWidget(self.content)


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


        self._was_moved = True

    def mouseReleaseEvent(self, event):
        '''

        :param event:
        :return:
        '''
        super().mouseReleaseEvent(event)
        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.storeHistory("Node moved")


        if self._last_selected_state != self.isSelected():
            self.node.scene.resetLastSelectedState()
            self._last_selected_state = self.isSelected()
            self.onSelected()


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
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        #CONTENT

        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        #OUTLINE
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        if self.isSelected():
            painter.setPen(self._pen_selected)
        else:
            painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())





















