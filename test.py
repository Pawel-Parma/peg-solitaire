import copy


def transform_to_dict(board):
    return {(y, x): board[y][x] for y in range(7) for x in range(7)}


def transform_to_list(list_dic):
    return [[[board[y, x] for x in range(7)] for y in range(7)] for board in list_dic]


def is_won(board):
    return list(board.values()).count(1) == 1 and board[3, 3] == 1


def solve(board, store_boards, out, skip):
    if skip[0] == 1:
        return 1

    if is_won(board):
        out += copy.deepcopy(store_boards)
        skip[0] = 1
        return 1

    else:
        for item in board:
            if item[0] < 5 and board[item] == 1 and board[item[0] + 2, item[1]] == 0 and \
                    board[item[0] + 1, item[1]] == 1:
                new = copy.deepcopy(board)
                new[item] = 0
                new[item[0] + 2, item[1]] = 1
                new[item[0] + 1, item[1]] = 0

                if new not in store_boards:
                    store_boards.append(new)
                    solve(new, store_boards, out, skip)
                    store_boards.remove(new)

            if item[0] > 1 and board[item] == 1 and board[item[0] - 2, item[1]] == 0 \
                    and board[item[0] - 1, item[1]] == 1:
                new = copy.deepcopy(board)
                new[item] = 0
                new[item[0] - 2, item[1]] = 1
                new[item[0] - 1, item[1]] = 0

                if new not in store_boards:
                    store_boards.append(new)
                    solve(new, store_boards, out, skip)
                    store_boards.remove(new)

            if item[1] < 5 and board[item] == 1 and board[item[0], item[1] + 2] == 0 and \
                    board[item[0], item[1] + 1] == 1:
                new = copy.deepcopy(board)
                new[item] = 0
                new[item[0], item[1] + 2] = 1
                new[item[0], item[1] + 1] = 0

                if new not in store_boards:
                    store_boards.append(new)
                    solve(new, store_boards, out, skip)
                    store_boards.remove(new)

            if item[1] > 1 and board[item] == 1 and board[item[0], item[1] - 2] == 0 \
                    and board[item[0], item[1] - 1] == 1:
                new = copy.deepcopy(board)
                new[item] = 0
                new[item[0], item[1] - 2] = 1
                new[item[0], item[1] - 1] = 0

                if new not in store_boards:
                    store_boards.append(new)
                    solve(new, store_boards, out, skip)
                    store_boards.remove(new)

        return 1


def solver(board):
    board = transform_to_dict(board)
    store_boards = []
    out = [board]
    skip = [0]
    solve(board, store_boards, out, skip)

    for k1, v1 in out[0].items():
        print(v1, end=" ")

        if k1[1] == 6:
            print()

    print()
    out = transform_to_list(out)

    for i in out[0]:
        print(*i)

    return out


if __name__ == "__main__":
    self_board = [[-1, -1, 0, 0, 0, -1, -1],
                  [-1, -1, 0, 0, 0, -1, -1],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [-1, -1, 0, 0, 1, -1, -1],
                  [-1, -1, 0, 0, 0, -1, -1]]

    # self_board = [[-1, -1, 1, 1, 1, -1, -1],
    #  [-1, -1, 1, 1, 1, -1, -1],
    #  [ 1,  1, 1, 1, 1,  1,  1],
    #  [ 1,  1, 1, 0, 1,  1,  1],
    #  [ 1,  1, 1, 1, 1,  1,  1],
    #  [-1, -1, 1, 1, 1, -1, -1],
    #  [-1, -1, 1, 1, 1, -1, -1]]

    solver(self_board)

