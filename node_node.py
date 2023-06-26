from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphic_node import QDmGraphicsNode
from nodeEditor.node_content_widget import QDMNodeContentWidget
from nodeEditor.node_socket import Socket
from nodeEditor.node_socket import *

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
        self.initInnerClasses()
        self.initSettings()


        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        self.initSockets(inputs, outputs)

        #DIRTY AND EVELUATION FLAGS
        self._is_dirty = False
        self._is_invalid = False




    def initInnerClasses(self):
        self.content = QDMNodeContentWidget(self)
        self.grNode = QDmGraphicsNode(self)

    def initSettings(self):
        self.socket_spacing = 22
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER
        self.input_multi_edged = False
        self.output_multi_edged = True

    def initSockets(self, inputs, outputs, reset=True):
        '''
        CREATE SCOKETS
        init the sockets
        :param inputs:
        :param outputs:
        :return:
        '''
        if reset:
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                for socket in (self.inputs + self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)

                self.inputs = []
                self.outputs = []

        #CREATE NEW SOCKETS

        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=self.input_socket_position, socket_type=item,
                            multi_edges=self.input_multi_edged, count_on_this_node_side=len(inputs),
                            is_input=True)
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=self.output_socket_position, socket_type=item,
                            multi_edges=self.output_multi_edged, count_on_this_node_side=len(outputs),
                            is_input=False)
            self.outputs.append(socket)
            counter += 1

    def onEdgeConnectionChanged(self, new_edge):
        '''
        this function is called when the edge connection is changed
        :param new_edge:
        :return:
        '''
        print("edge connection changed", new_edge)

    def onInputChanged(self, new_edge):
        '''
        this function is called when the input is changed
        :param socket:
        :return:
        '''
        print("input changed", new_edge)
        self.markDirty()
        self.markDescendantsDirty()


    def getSocketPosition(self, index, position, num_out_of=1):
        '''
        get the position of the socket
        :param index:
        :param position:
        :return:
        '''
        x = 0 if position in [LEFT_TOP, LEFT_CENTER,LEFT_BOTTOM] else self.grNode.width
        if position in [LEFT_BOTTOM, RIGHT_BOTTOM]:
            # start from the bottom
            y = self.grNode.height - self.grNode.edge_roundness - self.grNode._title_horizontal_padding - index * self.socket_spacing
        elif position in [LEFT_CENTER, RIGHT_CENTER]:
            number_of_sockets = num_out_of
            node_height = self.grNode.height
            top_offset = self.grNode.title_height + 2 * self.grNode._title_vertical_padding + self.grNode.edge_padding
            available_height = node_height - top_offset
            totoal_height_of_all_sockets = number_of_sockets * self.socket_spacing
            new_top = available_height - totoal_height_of_all_sockets
            #y = top_offset + index * self.socket_spacing + new_top / 2
            y = top_offset + available_height / 2 + (index - 0.5) * self.socket_spacing
            if num_out_of > 1:
                y -= self.socket_spacing * (number_of_sockets - 1 ) / 2

            # start from the middle
            #y = self.grNode.height / 2 - (len(self.inputs) - 1) * self.socket_spacing / 2 + index * self.socket_spacing

        elif position in [LEFT_TOP, RIGHT_TOP]:
            y = self.grNode.title_height + self.grNode._title_horizontal_padding + self.grNode.edge_roundness + index * 22
        else:
            # center
            y = 0

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
            #if socket.hasEdge():
            for edge in socket.edges:
                edge.updatePositions()
    def __str__(self):
        '''

        :return:
        '''
        return "<%s %s..%s>" % (self.__class__.__name__, hex(id(self))[2:5], hex(id(self))[-3:])

    def remove(self):
        '''

        :return:
        '''
        for socket in (self.inputs + self.outputs):
            #if socket.hasEdge():
            for edge in socket.edges:
                edge.remove()

        self.scene.grScene.update()

        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None

        self.scene.removeNode(self)

    #NODE EVALUATION
    def isDirty(self):
        return self._is_dirty

    def markDirty(self, new_value=True):
        self._is_dirty = new_value
        if self._is_dirty:
            self.onmarkDirty()

    def onmarkDirty(self):
        pass

    def markChildrenDirty(self, new_value=True):
        for node in self.getChildrenNodes():
            node.markDirty(new_value)


    def markDescendantsDirty(self, new_value=True):
        for node in self.getChildrenNodes():
            node.markDirty(new_value)
            node.markChildrenDirty(new_value)



    def isInvalid(self):
        return self._is_invalid

    def markInvalid(self, new_value=True):
        self._is_invalid = new_value
        if self._is_invalid:
            self.onmarkInvalid()

    def markChildrenInvalid(self, new_value=True):
        for node in self.getChildrenNodes():
            node.markInvalid(new_value)


    def markDescendantsInvalid(self, new_value=True):
        for node in self.getChildrenNodes():
            node.markInvalid(new_value)
            node.markChildrenInvalid(new_value)

    def onmarkInvalid(self):
        pass

    def eval(self):
        '''
        evaluate the node
        :return:
        '''
        self.markDirty(False)
        self.markInvalid(False)

        return 0

    def evalChildren(self):
        '''
        evaluate the children
        :return:
        '''
        for node in self.getChildrenNodes():
            node.eval()


    #TRAVERSING FUNCTIONS
    def getChildrenNodes(self):
        '''
        get the children nodes
        :return:
        '''
        if self.outputs == []:
            return []
        other_nodes = []
        for eachIndex in range(len(self.outputs)):
            for edge in self.outputs[0].edges:
                other_nodes.append(edge.getOtherSocket(self.outputs[eachIndex]).node)

        return other_nodes



    #SERIALIZATION AND DESERIALIZATION
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

    def deserialize(self, data, hashmap={}, restore_id=True):
        '''

        :param data:
        :param hashmap:
        :return:
        '''
        if restore_id:
            self.id = data['id']
        hashmap[data['id']] = self

        self.title = data['title']
        self.grNode.title = self.title
        self.grNode.setPos(data['pos_x'], data['pos_y'])
        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)

        self.inputs = []
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'],
                                count_on_this_node_side=len(data['inputs']), is_input=True)
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(new_socket)

        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'],
                                count_on_this_node_side=len(data['outputs']), is_input=False)
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(new_socket)

        #ALSO DESERIALIZE THE CONTENT
        res = self.content.deserialize(data['content'], hashmap)

        return True & res


