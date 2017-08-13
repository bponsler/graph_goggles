import pygraphviz as pgv

from qt_dotgraph.pydotfactory import PydotFactory


class Edge:
    """The Edge class encapsulates the data pertaining to
    a single edge in the graph.

    """

    def __init__(self, start, end, label=""):
        """
        * start -- the start node for the edge
        * end -- the end node for the edge
        * label -- the label for the edge

        """
        self.start = start
        self.end = end
        self.label = label

    def equals(self, other):
        """Determine if two edges are equal.

        * other -- the other edge

        """
        return (self.start == other.start and self.end == other.end)

    def __str__(self):
        """Get the string representation of the edge."""
        return str(self.label)


class DotFileGraph:
    """The DotFileGraph class provides the logic for loading a dot file
    into memory and providing the ability to generate a selected
    portion of the graph into dot code.

    """

    def __init__(self, dotFile, aboveDistance=1, belowDistance=1):
        """
        * dotFile -- is the path to the dot file to load
        * aboveDistance -- the default distance above the node to display
        * belowDistance -- the default distance below the node to display

        """
        self.__dotFile = dotFile
        self.__selectedNode = ""  # No node selected by default
        self.__aboveDistance = aboveDistance
        self.__belowDistance = belowDistance

        # Factory used to generate dot code
        self.__dotcodeFactory = PydotFactory()

        # List of all nodes in the graph (updated once file is loaded)
        self.__allNodes = None

        # List of graph nodes and edges to display
        self.nodes = []
        self.edges = []

        # Load the initial dot file
        self.__loadDotFile()

    def getNodes(self):
        """Get the list of all nodes in the graph."""
        return self.__allNodes

    def getSelectedNode(self):
        """Get the name of the currently selected node."""
        return self.__selectedNode

    def setSelectedNode(self, node):
        """Set the currently selected node.

        * node -- the newly selected node

        """
        self.__selectedNode = node
        self.__loadDotFile()

    def getAboveDistance(self):
        """Get the distance above the node that is being displayed."""
        return self.__aboveDistance

    def setAboveDistance(self, distance):
        """Set the distance above the node that is being displayed.

        * distance -- the new distance above the node to display

        """
        self.__aboveDistance = distance
        self.__loadDotFile()

    def getBelowDistance(self):
        """Get the distance below the node that is being displayed."""
        return self.__belowDistance

    def setBelowDistance(self, distance):
        """Set the distance below the node that is being displayed.

        * distance -- the new distance below the node to display

        """
        self.__belowDistance = distance
        self.__loadDotFile()

    def getDotCode(self,
                   orientation='LR',
                   rank='same',
                   ranksep=0.2,
                   rankdir='TB',
                   simplify=True):
        """Get the dot code for this graph.

        * orientation -- the orientation of the dot figure (UD, or LR)
        * rank -- the rank (none, same, min, max, source, sink)
        * ranksep -- vertical distance between layers
        * rankdir -- the direction of layout: TB (top-bottom), LR (left-right)
        * simplify -- True to remove double edges

        """
        # create the graph
        dotGraph = self.__dotcodeFactory.get_graph(
            rank=rank,
            ranksep=ranksep,
            simplify=simplify,
            rankdir=orientation)

        # Add all nodes to the graph
        if self.nodes is not None:
            for node in self.nodes:
                color = "blue" if node == self.__selectedNode else None

                self.__dotcodeFactory.add_node_to_graph(
                    dotGraph,
                    nodename=node,
                    nodelabel=node,
                    shape='ellipse',
                    color=color)

        # Add all edges to the graph
        if self.edges is not None:
            for edge in self.edges:
                self.__dotcodeFactory.add_edge_to_graph(
                    dotGraph,
                    edge.start,
                    edge.end,
                    label=edge.label)

        # Convert the dot graph into dot code
        return self.__dotcodeFactory.create_dot(dotGraph)

    def __loadDotFile(self):
        """Load a graph from a dot file and prune out nodes and edges based
        on the distance above and below the currently selected node.

        """
        # Load the dot file into memory
        self.__graph = pgv.AGraph(self.__dotFile)

        self.__allNodes = self.__graph.nodes()

        # Prune the graph, as desired
        if len(self.__selectedNode) > 0:
            neighbors = self.__getNodeNeighbors(
                self.__selectedNode,
                self.__aboveDistance,
                self.__belowDistance)

            # Remove all non-neighbor nodes
            nodes = self.__graph.nodes()
            for node in nodes:
                if node not in neighbors:
                    self.__graph.delete_node(node)

        # Grab the set of nodes to display
        self.nodes = self.__graph.nodes()

        # Create the edges to display
        self.edges = []
        for start, end in self.__graph.edges():
            self.edges.append(Edge(start, end))

    def __getNodeNeighbors(self, node, numAbove, numBelow):
        """Get the neighbors (above and below) to the given node.

        * node -- the name of the node
        * numAbove -- the number of levels above the node to include
        * numBelow -- the number of levels below the node to include

        """
        parents = self.__getNodeParents(node, numAbove)
        children = self.__getNodeChildren(node, numBelow)
        return parents + children + [node]

    def __getNodeParents(self, node, level):
        """Get the parents (up to a certain level away) of the given node.

        * node -- the name of the node
        * level -- the maximum levels away from the node to include

        """
        if level <= 0:
            return []

        allNodes = []

        # Add all nodes one level above the current node
        parents = self.__graph.predecessors(node)
        for subNode in parents:
            subNodes = self.__getNodeParents(subNode, level - 1)
            allNodes.append(subNode)
            allNodes.extend(subNodes)

        return list(set(allNodes))

    def __getNodeChildren(self, node, level):
        """Get the children (up to a certain level away) of the given node.

        * node -- the name of the node
        * level -- the maximum levels away from the node to include

        """
        if level <= 0:
            return []

        allNodes = []

        # Add all nodes one level below the current node
        parents = self.__graph.successors(node)
        for subNode in parents:
            subNodes = self.__getNodeChildren(subNode, level - 1)
            allNodes.append(subNode)
            allNodes.extend(subNodes)

        return list(set(allNodes))
