# David Omrai 14.10.21

from map import Map
from cleaner import Cleaner

"""
    All the information with visual representation will be
    printed into console
"""

"""
    This part of program shows the naive approach
    of cleaning the room. 
    It uses the bfs algorithm and it goes like this
    The first trash is found, then the robot moves
    to this place and the process repeats until.
    When no more trash is on the map the robot
    returns back to the origin position
"""
new_cleaner = Cleaner('./maps/4x4-1.txt')
new_cleaner.bfs_clean()

print("\n-----------------------------------------------------------------------\n")

"""
    This part of program shows the better approach.
    First it finds all the trash, creates the graph 
    (metrix) of distances between each two pieces of 
    trash, the manhaton distance is used.
    With the use of Kruskal's algorithm the minimum
    spanning tree is calculated. It's again stored
    in the matrix.
    Then from this new graph the plan is retrieved,
    in each step the best one is taken.
    The plan is then used in a-star algorithm.
    The plan ends when there is no more trash and 
    robot is back in the origin position.
"""
new_cleaner = Cleaner('./maps/4x4-1.txt')
new_cleaner.a_star_clean()
