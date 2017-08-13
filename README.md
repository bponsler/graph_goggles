# graph_goggles

View a dot file through configurable goggles.

This application enables you to easily view a large dot file by providing
the ability to select individual nodes in the graph, and selectively view
levels above and below that node. This can make it easier to inspect and
understand dot graphs.

## Installation

Use the following commands to install the application:

    git clone https://github.com/bponsler/graph_goggles
    cd graph_goggles
    sudo python setup.py install

## Using graph goggles

Use the following commands to run graph goggles:

    graph-goggles --help

This command will print out the following information:

    $ graph-goggles --help
    usage: graph-goggles [-h] [-d MAX_DISTANCE] [-v] [dot_file]

    View a graph of a dot file through controllable goggles

    positional arguments:
      dot_file              the dot file to load

    optional arguments:
      -h, --help            show this help message and exit
      -d MAX_DISTANCE, --max-distance MAX_DISTANCE
                            the maximum distance from the node to allow
      -v, --version         print the version of the application

Or view a specific dot file:

    graph-googles /tmp/my_graph.dot

This command will launch an application to allow you to view and adjust
the nodes in the graph that are currently visible.

## Examples

Using the following dot code as an example (saved to /tmp/example.dot):

    graph {
        rankdir=LR; // Left to Right, instead of Top to Bottom
        a -- { b c d };
        b -- { c e };
        c -- { e f };
        d -- { f g };
        e -- h;
        f -- { h i j g };
        g -- k;
        h -- { o l };
        i -- { l m j };
        j -- { m n k };
        k -- { n r };
        l -- { o m };
        m -- { o p n };
        n -- { q r };
        o -- { s p };
        p -- { s t q };
        q -- { t r };
        r -- t;
        s -- z;
        t -- z;
    }

You can view the above dot code using the following command:

    graph-goggles /tmp/example.dot

The above command will display the following window:

![Graph goggles example window](screenshots/full_graph.png?raw=true)

Now, clicking on the **p** node updates the graph to look like this:

![Default view of the p node](screenshots/p_node_only.png?raw=true)

And adjusting the "Distance above" and "Distance below" to be 2 changes
the graph to look like this:

![View of two levels around the p node](screenshots/p_node_plus_minus_2.png?raw=true)
