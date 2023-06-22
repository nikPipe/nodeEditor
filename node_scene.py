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

class InvalidFile(Exception): pass


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
        self._item_selected_listners = []
        self._item_deSelected_listners = []



        self.scene_width, self.scene_height = 64000, 64000
        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)
        self.grScene.itemSelected.connect(self.onItemSelected)
        self.grScene.itemDeselected.connect(self.onItemDeselected)


    def initUI(self):
        '''

        :return:
        '''
        self.grScene = QDMGraphicScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def onItemSelected(self):
        '''

        :return:
        '''
        print("scene.onItemSelected")

    def onItemDeselected(self):
        '''

        :return:
        '''
        print("scene.onItemDeselected")

    #CUSTOM FLAG TO DETECT IF THE SCENE HAS BEEN MODIFIED
    def resetLastSelectedState(self):
        for node in self.nodes:
            node.grNode._last_selected_state = False

        for edge in self.edges:
            edge.grEdge._last_selected_state = False

    def isModified(self):
        return self.hasBeenModified

    def getselectedItems(self):
        return self.grScene.selectedItems()

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


    def addSelectedItemListner(self, callback):
        self._item_selected_listners.append(callback)

    def addDeSelectedItemListner(self, callback):
        self._item_deSelected_listners.append(callback)

    def addDragEnterListener(self, callback):
        self.grScene.views()[0].addDragEnterListener(callback)

    def addDropListener(self, callback):
        self.grScene.views()[0].addDropListener(callback)


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
        if node in self.nodes:
            self.nodes.remove(node)
        else:
            print('ERROR: Scene.removeNode', 'wanna remove node', node, 'from self.nodes but it is not in the list')

    def removeEdge(self, edge):
        '''

        :param edge:
        :return:
        '''
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print('ERROR: Scene.removeEdge', 'wanna remove edge', edge, 'from self.edges but it is not in the list')

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
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            with open(filename, 'r') as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                self.deserialize(data)
                self.hasBeenModified = False

                QApplication.restoreOverrideCursor()

                return True
        except json.JSONDecodeError as e:
            QApplication.restoreOverrideCursor()
            raise InvalidFile('%s is not a valid JSON file' % filename)
            return False

        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "Error", "Could not open file: {}".format(e))
            return False

        finally:
            QApplication.restoreOverrideCursor()

        return False





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







