from PyQt.import_module import *
from nodeEditor.example.cal_window import calWindow
from nodeEditor.node_editor_window import NdeEditorWindow
from nodeEditor.utils import loadStylesheets
import inspect, os


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = calWindow()
    module_path = os.path.dirname(inspect.getfile(window.__class__))
    styleSheet_fileName = os.path.join(module_path, 'qss/dark.qss')
    loadStylesheets(styleSheet_fileName)
    window.show()
    sys.exit(app.exec_())


