# import
from collections import deque
import random
import math
dirs=[(0,1),(1,0),(0,-1),(-1,0)]
########################
# 关于check maze的可行性
def check(mz, x1, y1, x2, y2):
    dirs = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x, y - 1)
    ]
    n, m = len(mz), len(mz[0])
    global path_bfs
    fringe = []  # stores the node that are needed to explore
    fringe.append((x1, y1))
    mz[x1][y1] = 2

    while len(fringe) > 0:
        cur = fringe[0]

        if cur[0] == x2 and cur[1] == y2:
            return True

        for di in dirs:
            next = di(cur[0], cur[1])
            if next[0] < 0 or next[1] < 0 or next[0] > n - 1 or next[1] > m - 1:
                continue
            if mz[next[0]][next[1]] == 0:
                fringe.append(next)
                mz[next[0]][next[1]] = 2

        fringe = deque(fringe)
        fringe.popleft()
        fringe = list(fringe)
    return False


def back(mz):
    l = len(mz)
    for i in range(l):
        for j in range(l):
            if mz[i][j] == 2:
                mz[i][j] = 0
    return mz


def accessibility(mz):
    # check (unblock center and corner)center to 4 corner and upper left to bottom left(block center)
    # find the center
    l = len(mz)
    c = (l + 1) / 2 - 1
    c = int(c)
    # unblock center and corners
    tl = mz[0][0]
    tr = mz[0][l - 1]
    bl = mz[l - 1][0]
    br = mz[l - 1][l - 1]
    mid = mz[c][c]
    mz[0][0] = 0
    mz[0][l - 1] = 0
    mz[l - 1][0] = 0
    mz[l - 1][l - 1] = 0
    mz[c][c] = 0
    c1 = check(mz, c, c, 0, 0)
    mz = back(mz)
    c2 = check(mz, c, c, 0, l - 1)
    mz = back(mz)
    c3 = check(mz, c, c, l - 1, 0)
    mz = back(mz)
    c4 = check(mz, c, c, l - 1, l - 1)
    mz = back(mz)
    mz[c][c] = 1
    c5 = check(mz, 0, 0, l - 1, l - 1)
    mz = back(mz)
    if not (c1 and c2 and c3 and c4):
        mz[0][0] = tl
        mz[0][l - 1] = tr
        mz[l - 1][0] = bl
        mz[l - 1][l - 1] = br
        mz[c][c] = mid
        return False
    # block the center

    if not c5:
        mz[0][0] = tl
        mz[0][l - 1] = tr
        mz[l - 1][0] = bl
        mz[l - 1][l - 1] = br
        mz[c][c] = mid
        return False
    mz[0][0] = tl
    mz[0][l - 1] = tr
    mz[l - 1][0] = bl
    mz[l - 1][l - 1] = br
    mz[c][c] = mid
    return True


#########################
# generate an Accessible Maze
def generatemaze(num):
    maze = [[0 for i in range(num)] for i in range(num)]
    for i in range(num):
        for j in range(num):
            if random.uniform(0, 1) > 0.3:
                maze[i][j] = 0  # 0 for unblock
            else:
                maze[i][j] = 1  # 1 for wall
    if not accessibility(maze):
        maze = generatemaze(num)
    return maze


#########################
# Print readable Maze
def mazePrint(mz):
    l = len(mz)
    for i in range(l):
        print()
        for j in range(l):
            print(mz[i][j], end="")
    print()


###############################

# Each time agent moves one step, we implement this function for attaining a new probability matrix that stores the probability of catching a fire for each entry.
def Fire(q, maze):
    dirs = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x, y - 1)
    ]
    row = len(maze)
    col = len(maze[0])
    fm = [[0] * row for _ in range(col)]
    for i in range(row):
        for j in range(col):
            if maze[i][j] == 1 or maze[i][j] == 3:
                fm[i][j]=1
                continue
            count = 0;
            for di in dirs:
                cur = di(i, j)
                if cur[0] < 0 or cur[0] > row - 1 or cur[1] < 0 or cur[1] > col - 1:
                    continue
                if maze[cur[0]][cur[1]] == 3:
                    count = count + 1
            fm[i][j] = round(1 - (1 - q) ** count, 2)
    return fm


