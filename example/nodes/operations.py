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


