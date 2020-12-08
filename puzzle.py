import random
from tkinter import Frame, Label, CENTER
import colors as c

def new_riddle(n):
    matrix = []


    for i in range(n):
        matrix.append([0] * n)
    return matrix

def add_twotiles(matrix):
    a = random.randint(0, len(matrix)-1)
    b = random.randint(0, len(matrix)-1)
    while(matrix[a][b] != 0):
        a = random.randint(0, len(matrix)-1)
        b = random.randint(0, len(matrix)-1)
    matrix[a][b] = 2
    return matrix

def reverse(matrix):
    new = []
    for i in range(len(matrix)):
        new.append([])
        for j in range(len(matrix[0])):
            new[i].append(matrix[i][len(matrix[0])-j-1])
    return new

def transpose(matrix):
    new = []
    for i in range(len(matrix[0])):
        new.append([])
        for j in range(len(matrix)):
            new[i].append(matrix[j][i])
    return new

def wrapping(matrix):
    new = []
    for j in range(c.TILE_LEN):
        p_new = []
        for i in range(c.TILE_LEN):
            p_new.append(0)
        new.append(p_new)
    game = False
    for i in range(c.TILE_LEN):
        count = 0
        for j in range(c.TILE_LEN):
            if matrix[i][j] != 0:
                new[i][count] = matrix[i][j]
                if j != count:
                    game = True
                count += 1
    return (new, game)


def merge(matrix):
    game = False
    for i in range(c.TILE_LEN):
        for j in range(c.TILE_LEN-1):
            if matrix[i][j] == matrix[i][j+1] and matrix[i][j] != 0:
                matrix[i][j] *= 2
                matrix[i][j+1] = 0
                game = True
    return (matrix, game)

def left(puzzle):
    print("KEY_LEFT")
    puzzle, game = wrapping(puzzle)
    mat = merge(puzzle)
    puzzle = mat[0]
    game = game or mat[1]
    puzzle = wrapping(puzzle)[0]
    return (puzzle, game)


def right(puzzle):
    print("KEY_RIGHT")
    puzzle = reverse(puzzle)
    puzzle, game = wrapping(puzzle)
    mat = merge(puzzle)
    puzzle = mat[0]
    game = game or mat[1]
    puzzle = wrapping(puzzle)[0]
    puzzle = reverse(puzzle)
    return (puzzle, game)

def up(puzzle):
    print("KEY_UP")
    puzzle = transpose(puzzle)
    puzzle, game = wrapping(puzzle)
    mat = merge(puzzle)
    puzzle = mat[0]
    game = game or mat[1]
    puzzle = wrapping(puzzle)[0]
    puzzle = transpose(puzzle)
    return (puzzle, game)


def down(puzzle):
    print("backward")
    puzzle = reverse(transpose(puzzle))
    puzzle, game = wrapping(puzzle)
    mat = merge(puzzle)
    puzzle = mat[0]
    game = game or mat[1]
    puzzle = wrapping(puzzle)[0]
    puzzle = transpose(reverse(puzzle))
    return (puzzle, game)

def position(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2048:
                return 'win'
    for i in range(len(matrix)-1):

        for j in range(len(matrix[0])-1):
            if matrix[i][j] == matrix[i+1][j] or matrix[i][j+1] == matrix[i][j]:
                return 'move available'

    for i in range(len(matrix)): 
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                return 'move available'

    for k in range(len(matrix)-1):
        if matrix[len(matrix)-1][k] == matrix[len(matrix)-1][k+1]:
            return 'move available'

    for j in range(len(matrix)-1):  
        if matrix[j][len(matrix)-1] == matrix[j+1][len(matrix)-1]:
            return 'move available'
    return 'lose'

class puzzleGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.main_tile =Frame(self, width=10, height=10)
        self.main_tile.grid(pady=(80, 0))
        self.master.bind("<Key>", self.backward)

        self.commands = {c.KEY_UP:up, c.KEY_DOWN:down,c.KEY_LEFT:left, c.KEY_RIGHT:right}
        
        self.grid_cells = []
        self.init_tile()
        self.init_matrix()
        self.update_tile()
        self.mainloop()

    def init_tile(self):
        background = Frame(self,bg=c.BGC_PUZZLE,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.TILE_LEN):
            grid_row = []
            for j in range(c.TILE_LEN):
                cell = Frame(background, bg=c.BGC_CELL_EMPTY,
                             width=c.SIZE / c.TILE_LEN,
                             height=c.SIZE / c.TILE_LEN)
                cell.grid(row=i, column=j, padx=c.TILE_PADDING,
                          pady=c.TILE_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BGC_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = new_riddle(c.TILE_LEN)
        self.history_matrixs = list()
        self.matrix =add_twotiles(self.matrix)
        

    def update_tile(self):
        for i in range(c.TILE_LEN):
            for j in range(c.TILE_LEN):
                current_num = self.matrix[i][j]
                if current_num == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BGC_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        current_num), bg=c.BACKGROUND_COLOR[current_num],
                        fg=c.CELL_COLOR[current_num])
        self.update_idletasks()

    def backward(self, event):
        key = repr(event.char)
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_tile()
            print('backward:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, game = self.commands[repr(event.char)](self.matrix)
            if game:
                self.matrix = add_twotiles(self.matrix)
                self.history_matrixs.append(self.matrix)
                self.update_tile()
                game = False
        if position(self.matrix) == 'win':
            self.grid_cells[2][1].configure(text="You")
            self.grid_cells[2][2].configure(text="Win!")
        if position(self.matrix) == 'lose':
            self.grid_cells[2][1].configure(text="You")
            self.grid_cells[2][2].configure(text="Lose!")


puzzlegrid = puzzleGrid()
