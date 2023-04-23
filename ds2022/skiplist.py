from collections import MutableMapping
import math, random

class KeyError(Exception):
    """Error attempting to access an element which does not exist."""
    pass

class SkipList(MutableMapping):
    # add additional slots as you need
    __slots__ = '_head', '_tail', '_n', '_height'

    #------------------------------- nested _Node class -------------------------------
    class _Node:
        __slots__ = '_key', '_value', '_prev', '_next', '_below', '_above'

        """Lightweight composite to store key-value pairs as map items."""
        def __init__(self, k, v, prev=None, next=None, below=None, above=None):
            self._key = k
            self._value = v
            self._prev = prev
            self._next = next
            self._below = below
            self._above = above

        def __eq__(self, other):               
            if other == None:
                return False
            return self._key == other._key   # compare items based on their keys

        def __ne__(self, other):
            return not (self == other)       # opposite of __eq__

        def __lt__(self, other):               
            return self._key < other._key    # compare items based on their keys

    def __init__(self):
        """Create an empty map."""
        self._head = self._Node(-math.inf, None, None, None, None, None)   # Head: the first node in a skip list
        self._tail = self._Node(math.inf, None, None, None, None, None)    # Tail: the last node in a skip list
        self._head._next = self._tail         # Initially, there's no item -> head is directly linked to the tail
        self._tail._prev = self._head
        self._n = 0                              # Initially, there's no item, so _n = 0
        self._height = 1                        # initially, height of skip list = 1
  
    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        ptr = self._head
        while (ptr != self._tail):
            if (k == ptr._next._key):
                return ptr._next._value
            elif (k > ptr._next._key):
                ptr = ptr._next
            elif (k < ptr._next._key and ptr._below != None):
                ptr = ptr._below
            elif(ptr._below == None):
                raise KeyError('key not found')

        # if it reached tail without finding, there is no key
        raise KeyError('key not found')
   
    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        ptr = self._head
        found_flag = False
        while (ptr != self._tail):
            if (k == ptr._next._key):
                ptr = ptr._next     # found ptr to change the value
                found_flag = True
                break
            elif (k > ptr._next._key):
                ptr = ptr._next
            elif (k < ptr._next._key and ptr._below != None):
                ptr = ptr._below
            elif(ptr._below == None):
                found_flag = False
                break
        
        if (found_flag == False):

            newnode = None
            newkey_height = 1
            while(True):
                if(ptr is self._head):  # add ceiling!
                    self._head = self._Node(-math.inf, None, None, None, ptr, None)
                    ptr._above = self._head

                    temp = self._Node(math.inf, None, self._head, None, ptr._next, None)
                    ptr._next._above = temp
                    self._head._next = temp

                # insert new node
                nextnode = ptr._next
                if(newkey_height == 1):
                    newnode = self._Node(k, v, ptr, nextnode, None, None)
                else:
                    belownode = newnode
                    newnode = self._Node(k, v, ptr, nextnode, belownode, None)
                    belownode._above = newnode
                nextnode._prev = newnode
                ptr._next = newnode

                # reset ptr to next floor
                while(ptr._above == None):
                    ptr = ptr._prev
                ptr = ptr._above
                
                # flip coin!
                if(random.choice([True, False])):
                    newkey_height += 1
                    continue
                else:
                    break
            # print("coin wins: ", newkey_height)
            self._height = max(self._height, newkey_height+1)
            self._n += 1

        else:
            while ptr._below != None:   # reach to bottom
                ptr = ptr._below
            while ptr != None:   # reset all above
                ptr._value = v
                ptr = ptr._above
        return
        
        
    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        ptr = self._head
        found_flag = False
        while (ptr != self._tail):
            if (k == ptr._next._key):
                found_flag = True
                ptr = ptr._next
                break
            elif (k > ptr._next._key):
                ptr = ptr._next
            elif (k < ptr._next._key and ptr._below != None):
                ptr = ptr._below
            elif(ptr._below == None):
                raise KeyError('key not found')

        # if it reached tail without finding, there is no key
        if not found_flag:
            raise KeyError('key not found')

        while ptr._below != None:   # reach to bottom
            ptr = ptr._below
        while ptr != None:   # delete all above
            ptr._prev._next = ptr._next
            ptr._next._prev = ptr._prev
            ptr = ptr._above
        
        # if there are bunch of ceilings, only leave 1
        while(self._head._below != None and self._head._below._next._value == math.inf):
            self._head = self._head._below
            self._head._above = None
            self._head._next._above = None
            self._height -= 1

        self._n -= 1
        return


    def __len__(self):
        """Return number of items in the map."""
        return self._n

    def __iter__(self):                             
        """Generate iteration of the map's keys."""
        # hint: iterate over the base height (where the nodes that node._below is None)
        # go down all the way to the bottom
        
        node = self._head
        while node._below != None:
            node = self._head
            while node._below != None:
                node = node._below
        node = node._next
        while node._key != math.inf:
            yield node._key
            node = node._next
        # yield node._key while node._next is not having math.inf as the key

    # def print_tree(self):
    #     ptr = self._head
    #     h = self._height
    #     print(self._n)
    #     while(h > 0):
    #         if(ptr == self._tail):
    #             break
    #         while(ptr._next != None):
    #             print(f"({ptr._key},{ptr._value})--",end='')
    #             ptr = ptr._next
    #         print(f"({ptr._key},{ptr._value})")
    #         while(ptr._prev != None):
    #             ptr = ptr._prev
    #         ptr = ptr._below
    #         h -= 1

def display_skiplist(SL):
    p = SL._head
    
    # get the heads of each layer
    while p._below != None:
        p = p._below
    
    while p != None:
        _p = p
        str = ''
        while _p != None:
            str += f'({_p._key},{_p._value})\t'
            _p_below = _p
            _p = _p._above
            if _p != None and _p_below != _p._below:
                print('ERROR: below-above link mismatch')
            
        print(str)
        
        p_prev = p
        p = p._next
        
        if p != None and p_prev != p._prev:
            print("ERROR: prev-next link mismatch")