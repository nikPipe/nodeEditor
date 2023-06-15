from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_graphics_scene import QDMGraphicScene


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
        self.grScene = QDMGraphicScene(self)


        #CREATE GRAPHICS VIEW
        self.view = QGraphicsView(self)
        self.view.setScene(self.grScene)
        self.layout.addWidget(self.view)







        self.setWindowTitle('Node Editor')

        self.show()
