#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import List, Tuple, TypeVar
import random
import time
from math import log
import numpy as np

class Elem:
    def __init__(self, node: Tuple):
        self.number = node[0]
        self.data = node[1]

    def __str__(self):
        return "{" + f'{self.number} : {self.data}' + "}"

    def __gt__(self, other):
        return self.number > other.number

    def __lt__(self, other):
        return self.number < other.number



class Sorting:
    def __init__(self, list):
        self.list = list
        self.lst_length = len(self.list)

    def swap(self, index1: int, index2: int):
        self.list[index1], self.list[index2] = self.list[index2], self.list[index1]

    def sorting(self):
        k = int(log(2*(self.lst_length//3)+1, 3))
        h = (3**k-1)//2
        while h != 0:
            for idx in range(self.lst_length-h):
                if self.list[idx] > self.list[idx+h]:
                    self.swap(idx, idx+h)
                    for i in range(idx-h,-1,-h):
                        if self.list[i+h]<self.list[i]:
                            self.swap(i, i+h)
                        else:
                            break
            k -= 1
            h = (3**k-1)//2

    def print_out(self):
        tab_str: str = "{"
        for i in range(self.lst_length):
            tab_str += str(self.list[i]) + ', '
        if len(tab_str) >= 2:
            tab_str = tab_str[:-2]
        tab_str += '}'
        print(tab_str)


if __name__ == '__main__':
    rand_tab = [Elem((random.randint(0, 99), 'a')) for i in range(10000)]
    sorted_lst3 = Sorting(rand_tab)
    t_start = time.perf_counter()
    sorted_lst3.sorting()
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))