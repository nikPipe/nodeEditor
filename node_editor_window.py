
from PyQt.import_module import *
from nodeEditor.node_editor_widget import NodeEditorWidget

class NdeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        #ADD MENUBAR
        menubar = self.menuBar()

        #FILE
        fileAction = self.action_def(name='New', shortcut='Ctrl+N', statusTip='New File', toolTip='New File', connect=self.NewFile )
        openAction = self.action_def(name='Open', shortcut='Ctrl+O', statusTip='Open File', toolTip='Open File', connect=self.openFile )
        saveAction = self.action_def(name='Save', shortcut='Ctrl+S', statusTip='Save File', toolTip='Save File', connect=self.saveFile )
        saveAsAction = self.action_def(name='Save As', shortcut='Ctrl+Shift+S', statusTip='Save File As', toolTip='Save File As', connect=self.saveAsFile )
        exitAction = self.action_def(name='Exit', shortcut='Ctrl+Q', statusTip='Exit Application', toolTip='Exit Application', connect=QApplication.instance().quit)

        undoAction = self.action_def(name='Undo', shortcut='Ctrl+Z', statusTip='Undo', toolTip='Undo', connect=self.undoFile )
        redoAction = self.action_def(name='Redo', shortcut='Ctrl+Shift+Z', statusTip='Redo', toolTip='Redo', connect=self.redoFile )
        deleteAction = self.action_def(name='Delete', shortcut='Del', statusTip='Delete', toolTip='Delete', connect=self.deleteFile )

        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        helpMenu = menubar.addMenu('&Help')

        #FILE MENU
        fileMenu.addAction(fileAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        #EDIT MENU
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        editMenu.addSeparator()
        editMenu.addAction(deleteAction)

        self.nodeEditorWidget = NodeEditorWidget(self)
        self.setCentralWidget(self.nodeEditorWidget)

        #SET WINDOW PROPERTIES
        self.setGeometry(600, 300, 800, 600)
        self.setWindowTitle('Node Editor')
        #STATE BAR
        self.statusBar().showMessage('Ready')
        self.statusBar().setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);')
        self.statusMousePos = QLabel('')
        self.statusBar().addPermanentWidget(self.statusMousePos)
        self.nodeEditorWidget.view.scenePosChanged.connect(self.on_mouse_pos_change)


        self.show()

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

    def NewFile(self):
        '''

        :return:
        '''
        print('New File')
        self.nodeEditorWidget.New_def()


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

    def saveAsFile(self):
        '''

        :return:
        '''
        print('Save As File')
        fileName = self.nodeEditorWidget.SaveAs_def()
        self.statusBar().showMessage('File Saved As %s' % fileName)

    def undoFile(self):
        '''

        :return:
        '''
        print('Undo File')
        self.nodeEditorWidget.scene.history.undo()

    def redoFile(self):
        '''

        :return:
        '''
        self.nodeEditorWidget.scene.history.redo()

    def deleteFile(self):
        '''

        :return:
        '''
        print('Delete File')
        self.nodeEditorWidget.scene.grScene.views()[0].deleteSelected()

    def on_mouse_pos_change(self, x, y):

        '''

        :return:
        '''
        self.statusMousePos.setText('Scene Pos: %d, %d' % (x, y))
