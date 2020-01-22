import os
import sys


class APA(object):
    """APA"""
    def __init__(self, input_arcs=None, input_vertices=None):
        self.input_arcs = input_arcs
        self.input_vertices = input_vertices

    def load_input(self):
        """Loads input"""
        arcs = []
        vertices = []

        with open(self.input_arcs) as file:
            arcs = file.read().splitlines()

        with open(self.input_vertices) as file:
            vertices = file.read().splitlines()

        return arcs, vertices


class Vertex:  # facility
    def __init__(self, n):
        self.name = n


class Graph:  # fuel cycle
    vertices = {}
    arcs = []
    arc_indices = {}

    def build_graph(self, arc_list, vertex_list):

        for i in vertex_list:
            self.add_vertex(Vertex(i))

        for arc in arc_list:
            self.add_arc(arc[:1], arc[1:])

        return

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            for row in self.arcs:
                row.append(0)
            self.arcs.append([0] * (len(self.arcs)+1))
            self.arc_indices[vertex.name] = len(self.arc_indices)
            return True
        else:
            return False

    def add_arc(self, u, v, weight=1):
        if u in self.vertices and v in self.vertices:
            self.arcs[self.arc_indices[u]][self.arc_indices[v]] = weight
            # commented out because all fuel cycles are directed graphs,
            # which is also why these are arcs not edges
            # self.arcs[self.arc_indices[v]][self.arc_indices[u]] = weight
            return True
        else:
            return False

    def print_graph(self):
        for v, i in sorted(self.arc_indices.items()):
            print(v + ' ', end='')
            for j in range(len(self.arcs)):
                print(self.arcs[i][j], end='')
            print(' ')
