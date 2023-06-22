from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet



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
        itemList = ['Add', 'Subtract', 'Multiply', 'Divide', 'Modulus', 'Power', 'Square Root', 'Logarithm', 'Sine']
        itemList.append('Input')
        itemList.append('Output')
        for item in itemList:
            self.addMyItem(item)


    def addMyItem(self, name, icon=None, op_code=0):
        '''

        :param name:
        :param icon:
        :param op_code:
        :return:
        '''
        item = QListWidgetItem(name, self)
        image = QPixmap(icon if icon is not None else '')
        item.setIcon(QIcon(image))
        item.setSizeHint(QSize(30, 30))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
        item.setData(Qt.UserRole, image)
        item.setData(Qt.UserRole + 1, op_code)










