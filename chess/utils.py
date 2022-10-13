from tkinter import W
from chess.models import Rank
from chess import db

def get_moves(game_id, x, y, figure):
    if figure == 1:
        go, attack = get_white_pawn_moves(game_id, x, y)
    elif figure == 2:
        go, attack = get_white_knight_moves(game_id, x, y)
    elif figure == 3 or figure == 9:
        go, attack = get_bishop_moves(game_id, x, y)
    elif figure == 4 or figure == 10:
        go, attack = get_rook_moves(game_id, x, y)
    elif figure == 5 or figure == 11:
        go, attack = get_queen_moves(game_id, x, y)
    elif figure == 6:
        go, attack = get_white_king_moves(game_id, x, y)
    elif figure == 7:
        go, attack = get_black_pawn_moves(game_id, x, y)
    elif figure == 8:
        go, attack = get_black_knight_moves(game_id, x, y)
    else:
        go, attack = get_black_king_moves(game_id, x, y)
    return go, attack

def get_board(game_id):
    rank = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
                                           Rank.f, Rank.g, Rank.h).filter_by(game_id=game_id, 
                                           number=i).first()
    return rank

def get_white_pawn_moves(game_id, x, y):
    go = {}
    attack = {}
    rank = get_board(game_id)
    z = 0
    if rank[x+1][y] == 0:
        go[z] = [x+1, y]
        z += 1
    if x == 2 and rank[x+1][y] == 0 and rank[x+2][y] == 0:
        go[z] = [x+2, y]
        z += 1
    z = 0
    if y > 1 and rank[x+1][y-1] > 6:
        attack[z] = [x+1, y-1]
        z += 1
    if y < 8 and rank[x+1][y+1] > 6:
        attack[z] = [x+1, y+1]
        z += 1
    return go, attack

def get_knight_moves_part1(rank, x, y):
    go = {}
    z = 0
    if x < 7 and y < 8 and rank[x+2][y+1] == 0:
        go[z] = [x+2, y+1]
        z += 1
    if x < 8 and y < 7 and rank[x+1][y+2] == 0:
        go[z] = [x+1, y+2]
        z += 1
    if x > 1 and y < 7 and rank[x-1][y+2] == 0:
        go[z] = [x-1, y+2]
        z += 1
    if x > 2 and y < 8 and rank[x-2][y+1] == 0:
        go[z] = [x-2, y+1]
        z += 1
    if x > 2 and y > 1 and rank[x-2][y-1] == 0:
        go[z] = [x-2, y-1]
        z += 1
    if x > 1 and y > 2 and rank[x-1][y-2] == 0:
        go[z] = [x-1, y-2]
        z += 1
    if x < 8 and y > 2 and rank[x+1][y-2] == 0:
        go[z] = [x+1, y-2]
        z += 1
    if x < 7 and y > 1 and rank[x+2][y-1] == 0:
        go[z] = [x+2, y-1]
        z += 1 
    return go

def get_white_knight_moves(game_id, x, y):
    attack = {}
    rank = get_board(game_id)
    # dictionary of possible moves
    go = get_knight_moves_part1(rank, x, y)
    # dictionary of possible attacks
    z = 0
    if x < 7 and y < 8 and rank[x+2][y+1] > 6:
        attack[z] = [x+2, y+1]
        z += 1
    if x < 8 and y < 7 and rank[x+1][y+2] > 6:
        attack[z] = [x+1, y+2]
        z += 1
    if x > 1 and y < 7 and rank[x-1][y+2] > 6:
        attack[z] = [x-1, y+2]
        z += 1
    if x > 2 and y < 8 and rank[x-2][y+1] > 6:
        attack[z] = [x-2, y+1]
        z += 1
    if x > 2 and y > 1 and rank[x-2][y-1] > 6:
        attack[z] = [x-2, y-1]
        z += 1
    if x > 1 and y > 2 and rank[x-1][y-2] > 6:
        attack[z] = [x-1, y-2]
        z += 1
    if x < 8 and y > 2 and rank[x+1][y-2] > 6:
        attack[z] = [x+1, y-2]
        z += 1
    if x < 7 and y > 1 and rank[x+2][y-1] > 6:
        attack[z] = [x+2, y-1]
        z += 1
    return go, attack

