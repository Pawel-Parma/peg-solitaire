#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>


typedef struct {
    int y;
    int x;
} Point;

typedef struct {
    Point p1;
    Point p2;
    Point p3;
} Move;

typedef struct {
    void* ptr;
    int len;

} PtrL;


Move NULL_MOVE = {.p1={.y = -1, .x = -1}, .p2={.y = -1, .x = -1}, .p3={.y = -1, .x = -1}};
Move* solution_array;
Move* solution_array_h;
int solution_curent_place;
int solution_len;
int solved;


Move move_process(Point p1, Point p3); //

void board_print(int** board); //
int board_count(int** board, int item); //
int board_is_won(int** board); //
int** board_copy(int** board); //
int** board_rotate_right(int** board); //
void board_interact(int** board, Point p); // // ?&
void board_move(int** board, Move move); // //
int board_is_move_legal(int** board, Move move); //
PtrL board_legal_moves(int** board); //

void __solution(int** board, int depth); // // ?&
PtrL _solution(int** board); //
Move* solution(int** board); //


Move move_process(Point p1, Point p3) {
    Move result;

    result.p1 = p1;
    result.p2.y = (p1.y == p3.y) ? p1.y : ((p1.y < p3.y) ? p1.y + 1 : p1.y - 1);
    result.p2.x = (p1.x == p3.x) ? p1.x : ((p1.x < p3.x) ? p1.x + 1 : p1.x - 1);
    result.p3 = p3;

    return result;
}

void board_print(int** board) {
    for (int i = 0; i < 7; i++) {
        for (int j = 0; j < 7; j++) {
            if (board[i][j] != -1) {
                printf("%d ", board[i][j]);
            }
            else {
                printf("  ");
            }
        }

        printf("\n");
    }

    printf("\n");
}

int board_count(int** board, int item) {
    int result = 0;

    for (int i = 0; i < 7; i++) {
        for (int j = 0; j < 7; j++) {
            if (board[i][j] == item) {
                result += 1;
            }
        }
    }

    return result;
}

int board_is_won(int** board) {
    return board_count(board, 1) == 1 && board[3][3] == 1;
}

int** board_copy(int** board) {
    int** result;
    result = malloc(sizeof(int*) * 7);

    for (int i = 0; i < 7; i++) {
        result[i] = malloc(sizeof(int) * 7);
        memcpy(result[i], board[i], sizeof(int) * 7);
    }

    return result;
}

int** board_rotate_right(int** board) {
    int** copy; int** result;
    copy = malloc(sizeof(int*) * 7);
    result = malloc(sizeof(int*) * 7);

    for (int i = 0; i < 7; i++) {
        copy[i] = malloc(sizeof(int) * 7);
        for (int j = 0; j < 7; j++) {
            copy[i][j] = board[6 - j][i];
        }
    }

    for (int i = 0; i < 7; i++) {
        result[i] = malloc(sizeof(int) * 7);
        memcpy(result[i], copy[i], sizeof(int) * 7);
    }

    return result;
}

void board_interact(int** board, Point p) {
    int y = p.y, x = p.x;
    int v;

    printf("\n<Board 3> %d %d\n", y, x);
    board_print(board);

    // printf("\nBPTRPTR %d\n", board[y][x]);

    //memcpy(&v, &board[y][x], sizeof(int));
    //printf("%d\n", v);

    printf("");

    //v = !v;

    printf("");

   //board[y][x] = v;
}

void board_move(int** board, Move move) {
    printf("\n<Board 1>\n");
    board_print(board);

    board_interact(board, move.p1);
    board_interact(board, move.p2);
    board_interact(board, move.p3);

    printf("<Board 2>\n");
    board_print(board);
}

int board_is_move_legal(int** board, Move move) {
    int y1 = move.p1.y, x1 = move.p1.x;
    int y2 = move.p2.y, x2 = move.p2.x;
    int y3 = move.p3.y, x3 = move.p3.x;

    if (board[y1][x1] == 1) {
        if (board[y2][x2] == 1) {
            if (board[y3][x3] == 0) {
                if ((abs(y1 - y3) == 2) ^ (abs(x1 - x3) == 2)) {
                    return 1;
                }
            }
        }
    }

    return 0;
}

