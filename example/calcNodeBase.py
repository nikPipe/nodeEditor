
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
    def __init__(self, scene, op_code, op_title, contentLabel='', content_label_objectName='cal_node_bg', inputs=[2, 2], outputs=[1]):
        self.op_code = op_code
        self.op_title = op_title

        self.content_label = contentLabel
        self.content_label_objectName = content_label_objectName


        super().__init__(scene, title=self.op_title, inputs=inputs, outputs=outputs)


    def initInnerClasses(self):
        self.content = calContent(self)
        self.grNode = calGraphNode(self)
