import copy
#
#
# def transform_to_dict(board):
#     ret = {}
#
#     for y in range(7):
#         for x in range(7):
#             ret[x, y] = board[y][x]
#
#     return ret
#
#
# def transform_to_list(list_dic):
#     ret = []
#
#     for board in list_dic:
#         new_board = [[0] * 7 for _ in range(7)]
#
#         for y in range(7):
#             for x in range(7):
#                 new_board[y][x] = board[x, y]
#
#         ret.append(new_board)
#
#     return ret
#
#
# def is_won(board):
#     count = 0
#     for item in board:
#         if board[item] == 1:
#             count += 1
#             if count > 1:
#                 return False
#
#     if board[3, 3] == 1:
#         return True
#
#     return False
#
#
# def solve(board, store_boards, out, skip):
#     if skip[0] == 1:
#         return 1
#
#     if is_won(board):
#         out += copy.deepcopy(store_boards)
#         skip[0] = 1
#         return 1
#
#     else:
#         for item in board:
#             if item[0] < 5 and board[item] == 1 and board[item[0] + 2, item[1]] == 0 and \
#                     board[item[0] + 1, item[1]] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0] + 2, item[1]] = 1
#                 new[item[0] + 1, item[1]] = 0
#
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     solve(new, store_boards, out, skip)
#                     store_boards.remove(new)
#
#             if item[0] > 1 and board[item] == 1 and board[item[0] - 2, item[1]] == 0 \
#                     and board[item[0] - 1, item[1]] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0] - 2, item[1]] = 1
#                 new[item[0] - 1, item[1]] = 0
#
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     solve(new, store_boards, out, skip)
#                     store_boards.remove(new)
#
#             if item[1] < 5 and board[item] == 1 and board[item[0], item[1] + 2] == 0 and \
#                     board[item[0], item[1] + 1] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0], item[1] + 2] = 1
#                 new[item[0], item[1] + 1] = 0
#
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     solve(new, store_boards, out, skip)
#                     store_boards.remove(new)
#
#             if item[1] > 1 and board[item] == 1 and board[item[0], item[1] - 2] == 0 \
#                     and board[item[0], item[1] - 1] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0], item[1] - 2] = 1
#                 new[item[0], item[1] - 1] = 0
#
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     solve(new, store_boards, out, skip)
#                     store_boards.remove(new)
#
#         return 1
#
#
# def solver(board):
#     board = transform_to_dict(board)
#     store_boards = []
#     out = [board]
#     skip = [0]
#     solve(board, store_boards, out, skip)
#
#     for k1, v1 in out[0].items():
#         print(v1, end=" ")
#
#         if k1[0] == 6:
#             print()
#
#     print()
#
#     out = transform_to_list(out)
#
#     for i in out[0]:
#         print(*i)
#
#     return out
#
#
# self_board = [[-1, -1, 0, 0, 0, -1, -1],
#               [-1, -1, 0, 0, 0, -1, -1],
#               [0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 1, 1, 0],
#               [0, 0, 0, 0, 0, 0, 0],
#               [-1, -1, 0, 0, 0, -1, -1],
#               [-1, -1, 0, 0, 0, -1, -1]]
#
# solver(self_board)

# ============================


def transform_to_dict(board):
    return {(y, x): board[y][x] for y in range(7) for x in range(7)}


def is_won(board):
    return list(board.values()).count(1) == 1 and board[3, 3] == 1


