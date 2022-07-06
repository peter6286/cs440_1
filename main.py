def shortestPathBinaryMatrix(grid):
    row = len(grid)
    col = len(grid[0])

    if row == 1 and col == 1 and grid[0][0] == 0:
        return 1

    if grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1

    step = 1
    # grid[0][0] = 1
    queue = [(0, 0)]
    while queue:
        current_len = len(queue)
        for _ in range(current_len):
            i, j = queue.pop(0)
            grid[i][j] = 1
            for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                temp_i = i + x
                temp_j = j + y
                if 0 <= temp_i < row and 0 <= temp_j < col:
                    if temp_i == row - 1 and temp_j == col - 1:
                        return step + 1
                    if grid[temp_i][temp_j] == 1:
                        continue
                    if grid[temp_i][temp_j] == 0:
                        grid[temp_i][temp_j] = 1
                        queue.append((temp_i, temp_j))
        step += 1
    return -1

A = [[0, 0, 0],
     [1, 1, 0],
     [0, 0, 0]]

print(shortestPathBinaryMatrix(A))