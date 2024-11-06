# Given a portion of a checkerboard, look for tilings of this checkerboard with various types of polyominoes, including dominoes, the two types of triominoess, and larger polyominoes.
# Input: Two matrix with only 1/0.
# Output: The tilings of the checkerboard.

# Explanation: We can construct a recursive algorithm for it.
# Starting from the first tile on the first row, we can try all possible ways to cover the tile.
# If that way can cover the tile, we remove all the covered tiles from the board.
# Then input the board to the same function. Until it tries all the arrangements.
# The output should be the tiling of the checkerboard.

def find_first_one(board):
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if board[row][col] == 1:
                return row, col
    return -1, -1


def rotate_matrix(matrix):
    n = len(matrix)

    # Transpose the matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i].reverse()

    return matrix


def mirror_matrix_horizontally(matrix):
    mirrored_matrix = [row[::-1] for row in matrix]
    return mirrored_matrix


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


def find_all_poly_shape(polyominoe):
    all_basic_shapes = []
    for i in range(2):
        for j in range(4):
            polyominoe = rotate_matrix(polyominoe)
            if is_matrix_in_list(polyominoe, all_basic_shapes):
                continue
            all_basic_shapes.append(copy_matrix(polyominoe))
        polyominoe = mirror_matrix_horizontally(polyominoe)
    return all_basic_shapes


def expand_to_square_matrix(matrix):
    num_rows = len(matrix)
    num_cols = 0

    for sublist in matrix:
        if isinstance(sublist, list):
            current_length = len(sublist)
        else:
            current_length = 1
        if current_length > num_cols:
            num_cols = current_length

    max_dim = max(num_rows, num_cols)

    # Pad the matrix with zeros to make it square
    square_matrix = []
    for i in range(max_dim):
        if i < num_rows:
            if isinstance(matrix[i], list):
                row = matrix[i] + [0] * (max_dim - len(matrix[i]))
            else:
                row = [matrix[i]] + [0] * (max_dim - 1)
        else:
            row = [0] * max_dim
        square_matrix.append(row)

    return square_matrix


def find_center(shape, i):
    count = 0
    for row in range(0, len(shape)):
        for col in range(0, len(shape[row])):
            if (shape[row][col] == 1):
                if (count == i):
                    return row, col
                else:
                    count += 1
    return -1, -1


def convert_shape2offset(all_shapes):
    num_of_one = 0
    for row in all_shapes[0]:
        num_of_one += row.count(1)

    offsets = []
    for shape in all_shapes:
        for i in range(0, num_of_one):
            center_row, center_col = find_center(shape, i)
            offset = []
            for row in range(0, len(shape)):
                for col in range(0, len(shape[row])):
                    if shape[row][col] == 1:
                        offset.append([row - center_row, col - center_col])
            if is_matrix_in_list(offset, offsets):
                continue
            offsets.append(offset)

    return offsets


def get_offset_from_poly(polyominoe):
    # expand the polyominoe to square matrix first
    square_poly = expand_to_square_matrix(polyominoe)

    # find all possible shapes of the square matrix
    all_shapes = find_all_poly_shape(square_poly)

    # convert the shapes to offsets with different centers
    all_offsets = convert_shape2offset(all_shapes)

    return all_offsets


def find_tilings_recur(board, all_offsets, all_tilings, tile_count, num_of_result):
    # find the position of first 1 in the board
    first_one_row, first_one_col = find_first_one(board)
    if (first_one_row == -1):
        print("Found one tiling")
        successful_tiling = copy_matrix(board)
        all_tilings.append(successful_tiling)
        return 0
    for offsets in all_offsets:
        if (len(all_tilings) >= num_of_result):
            return 0
        can_tile = True
        for offset in offsets:
            if (
                    first_one_row + offset[0] < 0 or
                    first_one_col + offset[1] < 0 or
                    first_one_row + offset[0] >= len(board) or
                    first_one_col + offset[1] >= len(board[0])
            ):
                can_tile = False
                break
            if (board[first_one_row + offset[0]][first_one_col + offset[1]] != 1):
                can_tile = False
                break
        # recursively call the function if this offset can cover the tile.
        if can_tile:
            # cover the tiles
            for offset in offsets:
                board[first_one_row + offset[0]][first_one_col + offset[1]] = tile_count % 8 + 2
            find_tilings_recur(board, all_offsets, all_tilings, tile_count + 1, num_of_result)
            # uncover the tiles
            for offset in offsets:
                board[first_one_row + offset[0]][first_one_col + offset[1]] = 1
    return 0


def find_tilings(board, polyominoe, num_of_result=1):
    all_offsets = get_offset_from_poly(polyominoe)
    # after find all offsets, we can start the recursive algorithm to search for all tilings.
    result = []
    find_tilings_recur(board, all_offsets, result, 0, num_of_result)
    if (len(result) > 0):
        print("Board can be tiled")
    else:
        print("Board cannot be tiled")

    return result

def print_result(result):
    for matrix in result:
        for row in matrix:
            print(row)
        print()

if __name__ == "__main__":
    board_8x8 = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
    board_8x8_no_same_row_corners = [
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
    board_8x8_no_oppo_corners = [
        [0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0]
    ]

    dominoes = [1, 1]


    board_8x8_can_be_tiled_by_straight_triominoes = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]

    board_8x8_cannot_be_tiled_by_straight_triominoes = [
        [0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]

    straight_triominoes = [1, 1, 1] # straight triominoes
    L_triominoes = [[1, 1], [1]]    # L triominoes


    print_result(find_tilings(board_8x8, dominoes))
    print_result(find_tilings(board_8x8_no_same_row_corners, dominoes))
    print_result(find_tilings(board_8x8_no_oppo_corners, dominoes))

    print_result(find_tilings(board_8x8_can_be_tiled_by_straight_triominoes, straight_triominoes))
    print_result(find_tilings(board_8x8_cannot_be_tiled_by_straight_triominoes, straight_triominoes))
    print_result(find_tilings(board_8x8_can_be_tiled_by_straight_triominoes, L_triominoes))
    print_result(find_tilings(board_8x8_cannot_be_tiled_by_straight_triominoes, L_triominoes))

    straight_tetrominoes = [1, 1, 1, 1] # straight tetrominoes
    window_tetrominoes = [[1, 1],     # window tetrominoes
                          [1, 1]]
    L_tetrominoes = [[1, 1, 1],  # L tetrominoes
                     1]
    T_tetrominoes = [[0, 1, 0],  # T tetrominoes
                     [1, 1, 1]]
    snake_tetrominoes = [[0, 1, 1],  # snake tetrominoes
                        [1, 1, 0]]

    print_result(find_tilings(board_8x8, straight_tetrominoes))
    print_result(find_tilings(board_8x8, window_tetrominoes))
    print_result(find_tilings(board_8x8, L_tetrominoes))
    print_result(find_tilings(board_8x8, T_tetrominoes))
    print_result(find_tilings(board_8x8, snake_tetrominoes))

    board_10x10 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    print_result(find_tilings(board_10x10, straight_tetrominoes))

    board_6x6 = [
        [0, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 0]
    ]

    X_pentominoes = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

    print_result(find_tilings(board_6x6, X_pentominoes))

    board_4x4 = [
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1]
    ]

    O_tetrominoes = [[1, 1], [1, 1]]
    print_result(find_tilings(board_4x4, O_tetrominoes))