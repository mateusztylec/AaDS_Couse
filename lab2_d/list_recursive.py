#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import Tuple, List, Union, Dict

NodeValue = Union[List, Tuple, Dict]


class Node:
    def __init__(self, value: Tuple, next=None):
        self.value = value
        self.next = next


def nil() -> List:
    return []


def cons(el, list):
    return Node(el, list)


def first(list):
    if is_empty(list):
        raise UserWarning("Lista jest pusta")
    else:
        return list.value


def rest(list):
    if is_empty(list):
        raise UserWarning("Lista jest pusta")
    elif list.next is []:
        raise UserWarning("Lista zawiera tylko jeden element")
    return list.next


def is_empty(lst):
    return True if lst == [] else False


def add_end(el, lst):
    if is_empty(lst):
        return cons(el, lst)  # dojście do końca i wstawienie tam elementu
    else:
        first_el = first(lst)  # podział listy na: pierwszy element
        rest_lst = rest(lst)  # i całą resztę
        recreated_lst = add_end(el, rest_lst)  # 'zejście 'w dół' rekurencji z
        # przekazaniem dodawanego elementu, przy powrocie 'w górę' zwracana jest
        # odtworzona lista
        return cons(first_el, recreated_lst)  # cons dołącza pierwszy element do
        # 'odtwarzanej' przez rekurencję listy
        # zmienne first-el, rest_lst i recreated_lst są wprowadzone pomocniczo,
        # dla wyjaśnienia działania funkcji


def remove_end(list):
    first_el = first(list)
    rest_lst = rest(list)
    if is_empty(rest_lst):
        return nil()
    temp_list = remove_end(rest_lst)
    return cons(first_el, temp_list)


def create():
    return nil()


def destroy():
    list = nil()
    return list


def add(el, list):
    return cons(el, list)


def remove(list):
    return rest(list)


def length(list) -> int:
    n: int = 1
    if is_empty(list):
        return 0
    rest_lst = rest(list)
    n += length(rest_lst)
    return n


def take(list, n: int):
    if is_empty(list) or n == 0:
        return nil()
    first_el = first(list)
    rest_lst = rest(list)
    temp_list = take(rest_lst, n-1)
    return cons(first_el, temp_list)


def drop(list, n: int):
    rest_lst = rest(list)
    if is_empty(list) or n == 0:
        return rest_lst
    return drop(list, n-1)


def get(list):
    return first(list)


def list_as_str(list, lst_str=''):
    if is_empty(list):
        return lst_str
    lst_str += str(first(list))
    lst_str += " -> "
    rest_lst = rest(list)
    return list_as_str(rest_lst, lst_str)




if __name__ == '__main__':
    lst_3 = create()
    lst_3 = add(("kot", 2), lst_3)
    lst_3 = add(("pies", 1), lst_3)
    lst_3 = add_end(("ryba", 3), lst_3)
    lst_3 = add_end(("ptak", 4), lst_3)
    lst_3 = add_end(("slon", 5), lst_3)

    print("\nLista")
    print(list_as_str(lst_3))

    lst_3 = take(lst_3, 4)
    lst_3 = drop(lst_3, 1)

    print("\nLista")
    print(list_as_str(lst_3))

    print(f"\nDługość listy: {length(lst_3)}")

    print(f"\nGet: {get(lst_3)}")

    lst_3 = remove(lst_3)
    lst_3 = remove_end(lst_3)
    print("\nLista")
    print(list_as_str(lst_3))