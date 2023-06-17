from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_edge import *
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2





class Edge(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None, edge_type=EDGE_TYPE_DIRECT):
        '''
        :param scene:
        :param start_socket:
        :param end_socket:
        '''
        super().__init__()
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)


    @property
    def end_socket(self):
        '''
        :return:
        '''
        return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        '''
        :param value:
        :return:
        '''
        self._end_socket = value
        if self._end_socket is not None:
            self._end_socket.edge = self



    @property
    def start_socket(self):
        '''
        :return:
        '''
        return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        '''
        :param value:
        :return:
        '''
        self._start_socket = value
        if self._start_socket is not None:
            self._start_socket.edge = self

    @property
    def edge_type(self):
        '''
        :return:
        '''
        return self._edge_type

    @edge_type.setter
    def edge_type(self, value):
        '''

        :param value:
        :return:
        '''
        if hasattr(self, 'grEdge') and self.grEdge is not None:
            self.scene.grScene.removeItem(self.grEdge)

        self._edge_type = value
        if self._edge_type == EDGE_TYPE_DIRECT:
            self.grEdge = QDMGraphicsEdgeDirect(self)
        elif self._edge_type == EDGE_TYPE_BEZIER:
            self.grEdge = QDMGraphicsEdgeBasier(self)
        else:
            self.grEdge = QDMGraphicsEdgeBasier(self)

        self.scene.grScene.addItem(self.grEdge)
        if self.start_socket is not None:
            self.updatePositions()


    def updatePositions(self):
        '''

        :return:
        '''
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)

        self.grEdge.update()


    def remove_from_socket(self):
        '''
        :return:
        '''
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None

        self.end_socket = None
        self.start_socket = None

    def remove(self):
        '''
        :return:
        '''
        self.remove_from_socket()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        try:
            self.scene.removeEdge(self)
        except: pass

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
        dic_val['type'] = self.edge_type
        dic_val['start'] = self.start_socket.id
        dic_val['end'] = self.end_socket.id if self.end_socket is not None else None
        return dic_val

    def deserialize(self, data, hashmap={}):
        '''

        :param data:
        :param hashmap:
        :return:
        '''

        self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']] if data['end'] is not None else None
        self.edge_type = data['type']

        return True