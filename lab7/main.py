#!/usr/bin/python
# -*- coding: utf-8 -*-
import polska


class Node:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)


class ListGraph:
    def __init__(self):
        self.nodes = []  #uporządkowana lista wierzchołków
        self.map_idx = {}  #mapa konwertująca węzeł na indeks w self.nodes
        self.list_ngh = []  #lista sąsiedztwa

    def insertVertex(self, vertex):
        self.nodes.append(vertex)
        self.map_idx[vertex] = len(self.nodes) - 1
        self.list_ngh.append([])

    def insertEdge(self, vertex1, vertex2, edge):
        self.list_ngh[self.map_idx[vertex1]].append(self.map_idx[vertex2]) #czy hash map_inx[vertex1] jest równy hash zapisanego

    def deleteVertex(self, vertex1):
        del_idx = self.map_idx[vertex1]
        self.nodes.remove(vertex1)
        self.list_ngh.pop(del_idx)
        for idx, vertex in enumerate(self.nodes):
            self.map_idx[vertex] = idx
            for idx_n, node_idx in enumerate(self.neighbours(idx)):
                if node_idx == del_idx:
                    self.list_ngh[idx].pop(idx_n)
                    if idx_n >= len(self.list_ngh[idx])-1:
                        break
                    if self.list_ngh[idx][idx_n] > del_idx:
                        self.list_ngh[idx][idx_n] -= 1
                elif node_idx > del_idx:
                    self.list_ngh[idx][idx_n] -= 1

    def deleteEdge(self, vertex1, vertex2):
        v1 = self.map_idx[vertex1]
        v2 = self.map_idx[vertex2]
        self.list_ngh[v1].remove(v2)

    def getVertexIdx(self, vertex):   # returns vertex index in self.nodes
        return self.map_idx[vertex]

    def getVertex(self, vertex_idx):  # returns vertex object
        return self.nodes[vertex_idx]

    def neighbours(self, vertex_inx):
        return self.list_ngh[vertex_inx]

    def order(self):  #amount of nodes
        return len(self.nodes)

    def size(self): #amount of edges
        edge_sum = 0
        for i in self.list_ngh:
            edge_sum += len(i)
        return edge_sum

    def edges(self):
        edges = []

        for i in range(self.order()):
            for node in self.neighbours(i):
                edges.append((self.getVertex(i).key, self.getVertex(node).key))
        return edges


class MatrixGraph:
    def __init__(self):
        self.nodes = []  # uporządkowana lista wierzchołków
        self.map_idx = {}  # mapa konwertująca węzeł na indeks w self.nodes
        self.matrix = []

    def insertVertex(self, vertex):
        self.nodes.append(vertex)
        nodes_amount = len(self.nodes)
        self.map_idx[vertex] = nodes_amount - 1
        self.matrix.append([None])
        if nodes_amount > 1:
            for i in range(nodes_amount-1):
                self.matrix[i].append(None)
                self.matrix[nodes_amount-1].append(None)

    def insertEdge(self, vertex1, vertex2, edge):
        v1_idx = self.map_idx[vertex1]
        v2_idx = self.map_idx[vertex2]
        self.matrix[v1_idx][v2_idx] = v2_idx

    def deleteVertex(self, vertex1):
        del_idx = self.map_idx[vertex1]
        self.nodes.pop(del_idx)
        self.matrix.pop(del_idx)
        for idx, vertex in enumerate(self.nodes):
            self.map_idx[vertex] = idx
            del self.matrix[idx][del_idx]
            for i in range(del_idx-1, self.order()):
                if self.matrix[idx][i]:
                    self.matrix[idx][i] -= 1

    def deleteEdge(self, vertex1, vertex2):
        v1_idx = self.map_idx[vertex1]
        v2_idx = self.map_idx[vertex2]
        self.matrix[v1_idx][v2_idx] = None

    def getVertexIdx(self, vertex):
        return self.map_idx[vertex]

    def getVertex(self, vertex_idx):
        return self.nodes[vertex_idx]

    def neighbours(self, vertex_inx):
        ngbrs = []
        for i in range(self.order()):
            if self.matrix[vertex_inx][i]:
                ngbrs.append(self.matrix[vertex_inx][i])
        return ngbrs

    def order(self):
        return len(self.nodes)

    def size(self):
        edges_amount = 0
        size = self.order()
        for i in range(size):
            for j in range(size):
                if self.matrix[i][j]:
                    edges_amount += 1
        return edges_amount

    def edges(self):
        edges_m = []
        for i in range(self.order()):
            for j in range(self.order()):
                if self.matrix[i][j]:
                    edges_m.append((self.getVertex(i).key, self.getVertex(j).key))
        return edges_m


class Edge:
    def __init__(self, cost=1):
        self.cost = cost


if __name__ == "__main__":
    #lista sąsiedztwa
    n_list = ListGraph()
    for i in range(16):
        n_list.insertVertex(Node(polska.polska[i][2]))
    for i in polska.graf:
        n_list.insertEdge(Node(i[0]), Node(i[1]), Edge())
    n_list.deleteVertex(Node('K'))
    n_list.deleteEdge(Node('W'), Node('E'))
    n_list.deleteEdge(Node('E'), Node('W'))

    #macierz sąsiedztwa
    matrix_g = MatrixGraph()
    for i in range(16):
        matrix_g.insertVertex(Node(polska.polska[i][2]))
    for i in polska.graf:
        matrix_g.insertEdge(Node(i[0]), Node(i[1]), Edge())
    matrix_g.deleteVertex(Node('K'))
    matrix_g.deleteEdge(Node('W'), Node('E'))
    matrix_g.deleteEdge(Node('E'), Node('W'))

