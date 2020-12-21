import pygame
import sys
import tools

#Setup the pygame window
pygame.init()

#Window width needs to be 200 more than window_height for the drawing area and tool surface to line up correctly
window_width = 1000
window_height = 800

#Main drawing area
screen = pygame.display.set_mode((window_width, window_height))
#Tool menu for different colors, brushes, etc
tool_menu_background = pygame.Surface([200, window_height])

pygame.display.set_caption("Python Paint")

#Setup the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIME = (0, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (169, 169, 169)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)


#Create the grid squares
class GridSquare:
  def __init__(self, row, col, square_size):
    self.row = row
    self.col = col
    self.x = row * square_size
    self.y = col * square_size
    self.size = square_size
    self.color = WHITE
    self.neighbors = []

  def get_pos(self):
    return self.row, self.col

  def get_color(self):
    return self.color

  def get_neighbors(self):
    return self.neighbors

  #Change neighboring squares for bigger brush sizes
  def update_neighbors(self, grid, brush_size):
    self.neighbors = []
    #If statements like these are so it doesn't draw on the other side of the grid when the user draws on the edge
    if self.row < len(grid):
      self.neighbors.append(grid[self.row + (brush_size - 1)][self.col])
    if self.row > 0:
      self.neighbors.append(grid[self.row - (brush_size - 1)][self.col])
    if self.col > 0:
      self.neighbors.append(grid[self.row][self.col - (brush_size - 1)])
    if self.col < len(grid):
      self.neighbors.append(grid[self.row][self.col + (brush_size - 1)])

    #Fill in the gaps for larger brush sizes
    if brush_size >= 3:
      if self.row < len(grid):
        self.neighbors.append(grid[self.row + (brush_size - 2)][self.col])
      if self.row > 0:
        self.neighbors.append(grid[self.row - (brush_size - 2)][self.col])
      if self.col > 0:
        self.neighbors.append(grid[self.row][self.col - (brush_size - 2)])
      if self.row < len(grid):
        self.neighbors.append(grid[self.row][self.col + (brush_size - 2)])

    if brush_size == 4:
      if self.row < len(grid):
        self.neighbors.append(grid[self.row + (brush_size - 3)][self.col])
      if self.row > 0:
        self.neighbors.append(grid[self.row - (brush_size - 3)][self.col])
      if self.col > 0:
        self.neighbors.append(grid[self.row][self.col - (brush_size - 3)])
      if self.col < len(grid):
        self.neighbors.append(grid[self.row][self.col + (brush_size - 3)])


    return self.neighbors
  

  def draw(self, window):
    pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

  #Changes the color to whatever color is passed into the method
  def change_color(self, new_color):
    self.color = new_color

#Create the grid to draw on
def create_grid(grid_width, total_rows):
  gap = grid_width // total_rows
  grid = []

  for r in range(total_rows):
    grid.append([])
    for c in range (total_rows):
      #Create the squares in the grid
      square = GridSquare(r, c, gap)
      grid[r].append(square)

  return grid

#Draw the grid lines to the screen
def draw_grid_lines(window, rows, grid_width):
  gap = grid_width // rows
  for r in range(rows):
    pygame.draw.line(window, GRAY, (0, r * gap), (grid_width, r * gap))
    for c in range(rows):
      pygame.draw.line(window, GRAY, (c * gap, 0), (c * gap, grid_width))

#Draw the grid squares
def draw_squares(window, grid, total_rows, grid_width):
  window.fill(WHITE)

  for row in grid:
    for GridSquare in row:
      GridSquare.draw(window)

  draw_grid_lines(window, total_rows, grid_width)

#Function to get the clicked position so we can draw on that square in the grid
def get_clicked_pos(pos, rows, grid_width):
  gap = grid_width // rows
  y, x = pos

  #Divides the position by the width of each of the squares to get the correct location in the grid, rather than just the location in the overall window
  row = y // gap
  col = x // gap

  return row, col

def display_text(message, color, pos):
    font = pygame.font.Font(None, 40)
    text = font.render(message, 1, color)
    screen.blit(text, pos)

#Function to make buttons using images
def image_button(picture, coords, surface):
    image = pygame.image.load(picture)
    scaled_image = pygame.transform.scale(image, (50, 50))
    imagerect = scaled_image.get_rect()
    imagerect.topright = coords
    return (scaled_image,imagerect)

