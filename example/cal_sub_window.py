
from PyQt.import_module import *
from nodeEditor.node_editor_widget import NodeEditorWidget
from nodeEditor.example.calc_conf import *
from nodeEditor.example.calcNodeBase import *
from nodeEditor.utils import dumpException


class calSubWindow(NodeEditorWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent_self = self
        self.setTitle()
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)

    def setTitle(self):
        '''

        :return:
        '''
        self.setWindowTitle(self.getUserFriendlyFilename())

    def onDragEnter(self, event):
        '''
        :param event:
        :return:
        '''
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            print('---Denied---')
            event.setAccepted(False)


    def onDrop(self, event):
        '''
        :param event:
        :return:
        '''
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event_data = event.mimeData().data(LISTBOX_MIMETYPE)
            data_stream = QDataStream(event_data, QIODevice.ReadOnly)
            pixmap = QPixmap()
            data_stream >> pixmap
            op_code = data_stream.readInt()
            text = data_stream.readQString()
            mouse_position = event.pos()
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

            try:
                node = get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
                self.scene.history.storeHistory('Created %s node' % node.__class__.__name__)
            except Exception as e:
                dumpException(e)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            print('---Denied--- has not format: ', LISTBOX_MIMETYPE)
            event.ignore()


