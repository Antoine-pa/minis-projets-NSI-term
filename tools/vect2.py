class Vect2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norme(self):
        return (self.x**2+self.y**2)**0.5

    def normalize(self):
        n = self.norme()
        self.x /= n
        self.y /= n
        return self
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __mult__(self, other):
        if isinstance(other, int):
            self.x *= other
            self.y *= other
            return self
        elif isinstance(other, Vect2):
            return self.x*other.x+self.y*other.y
        else:
            return None
