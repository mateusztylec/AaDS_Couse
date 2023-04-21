#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time


class KopiecElem:
    def __init__(self, priority = None, data = None):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return bool(self.priority < other.priority)

    def __gt__(self, other):
        return bool(self.priority > other.priority)

    def __str__(self):
        result_str = "{" + str(self.priority) + " : " + str(self.data) + "}"
        return result_str


class PriorityQueue:
    def __init__(self, unsorted_tab = None):
        self.tab = []
        self.tab_size = 0
        self.elems_to_sort = unsorted_tab
        if unsorted_tab:
            self.heapify()

    def is_empty(self) -> bool:
        return not bool(self.tab)

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.tab[0]

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            peek_value = self.peek()
            self.tab[0], self.tab[self.tab_size-1] = self.tab[self.tab_size-1], self.tab[0]
            self.tab_size -= 1
            index = 0
            while True:
                right_child = self.right(index)
                left_child = self.left(index)
                if right_child >= self.tab_size or left_child >= self.tab_size:
                    return peek_value
                if self.tab[left_child] > self.tab[right_child]:
                    if self.tab[index] < self.tab[left_child]:
                        self.tab[index], self.tab[left_child] = self.tab[left_child], self.tab[index]
                        index = left_child
                    else:
                        break
                else:
                    if self.tab[index] < self.tab[right_child]:
                        self.tab[index], self.tab[right_child] = self.tab[right_child], self.tab[index]
                        index = right_child
                    else:
                        break

            return peek_value

    def enqueue(self, kopiec_elem):
        self.tab.append(kopiec_elem)
        self.tab_size += 1
        index = self.tab_size - 1
        if index != 0:
            while True:
                if index <= 1:
                    break
                i_parent = self.parent(index)
                if self.tab[i_parent] < self.tab[index]:
                    self.tab[i_parent], self.tab[index] = self.tab[index], self.tab[i_parent]
                else:
                    break
                if index == 1:
                    break
                index = i_parent

    def heapify(self):
        for elem in self.elems_to_sort:
            self.tab.append(elem)
            self.tab_size += 1

        not_leaf_index = self.parent(index=self.tab_size-1)
        for index in range(not_leaf_index, -1, -1):
            while True:
                right_child = self.right(index)
                left_child = self.left(index)
                if right_child >= self.tab_size or left_child >= self.tab_size:
                    break
                if self.tab[left_child] > self.tab[right_child]:
                    if self.tab[index] < self.tab[left_child]:
                        self.tab[index], self.tab[left_child] = self.tab[left_child], self.tab[index]
                        index = left_child
                    else:
                        break
                else:
                    if self.tab[index] < self.tab[right_child]:
                        self.tab[index], self.tab[right_child] = self.tab[right_child], self.tab[index]
                        index = right_child
                    else:
                        break

    def parent(self, index):
        return (index-1)//2

    def left(self, index):
        return 2*index+1

    def right(self, index):
        return 2*index+2

    def print_tab(self):
        tab_str: str = "{"
        for i in range(len(self.tab)):
            tab_str += str(self.tab[i]) + ', '
        if len(tab_str) >= 2:
            tab_str = tab_str[:-2]
        tab_str += '}'
        print(tab_str)

    def print_tree(self, idx, lvl):
        if idx < self.tab_size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.tab[idx] if self.tab[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

if __name__ == '__main__':
    tab = [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
    kopiec_tab = [KopiecElem(elem[0], elem[1]) for elem in tab]
    kopiec = PriorityQueue(kopiec_tab)
    kopiec.print_tree(0, 0)
    kopiec.print_tab()
    for i in range(len(tab)):
        kopiec.dequeue()
    kopiec.print_tab()

    rand_tab = [KopiecElem(int(random.random()*100)) for i in range(10000)]
    t_start = time.perf_counter()
    kopiec_rand = PriorityQueue(rand_tab)
    for i in range(10000):
        kopiec_rand.dequeue()
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
