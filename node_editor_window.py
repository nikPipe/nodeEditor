from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from nodeEditor.node_editor_widget import NodeEditorWidget

class NdeEditorWindow(QMainWindow):
    def __init__(self):
        '''

        :return:
        '''
        super(NdeEditorWindow, self).__init__()
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.color_variable = color_variable.COLOR_VARIABLE()
        self.styleSheet = styleSheet.STYLESHEET()
        self.name_company = 'Nikheel'
        self.name_product = 'Node Editor'
        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        self.createMenus()

        self.nodeEditorWidget = NodeEditorWidget(self)
        self.setCentralWidget(self.nodeEditorWidget)

        #SET WINDOW PROPERTIES
        self.setGeometry(600, 300, 800, 600)
        self.nodeEditorWidget.setTitle_(self)
        #STATE BAR
        self.createStatusBar()
        self.nodeEditorWidget.view.scenePosChanged.connect(self.on_mouse_pos_change)

        self.show()

    def closeEvent(self, event):
        '''

        :param event:
        :return:
        '''
        if self.nodeEditorWidget.maybeSave():
            event.accept()


    def action_def(self, name, shortcut, statusTip, toolTip, connect):
        '''

        :param name:
        :return:
        '''
        action = QAction(name, self)
        action.setShortcut(shortcut)
        action.triggered.connect(connect)
        action.setStatusTip(statusTip)
        action.setToolTip(toolTip)
        return action

    def createActions(self):
        '''

        :return:
        '''
        self.fileAction = self.action_def(name='New', shortcut='Ctrl+N', statusTip='New File', toolTip='New File',
                                     connect=self.NewFile)
        self.openAction = self.action_def(name='Open', shortcut='Ctrl+O', statusTip='Open File', toolTip='Open File',
                                     connect=self.openFile)
        self.saveAction = self.action_def(name='Save', shortcut='Ctrl+S', statusTip='Save File', toolTip='Save File',
                                     connect=self.saveFile)
        self.saveAsAction = self.action_def(name='Save As', shortcut='Ctrl+Shift+S', statusTip='Save File As',
                                       toolTip='Save File As', connect=self.saveAsFile)
        self.exitAction = self.action_def(name='Exit', shortcut='Ctrl+Q', statusTip='Exit Application',
                                     toolTip='Exit Application', connect=QApplication.instance().quit)

        self.undoAction = self.action_def(name='Undo', shortcut='Ctrl+Z', statusTip='Undo', toolTip='Undo',
                                     connect=self.undoFile)
        self.redoAction = self.action_def(name='Redo', shortcut='Ctrl+Shift+Z', statusTip='Redo', toolTip='Redo',
                                     connect=self.redoFile)
        self.deleteAction = self.action_def(name='Delete', shortcut='Del', statusTip='Delete', toolTip='Delete',
                                       connect=self.deleteFile)

        self.cutAction = self.action_def(name='Cut', shortcut='Ctrl+X', statusTip='Cut', toolTip='Cut', connect=self.cutFile)
        self.copyAction = self.action_def(name='Copy', shortcut='Ctrl+C', statusTip='Copy', toolTip='Copy',
                                     connect=self.copyFile)
        self.pasteAction = self.action_def(name='Paste', shortcut='Ctrl+V', statusTip='Paste', toolTip='Paste',
                                      connect=self.pasteFile)


    def createMenus(self):
        '''

        :return:
        '''
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.editMenu = menubar.addMenu('&Edit')

        self.createActions()

        # FILE MENU
        self.fileMenu.addAction(self.fileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        # EDIT MENU
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.deleteAction)

    def NewFile(self):
        '''

        :return:
        '''
        print('New File')
        val = self.nodeEditorWidget.New_def()


    def openFile(self):
        '''

        :return:
        '''
        self.nodeEditorWidget.Open_def()

    def saveFile(self):
        '''

        :return:
        '''
        print('Save File')

        fileName = self.nodeEditorWidget.Save_def()
        self.statusBar().showMessage('File Saved %s' % fileName)
        return True

    def saveAsFile(self):
        '''

        :return:
        '''
        print('Save As File')
        fileName = self.nodeEditorWidget.SaveAs_def()
        self.statusBar().showMessage('File Saved As')
        return fileName

    def undoFile(self):
        '''

        :return:
        '''
        print('Undo File')
        self.nodeEditorWidget.undo()

    def redoFile(self):
        '''

        :return:
        '''
        self.nodeEditorWidget.redo()

    def deleteFile(self):
        '''

        :return:
        '''
        print('Delete File')
        self.nodeEditorWidget.delete_def()

    def on_mouse_pos_change(self, x, y):

        '''

        :return:
        '''
        self.statusMousePos.setText('Scene Pos: %d, %d' % (x, y))

    def cutFile(self):
        '''

        :return:
        '''

        data = self.nodeEditorWidget.Cut_def()
        QApplication.instance().clipboard().setText(data)

    def copyFile(self):
        '''

        :return:
        '''
        data = self.nodeEditorWidget.Copy_def()
        QApplication.instance().clipboard().setText(data)

    def pasteFile(self):
        '''

        :return:
        '''
        raw_data = QApplication.instance().clipboard().text()
        self.nodeEditorWidget.Paste_def(raw_data)

    def readSettings(self):
        '''

        :return:
        '''
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        '''

        :return:
        '''
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def createStatusBar(self):
        '''

        :return:
        '''
        self.statusBar().showMessage('Ready')
        self.statusBar().setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);')
        self.statusMousePos = QLabel('')
        self.statusBar().addPermanentWidget(self.statusMousePos)
        self.nodeEditorWidget.view.scenePosChanged.connect(self.on_mouse_pos_change)