PtrL board_legal_moves(int** board) {
    Move* moves;
    moves = malloc(sizeof(Move));
    int current_place = 0;

    for (int i = 0; i < 7; i++) {
        for (int j = 0; j < 7; j++) {
            if (board[i][j] == 1) {
                if (j > 1) {
                    Point p1 = {.y = i, .x = j};
                    Point p2 = {.y = i, .x = j - 2};
                    Move move = move_process(p1, p2);

                    if (board_is_move_legal(board, move) == 1) {
                        moves[current_place] = move;
                        current_place++;
                        moves = realloc(moves, (current_place + 1) * sizeof(Move));
                    }
                }

                if (j < 5) {
                    Point p1 = {.y = i, .x = j};
                    Point p2 = {.y = i, .x = j + 2};
                    Move move = move_process(p1, p2);

                    if (board_is_move_legal(board, move) == 1) {
                        moves[current_place] = move;
                        current_place++;
                        moves = realloc(moves, (current_place + 1) * sizeof(Move));
                    }
                }

                if (i > 1) {
                    Point p1 = {.y = i, .x = j};
                    Point p2 = {.y = i - 2, .x = j};
                    Move move = move_process(p1, p2);

                    if (board_is_move_legal(board, move) == 1) {
                        moves[current_place] = move;
                        current_place++;
                        moves = realloc(moves, (current_place + 1) * sizeof(Move));
                    }
                }

                if (i < 5) {
                    Point p1 = {.y = i, .x = j};
                    Point p2 = {.y = i + 2, .x = j};
                    Move move = move_process(p1, p2);

                    if (board_is_move_legal(board, move) == 1) {
                        moves[current_place] = move;
                        current_place++;
                        moves = realloc(moves, (current_place + 1) * sizeof(Move));
                    }
                }
            }
        }
    }

   PtrL result = {.ptr = moves, .len = current_place};
   return result;
}


void __solution(int** board, int depth) {
    if (solved == 1 || depth > 4) {
        return;
   }

   //

   PtrL moves_legal_help = board_legal_moves(board);
   Move* moves_legal = moves_legal_help.ptr;
   int moves_legal_size = moves_legal_help.len;

   for (int i = 0; i < moves_legal_size; i++) {
      int** new_board = board_copy(board);
      board_move(new_board, moves_legal[i]);
      solution_array_h[solution_curent_place] = moves_legal[i];
      solution_curent_place += 1;

      if (board_is_won(new_board) == 1) {
         solved = 1;
         memcpy(solution_array, &solution_array_h, sizeof(Move) * solution_len); // Dont know if it should be with or without "&"
         return;
      }

      __solution(new_board, depth + 1);
      solution_array_h[solution_curent_place] = NULL_MOVE;
      solution_curent_place -= 1;
   }

   return;


}

PtrL _solution(int** board) {
    solved = 0;
    solution_curent_place = 0;
    solution_len = board_count(board, 1) - 1;
    solution_array = malloc(sizeof(Move) * solution_len);
    solution_array_h = malloc(sizeof(Move) * solution_len);

    __solution(board, 0);
    PtrL result = {.ptr = solution_array, .len = solution_len};

    return result;
}

Move* solution(int** board) {
    PtrL result = _solution(board);

    return result.ptr;
}


int main() {
   clock_t start = clock();

    /*
   int board[7][7] = {{-1, -1,  0,  0,  0, -1, -1},
                      {-1, -1,  0,  0,  0, -1, -1},
                      { 0,  0,  0,  0,  1,  0,  0},
                      { 1,  1,  1,  0,  1,  1,  0},
                      { 1,  1,  0,  1,  1,  1,  1},
                      {-1, -1,  1,  1,  1, -1, -1},
                      {-1, -1,  1,  1,  0, -1, -1}}; */

    int board[7][7] = {{-1, -1,  0,  0,  0, -1, -1},
                       {-1, -1,  0,  0,  0, -1, -1},
                       { 0,  0,  0,  0,  0,  0,  0},
                       { 0,  0,  0,  0,  0,  1,  0},
                       { 0,  0,  0,  0,  1,  0,  0},
                       {-1, -1,  0,  0,  1, -1, -1},
                       {-1, -1,  0,  0,  0, -1, -1}};

    int** board_ptr;
    board_ptr = malloc(sizeof(int*) * 7);

    printf("\nBoard:\n");

    for (int i = 0; i < 7; i++) {
        board_ptr[i] = malloc(sizeof(int) * 7);

        for (int j = 0; j < 7; j++) {
            board_ptr[i][j] = board[i][j];
        }
    }
    board_print(board_ptr);

    int** copy = board_copy(board_ptr);
    printf("Copy:\n");
    board_print(copy);

    int** rotate = board_rotate_right(copy);
    printf("Rotate:\n");
    board_print(rotate);

    Point p = {.y = 3, .x = 3};
    board_interact(rotate, p);
    printf("Interact:\n");
    board_print(rotate);

    printf("Solution\n\n");
    int solution_len = board_count(board_ptr, 1) - 1;
    Move* board_solution = solution(board_ptr);
    printf("\n\n");

    printf("Solution:\n", solution_len);
    for (int i = 0; i < solution_len; i++) {
        printf("%2d | ", i + 1);
        printf("(%d ", board_solution[i].p1.y);
        printf("%d); ", board_solution[i].p1.x);
        printf("(%d ", board_solution[i].p2.y);
        printf("%d); ", board_solution[i].p2.x);
        printf("(%d ", board_solution[i].p3.y);
        printf("%d);\n", board_solution[i].p3.x);
        board_move(board_ptr, board_solution[i]);
    }

    printf("\nSolved\n:");
    board_print(board_ptr);

    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Execution time\n%lf s\n", time_spent);

    return 0;
}