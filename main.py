import cv2
import pygame
import time
import math
from hand_tracker import HandTracker
from ai import computer_move

pygame.init()
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Tic Tac Toe")

cap = cv2.VideoCapture(0)
tracker = HandTracker()

game_state = "menu"
difficulty = "medium"

current_cell = None
hover_start_time = 0
hover_delay = 1.0

board = [["","",""],["","",""],["","",""]]
player_turn = True
computer_move_pending = False
computer_move_time = 0
computer_delay = 1
game_over = False
winner = None
win_line = None

# MENU 
def draw_menu(screen):
    title_font = pygame.font.SysFont(None,80)
    button_font = pygame.font.SysFont(None,50)
    title = title_font.render("Gesture Tic Tac Toe",True,(0,255,255))
    screen.blit(title,(WIDTH//2-title.get_width()//2,120))
    start = button_font.render("START GAME",True,(255,255,255))
    diff = button_font.render(f"DIFFICULTY: {difficulty.upper()}",True,(255,255,255))
    exit_btn = button_font.render("EXIT",True,(255,255,255))
    screen.blit(start,(WIDTH//2-start.get_width()//2,280))
    screen.blit(diff,(WIDTH//2-diff.get_width()//2,360))
    screen.blit(exit_btn,(WIDTH//2-exit_btn.get_width()//2,440))


def get_menu_selection(x,y):
    if 260 < y < 320:
        return "start"
    if 340 < y < 400:
        return "difficulty"
    if 420 < y < 480:
        return "exit"
    return None

# GRID 
def draw_neon_grid(screen):
    t = pygame.time.get_ticks() / 1000
    glow = int(150 + 100 * abs(math.sin(t)))
    color=(0,glow,glow)
    pygame.draw.line(screen,color,(266,0),(266,600),6)
    pygame.draw.line(screen,color,(533,0),(533,600),6)
    pygame.draw.line(screen,color,(0,200),(800,200),6)
    pygame.draw.line(screen,color,(0,400),(800,400),6)


def draw_board(screen):
    cell_width=WIDTH//3
    cell_height=HEIGHT//3
    font=pygame.font.SysFont(None,120)

    for r in range(3):
        for c in range(3):
            if board[r][c]!="":
                text=font.render(board[r][c],True,(255,255,255))
                x=c*cell_width+cell_width//3
                y=r*cell_height+cell_height//4
                screen.blit(text,(x,y))

def get_cell(x,y):
    cell_width=WIDTH//3
    cell_height=HEIGHT//3
    col=x//cell_width
    row=y//cell_height
    row=min(row,2)
    col=min(col,2)
    return row,col


def highlight_cell(screen,row,col):
    cell_width=WIDTH//3
    cell_height=HEIGHT//3
    rect_x=col*cell_width
    rect_y=row*cell_height
    pygame.draw.rect(screen,(0,120,255),(rect_x,rect_y,cell_width,cell_height),5)


# HOVER RING

def draw_hover_progress(screen,row,col,progress):
    cell_width=WIDTH//3
    cell_height=HEIGHT//3
    cx=col*cell_width+cell_width//2
    cy=row*cell_height+cell_height//2
    radius=40
    rect=pygame.Rect(cx-radius,cy-radius,radius*2,radius*2)
    end_angle=progress*360

    pygame.draw.arc(
        screen,
        (255,255,0),
        rect,
        math.radians(-90),
        math.radians(end_angle-90),
        6
    )

# WIN DETECTION
def check_winner(board):
    for r in range(3):
        if board[r][0]==board[r][1]==board[r][2]!="":
            return board[r][0],("row",r)

    for c in range(3):
        if board[0][c]==board[1][c]==board[2][c]!="":
            return board[0][c],("col",c)

    if board[0][0]==board[1][1]==board[2][2]!="":
        return board[0][0],("diag",0)

    if board[0][2]==board[1][1]==board[2][0]!="":
        return board[0][2],("diag",1)
    return None,None

def draw_win_line(screen,win_line):
    if not win_line:
        return
    color=(0,255,0)
    if win_line[0]=="row":
        r=win_line[1]
        y=r*200+100
        pygame.draw.line(screen,color,(50,y),(750,y),10)

    elif win_line[0]=="col":
        c=win_line[1]
        x=c*266+133
        pygame.draw.line(screen,color,(x,50),(x,550),10)

    elif win_line[0]=="diag":
        if win_line[1]==0:
            pygame.draw.line(screen,color,(50,50),(750,550),10)
        else:
            pygame.draw.line(screen,color,(750,50),(50,550),10)

def draw_game_over(screen,winner):
    font=pygame.font.SysFont(None,80)
    if winner=="X":
        text="PLAYER WINS"
    elif winner=="O":
        text="COMPUTER WINS"
    else:
        text="DRAW"

    label=font.render(text,True,(255,255,0))
    rect=label.get_rect(center=(WIDTH//2,HEIGHT//2))

    screen.blit(label,rect)
    small=pygame.font.SysFont(None,35)

    restart=small.render("Hold CENTER to Restart",True,(255,255,255))
    menu=small.render("Hold BOTTOM RIGHT for Menu",True,(255,255,255))

    screen.blit(restart,(260,520))
    screen.blit(menu,(220,560))

# RESET 
def reset_game():
    global board,player_turn,game_over,winner,win_line
    board=[["","",""],["","",""],["","",""]]
    player_turn=True
    game_over=False
    winner=None
    win_line=None

def go_to_menu():
    global game_state
    reset_game()
    game_state="menu"

# MAIN LOOP 
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    frame,index_pos=tracker.get_index_finger(frame)
    screen.fill((0,0,0))
    if game_state=="menu":
        draw_menu(screen)
        if index_pos:
            x,y=index_pos
            x=int(x*WIDTH/frame.shape[1])
            y=int(y*HEIGHT/frame.shape[0])
            pygame.draw.circle(screen,(0,255,0),(x,y),10)
            selection=get_menu_selection(x,y)

            if selection!=current_cell:
                current_cell=selection
                hover_start_time=time.time()
            else:
                hover=time.time()-hover_start_time
                if hover>hover_delay:
                    if selection=="start":
                        game_state="playing"
                    elif selection=="difficulty":
                        if difficulty=="easy":
                            difficulty="medium"
                        elif difficulty=="medium":
                            difficulty="hard"
                        else:
                            difficulty="easy"
                    elif selection=="exit":
                        running=False
                    hover_start_time=time.time()
        pygame.display.update()
        cv2.imshow("Camera",frame)
        continue

    draw_neon_grid(screen)
    draw_board(screen)
    draw_win_line(screen,win_line)

    if game_over:
        draw_game_over(screen,winner)
    if index_pos and player_turn and not game_over:
        x,y=index_pos
        x=int(x*WIDTH/frame.shape[1])
        y=int(y*HEIGHT/frame.shape[0])
        row,col=get_cell(x,y)
        highlight_cell(screen,row,col)
        cell=(row,col)

        if cell!=current_cell:
            current_cell=cell
            hover_start_time=time.time()
        else:
            hover=time.time()-hover_start_time
            progress=min(hover/hover_delay,1)
            draw_hover_progress(screen,row,col,progress)

            if hover>hover_delay:
                r,c=cell
                if board[r][c]=="":
                    board[r][c]="X"
                    player_turn=False
                    computer_move_pending=True
                    computer_move_time=time.time()
                hover_start_time=time.time()
        pygame.draw.circle(screen,(0,255,0),(x,y),10)

    if computer_move_pending and not game_over:
        if time.time()-computer_move_time>computer_delay:
            r,c=computer_move(board,difficulty)
            if board[r][c]=="":
                board[r][c]="O"
            computer_move_pending=False
            player_turn=True

    if not game_over:
        winner,win_line=check_winner(board)
        if winner:
            game_over=True
        elif all(cell!="" for row in board for cell in row):
            winner="Draw"
            game_over=True

    if game_over and index_pos:
        x,y=index_pos
        x=int(x*WIDTH/frame.shape[1])
        y=int(y*HEIGHT/frame.shape[0])
        row,col=get_cell(x,y)
        if row==1 and col==1:
            if time.time()-hover_start_time>2:
                reset_game()

        if row==2 and col==2:
            if time.time()-hover_start_time>2:
                go_to_menu()


    pygame.display.update()
    cv2.imshow("Camera",frame)

    if cv2.waitKey(1)&0xFF==27:
        break


cap.release()
pygame.quit()
cv2.destroyAllWindows()