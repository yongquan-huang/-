import numpy as np
import time

a = np.array([[0, 0, 0, 0, 0],
              [1, 0, 1, 0, 1],
              [0, 0, 1, 1, 1],
              [0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0]])

b = np.array([[0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
              [1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
              [0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
              [0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
              [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
              [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
              [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
              [1, 1, 0, 1, 0, 1, 1, 1, 1, 0]])

def gs(i, j, startx, starty):
    return abs(i - startx) + abs(j - starty)

def h1(i, j, endx,  endy):
    return abs(i - endx) + abs(j - endy)

def h2(i, j, endx,  endy):
    return pow(i - endx, 2) + pow(j - endy, 2)

class Node():
    '''定义点类'''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def initnode(self, parent, end):
        self.parent = parent
        if parent != None :
            # 处理初始节点时的情况，即初始节点距离为1，其他的节点是在其父节点的基础上+1
            self.g = parent.g + 1
        else:
            self.g = 1
        self.h = h1(self.x, self.y, end.x, end.y)
        self.f = self.g + self.h

def astar_search(matrix, start, end):
    '''
    A*算法求解迷宫寻路最短路径
    '''
    # openlist：可到达的格子； closelist：已到达的格子
    openlist, closelist = [], []
    # 把起点加入 openList
    openlist.append(start)
    # 扩展节点数
    extend_node_num = 1
    while(openlist != []):
        # 在openList中查找 F值最小的节点
        currentnode = find_min_node(openlist)
        # 将当前节点从openList中移除
        openlist.remove(currentnode)
        # 当前节点进入 closeList
        closelist.append(currentnode)
        # 判断是不是为终点
        if currentnode.x == end.x and currentnode.y == end.y:
            print('扩展节点数：{}'.format(extend_node_num))
            print('生成节点数：{}'.format(len(closelist)))
            return currentnode
        # 找到所有邻近节点
        neighbors = find_neighbors(matrix, currentnode, openlist, closelist)
        extend_node_num += len(neighbors)
        # 计算出相应的G、H、F值,设置其父节点，并加入到openlist
        for neighbor in neighbors:
            neighbor.initnode(currentnode, end)
            openlist.append(neighbor)
    print('扩展节点数：{}'.format(len(openlist)))
    print('生成节点数：{}'.format(len(closelist)))
    return

def find_min_node(openlist):
    min_node = openlist[0]
    for node in openlist:
        if node.f < min_node.f:
            min_node = node
    return min_node

def find_neighbors(matrix, currentnode, openlist, closelist):
    neighbors = []
    if isvalid_node(matrix, currentnode.x, currentnode.y+1, openlist, closelist):
        neighbors.append(Node(currentnode.x, currentnode.y+1))
    if isvalid_node(matrix, currentnode.x, currentnode.y-1, openlist, closelist):
        neighbors.append(Node(currentnode.x, currentnode.y-1))
    if isvalid_node(matrix, currentnode.x-1, currentnode.y, openlist, closelist):
        neighbors.append(Node(currentnode.x-1, currentnode.y))
    if isvalid_node(matrix, currentnode.x+1, currentnode.y, openlist, closelist):
        neighbors.append(Node(currentnode.x+1, currentnode.y))
    return neighbors

def isvalid_node(matrix, x, y, openlist, closelist):
    # 是否超过边界
    if x < 0 or x >= len(matrix[0]) or y < 0 or y >= len(matrix):
        return False
    # 是否有障碍物
    if matrix[x][y] == 1:
        return False
    # 是否已经在openList中
    if iscontain(openlist, x, y):
        return False
    if iscontain(closelist, x, y):
        return False
    return True

def iscontain(list, x, y):
    for node in list:
        if node.x == x and node.y == y:
            return True
    else:
        return False

def main(matrix, start, end):
    start_time = time.time()
    # 设置起点和终点,注意起点还要设置其初始的F，G，H值
    start.initnode(None, end)
    result = astar_search(matrix, start, end)
    # 记录路径
    open_path = []
    # 开始寻路时定义的数字
    road = 100
    # 回溯迷宫最短路径
    while result:
        open_path.append(Node(result.x, result.y))
        result = result.parent
    # 输出迷宫和路径，路径从road数值开始
    if open_path != []:
        for node in open_path[::-1]:
            x = node.x
            y = node.y
            matrix[x][y] = road
            road += 1
        print('存在最短路径:')
        print(matrix)
    else:
        print('找不到最短路径')
    end_time = time.time()
    print('算法运行时间：{}'.format(end_time - start_time))


class Node2():
    '''定义点类2'''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def initnode(self, parent, end):
        self.parent = parent
        if parent != None :
            # 处理初始节点时的情况，即初始节点距离为1，其他的节点是在其父节点的基础上+1
            self.g = parent.g + 1
        else:
            self.g = 1
        self.h = h2(self.x, self.y, end.x, end.y)
        self.f = self.g + self.h

def astar_search2(matrix, start, end):
    '''
    A*算法求解迷宫寻路最短路径
    '''
    # openlist：可到达的格子； closelist：已到达的格子
    openlist, closelist = [], []
    # 把起点加入 openList
    openlist.append(start)
    # 扩展节点数
    extend_node_num = 1
    while(openlist != []):
        # 在openList中查找 F值最小的节点
        currentnode = find_min_node(openlist)
        # 将当前节点从openList中移除
        openlist.remove(currentnode)
        # 当前节点进入 closeList
        closelist.append(currentnode)
        # 判断是不是为终点
        if currentnode.x == end.x and currentnode.y == end.y:
            print('扩展节点数：{}'.format(extend_node_num))
            print('生成节点数：{}'.format(len(closelist)))
            return currentnode
        # 找到所有邻近节点
        neighbors = find_neighbors2(matrix, currentnode, openlist, closelist)
        extend_node_num += len(neighbors)
        # 计算出相应的G、H、F值,设置其父节点，并加入到openlist
        for neighbor in neighbors:
            neighbor.initnode(currentnode, end)
            openlist.append(neighbor)
    print('扩展节点数：{}'.format(len(openlist)))
    print('生成节点数：{}'.format(len(closelist)))
    return

def find_neighbors2(matrix, currentnode, openlist, closelist):
    neighbors = []
    if isvalid_node(matrix, currentnode.x, currentnode.y+1, openlist, closelist):
        neighbors.append(Node2(currentnode.x, currentnode.y+1))
    if isvalid_node(matrix, currentnode.x, currentnode.y-1, openlist, closelist):
        neighbors.append(Node2(currentnode.x, currentnode.y-1))
    if isvalid_node(matrix, currentnode.x-1, currentnode.y, openlist, closelist):
        neighbors.append(Node2(currentnode.x-1, currentnode.y))
    if isvalid_node(matrix, currentnode.x+1, currentnode.y, openlist, closelist):
        neighbors.append(Node2(currentnode.x+1, currentnode.y))
    return neighbors

def main_2(matrix, start, end):
    start_time = time.time()
    # 设置起点和终点,注意起点还要设置其初始的F，G，H值
    start.initnode(None, end)
    result = astar_search2(matrix, start, end)
    # 记录路径
    open_path = []
    # 开始寻路时定义的数字
    road = 100
    # 回溯迷宫最短路径
    while result:
        open_path.append(Node2(result.x, result.y))
        result = result.parent
    # 输出迷宫和路径，路径从road数值开始
    if open_path != []:
        for node in open_path[::-1]:
            x = node.x
            y = node.y
            matrix[x][y] = road
            road += 1
        print('存在最短路径:')
        print(matrix)
    else:
        print('找不到最短路径')
    end_time = time.time()
    print('算法运行时间：{}'.format(end_time - start_time))

# 地图1求解
# main1 = main(a, Node(0, 0), Node(4, 4))

# 地图2求解
# main2 = main(b, Node(0, 0), Node(9, 9))

# 地图2状态2求解
# main3 = main(b, Node(0, 4), Node(6, 9))

# 地图2启发式函数h2求解
main4 = main_2(b, Node2(0, 0), Node2(9, 9))