def main():

  #Row number, will always be a square (row x row) grid
  rows = 50
  
  #Grid width, how wide the grid is across the screen, will be whatever the window width is minus 200 to make room for the tool surface
  grid_width = window_width - 200

  #Create the grid
  grid = create_grid(grid_width, rows)

  brush_size = 1
  current_color = BLACK

  #Create the tool object
  current_tool = tools.PaintBrush(brush_size, current_color)

  still_drawing = True

  while still_drawing:
    #Draw the grid
    draw_squares(screen, grid, rows, grid_width)
    #Make the tool buttons
    brush_button = image_button('images/brush.png',(window_width - 80, 50), screen)
    eraser_button = image_button('images/eraser.png', (window_width - 80, 110), screen)
    eye_dropper_button = image_button('images/eyeDropper.png', (window_width - 80, 160), screen)
    fill_button = image_button('images/fill.png', (window_width - 80, 220), screen)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        #Figure out if they have clicked in the tool menu or the drawing area

        #If it's in the drawing area change that part of the grid
        if pos[0] <= grid_width: #If they click inside the grid
          try:
            row, col = get_clicked_pos(pos, rows, grid_width)
            square = grid[row][col]
            current_tool.use(square, grid) #Use the use method of the current tool
          except Exception:
            pass
        else: #If they click in the tools menu
          #Tool Buttons
          if brush_button[1].collidepoint(pos): #PaintBrush
            current_tool = tools.PaintBrush(brush_size, current_color)
          if eraser_button[1].collidepoint(pos): #Eraser
            current_tool = tools.Eraser(brush_size)
          if eye_dropper_button[1].collidepoint(pos): #Eye Dropper
            current_tool = tools.EyeDropper()
          if fill_button[1].collidepoint(pos): #Fill Tool
            current_tool = tools.Fill()
          #Brush Size Buttons
          if size_1_rect.collidepoint(pos):
            brush_size = 1
            current_tool.change_brush_size(brush_size)
          if size_2_rect.collidepoint(pos):
            brush_size = 2
            current_tool.change_brush_size(brush_size)
          if size_3_rect.collidepoint(pos):
            brush_size = 3
            current_tool.change_brush_size(brush_size)
          if size_4_rect.collidepoint(pos):
            brush_size = 4
            current_tool.change_brush_size(brush_size)

          #Change the brush color upon clicking the color buttons
          if yellow_button.collidepoint(pos):
            current_tool.change_brush_color(YELLOW)
          if orange_button.collidepoint(pos):
            current_tool.change_brush_color(ORANGE)
          if red_button.collidepoint(pos):
            current_tool.change_brush_color(RED)
          if magenta_button.collidepoint(pos):
            current_tool.change_brush_color(MAGENTA)
          if purple_button.collidepoint(pos):
            current_tool.change_brush_color(PURPLE)
          if lime_button.collidepoint(pos):
            current_tool.change_brush_color(LIME)
          if green_button.collidepoint(pos):
            current_tool.change_brush_color(GREEN)
          if black_button.collidepoint(pos):
            current_tool.change_brush_color(BLACK)
          if cyan_button.collidepoint(pos):
            current_tool.change_brush_color(CYAN)
          if blue_button.collidepoint(pos):
            current_tool.change_brush_color(BLUE)
          


    #Displays the tool menu, which has a width of 200, so window_width - 200 is where it starts
    screen.blit(tool_menu_background, (window_width - 200,0))
    tool_menu_background.fill(GRAY)

    #Display the tool buttons
    screen.blit(brush_button[0], brush_button[1])
    screen.blit(eraser_button[0], eraser_button[1])
    screen.blit(eye_dropper_button[0], eye_dropper_button[1])
    screen.blit(fill_button[0], fill_button[1])

    #Display the brush size buttons
    size_1_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 180,330,30,30))
    size_2_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 140,330,30,30))
    size_3_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 100,330,30,30))
    size_4_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 60,330,30,30))
    #Display the text on the buttons
    display_text("1", BLACK, (window_width - 165,335))
    display_text("2", BLACK, (window_width - 125,335))
    display_text("3", BLACK, (window_width - 85,336))
    display_text("4", BLACK, (window_width - 45,335))

    #Display the color buttons
    yellow_button = pygame.draw.rect(screen, YELLOW, (window_width - 175, 430, 30, 30))
    orange_button = pygame.draw.rect(screen, ORANGE, (window_width - 145, 430, 30, 30))
    red_button = pygame.draw.rect(screen, RED, (window_width - 115, 430, 30, 30))
    magenta_button = pygame.draw.rect(screen, MAGENTA, (window_width - 85, 430, 30, 30))
    purple_button = pygame.draw.rect(screen, PURPLE, (window_width - 55, 430, 30, 30))
    lime_button = pygame.draw.rect(screen, LIME, (window_width - 175, 460, 30, 30))
    green_button = pygame.draw.rect(screen, GREEN, (window_width - 145, 460, 30, 30))
    black_button = pygame.draw.rect(screen, BLACK, (window_width - 115, 460, 30, 30))
    cyan_button = pygame.draw.rect(screen, CYAN, (window_width - 85, 460, 30, 30))
    blue_button = pygame.draw.rect(screen, BLUE, (window_width - 55, 460, 30, 30))

    #Displays the tool menu titles
    display_text("Tools", BLACK, (window_width - 140, 5))
    display_text("Brush Size", BLACK, (window_width - 180, 290))
    display_text("Colors", BLACK, (window_width - 150, 400))

    pygame.display.flip()

main()