import copy
import random
path=[]
dirs=[(0,1),(1,0),(0,-1),(-1,0)]


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

def passable(maze,pos): #检查迷宫maze的位置pos是否可通行
    if 0 <= pos[0] < len(maze) and 0 <= pos[1] < len(maze[0]):
        return maze[pos[0]][pos[1]]==0
    return False

#def mark(temp, pos):  # 给迷宫maze的位置pos标"2"表示“倒过了”
#    temp[pos[0]][pos[1]] = 2

def maze_solve(maze, start, end):
    path.append(start)
    if start == end:
        return True
    qu = []
    visted = set()
    visted.add(start)
    #mark(temp, start)
    qu.append(start)  # start位置入队
    while qu:  # 还有候选位置
        pos = qu.pop(0)  # 取出下一位置
        for i in range(4):  # 检查每个方向
            nextp = pos[0] + dirs[i][0], pos[1] + dirs[i][1]
            if nextp not in visted and passable(maze, nextp):  # 找到新的探索方向
                if nextp == end:  # 是出口，成功
                    path.append(end)
                    #print(maze)
                    return True
                #mark(temp, nextp)
                visted.add(nextp)
                qu.append(nextp)  # 新位置入队
                path.append(nextp)
    return False


def check(matrix):
    row, col = len(matrix), len(matrix[0])
    low, high = 0, row * col - 1
    mid = (low + high) // 2
    midgrid = (mid//col,mid%col)
    topleft = (0,0)
    topright = (0,len(matrix)-1)
    bottomleft = (len(matrix[0])-1,0)
    bottomrihgt = (len(matrix[0])-1,len(matrix)-1)

    if maze_solve(matrix,midgrid,topleft) and maze_solve(matrix,topleft,bottomrihgt) \
    and maze_solve(matrix,midgrid,topright) and maze_solve(matrix,midgrid,bottomleft) \
    and maze_solve(matrix,midgrid,bottomrihgt):
        return True
    else:
        return False



def genratemaze(rows,cols):
    maze=[[0 for i in range(cols)] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if rand_pick()==1:
                maze[i][j] = 1
            else:
                maze[i][j] = 0
    return maze



def env(rows,cols):
    maze = genratemaze(rows, cols)
    while check(maze) != True:
        maze = genratemaze(rows,cols)
    #print(maze)
    return maze


def fire(maze):
    row, col = len(maze), len(maze)
    low, high = 0, row * col - 1
    mid = (low + high) // 2
    if maze[mid//col][mid%col]==1:
        for i in range(4):  # 检查每个方向
            point = maze[mid // col + dirs[i][0]][mid % col + dirs[i][1]]
            if point == 0:
                maze[mid // col + dirs[i][0]][mid % col + dirs[i][1]] = "#"
                return maze
    else:
        maze[mid//col][mid%col]= "#"
    return maze
path_dfs = []
def dfs(mz,x1,y1,x2,y2): #start at (x1,y1), end at (x2,y2)
    dirs = [
        lambda x,y: ( x+1 , y ),
        lambda x,y: ( x-1 , y ),
        lambda x,y: ( x , y+1 ),
        lambda x,y: ( x , y-1 )
        ]
    global path_dfs
    
    if x1 == x2 and y1 == y2:
        print path_dfs
        return path_dfs
    
    for di in dirs:
        cur = [di(x1,y1)]
        if cur[0] > len(mz) - 2 or cur[1] > len[maze] - 2 or cur[0] < 0 or cur[1] < 0:
            continue
        direction = ''
        if cur[0] - x1 == 1:
            direction = 'D' #Downward
        if cur[0] - x1 == -1:
            direction = 'U' #Upward
        if cur[1] - y1 == 1:
            direction = 'R' #Rightward
        if cur[0] - y1 == -1:
            direction = 'L' #Leftward
        mz[cur[0]][cur[1]] = 1 #maze 1 for wall and 0 for acessible
        path_dfs += direction
        dfs(mz,cur[0], cur[1], x2, y2)
        path = path_dfs[:-1]
        maze[cur[0]][cur[1]] = 0
        
        
path_bfs = []
def bfs(mz,x1,y1,x2,y2):
    dirs = [
        lambda x,y: ( x+1 , y ),
        lambda x,y: ( x-1 , y ),
        lambda x,y: ( x , y+1 ),
        lambda x,y: ( x , y-1 )
        ]
    
    n,m = len(maze),len(maze[0])
    global path_dfs
    fringe = [] #stores the node that are needed to explore
    fringe.append((x1,y1))
    mz[x1][y1] = 1
    path_bfs.append(fringe[0])
    
    while len(fringe) > 0:
        cur = fringe[0]
        
        if cur[0] == x2 and cur[1] == y2:
            temp_path = []
            temp_path.append(path_bfs[-1])
            temp_Node = path_bfs[-1]
            path_bfs.pop()
            
            while (not temp_Node[0] == x1) and (not temp_Node[1] == y1):
                for di in dirs:
                    node = di(temp_Node[0],temp_Node[1])
                    count = 0
                    for n in path_bfs:
                        if node[0] == n[0] and node[1] == n[1]:
                            temp_path.append(node)
                            path_bfs.pop(count)
                        count++
            path_bfs = temp_path.reverse()
            return True
        
        for di in dirs:
            next = di(cur[0],cur[1])
            if mz[cur[0]][cur[1]] == 0:
                path_bfs.append(next)
                mz[cur[0]][cur[1]] = 1
    return False



A = [[0, 0, 0],
     [1, 0, 0],
     [0, 0, 0]]

#mymaze = genratemaze(9,9)
#print(env(3,3))
print(fire(A))


#check(A)
