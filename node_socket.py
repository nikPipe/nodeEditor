from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_socket import QDMGraphicsSocket
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable


LEFT_TOP = 1
LEFT_CENTER = 2
LEFT_BOTTOM = 3
RIGHT_TOP = 4
RIGHT_CENTER = 5
RIGHT_BOTTOM = 6

class Socket(Serializable):
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1, multi_edges=True, count_on_this_node_side=1, is_input=False):
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
        self.is_multi_edges = multi_edges
        self.count_on_this_node_side = count_on_this_node_side
        self.is_input = is_input
        self.is_output = not self.is_input

        self.grSocket = QDMGraphicsSocket(self.node.grNode, self.socket_type, self)
        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.setSocketPosition()

        self.edges = []

    def setSocketPosition(self):
        '''

        :param position:
        :return:
        '''
        self.grSocket.setPos(*self.node.getSocketPosition(self.index, self.position, self.count_on_this_node_side))

    def getSocketPosition(self):
        '''

        :param index:
        :param position:
        :return:
        '''
        return self.node.getSocketPosition(self.index, self.position, self.count_on_this_node_side)

    def addEdge(self, edge):
        '''
        :param edge:
        :return:
        '''
        self.edges.append(edge)

    def removeEdge(self, edge):
        '''
        :param edge:
        :return:
        '''
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("!W:", "Socket::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")


    #def hasEdge(self):
    #    '''
    #    :return:
    #    '''
    #    return self.edges is not None

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
        dic_val['multi_edges'] = self.is_multi_edges
        dic_val['position'] = self.position
        dic_val['socket_type'] = self.socket_type

        return dic_val

    def deserialize(self, data, hashmap={}, restore_id=True):
        '''

        :param data:
        :param hashmap:
        :return:
        '''
        if restore_id:
            self.id = data['id']

        self.is_multi_edges = data['multi_edges']
        hashmap[data['id']] = self


        return True

    def removeEdges(self):
        '''

        :return:
        '''
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()
        #self.edges.clear()
