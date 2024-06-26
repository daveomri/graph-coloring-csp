# David Omrai 14.10.21

import numpy as np
import os
import random

class Map:
    def __init__(self, path = '', height = 0, width = 0):
        # define what is important
        self.height = height
        self.width = width

        self.space_map = self.generate_random_map(height, width) if path == '' else self.read_map_file(path)

    """
        This method reads the content of given file (map)

        Parameters
        ----------
        path : str
            Path to the file with map
    """
    def read_map_file(self, path):
        new_map = []
        with open(path) as f:
            for line in f.readlines():
                line = line.replace('\n', '')
                sub_array = []

                # read all chars, exclude \n 
                for char in line:
                    if (self.height == 0): self.width += 1
                    sub_array.append(char)
                
                new_map.append(sub_array)
                self.height += 1
        return new_map
    
    """
        This getter returns the height of map
    """
    def get_height(self):
        return self.height

    """
        This getter returns the width of map
    """
    def get_width(self):
        return self.width

    """
        This method generates random map, for better testing of algorithms

        Parameters
        ----------
        height : int
            Representation of y coordinate
        width : int
            Representation of x coordinate
    """
    def generate_random_map(self, height, width):
        # to do
        trash_prob = 0.2
        new_map = []
        for i in range(height):
            tmp_row = []
            for j in range(width):
                tmp_row .append('.' if random.random() <= trash_prob else ' ')
            new_map.append(tmp_row)
        # add robot on random place
        new_map[random.randint(0,height-1)][random.randint(0, width-1)] = 'o'
        return new_map

    """
        This method tests if the given coordinates are valid
        They should be >= 0 and smaler then the map boundaries

        Parameters
        ----------
        x : int
            It represents the x coordinate
        y : int
            It represents the y coordinate
    """
    def are_coordinates_valid(self, x, y):
        if (x < 0 or y < 0):
            return False
        if (x >= self.width or y >= self.height):
            return False
        return True

    """
        This method is simple getter
        It returns the content of given place

        Parameters
        ----------
        x : int
            It represents the x coordinate
        y : int
            It represents the y coordinate
    """
    def get_place(self, x, y):
        if (not self.are_coordinates_valid(x, y)):
            raise ValueError("Bad coordinates input")
        return self.space_map[y][x]

    """
        This method writes place given value on given location of map

        Parameters
        ----------
        x : int
            It represents the x coordinate
        y : int 
            It represents the y coordinate
    """
    def write_value(self, x, y, value):
        if (not self.are_coordinates_valid(x, y)):
            raise ValueError("Bad coordinates input")
        self.space_map[y][x] = value

    """
        This method prints the map
    """
    def print(self):
        output = ""
        for i in range(self.height):
            output += "{:2}|".format(i)
            for j in range(self.width):
                output += "{:3}".format(self.space_map[i][j])
            output += "\n"
        print(output)