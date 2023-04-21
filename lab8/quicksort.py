#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from copy import copy
import time

def quicksort_inplace(lst2, start, stop):
    i = start
    j = stop
    pivot = divider(lst2[start:stop])
    while i < j:
        while lst2[i] < pivot:
            i += 1
        while lst2[j] > pivot:
            j -= 1
        if i <= j:
            lst2[i], lst2[j] = lst2[j], lst2[i]
            i += 1
            j -= 1
    if start < j:
        quicksort_inplace(lst2, start, j)
    if i < stop:
        quicksort_inplace(lst2, i, stop)


def quicksort(lst):
    lst2 = copy(lst)
    quicksort_inplace(lst2, 0, len(lst2)-1)
    return lst2

def divider(lst):
    if len(lst) == 1:
        return lst[0]
    else:
        median_lst = []
        for i in range(0, len(lst), 5):
            if len(lst[i:i+5]) == 5:
                median_lst.append(median_5(lst[i], lst[i+1], lst[i+2], lst[i+3], lst[i+4]))
            elif len(lst[i:i+5]) == 4:
                median_lst.append(median_4(lst[i], lst[i+1], lst[i+2], lst[i+3]))
            elif len(lst[i:i+5]) == 3:
                median_lst.append(median_3(lst[i], lst[i+1], lst[i+2]))
            elif len(lst[i:i+5]) == 2:
                median_lst.append(lst[i])
            elif len(lst[i:i+5]) == 1:
                median_lst.append(lst[i])
        return divider(median_lst)

def median_3(a, b, c):
    return max(min(a, b), min(c, max(a, b)))

def median_4(a, b, c, d):
    return max(min(a, b), min(c, d))

def median_5(a, b, c, d, e):
    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4
    return median_3(e, f, g)


if __name__ == "__main__":
    tab = [random.randint(0, 99) for _ in range(10000)]
    t_start = time.perf_counter()
    quicksort(tab)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


