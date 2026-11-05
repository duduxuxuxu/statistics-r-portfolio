# Selected student implementation excerpts. Original course framework and instructor-provided docstrings are omitted.
# These excerpts retain the saved implementation bodies and require their course framework to run.
from __future__ import annotations

def is_valid_matrix(matrix: list[list[Element]]) -> bool:
    if len(matrix) == 0:
        return True

    # get the length of the first row
    first_row_length = len(matrix[0])

    # check if all rows have the same length
    for row in matrix:
        if len(row) != first_row_length:
            return False

    return True

def combine_rows(
    matrix1: list[list[Element]], matrix2: list[list[Element]]
) -> None:
    if (is_valid_matrix(matrix1) and is_valid_matrix(matrix2)
            and len(matrix1) == len(matrix2)):
        # extend each row of matrix1 with corresponding row from matrix2
        for i in range(len(matrix1)):
            matrix1[i].extend(matrix2[i])

def invert_binary_values(matrix: list[list[int]]) -> None:
    for row in matrix:
        for j in range(len(row)):
            if row[j] == 0:
                row[j] = 1
            elif row[j] == 1:
                row[j] = 0

def convert_binary_to_str(matrix: list[list[int]]) -> None:
    for row in matrix:
        for j in range(len(row)):
            row[j] = get_random_char(row[j])

def convert_str_to_binary(matrix: list[list[str]]) -> None:
    for row in matrix:
        for j in range(len(row)):
            char = row[j]
            if char in ALL_VOWELS:
                row[j] = VOWEL_VALUE
            elif char in ALL_CONSONANTS:
                row[j] = CONSONANT_VALUE

def encrypt_or_decrypt(matrix: list[list[str]],
                       key: int,
                       encrypt: bool) -> None:
    for row in matrix:
        for j in range(len(row)):
            char = row[j]
            # get ASCII value of character
            ascii_val = ord(char)

            # encrypt by adding key, decrypt by subtracting key
            if encrypt:
                new_ascii = ascii_val + key
            else:
                new_ascii = ascii_val - key

            # convert back to character
            row[j] = chr(new_ascii)

def rotate_matrix(matrix: list[list[Element]]) -> list[list[Element]]:
    if not is_valid_matrix(matrix):
        return matrix

    # handle empty matrix
    if len(matrix) == 0:
        return matrix

    # create new matrix for 90 degree clockwise rotation
    rows = len(matrix)
    cols = len(matrix[0])
    new_matrix = []

    # fill new matrix by picking elements in reverse row order for each column
    for c in range(cols):
        new_row = []
        for r in range(rows - 1, -1, -1):
            new_row.append(matrix[r][c])
        new_matrix.append(new_row)

    return new_matrix

def flip_matrix(
    matrix: list[list[Element]], horizontal: bool
) -> list[list[Element]]:
    if not is_valid_matrix(matrix):
        return matrix

    # create new matrix for flipping
    new_matrix = []

    if horizontal:
        # horizontal flip means flip top to bottom (reverse row order)
        for i in range(len(matrix) - 1, -1, -1):
            new_row = []
            for j in range(len(matrix[i])):
                new_row.append(matrix[i][j])
            new_matrix.append(new_row)
    else:
        # vertical flip means flip left to right (reverse column order)
        for row in matrix:
            new_row = []
            for j in range(len(row) - 1, -1, -1):
                new_row.append(row[j])
            new_matrix.append(new_row)

    return new_matrix

def solve_mystery_phrase(
    encrypted_matrix: list[list[str]], target_hash: str, max_key_value: int
) -> list[list[int]]:
    for key in range(max_key_value + 1):
        # make a copy of the encrypted matrix to work with
        matrix_copy = deepcopy(encrypted_matrix)

        # decrypt the matrix with current key
        encrypt_or_decrypt(matrix_copy, key, False)

        # convert to binary matrix
        convert_str_to_binary(matrix_copy)

        # try all rotation and flip combinations
        for rotations in range(4):  # 0 to 3 rotations
            # start with current matrix state
            test_matrix = deepcopy(matrix_copy)

            # apply rotations
            for _ in range(rotations):
                test_matrix = rotate_matrix(test_matrix)

            # try all flip combinations: no flip, horizontal, vertical, both
            flip_combinations = [
                (False, False),  # no flip
                (True, False),   # horizontal flip only
                (False, True),   # vertical flip only
                (True, True)     # both flips
            ]

            for horizontal_flip, vertical_flip in flip_combinations:
                final_matrix = deepcopy(test_matrix)

                # apply flips if needed
                if horizontal_flip:
                    final_matrix = flip_matrix(final_matrix, True)
                if vertical_flip:
                    final_matrix = flip_matrix(final_matrix, False)

                # check if this matrix matches the target hash
                if check_secret_message(final_matrix, target_hash):
                    return final_matrix

    # if no combination worked, return empty list
    return []
