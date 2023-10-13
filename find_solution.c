#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <Python.h>


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
   Move* moves;
   int size;

} pMove;


Move NULL_MOVE = {.p1={.y = -1, .x = -1}, .p2={.y = -1, .x = -1}, .p3={.y = -1, .x = -1}};

Move* solution_array;
Move* solution_helper_array;
int solution_len;
int solution_curent_place = 0;
int solved = 0;

int count(int** board, int item) {
   int result = 16;

   for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 7; j++) {
         result += (int) board[i][j];
      }
   }

   return result;
 }

int is_won(int** board) {
   return count(board, 1) == 1 && board[3][3] == 1;
 }

void interact(int** board, Point p) {
   int y = p.y, x = p.x;
   board[y][x] = (int) (! board[y][x]);
}

Move process_move(Point p1, Point p3) {
   Move result;

   result.p1 = p1;
   result.p2.y = (p1.y == p3.y) ? p1.y : ((p1.y < p3.y) ? p1.y + 1 : p1.y - 1);
   result.p2.x = (p1.x == p3.x) ? p1.x : ((p1.x < p3.x) ? p1.x + 1 : p1.x - 1);
   result.p3 = p3;

   return result;
 }

int is_move_legal(int** board, Move move) {
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

void board_move(int** board, Move move) {
   interact(board, move.p1);
   interact(board, move.p2);
   interact(board, move.p3);
}

int** copy_board(int** board) {
   int **board_copy;
   board_copy = malloc(sizeof(int*) * 7);

   for (int i = 0; i < 7; i++) {
      board_copy[i] = malloc(sizeof(int) * 7);
      for (int j = 0; j < 7; j++) {
         board_copy[i][j] = board[i][j];
         }
      }

   return board_copy;
 }

pMove legal_moves(int** board) {
   Move* moves;
   moves = malloc(sizeof(Move));
   int current_place = 0;

   for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 7; j++) {
         if (board[i][j] == 1) {
            if (j > 1) {
               Point p1 = {.y = i, .x = j};
               Point p2 = {.y = i, .x = j - 2};
               Move processed_move = process_move(p1, p2);

               if (is_move_legal(board, processed_move) == 1) {
                  moves[current_place] = processed_move;
                  current_place++;
                  moves = realloc(moves, (current_place + 1) * sizeof(Move));
               }
            }

            if (j < 5) {
               Point p1 = {.y = i, .x = j};
               Point p2 = {.y = i, .x = j + 2};
               Move processed_move = process_move(p1, p2);

               if (is_move_legal(board, processed_move) == 1) {
                  moves[current_place] = processed_move;
                  current_place++;
                  moves = realloc(moves, (current_place + 1) * sizeof(Move));
               }
            }

            if (i > 1) {
               Point p1 = {.y = i, .x = j};
               Point p2 = {.y = i - 2, .x = j};
               Move processed_move = process_move(p1, p2);

               if (is_move_legal(board, processed_move) == 1) {
                  moves[current_place] = processed_move;
                  current_place++;
                  moves = realloc(moves, (current_place + 1) * sizeof(Move));
               }
            }

            if (i < 5) {
               Point p1 = {.y = i, .x = j};
               Point p2 = {.y = i + 2, .x = j};
               Move processed_move = process_move(p1, p2);

               if (is_move_legal(board, processed_move) == 1) {
                  moves[current_place] = processed_move;
                  current_place++;
                  moves = realloc(moves, (current_place + 1) * sizeof(Move));
               }
            }

         }
      }
   }

   pMove result = {.moves = moves, .size = current_place};
   return result;
}

int** rotate_right(int** board) {
   int **board_copy;
   board_copy = malloc(sizeof(int*) * 7);

   for (int i = 0; i < 7; i++) {
      board_copy[i] = malloc(sizeof(int) * 7);
      for (int j = 0; j < 7; j++) {
         board_copy[i][j] = board[6 - j][i];
         }
      }

   return board_copy;
 }

/*

def __solution(self, board_object):
    board_object_tuple = board_object.as_tuple()

    if self.solved or board_object_tuple in self.done_boards:
        return

    self.done_boards.add(board_object_tuple)

    for _ in range(3):
        board_object_tuple = rotate_2d_list_right(board_object_tuple)
        self.done_boards.add(board_object_tuple)

    for move in board_object.legal_moves():
        new_board_object = Board(board_object.as_list())
        new_board_object.move(move)
        self.solution_list_helper.append(move)

        if new_board_object.is_won() == 1:
            self.solved = 1
            self.solution_list = self.solution_list_helper.copy()

            return

        self.__solution(new_board_object)
        self.solution_list_helper.pop(-1)

    return

*/

