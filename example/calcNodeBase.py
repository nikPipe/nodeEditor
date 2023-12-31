
from PyQt.import_module import *

from nodeEditor.node_node import Node
from nodeEditor.node_graphic_node import QDmGraphicsNode
from nodeEditor.node_content_widget import QDMNodeContentWidget
from nodeEditor.node_socket import *
from nodeEditor.utils import dumpException


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
        self.edge_roundness = 5
        self.edge_padding = 10
        self._title_horizontal_padding = 8
        self._title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self._icon = QImage('icons/status_icons.png')

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        offset = 24.0
        if self.node.isDirty():
            offset = 0.0
        if self.node.isInvalid():
            offset = 48.0

        painter.drawImage(
            QRectF(-10, 10, 24.0, 24.0),
            self._icon,
            QRectF(offset, 0.0, 24.0, 24.0)
        )



class CalNode(Node):
    op_icon = ''
    op_code = 0
    op_title = 'Undefined'
    content_label = ''
    content_label_objectName = ''

    def __init__(self, scene,  inputs=[2, 2], outputs=[1]):
        super().__init__(scene, title=self.__class__.op_title, inputs=inputs, outputs=outputs)

        self.value = None
        self.markDirty()


    def initInnerClasses(self):
        self.content = calContent(self)
        self.grNode = calGraphNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER


    def evalImplementation(self):
        '''

        :return:
        '''
        return 123

    def eval(self):

        if not self.isDirty() and not self.isInvalid():
            print('skip eval')
            return self.value

        try:
            val =  self.evalImplementation()
            self.markDirty(False)
            self.markInvalid(False)
            return val


        except Exception as e:
            self.markInvalid()
            dumpException(e)




    def onInputChanged(self, socket=None):
        print('onInputChanged')
        self.markDirty()
        self.eval()


    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print('deserialize cal node', self.__class__.__name__, 'res: ', res)

        return res

