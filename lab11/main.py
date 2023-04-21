#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
from typing import List


class Node:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)


class MatrixGraph:
    def __init__(self):
        self.nodes = []  # uporządkowana lista wierzchołków
        self.map_idx = {}  # mapa konwertująca węzeł na indeks w self.nodes
        self.matrix = np.empty((0, 1), int)

    def insertVertex(self, vertex):
        if vertex not in self.nodes:
            self.nodes.append(vertex)
            nodes_amount = len(self.nodes)
            self.map_idx[vertex] = nodes_amount - 1
            if nodes_amount == 1:
                self.matrix = np.append(self.matrix, np.array([[0] * nodes_amount]), axis=0)
            else:
                self.matrix = np.append(self.matrix, np.array([[0] * (nodes_amount - 1)]), axis=0)
            if nodes_amount > 1:
                self.matrix = np.append(self.matrix, np.array([[0] for _ in range(nodes_amount)]), axis=1)

    def insertEdge(self, vertex1, vertex2, edge_cost: int):
        v1_idx = self.map_idx[vertex1]
        v2_idx = self.map_idx[vertex2]
        self.matrix[v1_idx][v2_idx] = edge_cost

    # def deleteVertex(self, vertex1):
    #     del_idx = self.map_idx[vertex1]
    #     self.nodes.pop(del_idx)
    #     self.matrix.pop(del_idx)
    #     for idx, vertex in enumerate(self.nodes):
    #         self.map_idx[vertex] = idx
    #         del self.matrix[idx][del_idx]
    #         for i in range(del_idx-1, self.order()):
    #             if self.matrix[idx][i]:
    #                 self.matrix[idx][i] -= 1

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


# class Edge:
#     def __init__(self, cost=1):
#         self.cost = cost

def ullman(used_columns: List, current_row, G, P, M, no_recursion, amount_of_isomorph):
    if current_row == M.shape[0]:
        if np.array_equal(P, np.matmul(M, np.transpose(np.matmul(M, G)))):
            amount_of_isomorph += 1
        return amount_of_isomorph, no_recursion

    M_prim = deepcopy(M)

    for i_n in range(M.shape[1]):
        if i_n not in used_columns:
            M_prim[current_row][i_n] = 1
            used_columns.append(i_n)
            amount_of_isomorph, no_recursion = ullman(used_columns, current_row + 1, G, P, M_prim, no_recursion + 1,
                                                      amount_of_isomorph)
            M_prim[current_row][i_n] = 0
            used_columns.pop(-1)
    return amount_of_isomorph, no_recursion


def ullman_2_0(used_columns: List, current_row, G, P, M, M_0, no_recursion, amount_of_isomorph):
    if current_row == M.shape[0]:
        if np.array_equal(P, np.matmul(M, np.transpose(np.matmul(M, G)))):
            amount_of_isomorph += 1
        return amount_of_isomorph, no_recursion

    M_prim = deepcopy(M)

    for i_n in range(M.shape[1]):
        if i_n not in used_columns and M_0[current_row][i_n] == 1:
            M_prim[current_row][i_n] = 1
            used_columns.append(i_n)
            amount_of_isomorph, no_recursion = ullman_2_0(used_columns, current_row + 1, G, P, M_prim, M_0,
                                                          no_recursion + 1, amount_of_isomorph)
            M_prim[current_row][i_n] = 0
            used_columns.pop(-1)
    return amount_of_isomorph, no_recursion


def ullman_3_0(used_columns: List, current_row, G, P, M, M_0, no_recursion, amount_of_isomorph):
    if current_row == M.shape[0]:
        if np.array_equal(P, np.matmul(M, np.transpose(np.matmul(M, G)))):
            amount_of_isomorph += 1
        return amount_of_isomorph, no_recursion

    M_prim = deepcopy(M)
    check_posibility = prune(M_prim)
    if not check_posibility:
        return amount_of_isomorph, no_recursion

    for i_n in range(M.shape[1]):
        if i_n not in used_columns and M_0[current_row][i_n] == 1:
            M_prim[current_row,:] = 0
            M_prim[current_row,i_n] = 1
            used_columns.append(i_n)
            amount_of_isomorph, no_recursion = ullman_3_0(used_columns, current_row + 1, G, P, M_prim, M_0,
                                                          no_recursion + 1, amount_of_isomorph)
            M_prim[current_row][i_n] = 0
            used_columns.pop(-1)
    return amount_of_isomorph, no_recursion


def prune(M):
    flag = True
    while flag:
        flag = False
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i][j]:
                    p_neigh = P[i]
                    g_neigh = G[j]
                    for p_idx, x in enumerate(p_neigh):
                        if x:
                            check = True
                            for g_idx, y in enumerate(g_neigh):
                                if y:
                                    if M[p_idx][g_idx]:
                                        check = False
                                        break
                            if check:
                                flag = True
                                M[i][j] = 0
                                break

    is_poss = True
    for x in range(M.shape[0]):
        check2 = False
        for y in range(M.shape[1]):
            if M[x][y]:
                check2 = True
        if check2:
            is_poss = True
        else:
            is_poss = False
            break
    return is_poss


if __name__ == "__main__":
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    matrix_G = MatrixGraph()
    for i in range(len(graph_G)):
        matrix_G.insertVertex(Node(chr(65 + i)))
    for edge in graph_G:
        matrix_G.insertEdge(Node(edge[0]), Node(edge[1]), edge[2])
        matrix_G.insertEdge(Node(edge[1]), Node(edge[0]), edge[2])

    matrix_P = MatrixGraph()
    for i in range(len(graph_P)):
        matrix_P.insertVertex(Node(chr(65 + i)))
    for edge in graph_P:
        matrix_P.insertEdge(Node(edge[0]), Node(edge[1]), edge[2])
        matrix_P.insertEdge(Node(edge[1]), Node(edge[0]), edge[2])

    # matrix_G = MatrixGraph()
    # matrix_P = MatrixGraph()
    # for edge in graph_G:
    #     matrix_G.insertVertex(edge[0])
    #     matrix_G.insertVertex(edge[1])
    #     matrix_G.insertEdge(edge[0], edge[1], 1)
    #
    # for edge in graph_P:
    #     matrix_P.insertVertex(edge[0])
    #     matrix_P.insertVertex(edge[1])
    #     matrix_P.insertEdge(edge[0], edge[1], 1)

    M = np.zeros((matrix_P.matrix.shape[0], matrix_G.matrix.shape[0]))
    G = matrix_G.matrix
    P = matrix_P.matrix
    print(ullman([], 0, G, P, M, 0, 0))

    M_0 = np.zeros((matrix_P.matrix.shape[0], matrix_G.matrix.shape[0]))
    for i in range(matrix_P.matrix.shape[0]):
        for j in range(matrix_G.matrix.shape[0]):
            if len(matrix_P.neighbours(i)) <= len(matrix_G.neighbours(j)):
                M_0[i][j] = 1

    print(ullman_2_0([], 0, G, P, M, M_0, 0, 0))

    M = np.full((matrix_P.matrix.shape[0], matrix_G.matrix.shape[0]), 1)
    print(ullman_3_0([], 0, G, P, M, M_0, 0, 0))
