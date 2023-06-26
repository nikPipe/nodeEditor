from nodeEditor.example.calc_conf import *
from nodeEditor.example.calcNodeBase import *
from nodeEditor.utils import dumpException


class CalInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.edit = QLineEdit('0')
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objectName)
        self.edit.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.layout.addWidget(self.edit)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.edit.setText(data['value'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_INPUT)
class CalcNode_input(CalNode):
    op_icon = 'icons/in.png'
    op_code = OP_NODE_INPUT
    op_title = 'Input'
    content_label = 'Input'
    content_label_objectName = 'calc_node_input'
    def __init__(self, scene):

        inputs = []
        outputs = [0]
        super().__init__(scene=scene, inputs=inputs, outputs=outputs)
        self.eval()

    def initInnerClasses(self):
        self.content = CalInputContent(self)
        self.grNode = calGraphNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)



    def onInputChanged(self):
        self.markDirty()
        self.eval()









