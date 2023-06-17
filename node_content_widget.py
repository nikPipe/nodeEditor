from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable
class QDMNodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()
        self.node = node

        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        self.layout = self.sample_widget_template.vertical_layout(parent_self=self)
        self.setLayout(self.layout)


        label = self.sample_widget_template.label(set_text='Test')
        self.layout.addWidget(label)

        self.layout.addWidget(QDMTextEdit('Sample'))

    def setEditingFlag(self, val):
        self.node.scene.grScene.views()[0].editingFlag = val


    def serialize(self):
        return OrderedDict([
            ('id', self.node.id),
            ('content', 'content')
        ])

    def deserialize(self, data, hashmap={}):
        print("deserializing node content for %s" % self.node.id)
        return True





class QDMTextEdit(QTextEdit):
    def fousInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)
































