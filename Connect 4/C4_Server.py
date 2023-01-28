import socket
from _thread import *
from C4_Game import Game
import pickle

server = ""  # Symbolic name meaning all available interfaces

port = 5555  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)

s.listen(2)
print("waiting for connection, server started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    while True:
        try:
            data = conn.recv(32768).decode()
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset[p] = True
                        if game.reset[0] and game.reset[1] and game.win != None:
                            if game.win == True:
                                game.reset_grid(1)
                            else:
                                game.reset_grid(0)
                            print(f"{game.reset},{game.win},{game.score},server")

                    elif data == "HR":
                        game.reset = [False, False]

                    elif data == "wait":
                        game.wait[p] = True

                    elif data == "win":
                        game.win = game.turn
                        print(game.win)

                    elif data[0] == "$":
                        data = data.split(",")  # col, then row then colour
                        print(data)
                        try:
                            if data[3] == "RED":
                                colour = (255, 0, 0)
                            elif data[3] == "YELLOW":
                                colour = (255, 255, 0)
                            game.change_grid(int(data[1]), int(data[2]), colour)  # convert data 3 to tup to send

                            if game.turn:
                                game.turn = False
                            else:
                                game.turn = True

                        except Exception as e:
                            print(e, "in server grid")
                            break

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("LOST CONNECTION")
    print("CLOSING GAME", gameId)
    try:
        del games[gameId]
        print("CLOSING GAME", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game ...")
    else:

        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