def get_bishop_moves(game_id, x, y):
    go = {}
    attack = {}
    rank = get_board(game_id)
    # we don't need a separate counter for attacks cause we don't really use keys anywhere 
    z = 0
    if x < 8 and y < 8:
        if x > y:
            steps = 9 - x
        else:
            steps = 9 - y
        for i in range (1, steps):
            if rank[x+i][y+i] == 0:
                go[z] = [x+i, y+i]
                z += 1
            elif (rank[x][y] < 7 and rank[x+i][y+i] > 6) or (rank[x][y] > 6  and rank[x+i][y+i] < 7):
                attack[z] = [x+i, y+i]
                z += 1
                break
            else:
                break
    if x < 8 and y > 1:
        if x > (9 - y) :
            steps = 9 - x
        else:
            steps = y
        for i in range (1, steps):
            if rank[x+i][y-i] == 0:
                go[z] = [x+i, y-i]
                z += 1
            elif (rank[x][y] < 7 and rank[x+i][y-i] > 6) or (rank[x][y] > 6 and rank[x+i][y-i] < 7):
                attack[z] = [x+i, y-i]
                z += 1
                break
            else:
                break
    if x > 1 and y > 1:
        if x < y:
            steps = x
        else:
            steps = y
        for i in range (1, steps):
            if rank[x-i][y-i] == 0:
                go[z] = [x-i, y-i]
                z += 1
            elif (rank[x][y] < 7 and rank[x-i][y-i] > 6) or (rank[x][y] > 6 and rank[x-i][y-i] < 7):
                attack[z] = [x-i, y-i]
                z += 1
                break
            else:
                break
    if x > 1 and y < 8:
        if (9 - x) > y:
            steps = x
        else:
            steps = 9 - y
        for i in range (1, steps):
            if rank[x-i][y+i] == 0:
                go[z] = [x-i, y+i]
                z += 1
            elif (rank[x][y] < 7 and rank[x-i][y+i] > 6) or (rank[x][y] > 6 and rank[x-i][y+i] < 7):
                attack[z] = [x-i, y+i]
                z += 1
                break
            else:
                break
    return go, attack
 
def get_rook_moves(game_id, x, y):
    go = {}
    attack = {}
    rank = get_board(game_id)
    # we use 20 here, so that we can merge dicts later (indexes need to be different)
    z = 20
    if y < 8:
        steps = 9 - y
        for i in range (1, steps):
            if rank[x][y+i] == 0:
                go[z] = [x, y+i]
                z += 1
            elif (rank[x][y] < 7 and rank[x][y+i] > 6) or (rank[x][y] > 6 and rank[x][y+i] < 7):
                attack[z] = [x, y+i]
                z += 1
                break
            else:
                break
    if x < 8:
        steps = 9 - x
        for i in range (1, steps):
            if rank[x+i][y] == 0:
                go[z] = [x+i, y]
                z += 1
            elif (rank[x][y] < 7 and rank[x+i][y] > 6) or (rank[x][y] > 6 and rank[x+i][y] < 7):
                attack[z] = [x+i, y]
                z += 1
                break
            else:
                break
    if y > 1:
        steps = y
        for i in range (1, steps):
            if rank[x][y-i] == 0:
                go[z] = [x, y-i]
                z += 1
            elif (rank[x][y] < 7 and rank[x][y-i] > 6) or (rank[x][y] > 6 and rank[x][y-i] < 7):
                attack[z] = [x, y-i]
                z += 1
                break
            else:
                break
    if x > 1:
        steps = x
        for i in range (1, steps):
            if rank[x-i][y] == 0:
                go[z] = [x-i, y]
                z += 1
            elif (rank[x][y] < 7 and rank[x-i][y] > 6) or (rank[x][y] > 6 and rank[x-i][y] < 7):
                attack[z] = [x-i, y]
                z += 1
                break
            else:
                break
    return go, attack

def get_queen_moves(game_id, x, y):
    go, attack = get_bishop_moves(game_id, x, y)
    go_2, attack_2 = get_rook_moves(game_id, x, y)
    go.update(go_2)
    attack.update(attack_2)
    return go, attack

def get_white_king_moves(game_id, x, y):
    pass
def get_black_pawn_moves(game_id, x, y):
    go = {}
    attack = {}
    rank = get_board(game_id)
    z = 0
    if rank[x-1][y] == 0:
        go[z] = [x-1, y]
        z += 1
    if x == 7 and rank[x-1][y] == 0 and rank[x-2][y] == 0:
        go[z] = [x-2, y]
        z += 1
    z = 0
    if y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0:
        attack[z] = [x-1, y-1]
        z +=1
    if y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0:
        attack[z] = [x-1, y+1]
        z +=1
    return go, attack

