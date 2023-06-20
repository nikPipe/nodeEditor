import json
import os

from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_view import QDMGraphicsView
from nodeEditor.node_scene import Scene
from nodeEditor.node_node import Node
from nodeEditor.node_edge import *


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(NodeEditorWidget, self).__init__(parent)
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.parent_self = parent
        self.initUI()


    def initUI(self):
        '''

        :return:
        '''
        self.layout = self.sample_widget_template.vertical_layout(parent_self=self)
        self.setLayout(self.layout)

        # CREATE GRAPHICS SCENE
        self.scene = Scene(self)

        self.addNodes()
        self.filename = None

        #CREATE GRAPHICS VIEW
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.setGeometry(300, 300, 800, 600)
        self.layout.addWidget(self.view)

        self.changeTitle(self)

        #self.addDebugContent()

    def addNodes(self):
        '''

        :return:
        '''
        node1 = Node(self.scene, "My Awesome Node 1", inputs=[0, 1, 2, 3, 4], outputs=[1, 2, 3, 4])
        node2 = Node(self.scene, "My Awesome Node 2", inputs=[0, 1, 2, 3, 4], outputs=[1, 2, 3, 4])
        node3 = Node(self.scene, "My Awesome Node 3", inputs=[0, 1, 2, 3, 4], outputs=[1, 2, 3, 4])

        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge = Edge(self.scene, node1.outputs[0], node2.inputs[4])
        edge = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)



    def addDebugContent(self):
        '''

        :return:
        '''
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)


        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsSelectable)

        text = self.grScene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsMovable)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        widget3 = QSlider()
        proxy3 = self.grScene.addWidget(widget3)
        proxy3.setFlag(QGraphicsItem.ItemIsMovable)
        proxy3.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy3.setPos(0, 90)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def New_def(self):
        '''

        :return:
        '''
        if self.maybeSave():
            self.scene.clear()
            self.filename = None
            return True
        return False

    def Open_def(self):
        '''

        :return:
        '''
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open file New')
            if fname == '':
                return

            if os.path.isfile(fname):
                self.scene.loadFromFile(fname)
                self.filename = fname
                print("Loaded", fname)
                self.changeTitle(self)

    def Save_def(self):
        '''

        :return:
        '''
        fname, filter = QFileDialog.getSaveFileName(self, 'Save file New', filter='*.json')
        if fname == '':
            return
        self.scene.saveToFile(fname)
        self.filename = fname
        return fname

    def SaveAs_def(self):
        '''

        :return:
        '''
        fname, filter = QFileDialog.getSaveFileName(self, 'Save file New', filter='*.json')
        if fname == '':
            return False
        self.scene.saveToFile(fname)
        self.filename = fname
        return True

    def Cut_def(self):
        '''

        :return:
        '''
        data = self.scene.clipboard.serializeSelected(delete=True)
        str_data = json.dumps(data, indent=4)
        return str_data

    def Copy_def(self):
        '''

        :return:
        '''
        data = self.scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(data, indent=4)
        return str_data

    def Paste_def(self, data):
        '''

        :return:
        '''
        try:
            json_data = json.loads(data)
        except ValueError as e:
            print("Paste Error: %s" % e)
            return

        #CHECK IF CLIPBOARD DATA IS VALID
        if 'nodes' not in json_data:
            print("Clipboard has no 'nodes' data")
            return

        self.scene.clipboard.deserializeFromClipboard(json_data)

    def isModified(self):
        '''

        :return:
        '''
        return self.scene.hasBeenModified

    def maybeSave(self):
        '''

        :return:
        '''
        if not self.isModified():
            return

        res = QMessageBox.warning(self, 'Warning', 'Scene Modified. Save Changes?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if res == QMessageBox.Yes:
            return self.SaveAs_def()

        elif res == QMessageBox.Cancel:
            return False

        return True

    def changeTitle(self, object=None):
        '''

        :return:
        '''
        title = 'Node Editor - '
        if self.filename is None:
            title += 'Untitled'

        else:
            title += os.path.basename(self.filename)

        if self.isModified():
            title += '*'

        if self.parent_self is None:
            object.setWindowTitle(title)
        else:
            self.parent_self.setWindowTitle(title)


    def undo(self):
        '''

        :return:
        '''
        self.scene.history.undo()

    def redo(self):
        '''

        :return:
        '''
        self.scene.history.redo()

    def delete_def(self):
        '''

        :return:
        '''
        self.scene.grScene.views()[0].deleteSelected()







