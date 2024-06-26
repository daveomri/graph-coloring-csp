# David Omrai 27.10.21
import random
from ColorNode import ColorNode

"""
    Class represents the GC problem graph
"""
class CGraph:
    """
        Method creates the array for nodes
        that are used for the coloring problem

        The algorithm used for this problem is BT-MAC
    """
    def __init__(self, graph_name, num_colors = 3):
        # Array of graph nodes
        self.nodes = []
        # Name of the graph
        self.name = ""
        # Number of colors to work with
        self.num_colors = num_colors
        # The result array
        self.graph_colors = []
        # One run results, for one component
        self.search_dict = dict()
        # Load the Australia graph
        self.load_graph("graphs/{}".format(graph_name))

    """
        Method returns the graph nodes
    """
    def get_nodes(self):
        return self.nodes
    
    """
        Method reads the given file with graph
        from graphs folder

        Parameters
        ----------
        file_path: str
            Path to a folder with graph
    """
    def load_graph(self, file_path):
        # Open the file containing the graph representation and nodes names
        with open(file_path, 'r') as f:
            # Read the graph name
            self.name = f.readline().strip()
            # Read node names and create them
            for node_name in str(f.readline().strip()).split(','):
                # Create and store the nodes of the graph
                self.nodes.append(ColorNode(node_name))
            # Create the graph
            for node_id in range(len(self.nodes)):
                # Read the line with current node neighbours
                node_neighbrs = f.readline().strip()
                # Connect the neighbours nodes with each other
                for neighbr_id in range(len(node_neighbrs)):
                    # If the node isn't a neigbour, continue
                    if node_neighbrs[neighbr_id] == '0':
                        continue
                    # Add this neighbour to current node
                    self.nodes[node_id].add_neighbour(self.nodes[neighbr_id])


    #======================algorithms======================
    """
        Method finds all untouched nodes and runs the backtracking 
        with maintaining arc consistency

        The color for each node is stored in the search_dict, when
        the root node is given True value from the recursion, that
        the recursion and search for colors was successful

        If any conflict happened on the way, the false is returned
        search ends, unable to get result
    """
    def color_graph(self):
        for node in self.nodes:
            # If the color of the node is set, continue
            if node.get_color() != None:
                continue

            # clean the nodes colors for current search
            self.search_dict = dict()

            # set valid colors to first node
            node.valid_colors = [i for i in range(self.num_colors)]
            
            # run the search on the first graph component
            if self.search_colors(node) == False:
                print("Not enough colors")
                break

            # add the found results to solution array
            else:
                self.graph_colors.append(self.search_dict)

    """
        Method returns the blank nodes from given array

        Parameters
        ----------
        nodes: array
            Array of nodes for which this method checks the color
    """
    def get_blank_nodes(self, nodes):
        blank_nodes = []
        for node in nodes:
            if node.get_color() == None:
                blank_nodes.append(node)
        return blank_nodes

    """
        Method returns the blank neighbours of given node

        Parameters
        ----------
        cur_node: ColorNode
            Node to be searched for blank neighbours
    """
    def get_blank_neighs(self, cur_node):
        nodes = cur_node.get_neighbours()
        blank_neighs = []
        for node in nodes:
            if node.get_color() == None:
                blank_neighs.append(node)

        return blank_neighs


    """
        Method checks if the node's color is valid
        Color is valid if it's conrained in node valid colors
    """
    def is_node_color_valid(self, cur_node):
        return cur_node.get_color() in cur_node.get_valid_colors()

    """
        Method is main part of the BT-MAC searching
        It uses the recursion in the following way

        For each of the neighbour that is not yet colored 
        is updated the array of valid colors, then the first one of 
        these nodes is used to move the search

        If there are no more nodes to color and no error has occured
        then the method returns True, if there is error, no color can be used
        yet there are still uncolored nodes, then the method returns False value

        If the False is returned, the current color of the node is removed, all
        the neighbours without color are updated, to contain again before removed 
        color from their valid array

        And the search goes like this untill all the possible combinations are tried

        Parameters
        ----------
        node: ColorNode
            Node for coloring
    """
    def search_colors(self, node):
        # Find the uncolored neighbours
        new_neighs = self.get_blank_neighs(node)

        # Shuffle the node colors, to get random results
        random.shuffle(node.valid_colors)

        # Use all possible colors for the current node
        for color in node.valid_colors:
            # set new color
            node.set_color(color)

            # store current node color
            self.search_dict[node.get_name()] = color

            # Check if the color is valid
            if self.is_node_color_valid(node) == False:
                node.set_color(None)
                continue
            
            # remove this color to neighbours possible colors
            for neigh in new_neighs:
                if neigh.valid_colors == None:
                    neigh.valid_colors = [i for i in range(self.num_colors)]
                if color in neigh.valid_colors:
                    neigh.valid_colors.remove(color)

            # Sort the neighs by the valid array length
            # This fixes the problem with already evaluated subgraph
            new_neighs.sort(key=lambda x: len(x.valid_colors))
            
            # Set the initial value
            valid_color = True

            # Search the rest of neighbours if the constraints for them are satisfied
            for neigh in new_neighs:
                # if the node's been already searched continue
                if neigh.get_color() != None:
                    continue

                # if the current color is not valid
                if self.search_colors(neigh) == False:
                    valid_color = False
                    break

            # is valid color
            if valid_color == True:
                break

            # color is not valid, fix the valid colors of neighbours
            for neigh in new_neighs:
                neigh.valid_colors.append(color)
            
            # remove current invalid color
            node.set_color(None)


        # If the node's color can't be set, return False
        if node.get_color() == None:
            return False
        
        # The node is colored, return true
        return True

    """
        Method returns the result of graph coloring
    """
    def get_colored_graph(self):
        return self.graph_colors

            
            
            

            

