import copy
from tkinter.constants import W
from graphics import *
from time import sleep


'''
gameoflife.py
Implementation of John Conway's Game of Life in Python
Roxy and Ako 
'''

'''  
RULES:
Any live cell with fewer than two live neighbours dies.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies.
Any dead cell with exactly three live neighbours becomes a live cell.
'''

def get_neighbor_states(board, x, y):
    'Takes a board and the x and y coordinates of a point on the board,'
    'finds how many neighbors are alive, and returns the amount of neighbors which are alive.'
    neighbors = [board[y - 1][x - 1], board[y - 1][x], board[y - 1][x + 1], board[y][x + 1], 
    board[y + 1][x + 1], board[y + 1][x], board[y + 1][x - 1], board[y][x - 1]]
    #print("getting neighbors")
    return sum(neighbors)


def game_loop(board):
    'Takes in a board and uses the data contained within to create the next generation of the game.'
    'Currently the entire board is iterated through, but perhaps creating a list of which pairs of'
    'coordinates point to which nodes are alive could allow for checking a subset of the board.'
    new_board = copy.deepcopy(board)
    for y in range(1, len(board) - 1): # got out of bounds errors checking neighbors without the -1
        for x in range(1, len(board[y]) - 1):
            alive_neighbors = get_neighbor_states(board, x, y)
            if board[y][x] == 1:
                if alive_neighbors == 2 or alive_neighbors == 3:
                    new_board[y][x] = 1
                else:
                    new_board[y][x] = 0
            elif board[y][x] == 0:
                if alive_neighbors == 3:
                    new_board[y][x] = 1
                else:
                    new_board[y][x] = 0
    return new_board


def standardize_board(board, window_width, cell_size):
    """
    Takes in the board, the width of the graphics window, and the size of each cell.
    The width and cell size variables should be taken from global constants.
    Returns a board which contains the same information as the input board, but padded with zeroes
    so it will fill the entire graphics window.
    """
    cell_amount = window_width//cell_size # constant that tells us what dimensions the return board should have
    padding = cell_amount - len(board) #amount of whitespace that needs to be filled
    
    # Check to make sure we're not trying to add whitespace to a board that doesn't need it
    #assert padding > -1, "board is too large"
    #assert padding > 0, "board is already standard size"
    
    # Initialize the first row of the return board with all zeroes as padding.
    # This row will be out of bounds as the edge of the board.
    return_board = [[0 for x in range(cell_amount + 2)]]
    # Loop to add rows to the return board, padded with empty space at the ends
    for row in board:
        temp_row = [0]
        for i in row:
            temp_row.append(i)
        for j in range(padding + 1):
            temp_row.append(0)
        return_board.append(temp_row)
    for k in range(padding + 1):
        return_board.append([0 for x in range(cell_amount + 2)])
    return return_board


def txt_to_board(filename):
    """
    Takes in the name of a text file, opens that file, and converts the text to integers to create a board.
    """
    infile = open(filename).readlines()
    # Remove newlines and split on commas from input file to get the board with string entries
    split_text = []
    for i in infile:
        split_text.append(i.split()[0].split(","))
    
    # Iterate through the 2d array to change the strings into ints to get a board
    for i in range(len(split_text)):
        for j in range(len(split_text[i])):
            split_text[i][j] = int(split_text[i][j])
    return split_text


def input(board, window_width, cell_size, window, limit):
    """
    A function that updates the array as squares are drawn by input
    """
    board_state = copy.deepcopy(board)
    for i in range(limit): # limit is the number of times user can draw squares 
        mouse = window.getMouse()
        x = mouse.getX()
        y = mouse.getY()
        a = x // cell_size * cell_size
        b = y // cell_size * cell_size
        c = a + cell_size
        d = b + cell_size
        square = Rectangle(Point(a, b), Point(c, d))
        square.setFill("black")
        square.draw(window)
        board_state[int(b // cell_size)][int(a // cell_size)] = 1
        #print(board_state[0], board_state[1])
        '''
        for each in board_state:
            lenght = len(each)
            print(lenght)
        '''
    return standardize_board(board_state, window_width, cell_size)


def draw_board(board, window_width, cell_size, window):
    """
    Draw initial state of the board from txt file on the graphics window
    """
    cell_amount = window_width // cell_size
    initial_board = copy.deepcopy(board)
    for i in range(1, cell_amount - 1):
        for j in range(1, cell_amount - 1):
            square = Rectangle(Point(i * cell_size, j * cell_size), Point(i * cell_size + cell_size, j * cell_size + cell_size))
            if initial_board[j][i] == 1:
                square.setFill("black")
                square.draw(window)
            else:
                square.setFill("white")
                square.setOutline("white")
    return initial_board


def update_graphics(logic_board, graphics_board, window, generations_number):
    """
    A version of game_loop with graphics drawing and updating
    """
    for i in range(generations_number):
        new_logic_board = copy.deepcopy(logic_board)
        update_array = []
        print(update_array)
        for y in range(1, 31): # we are hard coding the second value because it is breaking when we give len(board) - 1 
            for x in range(1, 31): # 31 is the expected value
                alive_neighbors = get_neighbor_states(logic_board, x, y)
                if logic_board[y][x] == 1:
                    if alive_neighbors != 2 and alive_neighbors != 3:
                        new_logic_board[y][x] = 0
                        cell = graphics_board[y][x]
                        cell.setFill("white")
                        cell.setOutline("white")
                        update_array.append(cell)
                elif logic_board[y][x] == 0:
                    if alive_neighbors == 3:
                        new_logic_board[y][x] = 1
                        cell = graphics_board[y][x]
                        cell.setFill("black")
                        cell.setOutline("black")
                        update_array.append(cell)

        for i in update_array:
            i.undraw()
            i.draw(window)
        logic_board = new_logic_board
        print(update_array)
        sleep(0.1)


def generate_graphics_board(board, cell_size):
    graphics_board = copy.deepcopy(board)
    for i in range(1, len(board) - 1):
        for j in range(1, len(board[i]) - 1):
            cell = Rectangle(Point((j - 1) * cell_size, (i - 1) * cell_size), Point(j * cell_size, i * cell_size))
            if board[i][j] == 0:
                cell.setFill("white")
                cell.setOutline("white")
            else:
                cell.setFill("black")
            graphics_board[i][j] = cell
    return graphics_board


def main():
    window_width = 900 # global variable 
    cell_size = 30 # global variable
    window = GraphWin("Game of Life", window_width, window_width) # graphics window 
    testboard = txt_to_board("testboard.txt") # extract the board from txt file as a 2d array
    standardized_board = standardize_board(testboard, window_width, cell_size)
    draw_board(standardized_board, window_width, cell_size, window) # draw the board on graphics window

    game_board = input(standardized_board, window_width, cell_size, window, 10) # draw new squares and update the board array
    new_graphics_board = generate_graphics_board(game_board, cell_size)
    startkey = window.getKey()
    update_graphics(game_board, new_graphics_board, window, 10) # play the game 
    stopkey = window.getKey() # press any key to close the graphics window
    window.close()   


main()