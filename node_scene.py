from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_scene import QDMGraphicScene

class Scene():
    def __init__(self):
        '''

        '''
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.nodes = []
        self.edges = []

        self.scene_width, self.scene_height = 64000, 64000

        self.initUI()


    def initUI(self):
        '''

        :return:
        '''
        self.grScene = QDMGraphicScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)



    def addNode(self, node):
        '''

        :param node:
        :return:
        '''
        self.nodes.append(node)

    def addEdge(self, edge):

        '''

        :param edge:
        :return:
        '''
        self.edges.append(edge)

    def removeNode(self, node):
        '''

        :param node:
        :return:
        '''
        self.nodes.remove(node)

    def removeEdge(self, edge):
        '''

        :param edge:
        :return:
        '''
        self.edges.remove(edge)




