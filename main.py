import pygame
import sys
import tools
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

#Setup the pygame window
pygame.init()

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
BROWN = (139, 69, 19)
TAN = (245, 222, 179)
PINK = (255, 105, 180)
DEEP_PINK = (255, 20, 147)
MAROON = (128, 0, 0)


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

#Draw the grid squares
def draw_squares(window, grid, total_rows, grid_width):
  window.fill(WHITE)

  for row in grid:
    for GridSquare in row:
      GridSquare.draw(window)

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

  #Booleans for what tool is selected, starts with brush
  brush_selected = True
  eraser_selected = False
  eye_dropper_selected = False

  #Booleans for what brush size is selected, starts with 1
  size_1_selected = True
  size_2_selected = False
  size_3_selected = False
  size_4_selected = False

  while still_drawing:
    #Draw the grid
    draw_squares(screen, grid, rows, grid_width)
    #Make the tool buttons
    brush_button = image_button('images/brush.png',(window_width - 80, 50), screen)
    eraser_button = image_button('images/eraser.png', (window_width - 80, 110), screen)
    eye_dropper_button = image_button('images/eyeDropper.png', (window_width - 80, 170), screen)

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
            if type(current_tool) is tools.PaintBrush or type(current_tool) is tools.Eraser: #Brush or eraser
              current_tool.use(square, grid) #Use the use method of the brush or eraser
            elif type(current_tool) is tools.EyeDropper: #Eyedropper
              current_color = current_tool.use(square) #Use the use method of the eyedropper

          except Exception:
            pass
        else: #If they click in the tools menu
          #Tool Buttons
          if brush_button[1].collidepoint(pos): #PaintBrush
            current_tool = tools.PaintBrush(brush_size, current_color)
            brush_selected = True
            eraser_selected = False
            eye_dropper_selected = False
          if eraser_button[1].collidepoint(pos): #Eraser
            current_tool = tools.Eraser(brush_size)
            brush_selected = False
            eraser_selected = True
            eye_dropper_selected = False
          if eye_dropper_button[1].collidepoint(pos): #Eye Dropper
            current_tool = tools.EyeDropper(brush_size)
            brush_selected = False
            eraser_selected = False
            eye_dropper_selected = True
          #Brush Size Buttons
          if size_1_rect.collidepoint(pos):
            brush_size = 1
            current_tool.change_brush_size(brush_size)
            size_1_selected = True
            size_2_selected = False
            size_3_selected = False
            size_4_selected = False
          if size_2_rect.collidepoint(pos):
            brush_size = 2
            current_tool.change_brush_size(brush_size)
            size_1_selected = False
            size_2_selected = True
            size_3_selected = False
            size_4_selected = False
          if size_3_rect.collidepoint(pos):
            brush_size = 3
            current_tool.change_brush_size(brush_size)
            size_1_selected = False
            size_2_selected = False
            size_3_selected = True
            size_4_selected = False
          if size_4_rect.collidepoint(pos):
            brush_size = 4
            current_tool.change_brush_size(brush_size)
            size_1_selected = False
            size_2_selected = False
            size_3_selected = False
            size_4_selected = True

          #Change the brush color upon clicking the color buttons
          if yellow_button.collidepoint(pos):
            current_color = YELLOW
            if type(current_tool) is tools.PaintBrush: #If statements like these are to check if the current tool is a paint brush to avoid errors
              current_tool.change_brush_color(YELLOW)

          if orange_button.collidepoint(pos):
            current_color = ORANGE
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(ORANGE)
          if red_button.collidepoint(pos):
            current_color = RED
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(RED)
          if magenta_button.collidepoint(pos):
            current_color = MAGENTA
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(MAGENTA)
          if purple_button.collidepoint(pos):
            current_color = PURPLE
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(PURPLE)
          if lime_button.collidepoint(pos):
            current_color = LIME
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(LIME)
          if green_button.collidepoint(pos):
            current_color = GREEN
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(GREEN)
          if black_button.collidepoint(pos):
            current_color = BLACK
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(BLACK)
          if cyan_button.collidepoint(pos):
            current_color = CYAN
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(CYAN)
          if brown_button.collidepoint(pos):
            current_color = BROWN
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(BROWN)
          if tan_button.collidepoint(pos):
            current_color = TAN
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(TAN)
          if maroon_button.collidepoint(pos):
            current_color = MAROON
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(MAROON)
          if pink_button.collidepoint(pos):
            current_color = PINK
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(PINK)
          if deep_pink_button.collidepoint(pos):
            current_color = DEEP_PINK
            if type(current_tool) is tools.PaintBrush:
              current_tool.change_brush_color(DEEP_PINK)


          #If they click on the save button
          if save_button.collidepoint(pos):
            #Ask which directory to save the image to using tkinter
            root = Tk() #Use tkinter to get the directory
            root.withdraw() #Makes it so the tkinter window doesn't pop up
            fileName = asksaveasfilename(title = 'Save Image',defaultextension=".png",filetypes = (("PNG file","*.png"),('all files','*.*'))) #Get image name
            root.destroy() #Delete the tkinter window after saving
            if fileName != "": #Make sure fileName isn't blank
              pygame.image.save(screen, fileName)

          


    #Displays the tool menu, which has a width of 200, so window_width - 200 is where it starts
    screen.blit(tool_menu_background, (window_width - 200,0))
    tool_menu_background.fill(GRAY)

    #Display the tool button indicators (indicate which tool is selected by changing the rect color)
    brush_indicator = pygame.draw.rect(screen, DARK_GRAY, (window_width - 130, 50, 50, 50))
    if brush_selected:
      brush_indicator = pygame.draw.rect(screen, LIME, ((window_width - 130, 50, 50, 50)))

    eraser_indicator = pygame.draw.rect(screen, DARK_GRAY, (window_width - 130, 110, 50, 50))
    if eraser_selected:
      eraser_indicator = pygame.draw.rect(screen, LIME, (window_width - 130, 110, 50, 50))

    eye_dropper_indicator = pygame.draw.rect(screen, DARK_GRAY, (window_width - 130, 170, 50, 50))
    if eye_dropper_selected:
      eye_dropper_indicator = pygame.draw.rect(screen, LIME, (window_width - 130, 170, 50, 50))

    #Display the tool buttons (image rects)
    screen.blit(brush_button[0], brush_button[1])
    screen.blit(eraser_button[0], eraser_button[1])
    screen.blit(eye_dropper_button[0], eye_dropper_button[1])

    #Display the brush size buttons
    size_1_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 180,270,30,30))
    if size_1_selected:
      size_1_rect = pygame.draw.rect(screen,LIME,(window_width - 180,270,30,30))

    size_2_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 140,270,30,30))
    if size_2_selected:
      size_2_rect = pygame.draw.rect(screen,LIME,(window_width - 140,270,30,30))

    size_3_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 100,270,30,30))
    if size_3_selected:
      size_3_rect = pygame.draw.rect(screen,LIME,(window_width - 100,270,30,30))

    size_4_rect = pygame.draw.rect(screen,DARK_GRAY,(window_width - 60,270,30,30))
    if size_4_selected:
      size_4_rect = pygame.draw.rect(screen,LIME,(window_width - 60,270,30,30))
    #Display the text on the buttons
    display_text("1", BLACK, (window_width - 165,275))
    display_text("2", BLACK, (window_width - 125,275))
    display_text("3", BLACK, (window_width - 85,276))
    display_text("4", BLACK, (window_width - 45,275))

    #Display the color buttons
    yellow_button = pygame.draw.rect(screen, YELLOW, (window_width - 175, 370, 30, 30))
    orange_button = pygame.draw.rect(screen, ORANGE, (window_width - 145, 370, 30, 30))
    red_button = pygame.draw.rect(screen, RED, (window_width - 115, 370, 30, 30))
    magenta_button = pygame.draw.rect(screen, MAGENTA, (window_width - 85, 370, 30, 30))
    purple_button = pygame.draw.rect(screen, PURPLE, (window_width - 55, 370, 30, 30))
    lime_button = pygame.draw.rect(screen, LIME, (window_width - 175, 400, 30, 30))
    green_button = pygame.draw.rect(screen, GREEN, (window_width - 145, 400, 30, 30))
    black_button = pygame.draw.rect(screen, BLACK, (window_width - 115, 400, 30, 30))
    cyan_button = pygame.draw.rect(screen, CYAN, (window_width - 85, 400, 30, 30))
    blue_button = pygame.draw.rect(screen, BLUE, (window_width - 55, 400, 30, 30))
    brown_button = pygame.draw.rect(screen, BROWN, (window_width - 175, 430, 30, 30))
    tan_button = pygame.draw.rect(screen, TAN, (window_width - 145, 430, 30, 30))
    maroon_button = pygame.draw.rect(screen, MAROON, (window_width - 115, 430, 30, 30))
    pink_button = pygame.draw.rect(screen, PINK, (window_width - 85, 430, 30, 30))
    deep_pink_button = pygame.draw.rect(screen, DEEP_PINK, (window_width - 55, 430, 30, 30))


    #Display the current color
    current_color_rect = pygame.draw.rect(screen, current_color, (window_width - 130, 525, 50, 50))

    #Display the save button
    save_button = pygame.draw.rect(screen, DARK_GRAY, (window_width - 150, 650, 100, 40))
    display_text("Save", BLACK, (window_width - 135, 660))

    #Displays the tool menu titles
    display_text("Tools", BLACK, (window_width - 140, 5))
    display_text("Brush Size", BLACK, (window_width - 180, 230))
    display_text("Colors", BLACK, (window_width - 150, 340))
    display_text("Current Color", BLACK, (window_width - 195, 490))

    pygame.display.flip()

main()
