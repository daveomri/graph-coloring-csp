# David Omrai 14.10.21

from map import Map

class Cleaner:
    """
        Parameters
        ----------
        path: str
            Path of the map file
        width: int
            Width of random map
        height: int
            Height of random map
    """
    def __init__(self, path = "", width = 0, height = 0):
        self.load_map(path, width, height)

    """
        Creates the new map with trash
        If the location of map file is given then this map is used, random otherwise

        Parameters
        ----------
        path: str
            Path of the map file
        width: int
            Width of random map
        height: int
            Height of random map
    """
    def load_map(self, path = "", width = 0, height = 0):
        # the cleaning path of cleaner
        self._cleaner_route = []
        # map with trash
        self._space_map = Map(path, width, height)
        # map height
        self._space_map_height = self._space_map.get_height()
        # map width
        self._space_map_width = self._space_map.get_width()
        # current cleaner location
        self._cleaner_loc = self.find_cleaner()

    """
        This method searches for the cleaner
        Returns robot position if it's found, empty otherwise
    """
    def find_cleaner(self):
        for i in range(self._space_map.get_height()):
            for j in range(self._space_map.get_width()):
                if (self._space_map.get_place(j, i) == "o"):
                    return [j, i]
        return []

    """
    -------------------------------------------------------------------------
        naive bfs cleaning approach
    """

    """
        This method is the main part of bfs cleaning approach
        In loop it searches for closest trash and stores its path
    """
    def bfs_clean(self):
        # current location of cleaner
        cleaner_loc = self._cleaner_loc
        # number of trash - for visualization sake
        trash_num = 0

        while True:
            clos_trash = self.bfs_find_element(cleaner_loc, '.')

            # no more trash
            if len(clos_trash) == 0:
                # find the path back to start
                self._space_map.write_value(self._cleaner_loc[0], self._cleaner_loc[1], 'o')
                origin_pos = self.bfs_find_element(cleaner_loc ,'o')
                self._cleaner_route.append(origin_pos[1])
                
                self.print_bfs_info(self._cleaner_route)
                return self._cleaner_route

            # increase the number of trash
            trash_num += 1

            # save the trash path
            self._cleaner_route.append(clos_trash[1])

            # clean the trash
            self._space_map.write_value(clos_trash[0][0], clos_trash[0][1], '{0}'.format(trash_num))

            # set new cleaner location
            cleaner_loc = clos_trash[0]

    def print_bfs_info(self, cleaner_path):
        # print the current approach
        print("Naive BFS cleaning approach")
        # print the map
        self._space_map.print()
        # print the cleaner path
        print(cleaner_path)

    """
        This method uses the bfs approach and searches for the closest element
        The [loc_closest_elem, path] is returned

        Parameters
        ----------
        cleaner_loc: list
            Location of the search start
        element: str
            Searched element
    """
    def bfs_find_element(self, cleaner_loc, element):
        space_map = [[0 for _ in range(self._space_map_width)] for _ in range(self._space_map_height)]
        space_map[cleaner_loc[1]][cleaner_loc[0]] = 1
        s_queue = []

        s_queue.append([cleaner_loc, []])

        while True:
            if len(s_queue) == 0:
                return []

            cur_elem = s_queue.pop(0)

            if self._space_map.get_place(cur_elem[0][0], cur_elem[0][1]) == element:
                return cur_elem
            
            """ look up left down right """
            #up
            if (cur_elem[0][1] - 1 >= 0) and space_map[cur_elem[0][1] - 1][cur_elem[0][0]] == 0:
                """add up"""
                up_pos = [cur_elem[0][0], cur_elem[0][1] - 1]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                s_queue.append([up_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1] - 1][cur_elem[0][0]] = 1

            #down
            if (cur_elem[0][1] + 1) < self._space_map_height and space_map[cur_elem[0][1] + 1][cur_elem[0][0]] == 0:
                """add up"""
                down_pos = [cur_elem[0][0], cur_elem[0][1] + 1]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                s_queue.append([down_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1] + 1][cur_elem[0][0]] = 1

            #left
            if (cur_elem[0][0] - 1) >= 0 and space_map[cur_elem[0][1]][cur_elem[0][0] - 1] == 0:
                """add up"""
                left_pos = [cur_elem[0][0] - 1, cur_elem[0][1]]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                s_queue.append([left_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1]][cur_elem[0][0] - 1] = 1

            #right
            if (cur_elem[0][0] + 1) < self._space_map_width and space_map[cur_elem[0][1]][cur_elem[0][0] + 1] == 0:
                """add up"""
                right_pos = [cur_elem[0][0] + 1, cur_elem[0][1]]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                s_queue.append([right_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1]][cur_elem[0][0] + 1] = 1




    """ 
    -------------------------------------------------------------------------
        Planning with astar approach 
    """
    """
        This mathod returns the location of all the trashes
        from the map
        The first place represents the robot position, this
        is because as the trash we want the robot to be in
        the graph
    """
    def get_all_trash(self):
        # add first the robot location
        trash_arr = [self._cleaner_loc]
        # find all the trashes
        for y in range(self._space_map_height):
            for x in range(self._space_map_width):
                if self._space_map.get_place(x, y) == '.':
                    trash_arr.append([x, y])
        return trash_arr

    """
        This method calculates the manhaton distance for given
        locations

        Parameters
        ----------
        pos1: list [x, y]
            Location of first element
        pos2: list [x, y]
            Location of the second element
    """
    def get_manhaton_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    """
        This method returns the matrix representing the graph
        with edges with distance between each two nodes

        Parameters
        ----------
        arr: list [[x, y], [x, y], ...]
            The array of locations
    """
    def get_distance_matrix(self, arr):
        # distance matrix
        distance_matrix = [[0 for _ in range(len(arr))] for _ in range(len(arr))]
        for i in range(len(arr)):
            curr_elem = arr[i]
            for j in range(i + 1, len(arr)):
                elems_dist = self.get_manhaton_distance(curr_elem, arr[j])
                # matrix is symetrical
                distance_matrix[i][j] = elems_dist
                distance_matrix[j][i] = elems_dist

        return distance_matrix

    """
        This method sorts the graph edges, incresing order

        Parameters
        ----------
        graph_matrix: 2d list
            Graph represented by matrix
    """
    def get_sorted_graph_edges(self, graph_matrix):
        edges = []
        for i in range(len(graph_matrix)):
            for j in range(i + 1, len(graph_matrix)):
                edges.append([i, j])

        edges.sort(key=lambda edge: graph_matrix[edge[0]][edge[1]])
        return edges

    """
        This method calculated the smallest spanning tree from
        given matrix (graph)
        The result is again graph (matrix)

        Parameters
        ----------
        graph_matrix: 2d list
            Matrix representing the graph
    """
    def get_smallest_spanning_tree(self, graph_matrix):
        new_graph_metrix = [[0 for _ in range(len(graph_matrix))] for _ in range(len(graph_matrix))]
        sorted_edges = self.get_sorted_graph_edges(graph_matrix)
        node_parents = [i for i in range(len(graph_matrix))]

        for edge in sorted_edges:
            if node_parents[edge[0]] == node_parents[edge[1]]:
                continue

            new_graph_metrix[edge[0]][edge[1]] = graph_matrix[edge[0]][edge[1]]
            new_graph_metrix[edge[1]][edge[0]] = graph_matrix[edge[1]][edge[0]]

            old_parent = node_parents[edge[1]]
            for i in range(len(node_parents)):
                if node_parents[i] == old_parent:
                    node_parents[i] = node_parents[edge[0]]
        
        return new_graph_metrix

    """
        This method uses the dfs to get the cleaning plan
        The result is list where on each position is the 
        place on map, where should the cleaner go next in
        order clean the map

        Parameters
        ----------
        graph_matrix: 2d list
            Graph matrix
    """
    def get_path_plan(self, graph_matrix):
        plan = []
        visited_nodes = [0 for _ in range(len(graph_matrix))]
        visited_nodes[0] = 1
        arr = [0]
        while len(arr) != 0:
            curr_node = arr.pop()

            plan.append(curr_node)

            cur_neigh = []
            for i in range(len(graph_matrix[curr_node])):
                if graph_matrix[curr_node][i] == 0:
                    continue
                if visited_nodes[i] == 1:
                    continue
                cur_neigh.append(i)
            
            cur_neigh.sort(key=lambda node: graph_matrix[node][curr_node])

            # append the next node
            for node in cur_neigh:
                visited_nodes[node] = 1
                arr.append(curr_node)
                arr.append(node)
        
        return plan

    """
        Method represents the top part of infomative cleaning of 
        the map. It first finds all the trash, creates the graph,
        then minimalizing it and getting the cleaning plan
    """
    def a_star_clean(self):
        all_trash = self.get_all_trash()
        # matrix representing the graph
        dist_matrix = self.get_distance_matrix(all_trash)
        # matrix representing the minimal spanning tree graph
        tree_graph = self.get_smallest_spanning_tree(dist_matrix)
        # cleaning plan
        plan = self.get_path_plan(tree_graph)
        # path of the cleaner on the map
        self._cleaner_route = []
        # if there is no plan, there is no need to search
        if len(plan) == 0:
            return self._cleaner_route
        # number of current trash
        trash_num = 0
        curr_pos = all_trash[plan[0]]
        for i in range(1, len(plan)):
            if self._space_map.get_place(curr_pos[0], curr_pos[1]) == ".":
                trash_num += 1
                # clean the trash
                self._space_map.write_value(curr_pos[0], curr_pos[1], "{0}".format(trash_num))

            fin_pos = all_trash[plan[i]]

            curr_path = self.a_star_search(curr_pos, fin_pos)

            self._cleaner_route.append(curr_path[1])

            curr_pos = fin_pos
        
        self.print_a_star_info(dist_matrix, tree_graph, plan)

    """
        This method prints the information into a console
        It shows how the parts of the cleaning process

        Parameters
        ----------
        dist_matrix: 2d list
            Trash graph in metrix
        tree_graph : 2d list
            Trash minimal spanning tree graph in matrix
        plan: list
            The positions where to go next
    """
    def print_a_star_info(self, dist_matrix, tree_graph, plan):
        # print the type of cleaner approach
        print("Informed cleaning approach")
        # the trash graph
        print("The trash graph metrix with distances")
        text_dist_matrix = ""
        for i in range(len(dist_matrix)):
            text_dist_matrix += "{:2}|".format(i)
            for j in range(len(dist_matrix[i])):
                text_dist_matrix += "{:3}".format(dist_matrix[i][j])
            text_dist_matrix += '\n'
        print(text_dist_matrix)
        # the min spanning tree
        text_tree_graph = ""
        for i in range(len(tree_graph)):
            text_tree_graph += "{:2}|".format(i)
            for j in range(len(tree_graph[i])):
                text_tree_graph += "{:3}".format(tree_graph[i][j])
            text_tree_graph += '\n'
        print("The minimal spanning tree graph")
        print(text_tree_graph)
         # the cleaning plan
        print("The cleaning plan")
        print(plan)
        # the cleaned map
        print("The cleaned map ")
        self._space_map.print()
        # cleaner path
        print("The cleaner path")
        print(self._cleaner_route)

    """
        This method represents the a-star search
        Two positions are given and it searches the path between them

        Parameters
        ----------
        curr_pos: list [x, y]
            From place
        fin_pos: list [x, y]
            To place
    """
    def a_star_search(self, curr_pos, fin_pos):
        space_map = [[0 for _ in range(self._space_map_width)] for _ in range(self._space_map_height)]
        space_map[curr_pos[1]][curr_pos[0]] = 1
        s_queue = []

        s_queue.append([curr_pos, []])

        while True:
            if len(s_queue) == 0:
                return []

            cur_elem = s_queue.pop()

            if cur_elem[0][0] == fin_pos[0] and cur_elem[0][1] == fin_pos[1]:
                return cur_elem
            
            curr_neigh = []

            """ look up left down right """
            #up
            if (cur_elem[0][1] - 1 >= 0) and space_map[cur_elem[0][1] - 1][cur_elem[0][0]] == 0:
                """add up"""
                up_pos = [cur_elem[0][0], cur_elem[0][1] - 1]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                curr_neigh.append([up_pos, elem_path])
                #s_queue.append([up_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1] - 1][cur_elem[0][0]] = 1

            #down
            if (cur_elem[0][1] + 1) < self._space_map_height and space_map[cur_elem[0][1] + 1][cur_elem[0][0]] == 0:
                """add up"""
                down_pos = [cur_elem[0][0], cur_elem[0][1] + 1]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                curr_neigh.append([down_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1] + 1][cur_elem[0][0]] = 1

            #left
            if (cur_elem[0][0] - 1) >= 0 and space_map[cur_elem[0][1]][cur_elem[0][0] - 1] == 0:
                """add up"""
                left_pos = [cur_elem[0][0] - 1, cur_elem[0][1]]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                curr_neigh.append([left_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1]][cur_elem[0][0] - 1] = 1

            #right
            if (cur_elem[0][0] + 1) < self._space_map_width and space_map[cur_elem[0][1]][cur_elem[0][0] + 1] == 0:
                """add up"""
                right_pos = [cur_elem[0][0] + 1, cur_elem[0][1]]
                elem_path = [x for x in cur_elem[1]]
                elem_path.append(cur_elem[0])
                curr_neigh.append([right_pos, elem_path])
                # remember place
                space_map[cur_elem[0][1]][cur_elem[0][0] + 1] = 1

            curr_neigh.sort(key=lambda pos: self.get_manhaton_distance(pos[0], fin_pos), reverse=True)

            for neigh in curr_neigh:
                s_queue.append(neigh)

    """
        Method returns the position of the cleaner
    """
    def get_cleaner_location(self):
        return self._cleaner_loc

    """
        Method prints the map
    """
    def print_map(self):
        self._space_map.print()
