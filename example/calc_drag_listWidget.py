from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.utils import dumpException
from nodeEditor.example.calc_conf import *




class QDMListBox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()

        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addMyitems()


    def addMyitems(self):
        '''

        :return:
        '''
        itemList = ['Add', 'Subtract', 'Multiply', 'Divide', 'Modulus', 'Power', 'Square Root', 'Logarithm', 'Sine', 'Input', 'Output']
        iconList = ['icons/add.png', 'icons/subtract.png', 'icons/multiply.png', 'icons/divide.png', 'icons/modulus.png', 'icons/power.png',
                    'icons/square_root.png', 'icons/logarithm.png', 'icons/sine.png', 'icons/input.png', 'icons/output.png']

        self.addMyItem('Input', 'icons/in.png', OP_NODE_INPUT)
        self.addMyItem('Output', 'icons/out.png', OP_NODE_OUTPUT)
        self.addMyItem('Add', 'icons/add.png', OP_NODE_ADD)
        self.addMyItem('Subtract', 'icons/sub.png', OP_NODE_SUB)
        self.addMyItem('Multiply', 'icons/mul.png', OP_NODE_MUL)
        self.addMyItem('Divide', 'icons/divide.png', OP_NODE_DIV)


    def addMyItem(self, name, icon=None, op_code=0):
        '''

        :param name:
        :param icon:
        :param op_code:
        :return:
        '''
        item = QListWidgetItem(name, self)
        image = QPixmap(icon if icon is not None else '.')
        item.setIcon(QIcon(image))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        item.setData(Qt.UserRole, image)
        item.setData(Qt.UserRole + 1, op_code)


    def startDrag(self, *args, **kwargs):
        #super().startDrag(*args, **kwargs)

        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)

            pixmap = QPixmap(item.data(Qt.UserRole))

            item_data = QByteArray()
            data_stream = QDataStream(item_data, QIODevice.WriteOnly)
            data_stream << pixmap
            data_stream.writeInt(op_code)
            data_stream.writeQString(item.text())

            mime_data = QMimeData()
            mime_data.setData(LISTBOX_MIMETYPE, item_data)

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)

        except Exception as err:
            dumpException(err)








