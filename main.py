# David Omrai 27.10.21

from CGraph import CGraph
from ColorNode import ColorNode

# Crate a new graph of Australia
color_graph = CGraph("australia.txt", 3)

# Color the graph using MAC-BT
color_graph.color_graph()

# Print the results
print(color_graph.get_colored_graph())