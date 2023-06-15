from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphic_node import QDmGraphicsNode


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

        self.grNode = QDmGraphicsNode(self, title)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []
