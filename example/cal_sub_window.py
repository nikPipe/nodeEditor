
from PyQt.import_module import *
from nodeEditor.node_editor_widget import NodeEditorWidget


class calSubWindow(NodeEditorWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent_self = self
        self.setTitle()


    def setTitle(self):
        '''

        :return:
        '''
        self.setWindowTitle(self.getUserFriendlyFilename())