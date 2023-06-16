from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2



class Edge():
    def __init__(self, scene, start_socket, end_socket, type=EDGE_TYPE_DIRECT):
        '''
        :param scene:
        :param start_socket:
        :param end_socket:
        '''
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.grEdge = QDMGraphicsEdgeDirect(self) if type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBasier(self)
        self.updatePositions()
        self.scene.grScene.addItem(self.grEdge)

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
        self.scene.removeEdge(self)
            


