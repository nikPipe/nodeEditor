
from PyQt.import_module import *
from nodeEditor.node_editor_widget import NodeEditorWidget
from nodeEditor.example.calc_conf import *
from nodeEditor.example.calcNodeBase import *


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
            print('Got Drop: (%d) %s' % (op_code, text), 'op_code: ', op_code, 'pixmap: ', pixmap, 'mouse_position: ', mouse_position, 'scene_position: ', scene_position)

            #TODO: add node at scene_position
            node = CalNode(self.scene, op_code, text, contentLabel=text,  inputs=[1, 1], outputs=[2])
            print('node: ', node)
            node.setPos(scene_position.x(), scene_position.y())



            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            print('---Denied--- has not format: ', LISTBOX_MIMETYPE)
            event.ignore()


