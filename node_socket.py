from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_socket import QDMGraphicsSocket
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket(Serializable):
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1):
        '''

        :param node:
        :param index:
        :param position:
        :param socket_type:
        '''
        super().__init__()

        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.grSocket = QDMGraphicsSocket(self.node.grNode, self.socket_type, self)
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

    def __str__(self):
        '''

        :return:
        '''
        return "<%s %s..%s>" % (self.__class__.__name__, hex(id(self))[2:5], hex(id(self))[-3:])


    def serialize(self):
        '''

        :return:
        '''
        dic_val = OrderedDict()
        dic_val['id'] = self.id
        dic_val['index'] = self.index
        dic_val['position'] = self.position
        dic_val['socket_type'] = self.socket_type

        return dic_val

    def deserialize(self, data, hashmap={}):
        '''

        :param data:
        :param hashmap:
        :return:
        '''
        print('deserialize: ', data)
        return False