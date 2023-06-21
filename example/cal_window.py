from PyQt.import_module import *
from PyQt import sample_widget_template, color_variable, styleSheet
from collections import OrderedDict
from nodeEditor.node_sertializable import Serializable
from nodeEditor.node_editor_window import NdeEditorWindow
from nodeEditor.example.cal_sub_window import calSubWindow
from nodeEditor.utils import *
import math

class calWindow(NdeEditorWindow):

    def initUI(self):
        '''

        :return:
        '''
        #super(calWindow, self).initUI()


        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.mdiArea.setDocumentMode(True)
        self.setCentralWidget(self.mdiArea)

        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.readSettings()
        self.writeSettings()

        self.createDockWindows()
        self.setWindowTitle("Calculator Node Editor")


    def createActions(self):
        super().createActions()
        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window",
                                triggered=self.mdiArea.closeActiveSubWindow)

        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows",
                                   triggered=self.mdiArea.closeAllSubWindows)

        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)

        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows",
                                  triggered=self.mdiArea.cascadeSubWindows)

        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdiArea.activateNextSubWindow)

        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
    
    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        #self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def NewFile(self):
        '''

        :return:
        '''
        try:
            subWindow = self.createMdiChild()
            subWindow.show()
            self.updateMenus()
        except Exception as e:
            dumpException(e)

    def openFile(self):
        '''

        :return:
        '''
        try:
            fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', filter='*.json')
            if fnames != []:
                for each in fnames:
                    existing = self.findMdiChild(os.path.basename(each))
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        self.nodeEditorWidget = calSubWindow()
                        if self.nodeEditorWidget.scene.loadFromFile(each):
                            self.statusBar().showMessage("File %s loaded" % (each), 5000)
                            self.nodeEditorWidget.setTitle()
                            subwnd = self.mdiArea.addSubWindow(self.nodeEditorWidget)
                            subwnd.show()
                            self.nodeEditorWidget.filename = os.path.abspath(each)
                            self.nodeEditorWidget.setTitle()
                        else:
                            self.nodeEditorWidget.close()

        except Exception as e:
            dumpException(e)
        self.updateMenus()

    def close(self):
        '''

        :return:
        '''
    def saveFile(self):
        '''

        :return:
        '''
        currentSubWindow = self.mdiArea.currentSubWindow()

        filename = currentSubWindow.widget().filename
        if filename is None:
            currentSubWindow.widget().filename = None

        currentSubWindow.widget().Save_def(fileName=filename)
        self.statusBar().showMessage("File %s saved" % (filename), 5000)
        currentSubWindow.widget().setTitle_()



    def saveAsFile(self):
        '''

        :return:
        '''
        print('''this is saveAsFile''')
        self.nodeEditorWidget.SaveAs_def()
        self.statusBar().showMessage("File %s saved" % (self.nodeEditorWidget.filename), 5000)
        self.nodeEditorWidget.setTitle_()


    def findMdiChild(self, fname):
        '''

        :param fname:
        :return:
        '''
        for wnd in self.mdiArea.subWindowList():
            if fname in wnd.widget().getUserFriendlyFilename():
                return wnd
        return None

    def createMdiChild(self):
        '''

        :return:
        '''
        self.nodeEditorWidget = calSubWindow()
        subwnd = self.mdiArea.addSubWindow(self.nodeEditorWidget)


        return subwnd


    def createToolBars(self):
        '''

        :return:
        '''
        pass

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None
    def updateMenus(self):
        '''

        :return:
        '''
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)
        self.saveAction.setEnabled(hasMdiChild)
        self.saveAsAction.setEnabled(hasMdiChild)
        self.cutAction.setEnabled(hasMdiChild)
        self.copyAction.setEnabled(hasMdiChild)
        self.pasteAction.setEnabled(hasMdiChild)
        self.undoAction.setEnabled(hasMdiChild)
        self.redoAction.setEnabled(hasMdiChild)
        self.deleteAction.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)




    def setActiveSubWindow(self, window):
        '''

        :param window:
        :return:
        '''
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def createDockWindows(self):
        '''

        :return:
        '''
        self.nodesDock = QDockWidget("calc Node", self)
        itemList = ['Add', 'Subtract', 'Multiply', 'Divide', 'Modulus', 'Power', 'Square Root', 'Logarithm', 'Sine']
        listWidget = self.sample_widget_template.list_widget(parent_self=self.nodesDock, items=itemList)
        self.nodesDock.setWidget(listWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.nodesDock)
        self.nodesDock.setFloating(False)
        self.nodesDock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

    def closeEvent(self, event):
        '''

        :param event:
        :return:
        '''
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")

    def updateWindowMenu(self):
        print('updateWindowMenu')
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        # toolbar_nodes.setChecked(self.nodesDock.isVisible())

        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createStatusBar(self):
        '''

        :return:
        '''
        self.statusMousePos = QLabel()
        self.statusBar().addWidget(self.statusMousePos)
        self.statusBar().showMessage('Ready')

