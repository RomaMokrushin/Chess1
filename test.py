WHITE = 0
BLACK = 1


# print('Вас приветствует игра шахматы! Напишите play_chess() чтобы начать!')


def play_chess():
    board = Board()
    flag = True
    while True:
        if flag:
            print(print_board(board))
            flag = False
        print("Команда 'ex' завершает игру")
        print("Команда 'move' принимает row, col и row1, col1 (из row, col, сходить в row1, col1")
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        comand = input()
        if comand == 'ex':
            break
        if comand != 'move':
            print('Неизвестная команда! Попробуйте снова!')
            print(print_board(board))
            continue
        cords = input().split()
        row, col, row1, col1 = int(cords[0]), int(cords[1]), int(cords[2]), int(cords[3])
        if board.move_piece(row, col, row1, col1):
            print('Ход сделан')
            print(print_board(board))
        else:
            print('Неправильные координаты или невозможный ход! Попробуйте снова!')
            print(print_board(board))


class Figure:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def get_color(self):
        return self.color


class Pawn(Figure):
    def char(self):
        return 'P'

    def can_move(self, row, col):
        if self.col != col:
            return False
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if self.row + direction == row:
            return True
        if self.row == start_row and self.row + 2 * direction == row:
            return True
        return False


class Knight(Figure):
    def char(self):
        return 'N'

    def can_move(self, row, col):
        if not correct_cords(row, col):
            return False
        if self.row == row or self.col == col:
            return False
        if abs(self.row - row) + abs(self.col - col) != 3:
            return False
        return True


class Bishop(Figure):
    def char(self):
        return 'B'

    def can_move(self, row, col):
        if not correct_cords(row, col):
            return False
        if self.row == row or self.col == col:
            return False
        if abs(self.row - row) != abs(self.col - col):
            return False
        return True


class Rook(Figure):
    def char(self):
        return 'R'

    def can_move(self, row, col):
        if self.row != row and self.col != col:
            return False
        return True


class Queen(Figure):
    def char(self):
        return 'Q'

    def can_move(self, row, col):
        if not correct_cords(row, col):
            return False
        if self.row == row and self.col == col:
            return False
        if abs(self.row - row) != abs(self.col - col) and (
                self.row != row and self.col != col):
            return False
        return True


class King(Figure):
    def char(self):
        return 'K'

    def can_move(self, row, col):
        if not correct_cords(row, col):
            return False
        if self.row == row and self.col == col:
            return False
        if abs(self.row - row) > 1 or abs(self.row - row):
            return False
        return True


def print_board(board):
    string = '     +----+----+----+----+----+----+----+----+\n'
    for i in range(7, -1, -1):
        string = string + '  ' + str(i) + '  '
        for j in range(8):
            string = string + '| ' + board.cell(i, j) + ' '
        string = string + '|\n'
        string = string + '     +----+----+----+----+----+----+----+----+\n'
    string = string + '        '
    for i in range(7):
        string = string + str(i) + '    '
    string = string + '7 \n'
    return string


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = list()
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0][0], self.field[0][7] = Rook(0, 0, WHITE), Rook(0, 7, WHITE)
        self.field[7][0], self.field[7][7] = Rook(7, 0, BLACK), Rook(7, 7, BLACK)
        self.field[0][1], self.field[0][6] = Knight(0, 1, WHITE), Knight(0, 6, WHITE)
        self.field[7][1], self.field[7][6] = Knight(7, 1, BLACK), Knight(7, 6, BLACK)
        self.field[0][2], self.field[0][5] = Bishop(0, 2, WHITE), Bishop(0, 5, WHITE)
        self.field[7][2], self.field[7][5] = Bishop(7, 2, BLACK), Bishop(7, 5, BLACK)
        self.field[0][3], self.field[0][4] = Queen(0, 3, WHITE), King(0, 4, WHITE)
        self.field[7][3], self.field[7][4] = Queen(7, 3, BLACK), King(7, 4, BLACK)
        for i in range(8):
            self.field[1][i] = Pawn(1, i, WHITE)
        for i in range(8):
            self.field[6][i] = Pawn(6, i, BLACK)

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        if color == WHITE:
            color_figure = 'w'
        else:
            color_figure = 'b'
        return color_figure + piece.char()

    def move_piece(self, row, col, row1, col1):
        if not correct_cords(row, col) or not correct_cords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if not piece.can_move(row1, col1):
            return False
        if isinstance(piece, King) and is_under_attack(self.field, row1, col1, piece.get_color()):
            return False
        if piece.row - row1 != 0:
            rrow = (piece.row - row1) // abs(piece.row - row1)
        else:
            rrow = 0
        if piece.col - col1 != 0:
            ccol = (piece.col - col1) // abs(piece.col - col1)
        else:
            ccol = 0
        if abs(piece.row - row1) >= abs(piece.col - col1):
            rnge = abs(piece.row - row1)
        else:
            rnge = abs(piece.col - col1)
        if not isinstance(piece, Knight):
            for i in range(1, abs(rnge) + 1):
                if self.field[piece.row - rrow * i][piece.col - ccol * i]:
                    return False
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if isinstance(self.field[i][j], King) and is_under_attack(self.field, i, j, opponent(self.color)):
                    if self.field[i][j].get_color() == self.color:
                        return False
        self.field[row][col] = None
        self.field[row1][col1] = piece
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
        return True

    def __str__(self):
        return print_board(self)


def correct_cords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def is_under_attack(field, row, col, color):
    for i in field:
        for j in i:
            if j:
                if j.can_move(row, col) and j.get_color() == color:
                    return True
    return False


def help():
    print("Команда 'exit' завершает игру")
    print("Команда 'move' принимает row, col и row1, col1 (из row, col, сходить в row1, col1")
