
from PyQt.import_module import *
from nodeEditor.node_edge import *
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

        self.initnewNodeActions()
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelected(self.getNodesClassFromData)

    def getNodesClassFromData(self, data):

        if 'op_code' not in data:
            return Node

        return get_class_from_opcode(data['op_code'])

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


    def contextMenuEvent(self, event):
        '''
        :param event:
        :return:
        '''
        try:
            item = self.scene.getItemAt(event.pos())
            if type(item)  == QGraphicsItem:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handleNodeContextMenu(event)

            elif hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)

            else:
                self.handleNewNodeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e:
            dumpException(e)


    def handleNodeContextMenu(self, event):
        '''

        :param event:
        :return:
        '''
        print('handleNodeContextMenu')
        contextMenu = QMenu()
        markDirtyAction = contextMenu.addAction('Mark Dirty')
        markInvalidAction = contextMenu.addAction('Mark Invalid')
        unmarkInvalidAction = contextMenu.addAction('Unmark Invalid')
        evalAction = contextMenu.addAction('Eval')

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node

        if hasattr(item, 'socket'):
            selected = item.socket.node

        print('item: ', item)


    def handleEdgeContextMenu(self, event):
        '''

        :param event:
        :return:
        '''
        print('handleEdgeContextMenu')
        contextMenu = QMenu()
        besierAction = contextMenu.addAction('Set Bezier Mode')
        straightAction = contextMenu.addAction('Set Direct Mode')


        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item  = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == besierAction:
            selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == straightAction:
            selected.edge_type = EDGE_TYPE_DIRECT



    def handleNewNodeContextMenu(self, event):
        '''

        :param event:
        :return:
        '''
        print('handleNewNodeContextMenu')
        contextMenu = self.initNodeContextMenu()
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action is not None:
            new_calc_node = get_class_from_opcode(action.data())(self.scene)
            scene_position = self.scene.getView().mapToScene(event.pos())
            new_calc_node.setPos(scene_position.x(), scene_position.y())
            print('SelectedNode: ', new_calc_node)

    def initNodeContextMenu(self):
        '''

        :return:
        '''
        contextMenu = QMenu()
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:
            contextMenu.addAction(self.nodee_action[key])

        return contextMenu

    def initnewNodeActions(self):
        '''

        :param key:
        :return:
        '''
        self.nodee_action = {}
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:
            node = CALC_NODES[key]
            self.nodee_action[node.op_code] = QAction(QIcon(node.op_icon), node.op_title)
            self.nodee_action[node.op_code].setData(node.op_code)

























