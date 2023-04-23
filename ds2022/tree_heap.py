class Empty(Exception):
    """Error attempting to access an element from an empty container."""
    pass

class TreeHeap:
    __slots__ = '_root', '_last', '_size'

    #-------------------- nonpublic
    class _Node:
        __slots__ = '_element', '_left', '_right', '_parent'
        def __init__(self, element, left, right, parent):
            self._element = element
            self._left = left
            self._right = right
            self._parent = parent
    
    def _swap(self, node1, node2):
        """Swap the elements at indices i and j of array."""
        n1_elem = node1._element
        node1._element = node2._element
        node2._element = n1_elem
    
    def _upheap(self, node):
        while(node._parent != None and node._element < node._parent._element):
            self._swap(node, node._parent)
            node = node._parent
        
    def _downheap(self, node):
        while(True):
            if(node._left == None and node._right == None):
                return
            elif(node._left == None):
                if(node._element > node._right._element):
                    self._swap(node, node._right)
                else:
                    return
            elif(node._right == None):
                if(node._element > node._left._element):
                    self._swap(node, node._left)
                else:
                    return
            elif(node._element <= node._left._element and node._element <= node._right._element):
                return
            else:
                if node._left._element <= node._right._element:
                    self._swap(node, node._left)
                    node = node._left
                else:
                    self._swap(node, node._right)
                    node = node._right

    #-------------------- public
    def __init__(self):
        """Create a new empty Priority Queue."""
        self._root = None
        self._last = None
        self._size = 0

    def __len__(self):
        """Return the number of items in the priority queue."""
        return self._size

    def is_empty(self):
        return self._size == 0

    def add(self, key):
        """Add a key to the priority queue."""
        if self.is_empty():
            self._root = self._last = self._Node(key, None, None, None)
            self._size += 1
            return

        pointer = self._last
        while(True):
            if pointer == self._root:
                break
            elif(pointer == pointer._parent._left):
                pointer = pointer._parent
                if(pointer._right == None):
                    pointer._right = self._Node(key, None, None, pointer)
                    self._last = pointer._right
                    self._size += 1
                    self._upheap(self._last)
                    return
                pointer = pointer._right
                break
            else:
                pointer = pointer._parent
        while(pointer._left != None):
            pointer = pointer._left
        pointer._left = self._Node(key, None, None, pointer)

        self._last = pointer._left
        self._size += 1
        self._upheap(self._last)
        return

    def min(self):
        """Return but do not remove (k,v) tuple with minimum key.
        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty('Heap is empty')
        return self._root._element
    
    def remove_min(self):
        """Remove and return the minimum key.
        Raise Empty exception if empty.
        """
        if(self.is_empty()):
            raise Empty('Heap is empty')
        if(self._last == self._root):
            minval = self._root._element
            self._root = self._last = None
            self._size -= 1
            return minval
        minval = self._root._element
        self._swap(self._root, self._last)

        pointer = self._last
        while(True):
            if pointer == self._root:
                break
            elif(pointer == pointer._parent._right):
                pointer = pointer._parent._left
                break
            else:
                pointer = pointer._parent
        while(pointer._right != None):
            pointer = pointer._right

        if(self._last == self._last._parent._right):
            self._last._parent._right = None
        else:
            self._last._parent._left = None

        self._last = pointer
        self._downheap(self._root)
        self._size -= 1
        return minval

    def display(self):
        self._display(self._root, 0)

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            self._display(node._right, depth+1)
        label = ''
        if node == self._root:
            label += '  <- root'
        if node == self._last:
            label += '  <- last'
        print(f'{"    "*depth}* {node._element}{label}')
        if node._left != None:
            self._display(node._left, depth+1)
