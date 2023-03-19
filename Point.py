class Point:
    def __init__(self, x, y, value, prev=None) -> None:
        self.x = x
        self.y = y
        self.value = value
        self.prev = prev
        
    def __add__(self, other):
        if isinstance(other, tuple):
            return (self.x + other[0], self.y + other[1])
        if isinstance(other, Point):
            return (self.x + other.x, self.y + other.y)
        return None
    
    def __sub__(self, other):
        if isinstance(other, tuple):
            return (self.x - other[0], self.y - other[1])
        if isinstance(other, Point):
            return (self.x - other.x, self.y - other.y)
        return None
    
    def __eq__(self, other):
        if(other == None):
            return False
        if isinstance(other, tuple):
            return (self.x == other[0]) and (self.y == other[1])
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        return None
    def __ne__(self, other):
        if(other == None):
            return True
        if isinstance(other, tuple):
            return (self.x != other[0]) or (self.y != other[1])
        if isinstance(other, Point):
            return (self.x != other.x) or (self.y != other.y)
        return None

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"