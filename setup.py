#!/usr/bin/env python
from distutils.core import setup


# Make sure python_qt_binding is installed
try:
    import python_qt_binding
except:
    print "ERROR: missing requirement: 'python_qt_binding'"
    print
    print "Please install python_qt_binding and try again:"
    print
    print "    sudo pip install python_qt_binding"
    exit(1)

# Make sure pygraphviz is installed
try:
    import pygraphviz
except:
    print "ERROR: missing requirement: 'pygraphviz'"
    print
    print "Please install pygraphviz and try again:"
    print
    print "    sudo pip install pygraphviz"
    exit(1)


setup(
    name="graph_goggles",
    version="0.0.1",
    description="View a dot graph through controllable goggles",
    author="Brett Ponsler",
    author_email="ponsler@gmail.com",
    packages=["graph_goggles"],
    scripts=["scripts/graph-goggles"]
)
