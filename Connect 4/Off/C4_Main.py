#Online connect 4, good luck

import pygame

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

Display_Width = 700
Display_Height = 600
win = pygame.display.set_mode((Display_Width,Display_Height))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()
pygame.init()

class Spot:
    def __init__(self,col,row):#width is the width of square
        self.colour = None
        self.width = 50
        self.row = row
        self.col = col
        self.x = col * 100 + 50
        self.y = row * 100 + 50

    def draw(self,win):
        if self.colour:
            pygame.draw.circle(win,self.colour,(self.x,self.y),self.width)

    def check_win(self,grid):
        Check = 0
        if self.row >= 3:  # up
            for i in range(4):
                if grid[self.col][self.row - i].colour == self.colour and self.colour is not None:
                    print(self.col, self.row - i)
                    Check += 1
            if Check == 4:
                return True
        Check = 0
        if self.row <= 2:  # down
            for i in range(4):
                if grid[self.col][self.row + i].colour == self.colour and self.colour is not None:
                    Check += 1
            if Check == 4:
                return True
        Check = 0
        if self.col <= 3:  # right
            for i in range(4):
                if grid[self.col + i][self.row].colour == self.colour and self.colour is not None:
                    Check += 1
            if Check == 4:
                return True
        Check =0
        if self.col >=3:#left
            for i in range(4):
                if grid[self.col - i][self.row].colour == self.colour and self.colour is not None:
                    Check += 1
            if Check == 4:
                return True
        Check = 0
        if self.col<=3 and self.row >=3:#upright
            for i in range(4):
                if grid[self.col + i][self.row - i].colour == self.colour and self.colour is not None:
                    Check += 1
            if Check == 4:
                return True
        Check = 0
        if self.col<=3 and self.row<=2:#downright
            for i in range(4):
                if grid[self.col + i][self.row + i].colour == self.colour and self.colour is not None:
                    Check += 1
            if Check == 4:
                return True
        Check = 0
        if self.col >=3 and self.row <= 2:#down left
            for i in range(4):
                if grid[self.col - i][self.row + i].colour == self.colour and self.colour is not None:
                    Check += 1
            if Check == 4:
                return True
        if self.col <= 3 and self.row >=3:#up left
            for i in range(4):
                if grid[self.col - i][self.row - i].colour == self.colour and self.colour is not None:
                    Check += 1
            if Check == 4:
                return True
        return False


    def change_colour(self,player):
        if player:
            self.colour = RED
        else:
            self.colour = YELLOW

    def __str__(self):
        return self.col



def make_grid(cols,rows):
    grid = []
    for i in range(cols):
        grid.append([])
        for j in range(rows):
            spot = (Spot(i,j))
            grid[i].append(spot)
    # for row in grid:
    #     for spot in row:
    #         print(spot.col,spot.row)
    #     print("-----------")
    return grid

def draw_grid(win,cols,rows):
    win.fill(BLACK)
    for i in range (cols):
        for j in range (rows):
            pygame.draw.circle(win,WHITE,(i*100+50,j*100+50 ),45)

def get_click(pos):
    x,y = pos
    col = x//100
    row = y//100
    return col,row

def draw(win,grid,cols,rows):
    draw_grid(win,cols,rows)
    for row in grid:
        for spot in row:
            spot.draw(win)

def row_check(grid,col,player):
    for spot in grid[col]:
        if spot.colour:
            if spot.row == 0:
                return
            grid[col][spot.row - 1].change_colour(player)
            return col,spot.row-1
    grid[col][5].change_colour(player)
    return col,5

def win_check(spot,grid):
    Check = spot.check_win(grid)
    if Check == True:
        return True
def show_win(win,player):
    font = pygame.font.SysFont("ariel", 150)
    if not player:
        text = font.render("RED WINS",True,BLACK)
    else:
        text = font.render("YELLOW WINS",True,BLACK)
    win.blit(text,(Display_Width // 2 - round(text.get_width() // 2), Display_Height // 2 - round(text.get_height() // 2)))


def main(win,cols,rows):
    player = True#true is red
    grid = make_grid(cols,rows)
    run = True
    draw_grid(win,cols,rows)
    while run:
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if click[0]:
                col,row = get_click(pos)
                print(col,row,"main")
                col,row = row_check(grid,col,player)
                player = not player
                draw(win,grid,cols,rows)
                spot = grid[col][row]
                Check = win_check(spot,grid)
                line = ""
                for row in grid:
                    line = ""
                    for spot in row:
                        line += str(spot.colour) + ","
                    print(line)
                if Check:
                    print("WINNNNEERRRRRR")
                    show_win(win,player)
        clock.tick(10)
        pygame.display.update()



main(win,7,6)


