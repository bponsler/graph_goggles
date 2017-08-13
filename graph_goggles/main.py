import argparse
import sys
import pkg_resources
from os.path import exists, abspath

from python_qt_binding import QtGui

from .window import GraphGogglesWindow


def main(argv=sys.argv):
    """The main method for the graph goggles application.

    * argv -- the command line arguments

    """
    parser = argparse.ArgumentParser(
        description="View a graph of a dot file through controllable goggles")
    parser.add_argument(
        "dot_file",
        type=str,
        nargs="?",
        help="the dot file to load")
    parser.add_argument(
        "-d",
        "--max-distance",
        type=int,
        default=10,
        help="the maximum distance from the node to allow")
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print the version of the application")
    args = parser.parse_args()

    # Handle the version argument
    if args.version:
        version = pkg_resources.get_distribution("graph_goggles").version
        print version
        exit(0)

    # Make sure the dot file is provided
    if args.dot_file is None:
        print "error: too few arguments"
        parser.print_help()
        exit(1)

    # Grab arguments
    dotFile = abspath(args.dot_file)
    maxDistance = args.max_distance

    # Make sure the dot file exists before continuing
    if not exists(dotFile):
        print "ERROR: could not find the dot file: %s" % dotFile
        exit(1)

    kwargs = {
        "dotFile": dotFile,
        "maxDistance": maxDistance,
    }

    app = QtGui.QApplication(argv)
    window = GraphGogglesWindow(**kwargs)
    window.show()
    ret = app.exec_()
    app.deleteLater()
    sys.exit(ret)