def get_black_knight_moves(game_id, x, y):
    attack = {}
    rank = get_board(game_id)
    # dictionary of possible moves
    go = get_knight_moves_part1(rank, x, y)
    # dictionary of possible attacks
    z = 0
    if x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0:
        attack[z] = [x+2, y+1]
        z += 1
    if x < 8 and y < 7 and rank[x+1][y+2] < 7 and rank[x+1][y+2] > 0:
        attack[z] = [x+1, y+2]
        z += 1
    if x > 1 and y < 7 and rank[x-1][y+2] < 7 and rank[x-1][y+2] > 0:
        attack[z] = [x-1, y+2]
        z += 1
    if x > 2 and y < 8 and rank[x-2][y+1] < 7 and rank[x-2][y+1] > 0:
        attack[z] = [x-2, y+1]
        z += 1
    if x > 2 and y > 1 and rank[x-2][y-1] < 7 and rank[x-2][y-1] > 0:
        attack[z] = [x-2, y-1]
        z += 1
    if x > 1 and y > 2 and rank[x-1][y-2] < 7 and rank[x-1][y-2] > 0:
        attack[z] = [x-1, y-2]
        z += 1
    if x < 8 and y > 2 and rank[x+1][y-2] < 7 and rank[x+1][y-2] > 0:
        attack[z] = [x+1, y-2]
        z += 1
    if x < 7 and y > 1 and rank[x+2][y-1] < 7 and rank[x+2][y-1] > 0:
        attack[z] = [x+2, y-1]
        z += 1
    return go, attack

def get_black_king_moves(game_id, x, y):
    pass

def create_game(game_id):
    rank = {}
    for i in range(1, 9):
        if i == 1:
            rank[i] = Rank(game_id=game_id, number=i, a=4, b=2, c=3, d=5, e=6, f=3, g=2, h=4)
        elif i == 2:
            rank[i] = Rank(game_id=game_id, number=i, a=1, b=1, c=1, d=1, e=1, f=1, g=1, h=1)
        elif i == 7:
            rank[i] = Rank(game_id=game_id, number=i, a=7, b=7, c=7, d=7, e=7, f=7, g=7, h=7)
        elif i == 8:
            rank[i] = Rank(game_id=game_id, number=i, a=10, b=8, c=9, d=11, e=12, f=9, g=8, h=10)
        else:
            rank[i] = Rank(game_id=game_id, number=i, a=0, b=0, c=0, d=0, e=0, f=0, g=0, h=0)
        db.session.add(rank[i])
    db.session.commit()

def check_can_move(game_id, figures):
    rank = get_board(game_id)
    moveable = {} 
    z = 0
    for x in range (1, 9):
        for y in range (1, 9):
            if figures == 0:
                if rank[x][y] == 1:
                    add_moveable, z = check_white_pawn_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 2:
                    add_moveable, z = check_white_knight_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 3:
                    add_moveable, z = check_white_bishop_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 4:
                    add_moveable, z = check_white_rook_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 5:
                    add_moveable, z = check_white_queen_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 6:
                    pass
            else:
                if rank[x][y] == 7:
                    add_moveable, z = check_black_pawn_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 8:
                    add_moveable, z = check_black_knight_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 9:
                    add_moveable, z = check_black_bishop_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 10:
                    add_moveable, z = check_black_rook_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 11:
                    add_moveable, z = check_black_queen_can_move(rank, z, x, y)
                    moveable.update(add_moveable)
                if rank[x][y] == 12:
                    pass
    return moveable
                
def check_white_pawn_can_move(rank, z, x, y):
    moveable = {}
    if x < 8:
        if rank[x+1][y] == 0 or (y < 8 and rank[x+1][y+1] > 6) \
        or (y > 1 and rank[x+1][y-1] > 6):
            moveable[z]=[x, y]
            z += 1
    return moveable, z

def check_black_pawn_can_move(rank, z, x, y):
    moveable = {}
    if x > 1:
        if rank[x-1][y] == 0 or (y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0) \
        or (y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0):
            moveable[z]=[x, y]
            z += 1
    return moveable, z

