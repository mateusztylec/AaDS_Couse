#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from typing import TypeVar, Tuple, List


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

    def insertEdge(self, vertex1, vertex2, edge1_):
        self.list_ngh[self.map_idx[vertex1]].append(
            (self.map_idx[vertex2], edge1_))  # czy hash map_inx[vertex1] jest równy hash zapisanego

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
    def __init__(self, capacity, isResidual: bool = False):
        self.capacity = capacity  # pojemność
        self.flow = 0  # początkowy przepływ
        self.residual = capacity  # przepływ resztowy
        self.isResidual: bool = isResidual  # czy resztowa

    def __repr__(self):
        return f'{self.capacity} {self.flow} {self.residual} {self.isResidual}'

    def getResidual(self):
        return self.isResidual

    def getResidualFlow(self):
        return self.residual


NeighList = TypeVar('NeighList', bound=ListGraph)


def BFS(graph: NeighList):
    visited = [False] * graph.order()
    parent_list = [-1] * graph.order()
    queue_ = [0]
    visited[0] = True

    while queue_:
        vertex_idx = queue_.pop(0)
        neigh_idx = graph.neighbours(vertex_idx)
        for i in neigh_idx:
            if not visited[i[0]]:
                if i[1].residual > 0:
                    queue_.append(i[0])
                    visited[i[0]] = True
                    parent_list[i[0]] = vertex_idx
    return parent_list


def path_analise(graph: NeighList, start_v, end_v, parent_lst_) -> int:
    vertex_idx = graph.getVertexIdx(end_v)
    vertex_idx_s = graph.getVertexIdx(start_v)
    min_capacity = np.inf
    if parent_lst_[vertex_idx] == -1:
        return 0
    else:
        while vertex_idx != vertex_idx_s:
            parent = parent_lst_[vertex_idx]
            neigh = graph.neighbours(parent)
            edge = -1
            for i in neigh:
                if i[0] == vertex_idx and not i[1].getResidual():
                    edge = i[1]
            if min_capacity > edge.getResidualFlow():
                min_capacity = edge.getResidualFlow()
            vertex_idx = parent
    return min_capacity


def path_augmentation(graph: NeighList, start_v, end_v, parent_list, min_capacity: int):
    vertex_idx = graph.getVertexIdx(end_v)
    vertex_idx_s = graph.getVertexIdx(start_v)
    if parent_list[vertex_idx] == -1:
        return 0
    else:
        while vertex_idx != vertex_idx_s:
            parent_idx = parent_list[vertex_idx]
            for i in graph.neighbours(parent_idx):
                if i[0] == vertex_idx:
                    if not i[1].getResidual():
                        i[1].flow += min_capacity
                        i[1].residual -= min_capacity
            for j in graph.neighbours(vertex_idx):
                if j[0] == parent_idx:
                    if j[1].getResidual():
                        j[1].residual += min_capacity

            vertex_idx = parent_idx


def ford_fulkerson(graph: NeighList, start_v, end_v):
    parent_list = BFS(graph)
    v_inx_end = graph.getVertexIdx(end_v)
    if parent_list[v_inx_end] == -1:
        return 0
    min_capacity = path_analise(graph, start_v, end_v, parent_list)

    while min_capacity > 0:
        path_augmentation(graph, start_v, end_v, parent_list, min_capacity)
        parent_list = BFS(graph)
        min_capacity = path_analise(graph, start_v, end_v, parent_list)

    neigh = graph.neighbours(v_inx_end)

    flow_sum = 0
    for edge in neigh:
        if edge[1].getResidual:
            flow_sum += edge[1].residual
    return flow_sum


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


def create_graph(graph: List[Tuple]):
    visited = []
    neigh_list = ListGraph()
    for edge in graph:
        if edge[0] not in visited:
            visited.append(edge[0])
            neigh_list.insertVertex(Node(edge[0]))
        if edge[1] not in visited:
            visited.append(edge[1])
            neigh_list.insertVertex(Node(edge[1]))
        neigh_list.insertEdge(Node(edge[0]), Node(edge[1]), Edge(edge[2]))
        edge2 = Edge(edge[2], True)
        edge2.residual = 0
        neigh_list.insertEdge(Node(edge[1]), Node(edge[0]), edge2)
    return neigh_list


if __name__ == "__main__":
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]

    ll0 = create_graph(graf_0)
    print(ford_fulkerson(ll0, Node('s'), Node('t')))
    printGraph(ll0)
    ll1 = create_graph(graf_1)
    print(ford_fulkerson(ll1, Node('s'), Node('t')))
    printGraph(ll1)
    ll2 = create_graph(graf_2)
    print(ford_fulkerson(ll2, Node('s'), Node('t')))
    printGraph(ll2)
    ll3 = create_graph(graf_3)
    print(ford_fulkerson(ll3, Node('s'), Node('t')))
    printGraph(ll3)
