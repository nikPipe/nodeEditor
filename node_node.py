from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphic_node import QDmGraphicsNode
from nodeEditor.node_content_widget import QDMNodeContentWidget
from nodeEditor.node_socket import Socket
from nodeEditor.node_socket import LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM

from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable
class Node(Serializable):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        '''

        :param scene:
        :param title:
        :param inputs:
        :param outputs:
        '''
        super().__init__()
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget(self)
        self.grNode = QDmGraphicsNode(self)


        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22


        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
            self.outputs.append(socket)
            counter += 1

    def getSocketPosition(self, index, position):
        '''
        get the position of the socket
        :param index:
        :param position:
        :return:
        '''
        x = 0 if position in [LEFT_TOP, LEFT_BOTTOM] else self.grNode.width
        if position in [LEFT_BOTTOM, RIGHT_BOTTOM]:
            # start from the bottom
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            y =  self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * 22

        return [x, y]

    @property
    def pos(self):
        '''
        get the position of the node
        :return:
        '''
        return self.grNode.pos()

    def setPos(self, x, y):
        '''
        set the position of the node
        :param x:
        :param y:
        :return:
        '''
        self.grNode.setPos(x, y)


    def updateConnectedEdges(self):
        '''
        update the connected edges
        :return:
        '''
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()
    def __str__(self):
        '''

        :return:
        '''
        return "<%s %s..%s>" % (self.__class__.__name__, hex(id(self))[2:5], hex(id(self))[-3:])

    def remove(self):
        '''

        :return:
        '''
        print ("Removing Node", self)
        print (" - remove all edges from sockets")
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                socket.edge.remove()

        print(" - remove all edges from scene")
        self.scene.grScene.update()

        print(" - remove all grNodes from scene")
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None

        print (" - remove all sockets from scene")
        print (" - remove node from scene")
        self.scene.removeNode(self)


    def serialize(self):
        '''

        :return:
        '''
        dic_val = OrderedDict()
        dic_val['id'] = self.id
        dic_val['title'] = self.title
        dic_val['pos_x'] = self.grNode.scenePos().x()
        dic_val['pos_y'] = self.grNode.scenePos().y()
        dic_val['inputs'] = [socket.serialize() for socket in self.inputs]
        dic_val['outputs'] = [socket.serialize() for socket in self.outputs]
        dic_val['content'] = self.content.serialize()

        return dic_val

    def deserialize(self, data, hashmap={}):
        '''

        :param data:
        :param hashmap:
        :return:
        '''
        print('deserialize: ', data)
        return False


