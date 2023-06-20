from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_scene import QDMGraphicScene
import json
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable
from nodeEditor.node_node import Node
from nodeEditor.node_edge import Edge
from nodeEditor.node_scene_history import SceneHistory
from nodeEditor.node_scene_clipboard import SceneClipboard


class Scene(Serializable):
    def __init__(self, parentSelf=None):
        '''

        '''
        super().__init__()
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()
        self.parentSelf = parentSelf

        self.nodes = []
        self.edges = []

        self._hasbeenModified = False
        self._hasbeenModified_listners = []

        self.scene_width, self.scene_height = 64000, 64000
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)


        self.initUI()


    @property
    def hasBeenModified(self):
        return self._hasbeenModified

    @hasBeenModified.setter
    def hasBeenModified(self, value):
        if not self._hasbeenModified and value:
            self._hasbeenModified = value

            #call all the listners
            for callback in self._hasbeenModified_listners:
                callback()

        self._hasbeenModified = value

    def addHasBeenModifiedListner(self, callback):
        self._hasbeenModified_listners.append(callback)


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

    def clear(self):
        '''

        :return:
        '''
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.hasBeenModified = False

    def saveToFile(self, filename):
        '''

        :param filename:
        :return:
        '''
        print('saveToFile: ', filename)
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))
            print('saveJson: ', filename)

            self.hasBeenModified = False


    def loadFromFile(self, filename):
        '''

        :param filename:
        :return:
        '''
        with open(filename, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)
            self.hasBeenModified = False



    def serialize(self):
        '''

        :return:
        '''
        nodes = []
        edges = []
        for node in self.nodes:
            nodes.append(node.serialize())

        for edge in self.edges:
            edges.append(edge.serialize())

        dic_val = OrderedDict()
        dic_val['id'] = self.id
        dic_val['scene_width'] = self.scene_width
        dic_val['scene_height'] = self.scene_height
        dic_val['nodes'] = nodes
        dic_val['edges'] = edges
        return dic_val

    def deserialize(self, data, hashmap={}, restore_id=True):
        '''

        :param data:
        :param hashmap:
        :return:
        '''
        self.clear()
        hashmap = {}

        if restore_id: self.id = data['id']


        #CREATE NODES
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap, restore_id)

        #CREATE EDGES
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True







