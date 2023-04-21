#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import copy

class KopiecElem:
    def __init__(self, data = None, priority = None):
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
    def __init__(self):
        self.tab = []
        self.tab_size = 0

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
            del self.tab[self.tab_size-1]
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

    def enqueue(self, data, priority):
        self.tab.append(KopiecElem(data, priority))
        self.tab_size += 1
        index = self.tab_size - 1
        if index != 0:
            while True:
                i_parent = self.parent(index)
                if self.tab[i_parent] < self.tab[index]:
                    self.tab[i_parent], self.tab[index] = self.tab[index], self.tab[i_parent]
                else:
                    break
                if index == 1:
                    break
                index = i_parent

    def parent(self, index):
        return (index-1)//2

    def left(self, index):
        return 2*index+1

    def right(self, index):
        return 2*index+2

    def print_tab(self):
        tab_str: str = "{"
        for i in range(self.tab_size):
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
    pri_que = PriorityQueue()
    list_pri: list = [4, 7, 6, 7, 5, 2, 2, 1]
    str_data: str = "ALGORYTM"
    for i in range(len(list_pri)):
        pri_que.enqueue(str_data[i], list_pri[i])
    pri_que.print_tree(0, 0)
    pri_que.print_tab()
    print(pri_que.dequeue())
    print(pri_que.peek())
    pri_que.print_tab()
    while pri_que.peek():
        print(pri_que.dequeue())
    pri_que.print_tab()