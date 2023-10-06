#include <stdio.h>
#include <stdlib.h>

// #include <iostream>
// using namespace std;

typedef struct {
    int y;
    int x;
} Point;

typedef struct {
    Point p1;
    Point p2;
    Point p3;
} Move;


Move process_move(Point move[2]) {
    Move result;

    result.p1 = move[0];
    result.p3 = move[1];
    result.p2.y = (result.p1.y == result.p3.y) ? result.p1.y : ((result.p1.y < result.p3.y) ? result.p1.y + 1 : result.p1.y - 1);
    result.p2.x = (result.p1.x == result.p3.x) ? result.p1.x : ((result.p1.x < result.p3.x) ? result.p1.x + 1 : result.p1.x - 1);

    return result;
}

int is_move_legal(int board[7][7], Move move) {
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

void swap(int *x, int *y){
    int temp = *x;
    *x = *y;
    *y = temp;
}
int rotate_2d_array_right(int mat[7][7]){
   int n=4;

   for(int i = 0; i < 7; i++){
     for(int j = i + 1; j < 7; j++)
         swap(&mat[i][j], &mat[j][i]);
    }

   for(int i = 0; i < 7; i++){
     for(int j = 0; j < 3.5; j++){
        swap(&mat[i][j], &mat[i][6 - j]);
     }
   }

//    def legal_moves(self):
//        legal_moves = []
//
//        for i in range(self.size):
//            for j in range(self.size):
//                if self.board[i][j] == 1:
//                    if j > 1:
//                        if self.is_move_legal(((i, j), (i, j - 2))):
//                            legal_moves.append(((i, j), (i, j - 2)))
//
//                    if j < 5:
//                        if self.is_move_legal(((i, j), (i, j + 2))):
//                            legal_moves.append(((i, j), (i, j + 2)))
//
//                    if i > 1:
//                        if self.is_move_legal(((i, j), (i - 2, j))):
//                            legal_moves.append(((i, j), (i - 2, j)))
//                    if i < 5:
//                        if self.is_move_legal(((i, j), (i + 2, j))):
//                            legal_moves.append(((i, j), (i + 2, j)))
//
//        return legal_moves

/*
Move * legal_moves(int board[7][7], int size, int legal_moves[][2]) {
    Move moves[]

    for (int i = 0; i < 7; i++) {
        for (int j = 0; j < 7; j++) {
            if (board[i][j] == 1) {
                if (j > 1) {
                    Point p1;
                    p1.y = i;
                    p1.y = j;

                    Point p2;
                    p2.y = i;
                    p2.y = j - 2;

                    Move move = process_move({p1, p2});

                    if (is_move_legal(board, move)) {
                        moves[0] = move
                    }
                }

                if (j < 5) {
                    Point p1;
                    p1.y = i;
                    p1.y = j;

                    Point p2;
                    p2.y = i;
                    p2.y = j + 2;

                    Move move = process_move({p1, p2});

                    if (is_move_legal(board, move)) {
                        moves[1] = move
                    }
                }

                if (i > 1) {
                    Point p1;
                    p1.y = i;
                    p1.y = j;

                    Point p2;
                    p2.y = i - 2;
                    p2.y = j;

                    Move move = process_move({p1, p2});

                    if (is_move_legal(board, move)) {
                        moves[1] = move
                    }
                }

                if (i < 5) {
                    Point p1;
                    p1.y = i;
                    p1.y = j;

                    Point p2;
                    p2.y = i + 2;
                    p2.y = j;

                    Move move = process_move({p1, p2});

                    if (is_move_legal(board, move)) {
                        moves[1] = move
                    }
                }


            }
        }
    }

    return moves

}

*/



Move * solution(){

}

int main()
{
    int board[7][7];
    board[0][4] = 1;
    board[0][3] = 1;

    Point p1 = {.y = 0, .x = 4;};
    Point p2 = {.y=0, .x=2};

    Point move_before[] = {p1, p2};
    Move move = process_move(move_before);

    for (int i = 0; i < 7; i++) {
        for (int j = 0; j < 7; j++) {
            cout << board[i][j];
        }

        cout << endl;
    }

    cout << endl;

    cout << move.p1.x << " " << move.p1.y << endl;
    cout << move.p2.x << " " << move.p2.y << endl;
    cout << move.p3.x << " " << move.p3.y << endl;
    cout << endl;

    // int move_legal = is_move_legal(board, move);

    // cout << move_legal << endl;


    return 0;
}
