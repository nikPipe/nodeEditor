import math

from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_scene import QDMGraphicScene
from nodeEditor.node_graphics_socket import QDMGraphicsSocket
from nodeEditor.node_graphics_edge import QDMGraphicsEdge
from nodeEditor.node_edge import *
from nodeEditor.node_graphic_cutline import QDMCutLine


MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10

class QDMGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)


    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()
        self.grScene = grScene
        self.initUI()

        self.mode = MODE_NOOP
        self.setScene(self.grScene)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]
        self.editingFlag = False

        self.cut_line = QDMCutLine()
        self.grScene.addItem(self.cut_line)

    def initUI(self):
        '''

        :return:
        '''
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mousePressEvent(self, event):
        '''

        :param event:
        :return:
        '''
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        '''

        :param event:
        :return:
        '''
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        '''

        :param event:
        :return:
        '''
        fake_event = QMouseEvent(event.MouseButtonRelease, event.localPos(), event.screenPos(),
                                 Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(fake_event)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fake_event = QMouseEvent(event.MouseButtonPress, event.localPos(), event.screenPos(),
                                    Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fake_event)

    def leftMouseButtonPress(self, event):
        '''

        :param event:
        :return:
        '''
        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if hasattr(item, 'node') or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                print('Left Shift + LMB on Node : {}'.format(item))
                event.ignore()
                fake_event = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                         Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                         event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fake_event)
                return


        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return





        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event):
        '''

        :param event:
        :return:
        '''
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)
        if isinstance(item, QDMGraphicsEdge):
            print(item.edge, '  connected sockets: ', item.edge.start_socket, '<------->',item.edge.end_socket)

        if type(item) is QDMGraphicsSocket:
            print(item.socket, ' has Edge: ', item.socket.edge)

        if item is None:
            print('Scene:')
            print('Nodes:')
            for node in self.grScene.scene.nodes:
                print('  {}'.format(node))
            print('Edges:')
            for edge in self.grScene.scene.edges:
                print('  {}'.format(edge))
            print('Socket:')

    def middleMouseButtonRelease(self, event):
        '''

        :param event:
        :return:
        '''
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                    Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fake_event)
        self.setDragMode(QGraphicsView.NoDrag)

    def edgeDragStart(self, item):
        '''

        :param item:
        :return:
        '''
        print('Start dragging edge')
        print('  assign start socket', item.socket)
        self.prev_edge = item.socket.edge
        self.last_start_socket = item.socket

        self.dragging_edge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        print('Edge drag start: ', self.dragging_edge, ' from ', self.dragging_edge.start_socket)

    def edgeDragEnd(self, item):
        '''

        :param item:
        :return:
        '''
        self.mode = MODE_NOOP
        print('End dragging edge')
        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket:

                print('  previous Edge: ', self.prev_edge)
                if item.socket.hasEdge():
                    item.socket.edge.remove()

                print('  Assign end Socket ', item.socket)
                if self.prev_edge is not None:
                    self.prev_edge.remove()

                self.dragging_edge.start_socket = self.last_start_socket
                self.dragging_edge.end_socket = item.socket
                self.dragging_edge.start_socket.setConnectedEdge(self.dragging_edge)
                self.dragging_edge.end_socket.setConnectedEdge(self.dragging_edge)

                self.dragging_edge.updatePositions()

                print('  Created: ', self.dragging_edge)

                return True

        self.dragging_edge.remove()
        self.dragging_edge = None

        if self.prev_edge is not None:
            self.prev_edge.start_socket.edge = self.prev_edge

        self.scene.grScene.history.storeHistory('Created new edge by dragging')


        return False

    def distanceBetweenClickAndRelease(self, event):
        '''

        :param event:
        :return:
        '''
        last_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = (last_release_scene_pos - self.last_lmb_click_scene_pos)
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y() ) > EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD

    def leftMouseButtonRelease(self, event):

        '''

        :param event:
        :return:
        '''
        item = self.getItemAtClick(event)

        if hasattr(item, 'node') or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                print('Left Rlease Shift + LMB on Node : {}'.format(item))
                event.ignore()
                fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                         Qt.LeftButton, Qt.NoButton,
                                         event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fake_event)
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.mode == MODE_EDGE_DRAG:
                if self.distanceBetweenClickAndRelease(event):
                    res = self.edgeDragEnd(item)
                    if res: return


        if self.mode == MODE_EDGE_CUT:

            self.cutIntersectingEdges()
            self.cut_line.line_points = []
            self.cut_line.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP

            return

        if self.dragMode() == QGraphicsView.RubberBandDrag:
            self.grScene.scene.history.storeHistory('Selection changed')

        super().mouseReleaseEvent(event)

    def rightMouseButtonRelease(self, event):
        '''

        :param event:
        :return:
        '''
        super().mouseReleaseEvent(event)


    def cutIntersectingEdges(self):
        '''

        :param item:
        :return:
        '''
        for idx in range(len(self.cut_line.line_points) - 1):
            p1 = self.cut_line.line_points[idx]
            p2 = self.cut_line.line_points[idx + 1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()

        self.grScene.scene.history.storeHistory('Delete cutted edges')


    def wheelEvent(self, event):
        '''

        :param event:
        :return:
        '''
        #CALCULATE ZOOM FACTOR
        zoomOutFactor = 1 / self.zoomInFactor

        #CALCULATE ZOOM
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        #SET NEW SCALE
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)


    def getItemAtClick(self, event):
        '''

        :param event:
        :return:
        '''
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj


    def mouseMoveEvent(self, event):
        '''

        :param event:
        :return:
        '''
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragging_edge.grEdge.setDestination(pos.x(), pos.y())
            self.dragging_edge.grEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cut_line.line_points.append(pos)
            self.cut_line.update()


        self.last_scene_mouse_position = self.mapToScene(event.pos())

        self.scenePosChanged.emit(int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y()))

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        '''

        :param event:
        :return:
        '''
        if event.key() == Qt.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)
        #elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
        #    print('Ctrl + S pressed')
        #    self.grScene.scene.saveToFile('graph.json')

        #elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
        #    self.grScene.scene.loadFromFile('graph.json')

        #elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier:
        #    self.grScene.scene.history.undo()

        #elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ShiftModifier:
        #    self.grScene.scene.history.redo()

        elif event.key() == Qt.Key_H:
            print('Key H pressed')

            print("HISTORY:     len(%d)" % len(self.grScene.scene.history.history_stake),
                  '-- current_step: %d' % self.grScene.scene.history.history_current_step)
            for i, item in enumerate(self.grScene.scene.history.history_stake):
                print(' ', i, '----', item['desc'])

        else:
            super().keyPressEvent(event)

    def deleteSelected(self):
        '''

        :return:
        '''
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

        self.grScene.scene.history.storeHistory('Delete selected')













