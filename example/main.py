from PyQt.import_module import *
from nodeEditor.example.cal_window import calWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = calWindow()
    window.show()
    sys.exit(app.exec_())


