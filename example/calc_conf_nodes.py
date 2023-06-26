from nodeEditor.example.calc_conf import *
from nodeEditor.example.calcNodeBase import *
from nodeEditor.utils import dumpException


@register_node(OP_NODE_ADD)
class CalcNode_add(CalNode):
    op_icon = 'icons/add.png'
    op_code = OP_NODE_ADD
    op_title = 'Add'
    content_label = '+'
    content_label_objectName = 'calc_node_add'

@register_node(OP_NODE_SUB)
class CalcNode_sub(CalNode):
    op_icon = 'icons/sub.png'
    op_code = OP_NODE_SUB
    op_title = 'Subtract'
    content_label = '-'
    content_label_objectName = 'calc_node_sub'

@register_node(OP_NODE_MUL)
class CalcNode_mul(CalNode):
    op_icon = 'icons/mul.png'
    op_code = OP_NODE_MUL
    op_title = 'Multiply'
    content_label = '*'
    content_label_objectName = 'calc_node_mul'

@register_node(OP_NODE_DIV)
class CalcNode_div(CalNode):
    op_icon = 'icons/divide.png'
    op_code = OP_NODE_DIV
    op_title = 'Divide'
    content_label = '/'
    content_label_objectName = 'calc_node_div'


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

    def initInnerClasses(self):
        self.content = CalInputContent(self)
        self.grNode = calGraphNode(self)


class CalOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.label = QLabel('0')
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setObjectName(self.node.content_label_objectName)
        self.layout.addWidget(self.label)


@register_node(OP_NODE_OUTPUT)
class CalcNode_output(CalNode):
    op_icon = 'icons/out.png'
    op_code = OP_NODE_OUTPUT
    op_title = 'Output'
    content_label = 'Output'
    content_label_objectName = 'calc_node_output'

    def __init__(self, scene):
        inputs = [0]
        outputs = []
        super().__init__(scene=scene,inputs=inputs, outputs=outputs)

    def initInnerClasses(self):
        self.content = CalOutputContent(self)
        self.grNode = calGraphNode(self)

