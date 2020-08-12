class Rectangle:
    # Init with width/height
    def __init__(self, width, height):
        self.width = width
        self.height = height
    # string repr
    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"
        
    def set_width(self, value):
        self.width = value

    def set_height(self, value):
        self.height = value

    def get_area(self):
        return self.width*self.height

    def get_perimeter(self):
        return 2*self.width+2*self.height

    def get_diagonal(self):
        return (self.width**2+self.height**2)**.5

    def get_picture(self):
        if (self.width > 50 or self.height > 50):
            return "Too big for picture."
        return "\n".join(["*"*self.width for _ in range(self.height)])+'\n'

    def get_amount_inside(self, other):
        return int(self.width/other.width*self.height/other.height)


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.side = side

    def __str__(self):
        return f"Square(side={self.side})"

    def set_side(self, value):
        self.side = value
        self.height = value
        self.width = value

    def set_width(self, value):
        self.set_side(value)

    def set_height(self, value):
        self.set_side(value)


bonito = Rectangle(15, 15)

print(bonito.get_picture())