def check_knight_can_move_part1(rank, x, y):
    if (x < 7 and y < 8 and rank[x+2][y+1] == 0) or (x < 8 and y < 7 and rank[x+1][y+2] == 0) or \
    (x > 1 and y < 7 and rank[x-1][y+2] == 0) or (x > 2 and y < 8 and rank[x-2][y+1] == 0) or \
    (x > 2 and y > 1 and rank[x-2][y-1] == 0) or (x > 1 and y > 2 and rank[x-1][y-2] == 0) or \
    (x < 8 and y > 2 and rank[x+1][y-2] == 0) or (x < 7 and y > 1 and rank[x+2][y-1] == 0):
        return True
    else:
        return False

def check_white_knight_can_move(rank, z, x, y):
    moveable = {}
    if check_knight_can_move_part1(rank, x, y) or (x < 7 and y < 8 and rank[x+2][y+1] > 6) or \
    (x < 8 and y < 7 and rank[x+1][y+2] > 6) or (x > 1 and y < 7 and rank[x-1][y+2] > 6) or \
    (x > 2 and y < 8 and rank[x-2][y+1] > 6) or (x > 2 and y > 1 and rank[x-2][y-1] > 6) or \
    (x > 1 and y > 2 and rank[x-1][y-2] > 6) or (x < 8 and y > 2 and rank[x+1][y-2] > 6) or \
    (x < 7 and y > 1 and rank[x+2][y-1] > 6):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_knight_can_move(rank, z, x, y):
    moveable = {}
    if check_knight_can_move_part1(rank, x, y) or \
    (x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0) or \
    (x < 8 and y < 7 and rank[x+1][y+2] < 7 and rank[x+1][y+2] > 0) or \
    (x > 1 and y < 7 and rank[x-1][y+2] < 7 and rank[x-1][y+2] > 0) or \
    (x > 2 and y < 8 and rank[x-2][y+1] < 7 and rank[x-2][y+1] > 0) or \
    (x > 2 and y > 1 and rank[x-2][y-1] < 7 and rank[x-2][y-1] > 0) or \
    (x > 1 and y > 2 and rank[x-1][y-2] < 7 and rank[x-1][y-2] > 0) or \
    (x < 8 and y > 2 and rank[x+1][y-2] < 7 and rank[x+1][y-2] > 0) or \
    (x < 7 and y > 1 and rank[x+2][y-1] < 7 and rank[x+2][y-1] > 0):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_white_bishop_can_move(rank, z, x, y):
    moveable = {}
    if (x < 8 and y < 8 and (rank[x+1][y+1] == 0 or rank[x+1][y+1] > 6)) or \
    (x < 8 and y > 1 and (rank[x+1][y-1] == 0 or rank[x+1][y-1] > 6)) or \
    (x > 1 and y > 1 and (rank[x-1][y-1] == 0 or rank[x-1][y-1] > 6)) or \
    (x > 1 and y < 8 (rank[x-1][y+1] == 0 or rank[x-1][y+1] > 6)):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_bishop_can_move(rank, z, x, y):
    moveable = {}
    if (x < 8 and y < 8 and rank[x+1][y+1] < 7) or (x < 8 and y > 1 and rank[x+1][y-1] < 7) or \
    (x > 1 and y > 1 and rank[x-1][y-1] < 7) or (x > 1 and y < 8 and rank[x-1][y+1] < 7):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_white_rook_can_move(rank, z, x, y):
    moveable = {}
    if (y < 8 and (rank[x][y+1] == 0 or rank[x][y+1] > 6)) or \
    (x < 8 and (rank[x+1][y] == 0 or rank[x+1][y] > 6)) or \
    (y > 1 and (rank[x][y-1] == 0 or rank[x][y-1] > 6)) or \
    (x > 1 and (rank[x-1][y] == 0 or rank[x-1][y] > 6)):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_rook_can_move(rank, z, x, y):
    moveable = {}
    if (y < 8 and (rank[x][y+1] < 7)) or (x < 8 and (rank[x+1][y] < 7)) or \
    (y > 1 and (rank[x][y-1] < 7)) or (x > 1 and (rank[x-1][y] < 7)):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_white_queen_can_move(rank, z, x, y):
    moveable, z = check_white_bishop_can_move(rank, z, x, y)
    moveable_2, z = check_white_rook_can_move(rank, z, x, y)
    moveable.update(moveable_2)
    return moveable, z

def check_black_queen_can_move(rank, z, x, y):
    moveable, z = check_black_bishop_can_move(rank, z, x, y)
    moveable_2, z = check_black_rook_can_move(rank, z, x, y)
    moveable.update(moveable_2)
    return moveable, z