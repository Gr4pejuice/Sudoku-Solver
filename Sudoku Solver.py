import random
import copy
import pygame, sys
import time
from pygame.locals import QUIT
pygame.init()

############################# FUNCTIONS ###############################
def printBoard(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j],end=" ")
            if j == 2 or j == 5:
                print('|', end=" ")
        print()
        if i == 2 or i == 5:
            print('-'*22)
    print()

def isValid(r, c, num, board): #num is a string
    not_in_row = board[r].count(num) < 1
    if not not_in_row:
        return False

    not_in_col = True
    for i in range(9):
        if board[i][c] == num and i != r:
            return False

    not_in_square = True
    for i in range(r//3*3, r//3*3+3):
        if i != r and num in board[i]:
            if board[i].index(num) in range(c//3*3, c//3*3+3):
                return False
    return True

def fillBoard(r,c, board, num_list):
    if r == 8 and c == 9:
        return True

    if c == 9:
        c = 0
        r += 1

    if board[r][c] != '.':
        return fillBoard(r,c+1, board, num_list)
    
    for num in num_list:
        if isValid(r,c,num, board):
            board[r][c] = num
            if fillBoard(r,c+1, board, num_list):
                return board
            else:
                board[r][c] = '.'
    return False

def solvePygame(r,c, board, num_list):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    drawBackground(screen)
    drawSelection(screen, board, 20, 20, selected_coords)
    drawGrid(screen, board, 20, 20)
    drawButtons(screen)
    drawKeypad(screen)
    pygame.display.update()
    time.sleep(0.07)

    if r == 8 and c == 9:
        return True

    if c == 9:
        c = 0
        r += 1

    if (r,c) not in empty_squares:
        return solvePygame(r,c+1, board, num_list)
    
    for num in num_list:
        if isValid(r,c,num, board):
            board[r][c] = num
            if solvePygame(r,c+1, board, num_list):
                return board
            else:
                board[r][c] = '.'
    return False

def getSolutions(r, c, board):
    if c == 9:
        c = 0
        r += 1

    if board[r][c] != '.':
        return getSolutions(r,c+1, board)
    
    for num in range(1,10):
        num = str(num)
        if isValid(r,c,num, board):
            board[r][c] = num
            if all(['.' not in board[i] for i in range(9)]):
                global solutions
                solutions += 1
                break
            else:
                getSolutions(r,c+1, board)
    board[r][c] = '.'
    return False

def generateFilledBoard(num_list):
    board = [['.' for i in range(9)] for j in range(9)]
    random.shuffle(num_list)
    return fillBoard(0,0,board,num_list)

def getFilledSquares(board):
    filled_squares = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                filled_squares.append((i,j))
    random.shuffle(filled_squares)
    return filled_squares

def getEmptySquares(board):
    empty_squares = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                empty_squares.append((i,j))
    return empty_squares

def removeNums(board):
    filled_squares = getFilledSquares(board)
    filled_squares_count = len(filled_squares)
    rounds = 7
    while rounds > 0 and filled_squares_count >= 17:
        row, col = filled_squares.pop()
        filled_squares_count -= 1
        removed_square = board[row][col]
        board[row][col] = '.'
        board_copy = copy.deepcopy(board)
        global solutions
        solutions = 0
        getSolutions(0,0,board_copy)
        if solutions != 1:
            board[row][col] = removed_square
            filled_squares_count += 1
            rounds -= 1
    return board

def generateSudoku():
    new_board = generateFilledBoard(std_num_list)
    without_squares = removeNums(new_board)
    return without_squares

#Pygame stuff
def drawBackground(screen):
    screen.fill((255,255,255))

def drawGrid(screen, board, left_margin, top_margin, txt_clr = (0,0,0)):
    for i in range(9):
        for j in range(9):
            box = board[i][j]
            pygame.draw.rect(screen, (0,0,0), (left_margin + j * gridsize, top_margin + i * gridsize, gridsize, gridsize), 1)

            if (i,j) in incorrect_nums:
                txt_clr = (255,0,0)
            else:
                txt_clr = (0,0,0)

            if box != '.':
                text = font.render(box, 1, txt_clr)
                screen.blit(text,(j*gridsize + 2 * gridsize//3,i*gridsize + gridsize//2))

    #draws thicker boarder around the 9 3x3 squares
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (0,0,0), (left_margin + j * gridsize * 3, top_margin + i * gridsize * 3, gridsize * 3, gridsize * 3), 3)

def drawSelection(screen, board, left_margin, top_margin, selected_coords):
    for i in range(9):
        for j in range(9):
            if (i,j) not in empty_squares:
                pygame.draw.rect(screen, (220,220,220), (left_margin + j * gridsize, top_margin + i * gridsize, gridsize, gridsize))
    i, j = selected_coords
    pygame.draw.rect(screen, (255,220,0), (left_margin + j * gridsize, top_margin + i * gridsize, gridsize, gridsize))

def drawButtons(screen):
    generate_board_button.drawButton(screen, 10, 8, 'Generate Board')
    solve_button.drawButton(screen, 10, 8, "Solve Board")
    x_button.drawButton(screen, 115, 0, '×', 35)

def drawKeypad(screen):
    for i in range(9):
        row = i // 3
        col = i % 3
        num_button = Button(col*85 + 600, row*85 + 40, 85, 85)
        num_button.drawButton(screen, 32, 20, str(i+1), 30)
    

############################# CLASSES ###############################

class Button():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.box = pygame.Rect(x,y,w,h)
    
    def drawButton(self, screen, left_margin, top_margin, txt = '', txt_size = 23):
        font = pygame.font.SysFont("Arial Black", txt_size)
        pygame.draw.rect(screen, (0,0,0), self.box, 3)
        text = font.render(txt, 1, (0,0,0))
        screen.blit(text,(self.x + left_margin,self.y + top_margin))

    def clickButton(self,mx,my):
        if self.box.collidepoint(mx,my):
            return True


############################# VARIABLES ###############################
clock = pygame.time.Clock()
std_num_list = ['1','2','3','4','5','6','7','8','9']

screen = pygame.display.set_mode((900,600))
gridsize = 60
fps = 30
font = pygame.font.SysFont("Arial Black", gridsize//2)

x_button = Button(600,300,255,50)
generate_board_button = Button(600,455,255,50)
solve_button = Button(600,510,255,50)
check_button = Button(600,510,255,50)

board = [['.' for i in range(9)] for j in range(9)]
empty_squares = getEmptySquares(board)
current_num = 0
selected_coords = (-10,-10)
incorrect_nums = set([])

############################# MAIN GAME LOOP ###############################
while True:
    for event in pygame.event.get():
        mx, my = pygame.mouse.get_pos()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if generate_board_button.clickButton(mx,my):
                board = generateSudoku()
                empty_squares = getEmptySquares(board)
                incorrect_nums.clear()
                
            if solve_button.clickButton(mx,my):
                solvePygame(0,0, board, std_num_list)
            
            if x_button.clickButton(mx,my):
                if selected_coords in empty_squares:
                    board[selected_coords[0]][selected_coords[1]] = '.'
                    incorrect_nums.discard(selected_coords)

            #places number on board
            for i in range(9):
                row = i // 3
                col = i % 3
                if mx in range(col*85 + 600, col*85 + 600 + 85) and my in range(row*85 + 40, row*85 + 40 + 85):
                    if selected_coords in empty_squares and 81 - len(empty_squares) > 0:
                        if isValid(selected_coords[0], selected_coords[1], str(i+1), board):
                            incorrect_nums.discard(selected_coords)
                        else:
                            incorrect_nums.add(selected_coords)
                        board[selected_coords[0]][selected_coords[1]] = str(i+1)

            #selects square on board
            for i in range(9):
                for j in range(9):
                    if mx in range(20 + j * gridsize, 20 + j * gridsize + gridsize) and my in range(20 + i * gridsize, 20 + i * gridsize + gridsize) and (i,j) in empty_squares:
                        selected_coords = (i,j)
            
    drawBackground(screen)
    drawSelection(screen, board, 20, 20, selected_coords)
    drawGrid(screen, board, 20, 20)
    drawButtons(screen)
    drawKeypad(screen)
    pygame.display.update()
    clock.tick(fps)