import os,inspect
from nodeEditor.utils import loadStylesheets

from PyQt.import_module import *
from nodeEditor.node_editor_widget import NodeEditorWidget
from nodeEditor.node_editor_window import NdeEditorWindow



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NdeEditorWindow()
    module_path = os.path.dirname(inspect.getfile(window.__class__))
    styleSheet_fileName = os.path.join(module_path, 'qss/dark.qss')
    loadStylesheets(styleSheet_fileName)

    window.show()


    sys.exit(app.exec_())
