from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphic_node import QDmGraphicsNode
from nodeEditor.node_content_widget import QDMNodeContentWidget
from nodeEditor.node_socket import Socket
from nodeEditor.node_socket import LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM


class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        '''

        :param scene:
        :param title:
        :param inputs:
        :param outputs:
        '''
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget()
        self.grNode = QDmGraphicsNode(self)


        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22


        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM)
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
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

