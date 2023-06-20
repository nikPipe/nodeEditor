

from PyQt.import_module import *
from nodeEditor.node_editor_widget import NodeEditorWidget
from nodeEditor.node_editor_window import NdeEditorWindow



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NdeEditorWindow()
    window.show()


    sys.exit(app.exec_())