# def solve(board, store_boards, store_moves, skip, out):
#     if skip[0] == 1:
#         return 1
#
#     if is_won(board):
#         out += copy.deepcopy(store_moves)
#         skip[0] = 1
#
#     else:
#         for item in board:
#             if item[0] < 5 and board[item] == 1 and board[item[0] + 2, item[1]] == 0 and \
#                     board[item[0] + 1, item[1]] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0] + 2, item[1]] = 1
#                 new[item[0] + 1, item[1]] = 0
#
#                 move = (item, (item[0] + 2, item[1]))
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     store_moves.append(move)
#                     solve(new, store_boards, store_moves, skip, out)
#                     store_moves.remove(move)
#                     store_boards.remove(new)
#
#             if item[0] > 1 and board[item] == 1 and board[item[0] - 2, item[1]] == 0 \
#                     and board[item[0] - 1, item[1]] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0] - 2, item[1]] = 1
#                 new[item[0] - 1, item[1]] = 0
#
#                 move = (item, (item[0] - 2, item[1]))
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     store_moves.append(move)
#                     solve(new, store_boards, store_moves, skip, out)
#                     store_moves.remove(move)
#                     store_boards.remove(new)
#
#             if item[1] < 5 and board[item] == 1 and board[item[0], item[1] + 2] == 0 and \
#                     board[item[0], item[1] + 1] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0], item[1] + 2] = 1
#                 new[item[0], item[1] + 1] = 0
#
#                 move = (item, (item[0], item[1] + 2))
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     store_moves.append(move)
#                     solve(new, store_boards, store_moves, skip, out)
#                     store_moves.remove(move)
#                     store_boards.remove(new)
#
#             if item[1] > 1 and board[item] == 1 and board[item[0], item[1] - 2] == 0 \
#                     and board[item[0], item[1] - 1] == 1:
#                 new = copy.deepcopy(board)
#                 new[item] = 0
#                 new[item[0], item[1] - 2] = 1
#                 new[item[0], item[1] - 1] = 0
#
#                 move = (item, (item[0], item[1] - 2))
#                 if new not in store_boards:
#                     store_boards.append(new)
#                     store_moves.append(move)
#                     solve(new, store_boards, store_moves, skip, out)
#                     store_moves.remove(move)
#                     store_boards.remove(new)
#
#         return 1


def solve(board, store_boards, store_moves, skip, out):
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
                    solve(new, store_boards, store_moves, skip, out)
                    store_boards.remove(new)

            if item[0] > 1 and board[item] == 1 and board[item[0] - 2, item[1]] == 0 \
                    and board[item[0] - 1, item[1]] == 1:
                new = copy.deepcopy(board)
                new[item] = 0
                new[item[0] - 2, item[1]] = 1
                new[item[0] - 1, item[1]] = 0

                if new not in store_boards:
                    store_boards.append(new)
                    solve(new, store_boards, store_moves, skip, out)
                    store_boards.remove(new)

            if item[1] < 5 and board[item] == 1 and board[item[0], item[1] + 2] == 0 and \
                    board[item[0], item[1] + 1] == 1:
                new = copy.deepcopy(board)
                new[item] = 0
                new[item[0], item[1] + 2] = 1
                new[item[0], item[1] + 1] = 0

                if new not in store_boards:
                    store_boards.append(new)
                    solve(new, store_boards, store_moves, skip, out)
                    store_boards.remove(new)

            if item[1] > 1 and board[item] == 1 and board[item[0], item[1] - 2] == 0 \
                    and board[item[0], item[1] - 1] == 1:
                new = copy.deepcopy(board)
                new[item] = 0
                new[item[0], item[1] - 2] = 1
                new[item[0], item[1] - 1] = 0

                if new not in store_boards:
                    store_boards.append(new)
                    solve(new, store_boards, store_moves, skip, out)
                    store_boards.remove(new)

        return 1


def solver(board):
    board = transform_to_dict(board)
    store_moves = []
    store_boards = []
    out = []
    skip = [0]
    solve(board, store_boards, store_moves, skip, store_moves)

    return out


if __name__ == "__main__":
    # self_board = [[-1, -1, 0, 0, 0, -1, -1],
    #               [-1, -1, 0, 0, 0, -1, -1],
    #               [0, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 0, 0, 1, 0],
    #               [0, 0, 0, 0, 1, 0, 0],
    #               [-1, -1, 0, 0, 1, -1, -1],
    #               [-1, -1, 0, 0, 0, -1, -1]]

    self_board = [[-1, -1, 1, 1, 1, -1, -1],
     [-1, -1, 1, 1, 1, -1, -1],
     [ 1,  1, 1, 1, 1,  1,  1],
     [ 1,  1, 1, 0, 1,  1,  1],
     [ 1,  1, 1, 1, 1,  1,  1],
     [-1, -1, 1, 1, 1, -1, -1],
     [-1, -1, 1, 1, 1, -1, -1]]

    print(solver(self_board))

