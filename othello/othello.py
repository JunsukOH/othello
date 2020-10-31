from bangtal import *
from enum import Enum

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)



# 1. 장면을 생성하고, 게임을 시작한다.
scene = Scene("Othello", "Images/background.png")



# 2. Stone 물체를 생성한다.
class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3
class Turn(Enum):
    BLACK = 1
    WHITE = 2
turn = Turn.BLACK



# 3. Stone의 상태를 바꾼다.
def setState(x, y, s):
    object = board[y][x]
    object.state = s
    if s == State.BLANK:
        object.setImage("Images/blank.png")
    elif s == State.BLACK:
        object.setImage("Images/black.png")
    elif s == State.WHITE:
        object.setImage("Images/white.png")
    elif turn == Turn.BLACK:
        object.setImage("Images/black possible.png")
    else:
        object.setImage("Images/white possible.png")



# 5. 돌이 놓일 수 있는 위치를 표시한다.
def setPossible_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK
    possible = False
    while True:
        x = x + dx
        y = y + dy
        if x < 0 or x > 7: return False
        if y < 0 or y > 7: return False
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            return possible
        else: return False
def setPossible_xy(x, y):
    object = board[y][x]
    if object.state == State.BLACK: return False
    if object.state == State.WHITE: return False
    setState(x, y, State.BLANK)
    if (setPossible_xy_dir(x, y, 0, 1)): return True
    if (setPossible_xy_dir(x, y, 1, 1)): return True
    if (setPossible_xy_dir(x, y, 1, 0)): return True
    if (setPossible_xy_dir(x, y, 1, -1)): return True
    if (setPossible_xy_dir(x, y, 0, -1)): return True
    if (setPossible_xy_dir(x, y, -1, -1)): return True
    if (setPossible_xy_dir(x, y, -1, 0)): return True
    if (setPossible_xy_dir(x, y, -1, 1)): return True
    return False
def setPossible():
    possible = False
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                setState(x, y, State.POSSIBLE)
                possible = True
    return possible



# 6. 자신의 돌과 사이에 있는 상대편 돌이 자신의 돌로 바뀐다.
def reverse_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK
    possible = False
    while True:
        x = x + dx
        y = y + dy
        if x < 0 or x > 7: return
        if y < 0 or y > 7: return
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy
                    object = board[y][x]
                    if object.state == other:
                        setState(x, y, mine)
                    else: return
        else: return
def reverse_xy(x, y):
    reverse_xy_dir(x, y, 0, 1)
    reverse_xy_dir(x, y, 1, 1)
    reverse_xy_dir(x, y, 1, 0)
    reverse_xy_dir(x, y, 1, -1)
    reverse_xy_dir(x, y, 0, -1)
    reverse_xy_dir(x, y, -1, -1)
    reverse_xy_dir(x, y, -1, 0)
    reverse_xy_dir(x, y, -1, 1)



# 8. 현재 보드의 상태를 표시한다.
black_left = Object("Images/blank.png")
black_left.locate(scene, 755, 280)
black_left.show()
black_right = Object("Images/blank.png")
black_right.locate(scene, 825, 280)
black_right.show()
white_left = Object("Images/blank.png")
white_left.locate(scene, 1075, 280)
white_left.show()
white_right = Object("Images/blank.png")
white_right.locate(scene, 1145, 280)
white_right.show()
def point():
    black = 0
    white = 0
    for y in range(8):
        for x in range(8):
            if board[y][x].state == State.BLACK: black += 1
            if board[y][x].state == State.WHITE: white += 1
    if black < 10:
        black_left.setImage("Images/blank.png")
        black_right.setImage("Images/L" + str(black%10) + ".png")
    else:
        black_left.setImage("Images/L" + str(black//10) + ".png")
        black_right.setImage("Images/L" + str(black%10) + ".png")
    if white < 10:
        white_left.setImage("Images/L" + str(white%10) + ".png")
        white_right.setImage("Images/blank.png")
    else:
        white_left.setImage("Images/L" + str(white//10) + ".png")
        white_right.setImage("Images/L" + str(white%10) + ".png")



# 9. White Stone은 컴퓨터가 놓는다.
def best_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK
    best = 0
    possible = False
    while True:
        x = x + dx
        y = y + dy 
        if x < 0 or x > 7: return
        if y < 0 or y > 7: return
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy
                    object = board[y][x]
                    if object.state == other:
                        best += 1
                    else: return best
        else: return
def best_xy(x,y):
    very_best = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            best = best_xy_dir(x, y, dx, dy)
            if best != None:
                if dx != 0 or dy != 0:
                    very_best += best
    return very_best
def stone_byComputer():
    global turn
    very_best, bx, by = -1, -1, -1
    for y in range(8):
        for x in range(8):
            if board[y][x].state == State.POSSIBLE:
                best = best_xy(x, y)
                if best != None:
                    if very_best < best:
                        very_best = best
                        bx, by = x, y
    if (bx > -1 and bx < 8) and (by > -1 and by < 8):
        object = board[by][bx]
        if object.state == State.POSSIBLE:
            setState(bx, by, State.WHITE)
            reverse_xy(bx, by)
            turn = Turn.BLACK
            if not setPossible():
                turn = Turn.BLACK
                if not setPossible():
                    showMessage("게임이 종료되었습니다")
    else: turn = Turn.BLACK



# 7. 돌을 놓을 수 없는 경우에 패스한다.
def stone_onMouseAction(x, y):
    global turn
    object = board[y][x]
    if object.state == State.POSSIBLE and turn == Turn.BLACK:
        setState(x, y, State.BLACK)
        reverse_xy(x, y)
        turn = Turn.WHITE
        if not setPossible():
            turn = Turn.WHITE
            if not setPossible():
                showMessage("게임이 종료되었습니다")
        stone_byComputer()
        point()



# 4. 게임을 초기화/시작한다.
board = []
for y in range(8):
    board.append([])
    for x in range(8):
        object = Object("Images/blank.png")
        object.locate(scene, 40 + x * 80, 40 + y * 80)
        object.show()
        object.onMouseAction = lambda mx, my, action, ix = x, iy = y: stone_onMouseAction(ix, iy)
        object.state = State.BLANK
        board[y].append(object)
setState(3, 3, State.BLACK)
setState(4, 4, State.BLACK)
setState(3, 4, State.WHITE)
setState(4, 3, State.WHITE)
setPossible()
point()
startGame(scene)