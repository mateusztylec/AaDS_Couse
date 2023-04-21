#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import Tuple


class LinedList:
    def __init__(self):
        self.head = None

    def destroy(self) -> None:
        self.head = None

    def add(self, val: Tuple) -> None:
        n = Node(val, self.head)
        self.head = n

    def remove(self) -> None:
        itr = self.head
        itr = itr.next
        self.head = itr

    def is_empty(self) -> bool:
        return self.head is None

    @property
    def get(self) -> Tuple:
        itr = self.head
        return itr.value

    def __str__(self) -> str:
        llstr = ''
        itr = self.head
        while itr:
            llstr += str(itr.value)
            llstr += "->"
            itr = itr.next
        return llstr

    def length(self) -> int:
        size = 0
        itr = self.head
        while itr:
            itr = itr.next
            size += 1
        return size

    def add_at_the_end(self, value) -> None:
        if self.is_empty():
            n = Node(value)
            self.head = n
        else:
            itr = self.head
            itr_2 = itr
            while itr:
                itr_2 = itr
                itr = itr.next
            n = Node(value)
            itr_2.next = n

    def remove_from_the_end(self) -> None:
        itr = self.head
        itr_2 = itr
        itr_3 = itr_2
        while itr:
            itr_3 = itr_2
            itr_2 = itr
            itr = itr.next
        itr_3.next = None

    def take(self, n: int):
        new_ll = LinedList()
        itr = self.head
        length = self.length()
        if n <= length:
            for i in range(n):
                new_ll.add_at_the_end(itr.value)
                itr = itr.next
        else:
            for i in range(length):
                new_ll.add_at_the_end(itr.value)
                itr = itr.next
        return new_ll

    def drop(self, n: int):
        length = self.length()
        new_ll = LinedList()
        if n >= length:
            return new_ll
        itr = self.head
        for i in range(n):
            itr = itr.next
        for i in range(length-n):
            new_ll.add_at_the_end(itr.value)
            itr = itr.next
        return new_ll


class Node:
    def __init__(self, value: Tuple, next=None):
        self.value = value
        self.next = next


if __name__ == '__main__':
    var1 = LinedList()
    print(f'\nCzy lista jest pusta? - {var1.is_empty()}')
    var1.add(('AGH', 'Krakow', 1919))
    var1.add(('UJ', 'krakow', 1364))
    var1.add_at_the_end(('PW', 'Warszawa', 1915))
    var1.add_at_the_end(('UW', 'Warszawa', 1915))
    var1.add_at_the_end(('UP', 'Poznań', 1919))
    print()
    print(var1)
    print("\nDługośc listy")
    print(var1.length())
    var1.remove()
    print("\nUsunięcie elementu z początku listy")
    print(var1)
    print("\nMetoda get: ")
    print(var1.get)
    print("\nDodanie elementu na koniec")
    var1.add_at_the_end(('PG', 'Gdańsk', 1945))
    print(var1)
    print("\nUsunięcie elementu z końca")
    var1.remove_from_the_end()
    print(var1)
    print("\nStworzenie nowej listy z 3 pierwszymi elementami")
    var2 = var1.take(3)
    print(var2)
    print("\nStworzenie nowej listy z 50 pierwszymi elementami")
    var3 = var1.take(50)
    print(var3)
    print("\nStworzenie nowej listy z pominięciem 2 elementów")
    var4 = var1.drop(2)
    print(var4)

