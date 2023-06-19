
from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet


class SceneClipboard():
    def __init__(self, scene):
        '''
        :param scene:
        '''
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.scene = scene


    def serializeSelected(self, delete=False):
        '''

        :param delete:
        :return:
        '''
        print('SceneClipboard.serializeSelected()')
        return {}

    def deserializeFromClipboard(self, data):

        '''

        :return:
        '''
        print('SceneClipboard.deserializeFromClipboard()', data)