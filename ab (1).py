import random
import numpy as np

# 棋盘显示函数,每次落子后显示棋盘
def show(chessboard):
    for i in range(len(chessboard)):
        mark = ' '
        row = chessboard[i]
        for j in row:
            mark = mark + tag[j + 1] + ' ' 
        print(mark)

# 判断是否产生赢家
def terminal(chessboard, win, position):
    for line in win:
        m1,n1 = position[line[0]][0],position[line[0]][1]
        m2,n2 = position[line[1]][0],position[line[1]][1]
        m3,n3 = position[line[2]][0],position[line[2]][1]
        if chessboard[m1][n1] == chessboard[m2][n2] == chessboard[m3][n3] == -1:
            return -1
        elif chessboard[m1][n1] == chessboard[m2][n2] == chessboard[m3][n3] == 1:
            return 1
    return 0

# 判断棋盘是否还有空位
def empty(chessboard, position):
     for point in position:
         if chessboard[point[0]][point[1]] == 0:
             return True
     return False
 
# 电脑走位之后,交换玩家,直到棋盘出现赢家或者没有空位
def alpha_beta(chessboard, win, position, now_player, next_player, alpha, beta):
    
    winner = terminal(chessboard, win, position)
    if winner != 0:
        return winner
    elif empty(chessboard, position) == False:
        return 0
    
    for i in range(len(position)):
        temp = position[i]
        if chessboard[temp[0]][temp[1]] == 0:
            chessboard[temp[0]][temp[1]] = now_player
            
            test = alpha_beta(chessboard, win, position, next_player, now_player, alpha, beta)
            
            chessboard[temp[0]][temp[1]] = 0
            
            # 如果现在是电脑,Max玩家,修改alpha值
            if now_player == 1:
                if test > alpha:
                    alpha = test
                if alpha >= beta:
                    return alpha
           
            # 如果现在是玩家,Min玩家,修改beta值
            else:
                if test < beta:
                    beta = test
                if alpha >= beta:
                    return alpha
   
    # 修改上一个节点的值      
    if now_player == 1:
        node = alpha
    else:
        node = beta
    return node

# 电脑计算目前最优的位置
def computer_move(chessboard, win, position):
    
    val = -2
    move_ = []
    for i in range(len(position)):
        temp = position[i]
        # 检查所有可走的位置
        if chessboard[temp[0]][temp[1]] == 0:
            chessboard[temp[0]][temp[1]] = 1   # 假设电脑走该位置
            
            if terminal(chessboard, win, position) == 1:
                return temp, i
            
            test = alpha_beta(chessboard, win, position, -1, 1, -2, 2)
            chessboard[temp[0]][temp[1]] = 0   # 将该位置清0
            
            if test > val:
                val = test 
                move_ = [temp]
            elif test == val:
                move_.append(temp)
    
    cmove = random.choice(move_)
    for j in range(len(position)):
        if cmove == position[j]:
            return cmove, j


if __name__ == '__main__':
    chessboard = [[0,0,0],[0,0,0],[0,0,0]]
    position = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    win = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
           (0, 3, 6), (1, 4, 7), (2, 5, 8),
           (0, 4, 8), (2, 4, 6))
    tag = ['x', '.', 'o']
    result = ['玩家胜利!', '平局!', '电脑胜利!']
    
    player = -1     # 玩家为Min玩家
    computer = 1    # 电脑为Max玩家
    
    first = input("请选择哪一方先下,输入x表示玩家先下,输入o表示电脑先下:")
    if first == "x":
        next_move = player 
    elif first == "o":
        next_move = computer
    else:
        next_move = player
        print("输入有误,默认玩家先下")
        
    show(chessboard)
    
    print('=========================')
    print('游戏开始!')
    while empty(chessboard, position) and terminal(chessboard, win, position) == 0:        
    
        if next_move == player and empty(chessboard, position):
            try:
                hmove = int(input("请选择你的落子位置(0-8):"))
                if chessboard[position[hmove][0]][position[hmove][1]] != 0:
                    print('该位置已有棋子,请重新选择')
                    continue
                chessboard[position[hmove][0]][position[hmove][1]] = player  
                next_move = computer     
            except:
                print("输入为0~8,请重试")
                continue
        
        if next_move == computer and empty(chessboard, position):
            cmove, po = computer_move(chessboard, win, position)         
            chessboard[cmove[0]][cmove[1]] = computer    
            print("电脑落子为:", po)
            next_move = player
          
        show(chessboard)
    
    print('=========================')
    print('最终棋局:')
    show(chessboard)
    s = terminal(chessboard, win, position)
    print('游戏结束:',result[s+1])
    print('=========================')
