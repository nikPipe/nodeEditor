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
        self.scene.grScene.addItem(self.grEdge)


