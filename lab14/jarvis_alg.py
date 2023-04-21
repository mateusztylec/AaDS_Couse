#!/usr/bin/python
# -*- coding: utf-8 -*-

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Jarvis:
    def __init__(self, points):
        self.points = points
        self.amount_of_points = len(self.points)
        self.temp_points = points
        self.path = []

    def algorithm(self):
        p = self.points[0]
        for anoth_node in self.points:
            if p.x > anoth_node.x:
                p = anoth_node
            if p.x == anoth_node.x:
                if p.y > anoth_node.y:
                    p = anoth_node

        self.temp_points.remove(p)
        start_node = p
        self.path.append(p)

        q = self.temp_points[0]
        for r in self.temp_points:
            if r == q:
                continue
            else:
                if angel(p, q, r) > 0:
                    q = r
                if angel(p, q, r) == 0:
                    r_distance = (r.x-p.x)**2+(r.y-p.y)**2
                    q_distance = (q.x-p.x)**2+(q.y-p.y)**2
                    if r_distance < q_distance:
                        q = r
        self.path.append(q)
        p = q
        self.temp_points.remove(p)
        self.temp_points.append(start_node)

        while p != start_node:
            q = self.temp_points[0]
            for r in self.temp_points:
                if r == q:
                    continue
                else:
                    if angel(p, q, r) > 0:
                        q = r
                    if angel(p, q, r) == 0:
                        r_distance = (r.x - p.x) ** 2 + (r.y - p.y) ** 2
                        q_distance = (q.x - p.x) ** 2 + (q.y - p.y) ** 2
                        if r_distance > q_distance:
                            q = r
            self.path.append(q)
            p = q
            self.temp_points.remove(p)

        return self.path


def angel(point1, point2, point3):
    return (point2.y - point1.y) * (point3.x - point2.x) - (point3.y - point2.y) * (point2.x - point1.x)


if __name__ == "__main__":
    points1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
    points2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
    points3 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
    points_lst = []
    for i in points3:
        points_lst.append(Point(i[0], i[1]))
    alg = Jarvis(points_lst)
    print(alg.algorithm())
