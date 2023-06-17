from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_scene import QDMGraphicScene
import json
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable


class Scene(Serializable):
    def __init__(self):
        '''

        '''
        super().__init__()
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


    def saveToFile(self, filename):
        '''

        :param filename:
        :return:
        '''
        print('saveToFile: ', filename)
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))

        print('saveJson: ', filename)


    def loadFromPickle(self, filename):
        '''

        :param filename:
        :return:
        '''
        with open(filename, 'r') as file:
            data = json.loads(file.read(), encoding='utf-8')
            self.deserialize(data)


    def serialize(self):
        '''

        :return:
        '''
        nodes = []
        edges = []
        print('serialize: ', self.nodes)
        for node in self.nodes:
            nodes.append(node.serialize())

        print('serialize: ', self.edges)
        for edge in self.edges:
            edges.append(edge.serialize())
        print('serialize all: ', nodes, edges)

        dic_val = OrderedDict()
        dic_val['id'] = self.id
        dic_val['scene_width'] = self.scene_width
        dic_val['scene_height'] = self.scene_height
        dic_val['nodes'] = nodes
        dic_val['edges'] = edges
        return dic_val

    def deserialize(self, data, hashmap={}):
        '''

        :param data:
        :param hashmap:
        :return:
        '''
        print('deserialize: ', data)
        return False







