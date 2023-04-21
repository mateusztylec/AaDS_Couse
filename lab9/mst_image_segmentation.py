import matplotlib.pyplot as plt
import cv2
import numpy as np
from typing import TypeVar


class Node:
    def __init__(self, key: str, bright=0):
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
        self.list_ngh = []  # lista sąsiedztwa, zawiera [index of node, edge]

    def insertVertex(self, vertex):
        self.nodes.append(vertex)
        self.map_idx[vertex] = len(self.nodes) - 1
        self.list_ngh.append([])

    def insertEdge(self, vertex1, vertex2, edge_):
        self.list_ngh[self.map_idx[vertex1]].append((self.map_idx[vertex2], edge_))  # czy hash map_inx[vertex1] jest równy hash zapisanego
        self.list_ngh[self.map_idx[vertex2]].append((self.map_idx[vertex1], edge_))
        self.list_ngh[self.map_idx[vertex1]] = list(set(self.list_ngh[self.map_idx[vertex1]]))
        self.list_ngh[self.map_idx[vertex2]] = list(set(self.list_ngh[self.map_idx[vertex2]]))

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
        temp_lst = [i[0] for i in self.list_ngh[v1]]
        self.list_ngh[v1].pop(temp_lst.index(v2))

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

    def edges(self):  # returns list of [index of node, index of node2, edge]
        edges = []

        for i in range(self.order()):
            for node in self.neighbours(i):
                edges.append((i, node[0], node[1]))
        return edges


class Edge:
    def __init__(self, cost=1):
        self.cost = cost

    def __repr__(self):
        return str(self.cost)

    def __gt__(self, other):
        return self.cost>other.cost

    def __lt__(self, other):
        return self.cost<other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __hash__(self):
        return hash(self.cost)

NeighList = TypeVar('NeighList', bound=ListGraph)


def MST(filename: str):
    I = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    x, y = I.shape
    tree = ListGraph()
    for i in range(x):
        for j in range(y):
            tree.insertVertex(Node(str(x * j + i), I[i][j]))
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            for i_n in range(i-1, i+2):
                for j_n in range(j-1, j+2):
                    if i != i_n or j != j_n:
                        tree.insertEdge(Node(str(x * j + i)), Node(str(x * j_n + i_n)), Edge(np.abs(I[i][j].astype(int) - I[i_n][j_n].astype(int))))

    mst_tree = prima(tree, 0)
    printGraph(tree)
    edges = mst_tree.edges()
    del_idx = edges.index(max(edges, key=lambda edge: edge[2].cost))
    mst_tree.deleteEdge(mst_tree.getVertex(edges[del_idx][0]), mst_tree.getVertex(edges[del_idx][1]))

    IS = np.zeros((x, y), dtype='uint8')
    mst_tree = searching(mst_tree, edges[del_idx][1], 150)
    mst_tree = searching(mst_tree, edges[del_idx][0], 30)

    for i in range(x):
        for j in range(y):
            IS[i][j] = mst_tree.getVertex(mst_tree.getVertexIdx(Node(str(x*j+i)))).bright

    plt.imshow(IS, 'gray',vmin=0, vmax=255)
    plt.show()

def searching(graph: NeighList, start_nde, color: int):  # start node is the index of node
    stack = [start_nde]
    visited = []
    while stack:
        start_node = stack.pop(-1)
        if start_node not in visited:
            visited.append(start_node)
            act_node: Node = graph.getVertex(start_node)
            neigh = [nodes[0] for nodes in graph.neighbours(start_node)]
            stack.extend(neigh)
            act_node.bright = color
    return graph





def prima(G: NeighList, start_node):
    intree = [0 for _ in range(G.order())]  # czy odwiedzony, indeksy oznaczają indeksy wierzchołków w G.nodes
    distance = [np.inf for _ in range(G.order())]
    parent = [-1 for _ in range(G.order())]
    v: int = start_node  # index wierzchołek
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
    return mst_tree


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


if __name__ == '__main__':
    MST('sample.png')

