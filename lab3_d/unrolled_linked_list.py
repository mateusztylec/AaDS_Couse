import math
max_node_capacity = 16

class Node:
    def __init__(self):
        self.arr = []
        self.arr_size = 0
        self.next = None



class UnrolledLinkedList:
    def __init__(self):
        self.head = None


    def __delitem__(self, index):
        if index < 0:
            absIndex = self.length + index
        else:
            absIndex = index

        if index > self.length - 1:  # Over the max
            raise IndexError(str(index) + ' out of range.')
        elif absIndex < 0:  # Below 0
            raise IndexError(str(index) + 'out of range.')

        # We now have a valid index.
        currentNode = self.head
        currentIndex = 0
        # Iterate until the right node is found.
        while len(currentNode.arr) - 1 + currentIndex < absIndex:
            currentIndex = currentIndex + len(currentNode.arr)
            currentNode = currentNode.next

        # We have the right node, time to get the item from the array.
        arrIndex = absIndex - currentIndex
        del currentNode.arr[arrIndex]  # Delete the data at the final index
        self.length = self.length - 1

        # Rebalance the list if the current node's array 
        # fell below half of max_node_capacity.
        nextNode = currentNode.next
        while nextNode:
            # Move over enough data to fill back up the current node
            if len(currentNode.arr) < self.max_node_capacity // 2 and nextNode is not None:
                numberToTransfer = self.max_node_capacity // 2 - len(currentNode.arr) + 1
                currentNode.arr = currentNode.arr + nextNode.arr[:numberToTransfer]
                nextNode.arr = nextNode.arr[numberToTransfer:]

                # If the next node has dwindled in unbelief, give him a pick me up
                if len(nextNode.arr) < self.max_node_capacity // 2:
                    # Merge the nodes
                    currentNode.arr = currentNode.arr + nextNode.arr
                    currentNode.next = nextNode.next
                    del nextNode
            currentNode = currentNode.next
            if currentNode:
                nextNode = currentNode.next
            else:
                nextNode = None

    """Returns the item in the given index.
    If the index is negative, return with the index starting from the back 
    (i.e. getting at -1 returns the last item)
    If the index is too large, raise an IndexError"""

    def __getitem__(self, index):
        if index < 0:
            absIndex = self.length + index
        else:
            absIndex = index

        if index > self.length - 1:  # Over the max
            raise IndexError(str(index) + ' out of range.')
        elif absIndex < 0:  # Below 0
            raise IndexError(str(index) + 'out of range.')

        currentNode = self.head
        currentIndex = 0
        # Iterate until the right node is found.
        while len(currentNode.arr) - 1 + currentIndex < absIndex:
            currentIndex = currentIndex + len(currentNode.arr)
            currentNode = currentNode.next

        # We have the right node, time to get the item from the array.
        arrIndex = absIndex - currentIndex
        return currentNode.arr[arrIndex]  # Delete the data at the final index

    '''Sets the item at key to value
    If the key is too large, raise an IndexError'''

    def __setitem__(self, key, value):
        index = key
        current_node = self.head
        current_index = 0

        while current_node.arr_size - 1 + current_index < index:
            current_index = current_index + len(current_node.arr)
            current_node = current_node.next

        proper_index = index - current_index
        current_node.arr[proper_index] = value

    '''Use the Python yield statement to make your list iterable. 
    This will allow you to use it in a for-each loop'''

    def __iter__(self):
        current = self.head
        while current is not None:
            for x in current.arr:
                yield x
            current = current.next

    '''Create a string representation of the list in the form 
    {[x, x, x], [x, x], [x, x, x, x]} where each set of [] indicates
    the list of values within a single node.'''

    def __str__(self):
        if self.length == 0:
            return '{}'

        result = '{'
        current = self.head
        while current is not None:
            result = result + '['
            for i in range(0, len(current.arr)):
                result = result + str(current.arr[i])
                if i + 1 < len(current.arr):
                    result = result + ', '
            result = result + ']'
            if current.next is not None:
                result = result + ', '
            current = current.next
        result = result + '}'
        return result

    '''returns the total # of data in the list, not the 
    number of nodes'''

    def __len__(self):
        return self.length

    '''Add the data to the end of the list
    If a node has reached its max capacity, 
    you must create a new node to put the data in'''

    def append(self, data):
        if self.head is None:
            self.head = Node()
            self.head.arr.append(data)
            self.tail = self.head
        elif len(self.tail.arr) < self.max_node_capacity:
            self.tail.arr.append(data)
        else:
            newNode = Node()
            middle = len(self.tail.arr) // 2
            newNode.arr = self.tail.arr[middle * -1:]
            self.tail.arr = self.tail.arr[:middle * -1]
            self.tail.next = newNode
            self.tail = newNode
            self.tail.arr.append(data)

        self.length = self.length + 1