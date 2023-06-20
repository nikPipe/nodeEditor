
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

        cutAction = self.action_def(name='Cut', shortcut='Ctrl+X', statusTip='Cut', toolTip='Cut', connect=self.cutFile)
        copyAction = self.action_def(name='Copy', shortcut='Ctrl+C', statusTip='Copy', toolTip='Copy', connect=self.copyFile)
        pasteAction = self.action_def(name='Paste', shortcut='Ctrl+V', statusTip='Paste', toolTip='Paste', connect=self.pasteFile)

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
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        editMenu.addSeparator()
        editMenu.addAction(deleteAction)

        self.nodeEditorWidget = NodeEditorWidget(self)
        self.setCentralWidget(self.nodeEditorWidget)

        #SET WINDOW PROPERTIES
        self.setGeometry(600, 300, 800, 600)
        self.nodeEditorWidget.changeTitle(self)
        #STATE BAR
        self.statusBar().showMessage('Ready')
        self.statusBar().setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);')
        self.statusMousePos = QLabel('')
        self.statusBar().addPermanentWidget(self.statusMousePos)
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
