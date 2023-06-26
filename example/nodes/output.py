from nodeEditor.example.calc_conf import *
from nodeEditor.example.calcNodeBase import *
from nodeEditor.utils import dumpException


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
