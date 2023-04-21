#!/usr/bin/python
# -*- coding: utf-8 -*-

class Root:
    def __init__(self) -> None:
        self.root = None

    def insert(self, key, value, node):
        if node is None:
            return NodeData(key, value)

        if key < node.key:
            node.left_node = self.insert(key, value, node.left_node)
            return node
        elif key > node.key:
            node.right_node = self.insert(key, value, node.right_node)
            return node
        else:
            node.value = value
            return node

    def search(self, key, node):
        if not node:
            return None
        elif node.key == key:
            return node.value

        if key > node.key:
            return self.search(key, node.right_node)
        elif key < node.key:
            return self.search(key, node.left_node)

    def min_node(self, node):
        if node.left_node:
            return self.min_node(node.left_node)
        else:
            return node

    def delete(self, key, node):
        if self.root is None:
            return None
        if key < node.key:
            if node.left_node:
                node.left_node = self.delete(key, node.left_node)

        elif key > node.key:
            if node.right_node:
                node.right_node = self.delete(key, node.right_node)

        else:
            if node.left_node is None and node.right_node is None:
                return None
            if node.left_node is None:
                return node.right_node
            if node.right_node is None:
                return node.left_node

            min_node = self.min_node(node.right_node)
            node.value = min_node.value
            node.key = min_node.key
            node.right_node = self.delete(min_node.key, node.right_node)
        return node

    def height(self, node):
        if node is None:
            return -1
        l_depth = self.height(node.left_node)
        r_depth = self.height(node.right_node)

        if l_depth>r_depth:
            return l_depth+1
        else:
            return r_depth+1

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right_node, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self._print_tree(node.left_node, lvl + 5)

    def sorted_list(self, node):
        if node is None:
            return ""
        result = self.sorted_list(node.left_node)
        result += f' {node.key}:{node.value} '
        result += self.sorted_list(node.right_node)
        return result

class NodeData:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.right_node = None
        self.left_node = None


if __name__ == '__main__':
    bst1 = Root()
    keys = [50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24]
    for value, key in enumerate(keys):
        bst1.root = bst1.insert(key, chr(ord('A')+value), bst1.root)
    bst1.print_tree()
    print(bst1.sorted_list(bst1.root))
    print(bst1.search(24, bst1.root))
    bst1.insert(20, 'AA', bst1.root)
    bst1.insert(6, 'M', bst1.root)
    bst1.delete(62, bst1.root)
    bst1.insert(59, 'N', bst1.root)
    bst1.insert(100, 'P', bst1.root)
    bst1.delete(8, bst1.root)
    bst1.delete(15, bst1.root)
    bst1.insert(55, 'R', bst1.root)
    bst1.delete(50, bst1.root)
    bst1.delete(5, bst1.root)
    bst1.delete(24, bst1.root)
    print(bst1.height(bst1.root))
    print(bst1.sorted_list(bst1.root))
    bst1.print_tree()
