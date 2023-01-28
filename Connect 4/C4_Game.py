import pygame

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self, id):
        self.turn = True#true is red.
        self.ready = False
        self.id = id
        self.win = None#True is red
        self.grid = make_grid(7,6)
        self.wait = [False,False]
        self.score = [0,0]
        self.reset = [False,False]

    def connected(self):
        return self.ready

    def change_grid(self,col,row,colour):
        self.grid[col][row].colour = colour

    def reset_grid(self,p):
        self.score[p] += 1
        self.grid = make_grid(7,6)
        self.reset = [False, False]
        self.win = None

def print_grid(grid):
    for i in range(6):
        for j in range(7):
            if (grid[j][i].colour == RED):
                print("X ", end= " ")
            elif(grid[j][i].colour == YELLOW):
                print("O ", end= " ")
        print()


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
        print_grid(grid)
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



def make_grid(cols,rows):
    grid = []
    for i in range(cols):
        grid.append([])
        for j in range(rows):
            spot = (Spot(i,j))
            grid[i].append(spot)
    print("grid created")
    return grid