void __solution(int **board) {
   if (solved == 1) {
      return;
   }

   //

   pMove moves_legal_help = legal_moves(board);
   Move* moves_legal = moves_legal_help.moves;
   int moves_legal_size = moves_legal_help.size;

   for (int i = 0; i < moves_legal_size; i++) {
      int** new_board = copy_board(board);
      board_move(new_board, moves_legal[i]);
      solution_helper_array[solution_curent_place] = moves_legal[i];
      solution_curent_place += 1;

      if (is_won(new_board) == 1) {
         solved = 1;
         memcpy(solution_array, solution_helper_array, sizeof(Move) * solution_len);
         return;
      }

      __solution(new_board);
      solution_helper_array[solution_curent_place] = NULL_MOVE;
      solution_curent_place -= 1;
      //for (int j = 0; j < 7; j++) free(new_board[j]);
      //free(new_board);
   }

   free(moves_legal);
   return;
 }

Move* Csolution(int** board) {
   solution_curent_place = 0;
   solved = 0;
   solution_len = count(board, 1) - 1;
   solution_array = malloc(sizeof(Move) * solution_len);
   solution_helper_array = malloc(sizeof(Move) * solution_len);

   __solution(board);

   return solution_array;
 }

int main() {
   int board[7][7] = {{-1, -1, 0, 0, 0, -1, -1},
                      {-1, -1, 0, 0, 0, -1, -1},
                      {0, 0, 0, 0, 0, 0, 0},
                      {0, 0, 0, 0, 1, 1, 0},
                      {0, 0, 0, 0, 0, 0, 0},
                      {-1, -1, 0, 0, 0, -1, -1},
                      {-1, -1, 0, 0, 0, -1, -1}};
   int** board_ptr;
   board_ptr = malloc(sizeof(int*) * 7);
   for (int i = 0; i < 7; i++) {
      board_ptr[i] = malloc(sizeof(int) * 7);
      for (int j = 0; j < 7; j++) {
         board_ptr[i][j] = board[i][j];
      }
   }

   printf("Show board:\n");
   for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 7; j++) {
         if (i > 1 && i < 5 && (j < 2 || j > 4)) {
            printf(" ");
         }

         printf("%d ", board_ptr[i][j]);
      }
      printf("\n");
   }

   int board_count = count(board_ptr, 1);
   printf("\nShow board count:\n%d\n", board_count);

   int board_won = is_won(board_ptr);
   printf("\nShow is won:\n%d\n\n", board_won);

   Point p1 = {.y = 5, .x = 4};
   Point p2 = {.y = 4, .x = 4};
   Point p3 = {.y = 3, .x = 4};
   interact(board_ptr, p1);
   interact(board_ptr, p2);
   interact(board_ptr, p3);
   printf("Show interact:\n");
   for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 7; j++) {
         if (i > 1 && i < 5 && (j < 2 || j > 4)) {
            printf(" ");
         }

         printf("%d ", board_ptr[i][j]);
      }
      printf("\n");
   }

   Move move = {.p1 = p1, .p2 = p2, .p3 = p3};
   int board_move_legal = is_move_legal(board_ptr, move);
   printf("\nShow if move legal:\n%d\n", board_move_legal);

   int** board_copy = copy_board(board_ptr);
   printf("\nShow board copy:\n");
   for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 7; j++) {
         if (i > 1 && i < 5 && (j < 2 || j > 4)) {
            printf(" ");
         }
         printf("%d ", board_copy[i][j]);
      }
      printf("\n");
   }

   pMove struct_moves = legal_moves(board_ptr);
   Move* board_legal_moves = struct_moves.moves;
   int board_legal_moves_size = struct_moves.size;
   printf("\nShow legal moves:\n");
   for (int i = 0; i < board_legal_moves_size; i++) {
      printf("(%d ", board_legal_moves[i].p1.y);
      printf("%d), (", board_legal_moves[i].p1.x);
      printf("%d ", board_legal_moves[i].p2.y);
      printf("%d), (", board_legal_moves[i].p2.x);
      printf("%d ", board_legal_moves[i].p3.y);
      printf("%d)\n", board_legal_moves[i].p3.x);
   }

   int** board_rotated = rotate_right(board_ptr);
   printf("\n\nShow rotated right:\n");
   for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 7; j++) {
         if (i > 1 && i < 5 && (j < 2 || j > 4)) {
            printf(" ");
         }
         printf("%d ", board_ptr[i][j]);
      }
      printf("\n");
   }
   printf("\n");
   for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 7; j++) {
         if (i > 1 && i < 5 && (j < 2 || j > 4)) {
            printf(" ");
         }
         printf("%d ", board_rotated[i][j]);
      }
      printf("\n");
   }

   Move* board_solution = Csolution(board_ptr);
   printf("\nShow solution:\n");
   for (int i = 0; i < 2; i++) {
      printf("(%d ", board_solution[i].p1.y);
      printf("%d), (", board_solution[i].p1.x);
      printf("%d ", board_solution[i].p2.y);
      printf("%d), (", board_solution[i].p2.x);
      printf("%d ", board_solution[i].p3.y);
      printf("%d)\n", board_solution[i].p3.x);
   }

   return 0;
}

