import copy


class BoardIterator:
    def __init__(self, board_object):
        self.board = board_object.board
        self.board_len = len(self.board)
        self.index = 0

    def __next__(self):
        if self.index < self.board_len:
            result = self.board[self.index]
            self.index += 1
            return result

        raise StopIteration


class Board:
    def __init__(self, board=None):
        if board is None:

            self.board = [[-1, -1, 0, 0, 0, -1, -1],
                          [-1, -1, 0, 0, 0, -1, -1],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [-1, -1, 0, 0, 0, -1, -1],
                          [-1, -1, 0, 0, 0, -1, -1]]

        else:
            self.board = board

        self.size = 7
        self.solution_list = []
        self.skip = 0
        self.solved = 0

    def interact(self, y, x):
        self.solved = 0
        self.board[y][x] = int(not self.board[y][x])

    def count(self, item):
        return sum(self.board, []).count(item)

    def is_won(self):
        return 1 if self.count(1) == 1 and self.board[3][3] == 1 else 0

    def is_end(self):
        return 0 if self.legal_moves() else 1

    def is_board_legal(self):
        return not self.board[3][3]

    def is_legal_to_start(self):
        return self.count(1) > 1 and self.is_board_legal()

    def is_empty(self):
        return not bool(self.count(1))

    def reset_board(self):
        self.solved = 0
        self.board = [[-1, -1, 0, 0, 0, -1, -1],
                      [-1, -1, 0, 0, 0, -1, -1],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [-1, -1, 0, 0, 0, -1, -1],
                      [-1, -1, 0, 0, 0, -1, -1]]

    def is_move_legal(self, move):
        (y1, x1), (y2, x2), (y3, x3) = process_move(move)

        if self.board[y1][x1] == 1:
            if self.board[y2][x2] == 1:
                if self.board[y3][x3] == 0:
                    if (abs(y1 - y3) == 2) ^ (abs(x1 - x3) == 2):
                        return 1

        return 0

    def legal_moves(self):
        legal_moves = []

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    if j > 1:
                        if self.is_move_legal(((i, j), (i, j - 2))):
                            legal_moves.append(((i, j), (i, j - 2)))

                    if j < 5:
                        if self.is_move_legal(((i, j), (i, j + 2))):
                            legal_moves.append(((i, j), (i, j + 2)))

                    if i > 1:
                        if self.is_move_legal(((i, j), (i - 2, j))):
                            legal_moves.append(((i, j), (i - 2, j)))
                    if i < 5:
                        if self.is_move_legal(((i, j), (i + 2, j))):
                            legal_moves.append(((i, j), (i + 2, j)))

        return legal_moves

    def move(self, move):
        if self.is_move_legal(move):
            self.solved = 0
            (y1, x1), (y2, x2), (y3, x3) = process_move(move)
            self.interact(y1, x1)
            self.interact(y2, x2)
            self.interact(y3, x3)
            return 1

        return 0

    def __solution_helper(self, board_object, board_level, solution):
        if self.skip == 1:
            return solution

        for i, move in enumerate(board_object.legal_moves()):
            new_board_object = Board(board_object.as_list())
            new_board_object.move(move)
            solution.append(move)

            if new_board_object.is_won() == 1:
                self.skip = self.solved = 1
                self.solution_list = copy.deepcopy(solution)
                return solution

            else:
                self.__solution_helper(new_board_object, board_level + 1, solution)
                try:
                    self.solution_list.pop(-1)

                except:
                    pass

        return solution

    def solution(self):
        self.skip = 0
        self.solved = 0
        solution = []

        self.__solution_helper(self, 1, solution)
        return self.solution_list

    def solve(self):
        solution = self.solution_list if self.solved == 1 else self.solution()
        for i in solution:
            self.move(i)

    def __str__(self):
        ret = "\n   A B C D E F G \n"

        for i, j in enumerate(self.board):
            ret += f"{i + 1}  "

            for k in j:
                if k == -1:
                    ret += "  "

                else:
                    ret += f"{k} "

            ret += f" {i + 1}"
            ret += "\n"

        ret += "   A B C D E F G\n"

        return ret

    def as_list(self):
        return [[int(x) for x in y] for y in self.board]

    def as_dict(self):
        return {(y, x): self.board[y][x] for y in range(7) for x in range(7)}

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return BoardIterator(self)

    def __getitem__(self, item):
        if type(item) == tuple:
            y, x = item
            return self.board[y][x]

        elif type(item) == int:
            return self.board[item]

        else:
            raise NotImplementedError


def process_move(move):
    (y1, x1), (y3, x3) = move[0], move[-1]

    y2 = y1 if y1 == y3 else y1 + 1 if y1 < y3 else y1 - 1
    x2 = x1 if x1 == x3 else x1 + 1 if x1 < x3 else x1 - 1

    return (y1, x1), (y2, x2), (y3, x3)


def translate_move(move):
    (y1, x1), (y3, x3) = process_move(move)[::2]

    translated_move = f"{chr(65 + x1)}{7 - y1}"
    adder = "L" if y1 == y3 and x1 > x3 else "R" if y1 == y3 else ""
    adder += "U" if x1 == x3 and y1 > y3 else "D" if x1 == x3 else ""
    translated_move += adder

    return translated_move


def translate_moves(moves):
    for move in moves:
        yield translate_move(move)
