#Classes for the different types of tools that can be used on the canvas

WHITE = (255, 255, 255) #For eraser class to use

#Class Tool for each of the tools to inherit from
class Tool:
  def __init__(self, brush_size):
    self.brush_size = brush_size

  def change_brush_size(self, new_brush_size):
    self.brush_size = new_brush_size

#Class Brush inherits Tool
class PaintBrush(Tool):
  def __init__(self, brush_size, color):
    self.brush_size = brush_size
    self.color = color

  def change_brush_color(self, new_color):
    self.color = new_color

  def use(self, square, grid):
    square.change_color(self.color)
    neighbors = square.update_neighbors(grid, self.brush_size)
    for eachSquare in neighbors:
      eachSquare.change_color(self.color)

#Class eraser inherits Tool
class Eraser(Tool):
  def __init__(self, brush_size):
    self.brush_size = brush_size

  def use(self, square, grid):
    square.change_color(WHITE)
    neighbors = square.update_neighbors(grid, self.brush_size)
    for eachSquare in neighbors:
      eachSquare.change_color(WHITE)

#Class eyedropper inherits Tool
class EyeDropper(Tool):
  def __init__(self):
    super().__init__()

#Class fill inherits Tool
class Fill(Tool):
  def __init__(self):
    super().__init__()