maze=[[0,0,0],
      [0,1,0],
      [0,0,0]]




def valid(maze,x,y):
  if (x>=0 and x<len(maze) and y>=0 and y<len(maze[0]) and maze[x][y]==1):
    return True
  else:
    return False
# 移步函数实现
def walk(maze,x,y):
  # 如果位置是迷宫的出口，说明成功走出迷宫
  if(x==0 and y==0):
    print("successful!")
    return True
  # 递归主体实现
  if valid(maze,x,y):
    # print(x,y)
    maze[x][y]=2 # 做标记，防止折回
    # 针对四个方向依次试探，如果失败，撤销一步
    if not walk(maze,x-1,y):
      maze[x][y]=1
    elif not walk(maze,x,y-1):
      maze[x][y]=1
    elif not walk(maze,x+1,y):
      maze[x][y]=1
    elif not walk(maze,x,y+1):
      maze[x][y]=1
    else:
      return False # 无路可走说明，没有解
  return True
print(walk(maze,1,1))