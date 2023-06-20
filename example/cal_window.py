from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable

class calWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        '''

        :return:
        '''
        pass