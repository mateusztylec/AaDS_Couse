#!/usr/bin/python
# -*- coding: utf-8 -*-
import time


def string_compare_recurion(P, T, i, j):
    if i == 0:
        return j
    if j == 0:
        return i
    zamian = string_compare_recurion(P, T, i - 1, j - 1) + (P[i] != T[j])
    wstawień = string_compare_recurion(P, T, i, j - 1) + 1
    usunięć = string_compare_recurion(P, T, i - 1, j) + 1

    najniższy_koszt = min(zamian, wstawień, usunięć)

    return najniższy_koszt


def string_compare_pd(P, T):
    D = [[0 for _ in range(len(T))] for _ in range(len(P))]
    D[0] = list(range(len(T)))
    for i in range(len(P)):
        D[i][0] = i

    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    parent[0] = ['I' for _ in range(len(T))]
    for i in range(len(P)):
        parent[i][0] = 'D'
    parent[0][0] = 'X'

    for i in range(1, len(P)):
        for j in range(1, len(T)):
            zamian = D[i - 1][j - 1] + (P[i] != T[j])
            wstawień = D[i][j - 1] + 1
            usunięć = D[i - 1][j] + 1
            D[i][j] = min(zamian, wstawień, usunięć)
            if zamian == min(zamian, wstawień, usunięć):
                if P[i] == T[j]:
                    parent[i][j] = 'M'
                else:
                    parent[i][j] = 'S'
            elif wstawień == min(zamian, wstawień, usunięć):
                parent[i][j] = 'I'
            else:
                parent[i][j] = 'D'

    return D[-1][-1], parent


def string_compare_path(P, T):
    _, parent = string_compare_pd(P, T)
    i = len(parent) - 1
    j = len(parent[0]) - 1
    path = ""
    decision = parent[i][i]
    while decision != 'X':
        path += decision
        if decision == 'M' or decision == 'S':
            i -= 1
            j -= 1
        elif decision == 'D':
            i -= 1
        elif decision == 'I':
            j -= 1
        decision = parent[i][j]

    return path[::-1]


def string_compare_d(P, T):
    D = [[0 for _ in range(len(T))] for _ in range(len(P))]
    for i in range(len(P)):
        D[i][0] = i

    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    for i in range(len(P)):
        parent[i][0] = 'D'
    parent[0][0] = 'X'

    for i in range(1, len(P)):
        for j in range(1, len(T)):
            zamian = D[i - 1][j - 1] + (P[i] != T[j])
            wstawień = D[i][j - 1] + 1
            usunięć = D[i - 1][j] + 1
            D[i][j] = min(zamian, wstawień, usunięć)
            if zamian == min(zamian, wstawień, usunięć):
                if P[i] == T[j]:
                    parent[i][j] = 'M'
                else:
                    parent[i][j] = 'S'
            elif wstawień == min(zamian, wstawień, usunięć):
                parent[i][j] = 'I'
            else:
                parent[i][j] = 'D'

    i = len(P) - 1
    j = 0
    for k in range(1, len(T)):
        if D[i][k] < D[i][j]:
            j = k
    return j - len(P) + 2


def string_compare_e(P, T):
    D = [[0 for _ in range(len(T))] for _ in range(len(P))]
    D[0] = list(range(len(T)))
    for i in range(len(P)):
        D[i][0] = i

    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    parent[0] = ['I' for _ in range(len(T))]
    for i in range(len(P)):
        parent[i][0] = 'D'
    parent[0][0] = 'X'

    for i in range(1, len(P)):
        for j in range(1, len(T)):
            if P[i] != T[j]:
                zamian = D[i - 1][j - 1] + 99
            else:
                zamian = D[i - 1][j - 1]
            wstawień = D[i][j - 1] + 1
            usunięć = D[i - 1][j] + 1
            D[i][j] = min(zamian, wstawień, usunięć)
            if zamian == min(zamian, wstawień, usunięć):
                if P[i] == T[j]:
                    parent[i][j] = 'M'
                else:
                    parent[i][j] = 'S'
            elif wstawień == min(zamian, wstawień, usunięć):
                parent[i][j] = 'I'
            else:
                parent[i][j] = 'D'

    i = len(parent) - 1
    j = len(parent[0]) - 1
    path = ""
    decision = parent[i][i]
    while decision != 'X':
        if decision == 'M':
            path += T[j]
            i -= 1
            j -= 1
        elif decision == 'S':
            i -= 1
            j -= 1
        elif decision == 'D':
            i -= 1
        elif decision == 'I':
            j -= 1
        decision = parent[i][j]

    return path[::-1]  # M sie liczy


def string_compare_f(P, T):
    D = [[0 for _ in range(len(T))] for _ in range(len(P))]
    D[0] = list(range(len(T)))
    for i in range(len(P)):
        D[i][0] = i

    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    parent[0] = ['I' for _ in range(len(T))]
    for i in range(len(P)):
        parent[i][0] = 'D'
    parent[0][0] = 'X'

    for i in range(1, len(P)):
        for j in range(1, len(T)):
            if P[i] != T[j]:
                zamian = D[i - 1][j - 1] + 99
            else:
                zamian = D[i - 1][j - 1]
            wstawień = D[i][j - 1] + 1
            usunięć = D[i - 1][j] + 1
            D[i][j] = min(zamian, wstawień, usunięć)
            if zamian == min(zamian, wstawień, usunięć):
                if P[i] == T[j]:
                    parent[i][j] = 'M'
                else:
                    parent[i][j] = 'S'
            elif wstawień == min(zamian, wstawień, usunięć):
                parent[i][j] = 'I'
            else:
                parent[i][j] = 'D'

    i = len(parent) - 1
    j = len(parent[0]) - 1
    path = ""
    decision = parent[i][i]
    while decision != 'X':
        if decision == 'M':
            path += T[j]
            i -= 1
            j -= 1
        elif decision == 'S':
            i -= 1
            j -= 1
        elif decision == 'D':
            i -= 1
        elif decision == 'I':
            j -= 1
        decision = parent[i][j]

    return path[::-1]  # M sie liczy


if __name__ == "__main__":
    P = ' kot'
    T = ' pies'
    print(string_compare_recurion(P, T, len(P) - 1, len(T) - 1))

    P = ' biały autobus'
    T = ' czarny autokar'
    print(f'{string_compare_pd(P, T)[0]}')

    P = ' thou shalt not'
    T = ' you should not'
    print(string_compare_path(P, T))

    P = ' ban'
    T = ' mokeyssbanana'
    print(string_compare_d(P, T))

    P = ' democrat'
    T = ' republican'
    print(string_compare_e(P, T))

    P = ' 123456789'
    T = ' 243517698'
    print(string_compare_f(P, T))
