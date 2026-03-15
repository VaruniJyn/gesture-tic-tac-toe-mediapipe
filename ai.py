import random

def check_winner(board):
    for row in board:
        if row[0]==row[1]==row[2]!="":
            return row[0]
    for col in range(3):
        if board[0][col]==board[1][col]==board[2][col]!="":
            return board[0][col]

    if board[0][0]==board[1][1]==board[2][2]!="":
        return board[0][0]

    if board[0][2]==board[1][1]==board[2][0]!="":
        return board[0][2]
    return None

def is_full(board):
    for row in board:
        if "" in row:
            return False
    return True

def minimax(board,is_max):
    winner=check_winner(board)
    if winner=="O":
        return 1
    if winner=="X":
        return -1
    if is_full(board):
        return 0

    if is_max:
        best=-100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="O"
                    score=minimax(board,False)
                    board[r][c]=""
                    best=max(best,score)
        return best
    else:
        best=100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="X"
                    score=minimax(board,True)
                    board[r][c]=""
                    best=min(best,score)
        return best
    
def best_move(board):
    best_score=-100
    move=None
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                board[r][c]="O"
                score=minimax(board,False)
                board[r][c]=""
                if score>best_score:
                    best_score=score
                    move=(r,c)
    return move

def random_move(board):
    empty=[]
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                empty.append((r,c))
    return random.choice(empty)

def computer_move(board,difficulty):
    if difficulty=="easy":
        return random_move(board)
    if difficulty=="medium":
        if random.random()<0.5:
            return random_move(board)
        else:
            return best_move(board)

    if difficulty=="hard":
        if random.random()<0.9:
            return best_move(board)
        else:
            return random_move(board)