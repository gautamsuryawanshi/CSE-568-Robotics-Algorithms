#! /usr/bin/env python

import numpy as np



class Node():
  
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def sort_node_list(open_list):

  for num in range(len(open_list) -1 ,0 ,-1):
    for idx in range(num):
      if (open_list[idx].f > open_list[idx+1].f):
        temp = open_list[idx]
        open_list[idx] = open_list[idx+1]
        open_list[idx+1] = temp

  return open_list

def get_heuristic_distance(child,goal):
  distance = (np.square(goal[0] - child.position[0]) + np.square(goal[1] - child.position[1]))
  return distance

def get_neighbour_nodes(node,maze):
  
  row,col = maze.shape
  children = []
  
  cx = node.position[0]
  cy = node.position[1]

  neighbour_pos = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

  
  
  for n in neighbour_pos:
    
    nx = n[0]
    ny = n[1]
  

    node_position = (cx + nx, cy + ny)

    if node_position[0] >= 0 and node_position[1]>=0 and node_position[0] <= row-1 and node_position[1] <= col-1 and maze[node_position[0]][node_position[1]] != 1  :
      new_node = Node(node, node_position)
      children.append(new_node)


  return children

def astar(maze,start_node,goal_node,start,goal):
  
    
    open_nodes = []
    closed_nodes = []

    open_nodes.append(start_node)

    while len(open_nodes) > 0:
      
      open_nodes = sort_node_list(open_nodes)
      current_node = open_nodes[0]
      open_nodes.pop(0)
      closed_nodes.append(current_node)


      if current_node == goal_node:
        path = []
        current = current_node
        while current is not None:
          path.append(current.position)
          current = current.parent
        return path[::-1] 

      current_node_neighbours = get_neighbour_nodes(current_node,maze)


      for node in current_node_neighbours:
          
        if node not in closed_nodes and node not in open_nodes:
          
          x = np.sqrt(np.square(start[0] - node.position[0]) + np.square(start[1] - node.position[1]))
          if x > 1:
            x = 1.5
          node.g = current_node.g + x
          node.h = get_heuristic_distance(node,goal)
          node.f = node.g + node.h
          open_nodes.append(node)

def givePath():

    maze = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,
       0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,
       0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,
       0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,
       0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,
       0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,
       0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,
       0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,
       0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,
       0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0,
       0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]

    arr = []
    for i in range(0,len(maze),18):
      ls = maze[i:i+18]
      arr.append(ls)

    maze = np.asarray(arr)

    row,col = maze.shape

    for r in range(row):
      for c in range(col):
        x1 = r - 1
        y1 = c

        x2 = r
        y2 = c + 1

        if x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0 and x1 <= row-1 and y1 <= col-1 and x2 <= row-1 and y2 <= col-1 and maze[x1][y1] == 1 and maze[x2][y2] == 1:
          maze[r][c] = 1

    start = (12, 1)
    goal = (1, 13)

    start_node = Node(None, start)
    goal_node = Node(None, goal)
    
    path = astar(maze,start_node,goal_node,start, goal)

    map_stage_ros = []
    for y in range(-10,10):
        row = []
        for x in range(-9,9):
            row.append([x,y*-1])

        map_stage_ros.append(row)

    map_stage_ros = np.asarray(map_stage_ros) 

    
    final_path = []
    for p in path:
        x = p[0]
        y = p[1]
        final_path.append(map_stage_ros[x][y])


    final_path.pop(0)
    
    return final_path

    # for p in path:
    #   maze[p[0]][p[1]] = 3

    # import matplotlib.pyplot as plt
    # plt.imshow(maze)


