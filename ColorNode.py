# David Omrai 24.10.21

"""
    This class represents the graph node
    for the graph coloring problem
"""
class ColorNode: 
    """
        Init method sets the name of the graph
        and its default color

        Parameters
        ----------
        name: str
            Name of the graph node
    """
    def __init__(self, name):
        self.name = name
        self.color = None
        self.valid_colors = None
        self.neighbours = []

    """
        Method adds node to a neighbours array

        Parameters
        ----------
        neighbour: Node
            Node representation of neighbour
    """
    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
    
    """
        Method returns the node neighbours
    """
    def get_neighbours(self):
        return self.neighbours

    """
        Method returns node color
    """
    def get_color(self):
        return self.color
    """
        Method returns the nodes' name
    """
    def get_name(self):
        return self.name
    """
        Method returns all possible colors
    """
    def get_valid_colors(self):
        return self.valid_colors

    """
        Method sets the color of the graph

        Parameters
        ----------
        new_color: str
            Name of the color for this graph
    """
    def set_color(self, new_color):
        self.color = new_color

    """
        Method cleans the node color to default
    """
    def clean_graph(self):
        self.color = None
    