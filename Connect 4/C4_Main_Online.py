# Online connect 4, good luck

import pygame
from C4_Network import Network

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

Display_Width = 700
Display_Height = 600
win = pygame.display.set_mode((Display_Width, Display_Height))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()
n = Network()
pygame.init()


def draw_grid(win, cols, rows):
    win.fill(BLACK)
    for i in range(cols):
        for j in range(rows):
            pygame.draw.circle(win, WHITE, (i * 100 + 50, j * 100 + 50), 45)


def get_click(pos):
    x, y = pos
    col = x // 100
    row = y // 100
    return col, row


def draw(win, grid, cols, rows):
    draw_grid(win, cols, rows)
    for row in grid:
        for spot in row:
            spot.draw(win)


def row_check(grid, col, player):
    for spot in grid[col]:
        if spot.colour:
            if spot.row == 0:
                return
            grid[col][spot.row - 1].change_colour(player)
            return col, spot.row - 1
    grid[col][5].change_colour(player)
    return col, 5


def win_check(spot, grid):
    Check = spot.check_win(grid)
    if Check == True:
        return True


def show_win(win, player):
    font = pygame.font.SysFont("ariel", 130)
    font1 = pygame.font.SysFont("ariel", 70)
    if not player:
        text = font.render("RED WINS", True, RED)
    else:
        text = font.render("YELLOW WINS", True, YELLOW)
    text1 = font1.render("Press R to play again", True, BLUE)
    n.send("HR")
    run = True
    while run:
        try:
            game = n.send("get")
        except Exception as e:
            print(e)
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    n.send("reset")
        if game.reset[0] and game.reset[1]:
            print("pass reset score ")
            print(game.reset)
            text2 = font.render(f"{str(game.score[0])},{str(game.score[1])}", True, BLACK)
            win.fill(WHITE)
            win.blit(text2, ((Display_Width // 2), Display_Height // 2 - round(text.get_height() // 2)))
            pygame.display.update()
            pygame.time.delay(500)
            run = False
            main(win, 7, 6)

        win.blit(text,
                 (Display_Width // 2 - round(text.get_width() // 2),
                  Display_Height // 2 - round(text.get_height() // 2)))
        win.blit(text1,
                 (Display_Width // 2 - round(text.get_width() // 2),
                  Display_Height // 2 - round(text.get_height() // 2) + 200))
        pygame.display.update()


def main(win, cols, rows):
    # player = True#true is red
    run = True
    draw_grid(win, cols, rows)
    player = int(n.getP())  # 1 is red
    print(f"you are {player}")
    game = n.send("get")
    print(game.reset, game.win)
    if player == 0:
        player = True
    else:
        player = False

    while run:
        clock.tick(10)
        try:
            game = n.send("get")
            grid = game.grid
        except Exception as e:
            print(e)
            print("Could not find game")
            break

        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if click[0]:
                if player == game.turn:
                    col, row = get_click(pos)
                    col, row = row_check(grid, col, player)
                    spot = grid[col][row]
                    Check = win_check(spot, grid)
                    if Check:
                        n.send("win")
                    if player:
                        sp_col = "RED"
                    else:
                        sp_col = "YELLOW"
                    n.send(f"$,{col},{row},{sp_col}")
                    game = n.send("get")

        draw(win, grid, cols, rows)
        if game.win == True or game.win == False:
            print("pass win main")
            print(game.win)
            show_win(win, not game.win)


        pygame.display.update()


def menu_screen():
    run = True
    Waiting = False
    clock.tick(10)
    while run:
        try:
            game = n.send("get")
        except Exception as e:
            print(e)
            print("Could not get game,Menu")

        win.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 60)
        if not Waiting:
            text = font.render("Click to Play!", True, (255, 0, 0))
        else:
            text = font.render("Waiting for players...", True, (255, 0, 0))
            if game.ready and game.wait[0] and game.wait[1]:
                run = False
                main(win, 7, 6)

        win.blit(text, (Display_Width / 2 - text.get_width() / 2, Display_Height / 2 - text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Waiting = True
                n.send("wait")
        pygame.time.delay(500)


menu_screen()