def firecheck(maze):
    row, col = len(maze), len(maze)
    low, high = 0, row * col - 1
    mid = (low + high) // 2
    if maze[mid//col][mid%col]==1:
        for i in range(4):  # 检查每个方向
            point = maze[mid // col + dirs[i][0]][mid % col + dirs[i][1]]
            if point == 0:
                maze[mid // col + dirs[i][0]][mid % col + dirs[i][1]] = 3
                return maze
    else:
        maze[mid//col][mid%col]= 3
    return maze


A = [[0, 0, 0],
     [1, 3, 0],
     [0, 0, 0]]
print("the maze for the fire")
print(Fire(0.2, A))


###########################################
# bfs
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.parent = None


class lList:
    def __init__(self):
        self.head = None


def find_Node(head, target):
    temp = head
    while not temp.data == target:
        temp = temp.next
    return temp


path_bfs = lList()


def bfs(mz, x1, y1, x2, y2):
    dirs = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x, y - 1)
    ]
    n, m = len(mz), len(mz[0])
    global path_bfs
    fringe = []  # stores the node that are needed to explore
    fringe.append((x1, y1))
    mz[x1][y1] = 2
    path_bfs.head = Node((x1, y1))
    Ncur = path_bfs.head

    while len(fringe) > 0:
        cur = fringe[0]

        if cur[0] == x2 and cur[1] == y2:
            return True

        for di in dirs:
            ne = di(cur[0], cur[1])
            if ne[0] < 0 or ne[1] < 0 or ne[0] > n - 1 or ne[1] > m - 1:
                continue
            if mz[ne[0]][ne[1]] == 1:
                continue
            if mz[ne[0]][ne[1]] == 0:
                fringe.append(ne)
                mz[ne[0]][ne[1]] = 2
                Ncur.next = Node((ne[0], ne[1]))
                Ncur = Ncur.next
                pa = find_Node(path_bfs.head, cur)
                Ncur.parent = pa

        fringe = deque(fringe)
        fringe.popleft()
        fringe = list(fringe)
    return False

'''
# bfs test
A = [[0, 0, 0],
     [1, 0, 0],
     [0, 0, 0]]
res = bfs(A, 0, 0, 2, 2)
use = path_bfs.head
print(A)
while not use.data == (2, 2):
    print(use.data)
    use = use.next

print()
print(use.data)
print(use.parent.data)
use = use.parent
print(use.parent.data)
use = use.parent
print(use.parent.data)
use = use.parent
print(use.parent.data)
'''

##################################
# dfs
def find_Node(head, target):
    temp = head
    while not temp.data == target:
        temp = temp.next
    return temp


path_dfs = lList()


def dfs(mz, x1, y1, x2, y2):  # start at (x1,y1), end at (x2,y2)
    dirs = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x, y - 1)
    ]

    global path_dfs
    l = len(mz)

    fringe = [(x1, y1)]
    mz[x1][y1] = 2
    path_dfs.head = Node((x1, y1))
    N = path_dfs.head

    while not fringe == []:
        cur = fringe.pop()
        if cur == (x2, y2):
            return True

        for di in dirs:
            ne = di(cur[0], cur[1])
            if ne[0] < 0 or ne[1] < 0 or ne[0] > l - 1 or ne[1] > l - 1:
                continue
            if mz[ne[0]][ne[1]] == 1:
                continue
            if mz[ne[0]][ne[1]] == 0:
                fringe.append(ne)
                mz[ne[0]][ne[1]] = 2
                N.next = Node((ne[0], ne[1]))
                N = N.next
                pa = find_Node(path_dfs.head, cur)
                N.parent = pa

    return False

