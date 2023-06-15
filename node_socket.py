from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_socket import QDMGraphicsSocket


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP):

        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.node = node
        self.index = index
        self.position = position
        self.grSocket = QDMGraphicsSocket(self.node.grNode)
        self.grSocket.setPos(*self.node.getSocketPosition(index, position))
