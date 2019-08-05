from clear import clear
import sys

size = 4


def draw_board(matrix = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]):
    clear()
    print('---------   ---------   ---------   ---------')
    for y in range(4):
        print('|', end='')
        for z in range(4):
            for x in range(4):
                if matrix[x][y][z] == -1:
                    print('O|', end='')
                elif matrix[x][y][z] == 1:
                    print('X|', end='')
                else:
                    print(' |', end='')
            if z < 3:
                print('   |', end='')
        print('')
    print('---------   ---------   ---------   ---------')
# BoardDrawing.draw_board()
