# 265 / 2018, 33.13 score, py3
# no use of "Back in Time"
# find biggest rectangle relative to current position, enclose it

import sys
import math
import numpy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

opponent_count = int(input())  # Opponent count


#find the biggest rectangle using current position as vertex
def find_biggest_rectangle(x,y,board):
    max_gained,target_x,target_y = 0,0,0
    for rect_x in range(0,35):
        for rect_y in range(0,20):
            if is_available_rectangle(rect_x,rect_y,x,y,board):
                num_gained = count_spaces_gained(rect_x,rect_y,x,y,board)
                if num_gained > max_gained:
                    target_x = rect_x
                    target_y = rect_y
                    max_gained = num_gained
                    # print("x:"+str(target_x)+"y:"+str(target_y)+"a:"+str(max_gained),file=sys.stderr)
    if max_gained == 0:
        print("should find somewhere to go",file=sys.stderr)
        target_x, target_y = find_closest(x,y,board)
    return target_x,target_y,x,y

def find_closest(x,y,board):
    min_dist = 99999
    for i in range(0,35):
        for j in range(0,20):
            if board[j][i] == '.':
                dist = math.sqrt((i-x)**2 + (j-y)**2)
                if dist < min_dist:
                    target_x = i
                    target_y = j
                    min_dist = dist
    return target_x,target_y

def is_available_rectangle(x1,y1,x2,y2,board):
    space_to_check = board[min(y1,y2):max(y1,y2)+1,min(x1,x2):max(x1,x2)+1]
    unique_values = numpy.unique(space_to_check)
    return numpy.array_equal(unique_values,['.','0']) and not(numpy.array_equal(unique_values,['0']))

def count_spaces_gained(x1,y1,x2,y2,board):
    space_to_check = board[min(y1,y2):max(y1,y2)+1,min(x1,x2):max(x1,x2)+1]
    num_gained = len(space_to_check[numpy.where(space_to_check=='.')])
    print(x1,y1,x2,y2,num_gained,file=sys.stderr)
    return num_gained

def choose_destination(x1,y1,x2,y2,board,x0,y0,xf,yf):
    print(x1,y1,x2,y2,file=sys.stderr)
    xrange = range(min(x1,x2),max(x1,x2)+1)
    yrange = range(min(y1,y2),max(y1,y2)+1)
    xway1 = []
    xway2 = []
    yway1 = []
    yway2 = []
    
    for x in xrange:
        if board[y1][x] == '.':
            xway1.append(x)
    for y in yrange:
        if board[y][x1] == '.':
            yway1.append(y)
    for x in xrange:
        if board[y2][x] == '.':
            xway2.append(x)
    for y in yrange:
        if board[y][x2] == '.':
            yway2.append(y)
    if len(xway1)==0 and len(xway2) == 0 and len(yway1)==0 and len(yway2)==0:
        print("square done",file=sys.stderr)
        return find_closest(x0,y0,board) 
    if x0 == x1 and y0 == y1:
        print("decide corner 1",file=sys.stderr)
        if len(xway1) > len(yway1):
            return x2,y1
        else:
            return x1,y2
    elif x0 == x1 and y0 == y2:
        print("decide corner 2",file=sys.stderr)
        if len(xway2) > len(yway1):
            return x2,y2
        else:
            return x1,y1
    elif x0 == x2 and y0 == y1:
        print("decide corner 3",file=sys.stderr)
        if len(xway1) > len(yway2):
            return x1,y2
        else:
            return x2,y2
    elif x0 == x2 and y0 == y2:
        print("decide corner 4",file=sys.stderr)
        if len(xway2) > len(yway2):
            return x1,y2
        else:
            return x2,y1
    else:
        if xf is not None and yf is not None:
            print("decide as you were",file=sys.stderr)
            return xf, yf
        else:
            print("need close one",file=sys.stderr)
            return find_closest(x0,y0,board)
    
def check_stuck(x1,y1,x0,y0):
    if x1==x0 and y1==y0:
        return 0,0
    else:
        return x1,y1
    
memory_x1,memory_y1,memory_x2,memory_y2, target_x, target_y = -1,-1,-1,-1,-1,-1
# game loop
while 1:
    game_round = int(input())
    
    # x: Your x position
    # y: Your y position
    # back_in_time_left: Remaining back in time
    x, y, back_in_time_left = [int(i) for i in input().split()]
    
    for i in range(opponent_count):
        # opponent_x: X position of the opponent
        # opponent_y: Y position of the opponent
        # opponent_back_in_time_left: Remaining back in time of the opponent
        opponent_x, opponent_y, opponent_back_in_time_left = [int(j) for j in input().split()]
    board = []
    for i in range(20):
        line = input()  # One line of the map ('.' = free, '0' = you, otherwise the id of the opponent)
        board.append(list(line))
    m = numpy.array(board)

    print("last target x:"+str(target_x)+"y:"+str(target_y),file=sys.stderr)
    if x == target_x and y == target_y:
        print("targets hit",file=sys.stderr)
        target_x = None
        target_y = None
    
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    if memory_x1 == -1 or not(is_available_rectangle(memory_x1,memory_y1,memory_x2,memory_y2,m)):
        print("finding new target",file=sys.stderr)
        # if count_spaces_gained(memory_x1,memory_y1,memory_x2,memory_y2,m) > 50 and back_in_time_left and game_round > 20:
        #     print("BACK 25")
        #     continue
        memory_x1,memory_y1,memory_x2,memory_y2 = find_biggest_rectangle(x,y,m)

    target_x, target_y = choose_destination(memory_x1,memory_y1,memory_x2,memory_y2,m,x,y,target_x,target_y)
    target_x, target_y = check_stuck(target_x,target_y,x,y)
    
    print(str(target_x) + " "+ str(target_y))