'''
# dfs test
A = [[0, 0, 0],
     [1, 0, 0],
     [0, 0, 0]]
res = dfs(A, 0, 0, 2, 2)
use = path_dfs.head
print(A)
while not use.next == None:
    print(use.data)
    use = use.next

print()
print(use.data)
use = use.parent
print(use.data)
use = use.parent
print(use.data)
use = use.parent
print(use.data)
use = use.parent
print(use.data)
'''

#######################################
def heuristic(x1, y1, x2, y2):  # Euclidean distance
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)


def find_min(fg):
    count = -1
    temp = fg[0]
    pos = 0
    nmin = temp[2]
    for ele in fg:
        count = count + 1
        if ele[2] < nmin:
            nmin = ele[2]
            pos = count
    return pos


path_A = lList()


def As(mz, x1, y1, x2, y2):
    dirs = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x, y - 1)
    ]

    l = len(mz)
    global path_A
    sc = heuristic(x1, y1, x1, y1)  # start to current distance g(n)
    ce = heuristic(x1, y1, x2, y2)  # current to end distance h(n)
    cost = sc + ce
    fringe = []  # stores the node that are needed to explore
    fringe.append((x1, y1, cost))
    mz[x1][y1] = 2
    path_A.head = Node((x1, y1))
    Ncur = path_A.head

    while len(fringe) > 0:
        ps = find_min(fringe)
        cur = fringe[ps]
        fringe.pop(ps)

        if cur[0] == x2 and cur[1] == y2:
            return True

        for di in dirs:
            ne = di(cur[0], cur[1])
            if ne[0] < 0 or ne[1] < 0 or ne[0] > l - 1 or ne[1] > l - 1:
                continue
            if mz[ne[0]][ne[1]] == 1:
                continue
            if mz[ne[0]][ne[1]] == 0:
                sc = heuristic(ne[0], ne[1], x1, y1)  # start to current distance g(n)
                ce = heuristic(ne[0], ne[1], x2, y2)  # current to end distance h(n)
                cost = sc + ce
                fringe.append((ne[0], ne[1], cost))
                mz[ne[0]][ne[1]] = 2
                Ncur.next = Node((ne[0], ne[1]))
                Ncur = Ncur.next
                pa = find_Node(path_A.head, (cur[0], cur[1]))
                Ncur.parent = pa
    return False

'''
# A star test
A = [[0, 0, 0],
     [1, 0, 1],
     [0, 0, 0]]
res = As(A, 0, 0, 2, 2)
use = path_A.head
print(A)
while not use.data == (2, 2):
    print(use.data)
    use = use.next

print()
while not use.parent == None:
    print(use.data)
    use = use.parent
print(use.data)
print()
'''

def agent(maze):
    As(maze,0,0,len(maze)-1,len(maze[0])-1)
    use = path_A.head
    res = [(len(maze)-1, len(maze[0])-1)]
    while not use.data == ((len(maze)-1, len(maze[0])-1)):
        #print(use.data)
        use = use.next


    while not use.parent == None:
        use = use.parent
        #print(use.data)
        res.append(use.data)
    return res



def walkfire(maze):
    dirs = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x, y - 1)
    ]
    l = len(maze)
    small = 2
    for di in dirs:
        ne = di(0,0)
        if ne[0] < 0 or ne[1] < 0 or ne[0] > l - 1 or ne[1] > l - 1:
            continue
        if maze[ne[0]][ne[1]] == 1:
            continue
        if maze[ne[0]][ne[1]] < 1:
            if maze[ne[0]][ne[1]] < small:
                small = maze[ne[0]][ne[1]]
    return small




def agent2(maze):
    #print(maze)
    firecheck(maze) #设置起火的地方
    mz = Fire(0.2, maze) #拿出初始化着火的matrix
    print(walkfire(mz))






A = [[0, 0, 0],
     [1, 0, 1],
     [0, 0, 0]]
print("test for the agent 2")
# print(agent(A))
print(agent2(A))
