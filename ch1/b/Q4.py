# Question: Try to find winning strategies for the game of Chomp for different initial configurations of cookies

# Input: A initial configurations of cookies.
# Output: The first move of winning strategy.

# Explanation: Find the first winning strategy recursively and exhaustively.

def copy_matrix(original_matrix):
    # Get the dimensions of the original matrix
    rows = len(original_matrix)
    cols = len(original_matrix[0]) if rows > 0 else 0

    # Create a new matrix with the same dimensions as the original matrix
    new_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # Copy the elements from the original matrix to the new matrix
    for i in range(rows):
        for j in range(cols):
            new_matrix[i][j] = original_matrix[i][j]

    return new_matrix

def is_matrix_in_list(target_matrix, matrix_list):
    for matrix in matrix_list:
        if matrix == target_matrix:
            return True
    return False

def winning_move(board, memo={}):
    deep_copy_board = copy_matrix(board)
    tuple_board = tuple(tuple(inner_list) for inner_list in deep_copy_board)
    if tuple_board in memo:
        return memo[tuple_board]
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if i == 0 and j == 0:
                continue
            new_board = copy_matrix(board)
            deep_copy_new_board = [list(inner_list) for inner_list in new_board]
            tuple_new_board = tuple(tuple(inner_list) for inner_list in deep_copy_new_board)
            if update_board(new_board, i, j):
                #print(new_board)
                next_x, next_y = winning_move(new_board)
                if next_x == -1:
                    memo[tuple_new_board] = [i, j]
                    return i, j
    memo[tuple_board] = [-1, -1]
    return -1, -1

def update_board(board, move_x, move_y):
    if (board[move_x][move_y] == 'x'):
        return False
    for i in range(move_x, len(board)):
        for j in range(move_y, len(board[i])):
            board[i][j] = 'x'
    return True


def gen_board(m, n):
    board = []
    for i in range(0, m):
        column = []
        for j in range(0, n):
            column.append('o')
        board.append(column)
    return board


def print_board(board):
    for i in range(0, len(board[0])):
        for j in range(0, len(board)):
            print("{0}    ".format(board[j][i]), end='')
        print()


if __name__ == "__main__":
    for i in range(2, 11):
        for j in range(2, 11):
            print("board {0}x{1} first move:".format(i, j))
            print(winning_move(gen_board(i, j)))
