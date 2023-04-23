class EmptyException(Exception):
   """Raised when the data structure is empty"""
   pass

class Deque: # Space used: O(n)
    # Always start from initial capacity=2. Resize if needed.
    DEFAULT_CAPACITY = 2
    
    def __init__(self, capacity=DEFAULT_CAPACITY):
        self._data = [None]*capacity
        self._f = 0 # front pointer. address of starting element.
        self._r = 0 # rear pointer. address of last element.
        
    def __str__(self):
        return f'DEQUE({len(self)}: {self._data} / {self._f}, {self._r})'

    @property
    def N(self):
        return len(self._data)

    def __len__(self): # O(1)
        return self._r - self._f

    def is_empty(self): # O(1)
        if (self._r - self._f) == 0:
            return True
        return False

    def add_first(self, e): # O(1)*
        self._f -= 1
        self._data[self._f] = e
        if (self._r - self._f) >= self.N:
            self._resize(self.N*2)

    def first(self): # O(1)
        if self.is_empty():
            raise EmptyException('Deque is empty')
        return self._data[self._f]

    def delete_first(self):   # O(1)*
        if self.is_empty():
            raise EmptyException('Deque is empty')
        ret = self._data[self._f]
        self._data[self._f] = None
        self._f += 1  
        if (self._r - self._f) < self.N/2:
            self._resize(int(self.N/2))
        return ret
    
    def add_last(self, e): # O(1)*
        self._data[self._r] = e
        self._r += 1
        if (self._r - self._f) >= self.N:
            self._resize(self.N*2)

    def last(self):
        if self.is_empty():
            raise EmptyException('Deque is empty')
        return self._data[self._r - 1]

    def delete_last(self):
        if self.is_empty():
            raise EmptyException('Deque is empty')
        ret = self._data[self._r - 1]
        self._data[self._r - 1] = None
        self._r -= 1  
        if (self._r - self._f) < self.N/2:
            self._resize(int(self.N/2))
        return ret
        
    # Use doubling strategy for resizing the buffer.
    def _resize(self, cap): # O(n)
        cap = max(cap, 2)
        buff = self._data[self._f:] +self._data[:self._r]
        buff = buff + [None]*(cap- (self._r-self._f))
        self._data = buff
        self._r -= self._f
        self._f = 0