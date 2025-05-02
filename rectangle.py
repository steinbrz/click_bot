class Rectangle:
    x: int
    y: int
    width: int
    height: int
    center_x: int
    center_y: int
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = self._center_x()
        self.center_y = self._center_y()


    def _center_x(self) -> int:
        return int(self.x + (self.width / 2))
    def _center_y(self) -> int:
        return int(self.y + (self.height / 2))