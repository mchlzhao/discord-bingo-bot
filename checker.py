def to_matrix(input_list, rows, cols):
    matrix = []
    for i in range(rows):
        matrix.append(list(input_list[cols*i:cols*(i+1)]))
    return matrix

def is_success(success_list, size):
    success_matrix = to_matrix(success_list, size, size)
    for i in range(size):
        f = True
        for j in range(size):
            if not success_matrix[i][j]:
                f = False
                break
        if f:
            return True
    for j in range(size):
        f = True
        for i in range(size):
            if not success_matrix[i][j]:
                f = False
                break
        if f:
            return True
    f = True
    for i in range(size):
        if not success_matrix[i][i]:
            f = False
            break
    if f:
        return True
    f = True
    for i in range(size):
        if not success_matrix[i][size-1-i]:
            f = False
            break
    return f
