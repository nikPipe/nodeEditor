import math

from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_scene import QDMGraphicScene
from nodeEditor.node_graphics_socket import QDMGraphicsSocket

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
EDGE_DRAG_START_THRESHOLD = 10

class QDMGraphicsView(QGraphicsView):
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

    def initUI(self):
        '''

        :return:
        '''
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

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
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event):
        '''

        :param event:
        :return:
        '''
        super().mousePressEvent(event)

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
        print('  assign start socket')


    def edgeDragEnd(self, item):
        '''

        :param item:
        :return:
        '''
        self.mode = MODE_NOOP
        print('End dragging edge')
        if type(item) is QDMGraphicsSocket:
            print('  Assign end Socket')
            return True

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
        if self.mode == MODE_EDGE_DRAG:


            if self.mode == MODE_EDGE_DRAG:
                if self.distanceBetweenClickAndRelease(event):
                    res = self.edgeDragEnd(item)
                    if res: return

        super().mouseReleaseEvent(event)

    def rightMouseButtonRelease(self, event):
        '''

        :param event:
        :return:
        '''
        super().mouseReleaseEvent(event)

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



