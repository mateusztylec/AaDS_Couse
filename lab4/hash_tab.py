#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import Union, Optional


class TableException(BaseException):
    def __init__(self, mess: Optional[str] = None):
        if mess:
            super().__init__(mess)
        else:
            super().__init__()


class TabElem:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value


class Table:
    def __init__(self, tab_size: int, c1: int = 1, c2: int = 0) -> None:
        self.tab = [None for _ in range(tab_size)]
        self.tab_size = len(self.tab)
        self.c1 = c1
        self.c2 = c2

    def get_hash(self, key) -> int:
        if isinstance(key, str):
            sum_h = 0
            for i in key:
                sum_h += ord(i)
        elif isinstance(key, int) or isinstance(key, float):
            sum_h = key
        else:
            raise TableException("Wrong variable type")
        return sum_h % self.tab_size

    def colision_solver(self, index):
        for i in range(self.tab_size):
            temporary_index = index + self.c1*i + self.c2*(i**2)
            yield temporary_index % self.tab_size

    def search(self, key):
        index = self.get_hash(key)
        if isinstance(self.tab[index], TabElem):
            if self.tab[index].key == key:
                return self.tab[index].value
            else:
                for i in self.colision_solver(index):
                    if isinstance(self.tab[i], TabElem):
                        if self.tab[i].key == key:
                            return self.tab[i].value
                    else:
                        return None


    def insert(self, key, value):
        index: int = self.get_hash(key)
        if not self.tab[index]:
            self.tab[index] = TabElem(key, value)
        else:
            for i in self.colision_solver(index):
                if not self.tab[i]:
                    self.tab[i] = TabElem(key, value)
                    break
                elif isinstance(self.tab[i], TabElem):
                    if self.tab[i].key == key:
                        self.tab[i].value = value
                        break
            else:
                print("Brak miejsca")

    def __str__(self):
        result_str = "{"
        for i in self.tab:
            if not i:
                result_str += "None:None, "
            else:
                result_str += f'{i.key}:{i.value}, '
        result_str = result_str[:-2]
        result_str += "}"
        return result_str

    def remove(self, key):
        index = self.get_hash(key)
        if isinstance(self.tab[index], TabElem):
            if self.tab[index].key == key:
                self.tab[index] = None
            else:
                for i in self.colision_solver(key):
                    if self.tab[i] == key:
                        self.tab[i] = None
                        break
                    elif not self.tab[i]:
                        print("Brak danej")
                        break
        else:
            print("Brak danej")


def fun1(tab_size, c1, c2):
    table1 = Table(tab_size, c1, c2)
    for i in range(1, 16):
        if i == 6:
            table1.insert(18, chr(i+64))
        elif i == 7:
            table1.insert(31, chr(i+64))
        else:
            table1.insert(i, chr(i+64))
    print(table1)
    print(table1.search(5))
    print(table1.search(14))
    table1.insert(5, 'Z')
    print(table1.search(5))
    table1.remove(5)
    print(table1)
    print(table1.search(31))
    table1.insert('W', 'test')
    print(table1)


def fun2(tab_size, c1, c2):
    table1 = Table(tab_size, c1, c2)
    for i in range(1, 16):
        table1.insert(13*i, chr(i+64))
    print(table1)

if __name__ == '__main__':
    # fun1(13, 1, 0)
    fun2(13, 1, 0)
    fun2(13, 0, 1)
    fun1(13, 0, 1)

