#!/usr/bin/python
# -*- coding: utf-8 -*-
import graf_mst
import numpy as np
from typing import TypeVar


class Node:
    def __init__(self, key, bright=0):
        self.key = key
        self.bright = bright

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return str(self.key)


class ListGraph:
    def __init__(self):
        self.nodes = []  # uporządkowana lista wierzchołków
        self.map_idx = {}  # mapa konwertująca węzeł na indeks w self.nodes
        self.list_ngh = []  # lista sąsiedztwa

    def insertVertex(self, vertex):
        self.nodes.append(vertex)
        self.map_idx[vertex] = len(self.nodes) - 1
        self.list_ngh.append([])

    def insertEdge(self, vertex1, vertex2, edge_):
        self.list_ngh[self.map_idx[vertex1]].append((self.map_idx[vertex2], edge_))  # czy hash map_inx[vertex1] jest równy hash zapisanego
        self.list_ngh[self.map_idx[vertex2]].append((self.map_idx[vertex1], edge_))

    def deleteVertex(self, vertex1):
        del_idx = self.map_idx[vertex1]
        self.nodes.remove(vertex1)
        self.list_ngh.pop(del_idx)
        for idx, vertex in enumerate(self.nodes):
            self.map_idx[vertex] = idx
            for idx_n, node_idx in enumerate(self.neighbours(idx)):
                if node_idx == del_idx:
                    self.list_ngh[idx].pop(idx_n)
                    if idx_n >= len(self.list_ngh[idx]) - 1:
                        break
                    if self.list_ngh[idx][idx_n] > del_idx:
                        self.list_ngh[idx][idx_n] -= 1
                elif node_idx > del_idx:
                    self.list_ngh[idx][idx_n] -= 1

    def deleteEdge(self, vertex1, vertex2):
        v1 = self.map_idx[vertex1]
        v2 = self.map_idx[vertex2]
        self.list_ngh[v1].remove(v2)

    def getVertexIdx(self, vertex):  # returns vertex index in self.nodes
        return self.map_idx[vertex]

    def getVertex(self, vertex_idx):  # returns vertex object
        return self.nodes[vertex_idx]

    def neighbours(self, vertex_inx):
        return self.list_ngh[vertex_inx]

    def order(self):  # amount of nodes
        return len(self.nodes)

    def size(self):  # amount of edges
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


class Edge:
    def __init__(self, cost=1):
        self.cost = cost

    def __repr__(self):
        return str(self.cost)


NeighList = TypeVar('NeighList', bound=ListGraph)


def prima(G: NeighList):
    intree = [0 for _ in range(G.order())]  # czy odwiedzony, indeksy oznaczają indeksy wierzchołków w G.nodes
    distance = [np.inf for _ in range(G.order())]
    parent = [-1 for _ in range(G.order())]
    v: int = 0  # index wierzchołek
    mst_distance = 0
    mst_tree: NeighList = ListGraph()
    for i in range(G.order()):
        mst_tree.insertVertex(G.getVertex(i))

    while intree[v] == 0:
        intree[v] = 1
        for i in G.neighbours(v):
            if not intree[i[0]]:
                if i[1].cost < distance[i[0]]:
                    distance[i[0]] = i[1].cost
                    parent[i[0]] = v
        min_dist = np.inf
        for i in range(G.order()):
            if intree[i] == 0:
                if distance[i] < min_dist:
                    v = i
                    min_dist = distance[i]

        if any(not elem for elem in intree):
            mst_tree.insertEdge(G.getVertex(v), G.getVertex(parent[v]), Edge(distance[v]))
            mst_distance += distance[v]
    printGraph(mst_tree)


def printGraph(g: NeighList):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j), w, end=";")
        print()
    print("-------------------")


if __name__ == "__main__":
    visited = []
    nodes = []
    neigh_list = ListGraph()
    for edge in graf_mst.graf:
        if edge[0] not in visited:
            visited.append(edge[0])
            neigh_list.insertVertex(Node(edge[0]))
        if edge[1] not in visited:
            visited.append(edge[1])
            neigh_list.insertVertex(Node(edge[1]))
        neigh_list.insertEdge(Node(edge[0]), Node(edge[1]), Edge(edge[2]))

    printGraph(neigh_list)
    prima(neigh_list)
