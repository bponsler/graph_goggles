from os.path import abspath, basename, dirname, join, splitext

from python_qt_binding import QtCore, QtGui

from .widget import GraphGogglesWidget


class GraphGogglesWindow(QtGui.QMainWindow):
    """A simple QT window to display the dot graph."""

    def __init__(self, *args, **kwargs):
        """
        * args -- input args
        * kwargs -- input keyword arguments

        """
        QtGui.QMainWindow.__init__(self)

        # Create the menu
        self.__createMenu()

        self.__widget = GraphGogglesWidget(*args, **kwargs)
        self.setCentralWidget(self.__widget)
        self.setWindowTitle("Graph Goggles")

        self.setGeometry(0, 0, self.__widget.width(), self.__widget.height())

    def show(self):
        """Show the window."""
        QtGui.QMainWindow.show(self)
        self.__widget.show()

    def keyPressEvent(self, e):
        """Handle a key press event.

        * e -- the key press event

        """
        if e.key() == QtCore.Qt.Key_Escape:
            QtGui.QApplication.quit()

    def __createMenu(self):
        """Create a menu for the window."""
        # Create a save-as button
        saveAsAction = QtGui.QAction("&Save As", self)
        saveAsAction.setShortcut("Ctrl+S")
        saveAsAction.setStatusTip("Save the graph to a file")
        saveAsAction.triggered.connect(self.__onSaveAs)

        # Create an exit button
        exitAction = QtGui.QAction("&Exit", self)
        exitAction.setShortcut("Escape")
        exitAction.setStatusTip("Exit the application")
        exitAction.triggered.connect(QtGui.qApp.quit)

        # Create the menu bar, and add entries
        menuBar = self.menuBar()

        # Create the file menu
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(exitAction)

    def __onSaveAs(self):
        """Called when the save as option is selected."""
        dotFile = self.__widget.getDotFile()

        # Use the name of the selected node, if one is selected
        selectedNode = self.__widget.getSelectedNode()
        if len(selectedNode) == 0:
            # Use the same name as the dot file
            selectedNode = splitext(basename(dotFile))[0]

        # Create the path to the dot file to save it in the same
        # location as the loaded dot file
        filename = join(dirname(abspath(dotFile)), "%s.dot" % selectedNode)

        # Prompt the user where to save the file
        saveFilename = QtGui.QFileDialog.getSaveFileName(
            self, "Save As", filename, "*.dot")

        # Save the file -- if one was selected
        if len(saveFilename) == 2 and len(saveFilename[0]) > 0:
            self.__widget.onSaveAs(str(saveFilename[0]))
