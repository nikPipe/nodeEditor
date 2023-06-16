from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_socket import QDMGraphicsSocket


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1):

        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.grSocket = QDMGraphicsSocket(self.node.grNode, self.socket_type)
        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None

    def getSocketPosition(self):
        '''

        :param index:
        :param position:
        :return:
        '''
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge=None):
        '''
        :param edge:
        :return:
        '''
        self.edge = edge

    def hasEdge(self):
        '''
        :return:
        '''
        return self.edge is not None
