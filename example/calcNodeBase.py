
from PyQt.import_module import *

from nodeEditor.node_node import Node
from nodeEditor.node_graphic_node import QDmGraphicsNode
from nodeEditor.node_content_widget import QDMNodeContentWidget


class calContent(QDMNodeContentWidget):
    def initUI(self):

        label = QLabel(self.node.content_label, self)
        label.setObjectName(self.node.content_label_objectName)


class calGraphNode(QDmGraphicsNode):

    def initSize(self):
        '''

        :return:
        '''
        super().initSize()
        self.width = 160
        self.height = 74
        self.edge_size = 5
        self._padding = 8



class CalNode(Node):
    op_icon = ''
    op_code = 0
    op_title = 'Undefined'
    content_label = ''
    content_label_objectName = ''

    def __init__(self, scene,  inputs=[2, 2], outputs=[1]):



        super().__init__(scene, title=self.__class__.op_title, inputs=inputs, outputs=outputs)


    def initInnerClasses(self):
        self.content = calContent(self)
        self.grNode = calGraphNode(self)
