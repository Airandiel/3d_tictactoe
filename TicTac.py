from draw_board import draw_board
from clear import clear
import random
import numpy as np
import copy
from random import shuffle

size = 4


class Position():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class TicTac():
    def __init__(self):
        self.board = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]
        self.copy = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]
        self.counter = 0

    def check_sum(self, summ):
        if summ == size:
            return 'X'
        elif summ == -size:
            return 'O'
        else:
            return None

    ### MINMAX should return position of next move
    def minmax(self, boardTemp, player, depth, maxDepth, position=Position(), alpha=-100000, beta=100000):
        if (depth <= maxDepth):
            depth += 1
            depthEven = False
            # if depth is even than we are minimazing
            if (depth % 2) == 0:
                localMinmax = 100000
                depthEven = True
            else:
                localMinmax = -100000
            localMove = Position()
            isFirst = True
            toPrune = False
            children = [Position(x, y, z) for x in range(size) for y in range(size) for z in range(size)]
            shuffle(children)
            for child in children:
                x = child.x
                y = child.y
                z = child.z
                if boardTemp[x][y][z] == 0:
                    if alpha >= beta:
                        toPrune = True
                    if not toPrune or isFirst:
                        isFirst = False
                        boardCopy = copy.deepcopy(boardTemp)
                        boardCopy[x][y][z] = player
                        pos, score = self.minmax(boardCopy, -player, depth, maxDepth,
                                                 Position(x, y, z), alpha, beta)
                        if depthEven:
                            if localMinmax > score:
                                localMinmax = score
                                localMove = Position(x, y, z)
                            if beta > localMinmax:
                                beta = localMinmax
                        else:
                            if localMinmax < score:
                                localMinmax = score
                                localMove = Position(x, y, z)
                            if alpha < localMinmax:
                                alpha = localMinmax

            return localMove, localMinmax
        score, win = self.score_move(boardTemp, position, player)
        return position, score

    def check_vector(self, vector, player):
        summ = vector[0] + vector[1] + vector[2] + vector[3]
        items = abs(vector[0]) + abs(vector[1]) + abs(vector[2]) + abs(vector[3])
        win = self.check_sum(summ)
        if summ == 4:
            return 300 * summ + player, 'X'
        elif summ == -4:
            return 300 * summ + player, 'O'
        elif (summ == 1 or summ == -1) and (items == 3):
            return player * 4, None
        elif summ == 0 and (items == 4):
            return -player * 10, None
        elif (summ == 2 or summ == -2) and items == 4:
            return -summ * 8, None
        else:
            return summ * abs(summ) + player, None

    def score_move(self, boardTemp, position, player):
        x = position.x
        y = position.y
        z = position.z
        score = 0
        allPossi = []
        allPossi.append([boardTemp[x][0][z], boardTemp[x][1][z], boardTemp[x][2][z], boardTemp[x][3][z]])
        allPossi.append([boardTemp[0][y][z], boardTemp[1][y][z], boardTemp[2][y][z], boardTemp[3][y][z]])
        allPossi.append([boardTemp[x][y][0], boardTemp[x][y][1], boardTemp[x][y][2], boardTemp[x][y][3]])
        allPossi.append([boardTemp[x][0][0], boardTemp[x][1][1], boardTemp[x][2][2], boardTemp[x][3][3]])
        allPossi.append([boardTemp[x][3][0], boardTemp[x][2][1], boardTemp[x][1][2], boardTemp[x][0][3]])
        allPossi.append([boardTemp[0][y][0], boardTemp[1][y][1], boardTemp[2][y][2], boardTemp[3][y][3]])
        allPossi.append([boardTemp[3][y][0], boardTemp[2][y][1], boardTemp[1][y][2], boardTemp[0][y][3]])
        allPossi.append([boardTemp[0][0][z], boardTemp[1][1][z], boardTemp[2][2][z], boardTemp[3][3][z]])
        allPossi.append([boardTemp[3][0][z], boardTemp[2][1][z], boardTemp[1][2][z], boardTemp[0][3][z]])
        # if z == x and x == y:
        allPossi.append([boardTemp[0][0][0], boardTemp[1][1][1], boardTemp[2][2][2], boardTemp[3][3][3]])
        # if x == size - 1 - z and z == y:
        allPossi.append([boardTemp[3][0][0], boardTemp[2][1][1], boardTemp[1][2][2], boardTemp[0][3][3]])
        # if y == size - 1 - z and z == x:
        allPossi.append([boardTemp[0][3][0], boardTemp[1][2][1], boardTemp[2][1][2], boardTemp[3][0][3]])
        # if y == size - 1 - z and x == y:
        allPossi.append([boardTemp[3][3][0], boardTemp[2][2][1], boardTemp[1][1][2], boardTemp[0][0][3]])
        winn = None
        for item in allPossi:
            summ, win = self.check_vector(item, player)
            if win != None:
                winn = win
            score += summ
        # return position, 0, None
        return score, winn

    def user_move(self, board):
        correctMove = False
        posArr = []
        pos = Position()
        while (not correctMove):
            givenPosition = input("Give me position(x,y,z - from 0 to 3): ")
            posArr = givenPosition.split(",")
            pos.x = int(posArr[0])
            pos.y = int(posArr[1])
            pos.z = int(posArr[2])
            if board[pos.x][pos.y][pos.z] == 0:
                correctMove = True
        return pos

    def play_game(self, playerOneAI=True, playerTwoAI=True, maxDepthPlayerOne=1, maxDepthPlayerTwo=1):
        summ = 0
        while summ < 64:
            ### Player One - 1(X):
            if playerOneAI:
                pos, score = self.minmax(self.board, 1, 0, maxDepthPlayerOne)
            else:
                pos = self.user_move(self.board)

            self.board[pos.x][pos.y][pos.z] = 1
            score, win = self.score_move(self.board, pos, 1)
            if win != None:
                print(win, " wins!!!")
                draw_board(self.board)
                break

            ### Player Two - -1(O)
            if playerTwoAI:
                for x in range(size):
                    for y in range(size):
                        for z in range(size):
                            self.copy[x][y][z] = -copy.deepcopy(self.board[x][y][z])

                pos, score = self.minmax(self.copy, 1, 0, maxDepth=maxDepthPlayerTwo)
            else:
                pos = self.user_move(self.board)

            self.board[pos.x][pos.y][pos.z] = -1
            score, win = self.score_move(self.board, pos, -1)
            if win != None:
                print(win, " wins!!!")
                draw_board(self.board)
                break

            draw_board(self.board)

            summ = 0
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                        summ += abs(self.board[x][y][z])
        if summ == 64:
            print("No one  wins!!!")

    def menu(self):
        clear()
        print("####MENU####")
        self.menuOptions = []
        self.menuOptions.append(('play_game', "User vs AI"))
        self.menuOptions.append(('play_game', "AI vs AI"))
        self.menuOptions.append(('exit', "Exit"))
        for i, j in enumerate(self.menuOptions):
            print(i, ". ", j[1])
        x = input("Enter number: ")
        if int(x) == 0:
            x = input("Enter max depth of AI (default: 1 - means one max and one min, 2 adds one layer): ")
            if x == '':
                getattr(self, self.menuOptions[0][0])(False, True)
            else:
                getattr(self, self.menuOptions[0][0])(False, True, 0, int(x))
        elif int(x) == 1:
            x1 = input("Enter max depth of first AI (default: 1 - means one max and one min, 2 adds one layer): ")
            x2 = input("Enter max depth of second AI (default: 1 - means one max and one min, 2 adds one layer): ")
            if x1 == '' and x2 == '':
                getattr(self, self.menuOptions[1][0])(True, True)
            elif x1 == '' and x2 != '':
                getattr(self, self.menuOptions[1][0])(True, True, 1, int(x2))
            elif x1 != '' and x2 == '':
                getattr(self, self.menuOptions[1][0])(True, True, int(x1))
            else:
                getattr(self, self.menuOptions[1][0])(True, True, int(x1), int(x2))
        else:
            getattr(self, self.menuOptions[int(x)][0])()


TicTac().menu()
