#skończone
from typing import List, Tuple
import random
import time
import numpy as np

class Elem:
    def __init__(self, node: Tuple):
        self.data = node[1]
        self.number = node[0]

    def __gt__(self, other):
        return self.number > other.number

    def __lt__(self, other):
        return self.number < other.number

    def __str__(self):
        return "{" + f'{self.number} : {self.data}' + "}"


class Sorting:
    def __init__(self, list):
        self.list = list
        self.lst_length = len(self.list)

    def swap(self, index1: int, index2: int):
        self.list[index1], self.list[index2] = self.list[index2], self.list[index1]

    def sorting(self, method):
        min_val = self.list[0].number
        min_idx = 0
        for i in range(self.lst_length):
            for idx in range(i, self.lst_length):
                if self.list[idx].number < min_val:
                    min_val = self.list[idx].number
                    min_idx = idx
            if min_idx != i:
                if method == 'swap':
                    self.swap(i, min_idx)
                elif method == "shift":
                    self.shift(i, min_idx)
            min_val = np.inf
            min_idx = -1

    def shift(self, index1: int, index2: int):
        self.list.insert(index1, self.list.pop(index2))
        self.list.insert(index2, self.list.pop(index1+1))

    def print_out(self):
        tab_str: str = "{"
        for i in range(self.lst_length):
            tab_str += str(self.list[i]) + ', '
        if len(tab_str) >= 2:
            tab_str = tab_str[:-2]
        tab_str += '}'
        print(tab_str)


if __name__ == '__main__':
    lst = [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
    lst_elem = [Elem(i) for i in lst]
    lst_elem2 = [Elem(i) for i in lst]
    sorted_lst = Sorting(lst_elem)
    sorted_lst.sorting('swap')
    sorted_lst.print_out()
    sorted_lst2 = Sorting(lst_elem2)
    sorted_lst2.sorting('shift')
    sorted_lst2.print_out()

    rand_tab = [Elem((random.randint(0, 1000), 'a')) for i in range(10000)]
    t_start = time.perf_counter()
    sorted_lst3 = Sorting(rand_tab)
    sorted_lst3.sorting('swap')
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))