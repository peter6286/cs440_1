import random

def rand_pick():
    value_list = [0, 1]
    x = random.uniform(0 ,1)
    probabilities = [0.7, 0.3]
    cumprob = 0.0
    for item , item_pro in zip(value_list , probabilities):
        cumprob += item_pro
        if x < cumprob:
            break
    return item
def UniquePathHelper(i, j, r, c, A):
    # boundary condition or constraints
    if (i == r or j == c):
        return 0
    if (A[i][j] == 1):
        return 0
    # base case
    if (i == r - 1 and j == c - 1):
        return 1
    return UniquePathHelper(i + 1, j, r, c, A) + UniquePathHelper(i, j + 1, r, c, A)


def check(matrix):
    row, col = len(matrix), len(matrix[0])
    low, high = 0, row * col - 1
    mid = (low + high) // 2
    num = matrix[mid // col][mid % col]
    UniquePathHelper(mid // col,mid % col, r, c, matrix)

def UniquePathHelper(i, j, r, c, A):
    # boundary condition or constraints
    if (i == r or j == c):
        return 0
    if (A[i][j] == 1):
        return 0
    # base case
    if (i == r - 1 and j == c - 1):
        return 1
    return UniquePathHelper(i + 1, j, r, c, A) + UniquePathHelper(i, j + 1, r, c, A)


def uniquePathsWithObstacles(A):
    r, c = len(A), len(A[0])

    return UniquePathHelper(0, 0, r, c, A)



rows = 3
cols = 3
maze=[[0 for i in range(cols)] for i in range(rows)]
for i in range(rows):
    for j in range(cols):
        if rand_pick()==1:
            maze[i][j] = 1
        else:
            maze[i][j] = 0

print(maze)
print(check(maze))






def rand_pick():
    value_list = [0, 1]
    x = random.uniform(0 ,1)
    probabilities = [0.3, 0.7]
    cumprob = 0.0
    for item , item_pro in zip(seq , probabilities):
        cumprob += item_pro
        if x < cumprob:
            break
    return item