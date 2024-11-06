# Question: Given positive integers m and n, interactively play the game of Chomp.

# Input: m, n
# Output: A Chomp game which the user can input coordinate and the updated status of the game.

# Explanation: The user first input the number of rows and columns of the game.
# The program will display the board. For example, when m = 5, n = 4, the board will be like this:
# o    o    o    o    o
# o    o    o    o    o
# o    o    o    o    o
# o    o    o    o    o
# Then, the program will ask the user to take turns to input the target x coordinate and y coordinate of his move.
# For example, if the user enters 2 then 3, the target move will be (2, 3)
# That means the cookies ( on or to the right of column 2 ) and ( on or below row 3 ) will be eaten.
# Of course, the player must enter a coordinate which requires him to eat at least one cookie.
# The program will ask him to enter again if not.
# o    o    o    o    o
# o    o    o    o    o
# o    x    x    x    x
# o    x    x    x    x

# When the board is like this, the next player will need to enter (1, 1) and eat the last cookie.
# That means this player loses and the game ends.
# o    x    x    x    x
# x    x    x    x    x
# x    x    x    x    x
# x    x    x    x    x
# The program will ask the user to play again or not.

def chomp(m, n):
    # generate board
    board = gen_board(m, n)
    print_board(board)
    player = 1
    while True:
        print("Player {0}".format(player))
        while (True):
            new_x, new_y = input_coor()
            if (new_x - 1 >= m or new_y - 1 >= n):
                print("Please input valid number")
                continue
            if not (update_board(board, new_x - 1, new_y - 1)):
                print("Please input valid number")
                continue
            break

        print_board(board)
        if (board[0][0] == 'x'):
            print("Player {0} lost!".format(player))
            return
        if player == 1:
            player = 2
        else:
            player = 1


def update_board(board, move_x, move_y):
    valid_move = False
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if i >= move_x and j >= move_y and board[i][j] == 'o':
                valid_move = True
                board[i][j] = 'x'
    return valid_move


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


def input_coor():
    try:
        m = input("Please input m: ")
        m = int(m)
        if m <= 0:
            raise ValueError("Input is not a positive integer. Please enter a positive integer.")
    except ValueError as e:
        raise ValueError(e)

    try:
        n = input("Please input n: ")
        n = int(n)
        if n <= 0:
            raise ValueError("Input is not a positive integer. Please enter a positive integer.")
    except ValueError as e:
        raise ValueError(e)
    return m, n


if __name__ == "__main__":
    again = True
    while (again):
        m, n = input_coor()
        chomp(m, n)
        ans = input("Play again?(y/n): ")
        if (ans == "y"):
            again = True
        else:
            again = False
    print("Goodbye!")
