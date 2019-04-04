__author__ = 'Eytan'

import networkx as nx
import Course
import color

class Graph:
    #get all nodes from course recursion
    def fill_nodes_from_course(self):
        self._course.add_nodes_to_nxGraph(self._graph)

    #create a graph, optionally pass a course object and fill it
    def __init__(self, course = None):
        self._graph = nx.Graph()
        self._course = None
        if course:
            self._course = course
            self.fill_nodes_from_course()

    def _color_first_nodes(self):
