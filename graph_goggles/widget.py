from python_qt_binding.QtCore import Qt
from python_qt_binding import QtCore, QtGui

from qt_dotgraph.dot_to_qt import DotToQtGenerator

from .graph import DotFileGraph


class GraphGogglesWidget(QtGui.QWidget):
    """A QT Widget to selectively view the graph of a dot file."""

    def __init__(self, dotFile, maxDistance):
        """
        * dotfile -- the path to the dot file to load
        * maxDistance -- the maximum distance from the node to allow

        """
        QtGui.QWidget.__init__(self)
        self.__dotFile = dotFile
        self.__maxDistance = maxDistance

        # Load the graph from the dot file
        self.__graph = DotFileGraph(dotFile)
        self.__dotcode = None

        # Create a layout for the widget
        self.__layout = QtGui.QVBoxLayout()
        self.setLayout(self.__layout)

        # Create the graphics scene and view to display the graph
        self.__scene = QtGui.QGraphicsScene()
        self.__scene.setBackgroundBrush(Qt.white)
        self.__view = QtGui.QGraphicsView()
        self.__view.setScene(self.__scene)
        self.__layout.addWidget(self.__view)

        # Create a slider to change the parent depth
        self.__aboveSlider, self.__aboveLabel = self.__createDistanceSlider(
            "Distance above",
            self.__graph.getAboveDistance(),
            self.__onAboveDistance)

        # Create a slider to change the child depth
        self.__belowSlider, self.__belowLabel = self.__createDistanceSlider(
            "Distance below",
            self.__graph.getBelowDistance(),
            self.__onBelowDistance)

        # Create a list to view all nodes
        self.__createNodeListWidget()

        # Generates QT widgets from dot code
        self.__dotToQt = DotToQtGenerator()

        # Do the initial display of the graph
        self.updateGraph()

        self.setGeometry(0, 0, 1000, 600)

    def getDotFile(self):
        """Get the dot file that is being viewed."""
        return self.__dotFile

    def getSelectedNode(self):
        """Get the name of the currently selected node"""
        return self.__graph.getSelectedNode()

    def onSaveAs(self, saveFilename):
        """Save the current graph to the given file.

        * saveFilename -- the file to save the graph to

        """
        # Write the dot code to the file
        if self.__dotcode is not None:
            fd = open(saveFilename, "w")
            fd.write(self.__dotcode)
            fd.close()

    def updateGraph(self):
        """Update the graph."""
        self.__scene.clear()

        # Generate the dot graph
        self.__dotcode = self.__graph.getDotCode(
            orientation='UD',
            rank='same',
            simplify=False)  # Allow duplicate edges

        # Generate the QT items corresponding to the given dot graph
        highlight_level = 3
        (nodes, edges) = self.__dotToQt.dotcode_to_qt_items(
            self.__dotcode,
            highlight_level=highlight_level,
            same_label_siblings=True)

        # Add all the QT items to the scene
        for node_item in nodes.itervalues():
            self.__scene.addItem(node_item)
        for edge_items in edges.itervalues():
            for edge_item in edge_items:
                edge_item.add_to_scene(self.__scene)

        self.__scene.setSceneRect(self.__scene.itemsBoundingRect())

    def __onAboveDistance(self, distance):
        """Called when the above distance is changed.

        * distance -- the new above distance

        """
        # Update the label
        label = "%s" % distance
        self.__aboveLabel.setText(label)

        self.__graph.setAboveDistance(distance)
        self.updateGraph()  # Redisplay the graph

    def __onBelowDistance(self, distance):
        """Called when the below distance is changed.

        * distance -- the new below distance

        """
        # Update the label
        label = "%s" % distance
        self.__belowLabel.setText(label)

        self.__graph.setBelowDistance(distance)
        self.updateGraph()  # Redisplay the graph

    def __onSelectNode(self, node):
        """Called when a node is selected.

        * node -- the selected node

        """
        self.__graph.setSelectedNode(node)
        self.updateGraph()  # Redisplay the graph

    def __onNodeClicked(self, current, previous):
        """Called when a node is clicked in the list of nodes.

        * current -- the current node selected
        * previous -- the previously selected node

        """
        self.__onSelectNode(current.text())

    def __createDistanceSlider(self, label, distance, callback):
        """Create a slider widget to control the distance from the
        selected node.

        * label -- the label for the slider
        * distance -- the default distance value
        * callback -- the function to call when the slider is changed

        """
        frame = QtGui.QFrame()
        layout = QtGui.QHBoxLayout()
        frame.setLayout(layout)

        # Create a main label for the slider
        label = QtGui.QLabel("%s:" % label)
        layout.addWidget(label)

        # Create the slider
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(self.__maxDistance)
        slider.setValue(distance)
        slider.setTickPosition(QtGui.QSlider.TicksBelow)
        slider.setTickInterval(1)  # Every 1 level
        slider.valueChanged.connect(callback)
        layout.addWidget(slider)

        # Create a label to display the value
        label = QtGui.QLabel("%s" % distance)
        layout.addWidget(label)

        # Add a button to reset the slider to its original value
        resetButton = QtGui.QPushButton("Reset")
        resetButton.clicked.connect(self.__getClickWrapper(slider, distance))
        layout.addWidget(resetButton)

        self.__layout.addWidget(frame)

        return slider, label

    def __createNodeListWidget(self):
        """Create a list widget to display all possible nodes."""
        frame = QtGui.QFrame()
        layout = QtGui.QVBoxLayout()
        frame.setLayout(layout)

        # Add a label
        label = QtGui.QLabel("Nodes:")
        layout.addWidget(label)

        # Add the list of known nodes
        self.__nodeListWidget = QtGui.QListWidget()
        layout.addWidget(self.__nodeListWidget)

        # Display nodes in alphabetical order
        sortedNodes = sorted(self.__graph.getNodes())
        for node in sortedNodes:
            self.__nodeListWidget.addItem(node)

        # Update the graph with the currently selected widget
        self.__nodeListWidget.currentItemChanged.connect(self.__onNodeClicked)

        self.__layout.addWidget(frame)

    def __getClickWrapper(self, slider, resetValue):
        """Get a function wrapper to reset the given slider.

        * slider -- reset the slider
        * resetValue -- the value to reset the slider to

        """
        def __wrapper():
            slider.setValue(resetValue)
        return __wrapper
