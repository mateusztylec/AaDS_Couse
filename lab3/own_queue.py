#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import Optional, List

class QueueOwn:
    def __init__(self) -> None:
        self.tab = [None] * 5
        self.tab_size: int = 5
        self.save_index: int = 0
        self.read_index: int = 0

    def is_empty(self) -> bool:
        return self.read_index == self.save_index

    def peek(self) -> Optional[int]:
        if self.is_empty():
            return None
        else:
            return self.tab[self.read_index]

    def realloc(self, size: int) -> None:
        temp_tab = [None] * size
        temp_tab[self.tab_size] = self.tab[self.read_index]
        self.read_index += 1
        for i in range(1, self.tab_size):
            temp_tab[self.tab_size+i] = self.dequeue()
        self.tab = temp_tab
        self.save_index = 0
        self.read_index = size - self.tab_size
        self.tab_size = size

    def dequeue(self) -> Optional[int]:
        if self.is_empty():
            return None
        else:
            if self.read_index < self.tab_size:
                return_value = self.peek()
                self.read_index += 1
                if self.read_index == self.tab_size:
                    self.read_index = 0
            else:
                self.read_index = 0
                return_value = self.peek()
                self.read_index += 1
            return return_value

    def enqueue(self, data) -> None:
        self.tab[self.save_index] = data
        if self.save_index >= self.tab_size-1:
            self.save_index = 0
        else:
            self.save_index += 1

        if self.is_empty():
            self.realloc(self.tab_size*2)

    def tab_str(self) -> str:
        return str(self.tab)

    def queue_str(self) -> str:
        que_list: List = []
        temporary_read_index: int = self.read_index
        temporary_save_index: int = self.save_index
        while self.peek():
            que_list.append(self.dequeue())
        self.read_index = temporary_read_index
        self.save_index = temporary_save_index
        return str(que_list)


if __name__ == '__main__':
    que1 = QueueOwn()
    que1.enqueue(1)
    que1.enqueue(2)
    que1.enqueue(3)
    que1.enqueue(4)
    print(f'dequeue: {que1.dequeue()}')
    print(f'peek: {que1.peek()}')
    print(f'kolejka: {que1.queue_str()}')
    que1.enqueue(5)
    que1.enqueue(6)
    que1.enqueue(7)
    que1.enqueue(8)
    print(f'tablica: {que1.tab_str()}')
    while que1.peek():
        print(que1.dequeue())
    print(f'kolejka: {que1.queue_str()}')
