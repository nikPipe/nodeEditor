from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_view import QDMGraphicsView
from nodeEditor.node_scene import Scene
from nodeEditor.node_node import Node
from nodeEditor.node_edge import *


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super(NodeEditorWnd, self).__init__(parent)
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()


        self.initUI()


    def initUI(self):
        '''

        :return:
        '''
        self.setGeometry(300, 300, 800, 600)
        self.layout = self.sample_widget_template.vertical_layout(parent_self=self)
        self.setLayout(self.layout)

        # CREATE GRAPHICS SCENE
        self.scene = Scene()




        self.addNodes()



        #CREATE GRAPHICS VIEW
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle('Node Editor')

        self.show()

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

        edge = Edge(self.scene, node1.outputs[0], node2.inputs[0])
        edge = Edge(self.scene, node2.outputs[0], node3.inputs[0], type=EDGE_TYPE_BEZIER)



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
























