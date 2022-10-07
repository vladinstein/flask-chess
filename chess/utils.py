from chess.models import Rank
from chess import db

def get_moves(game_id, x, y, figure):
    go = {}
    attack = {}
    if figure == 1:
        go, attack = get_white_pawn_moves(game_id, x, y)
    elif figure == 2:
        go, attack = get_white_knight_moves(game_id, x, y)
    elif figure == 3:
        go, attack = get_white_bishop_moves(game_id, x, y)
    elif figure == 4:
        go, attack = get_white_rook_moves(game_id, x, y)
    elif figure == 5:
        go, attack = get_white_queen_moves(game_id, x, y)
    elif figure == 6:
        go, attack = get_white_king_moves(game_id, x, y)
    elif figure == 7:
        go, attack = get_black_pawn_moves(game_id, x, y)
    elif figure == 8:
        go, attack = get_black_knight_moves(game_id, x, y)
    elif figure == 9:
        go, attack = get_black_bishop_moves(game_id, x, y)
    elif figure == 10:
        go, attack = get_black_rook_moves(game_id, x, y)
    elif figure == 11:
        go, attack = get_black_queen_moves(game_id, x, y)
    else:
        go, attack = get_black_king_moves(game_id, x, y)
    return go, attack

def get_white_pawn_moves(game_id, x, y):
    rank={}
    go = {}
    attack = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
                                           Rank.f, Rank.g, Rank.h).filter_by(game_id=game_id, 
                                           number=i).first()
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


def get_white_knight_moves(game_id, x, y):
    pass
def get_white_bishop_moves(game_id, x, y):
    pass
def get_white_rook_moves(game_id, x, y):
    pass
def get_white_queen_moves(game_id, x, y):
    pass
def get_white_king_moves(game_id, x, y):
    pass
def get_black_pawn_moves(game_id, x, y):
    rank={}
    go = {}
    attack = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
                                           Rank.f, Rank.g, Rank.h).filter_by(game_id=game_id, 
                                           number=i).first()
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
    pass
def get_black_bishop_moves(game_id, x, y):
    pass
def get_black_rook_moves(game_id, x, y):
    pass
def get_black_queen_moves(game_id, x, y):
    pass
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

def can_move(game_id, figures):
    rank={}
    moveable = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, Rank.f,
                                           Rank.g, Rank.h).filter_by(game_id=game_id, number=i).first()
    x = 0
    for i in range (1, 9):
        for j in range (1, 9):
            if figures == 0:
                if rank[i][j] == 1:
                    add_moveable, x = can_move_white_pawn(rank, x, i, j )
                    moveable.update(add_moveable)
                if rank[i][j] == 2:
                    pass
                if rank[i][j] == 3:
                    pass
                if rank[i][j] == 4:
                    pass
                if rank[i][j] == 5:
                    pass
                if rank[i][j] == 6:
                    pass
            else:
                if rank[i][j] == 7:
                    add_moveable, x = can_move_black_pawn(rank, x, i, j)
                    moveable.update(add_moveable)
                if rank[i][j] == 8:
                    pass
                if rank[i][j] == 9:
                    pass
                if rank[i][j] == 10:
                    pass
                if rank[i][j] == 11:
                    pass
                if rank[i][j] == 12:
                    pass
    return moveable
                
def can_move_white_pawn(rank, x, i, j):
    moveable = {}
    if rank[i+1][j] == 0 or (j < 8 and rank[i+1][j+1] > 6) \
                    or (j > 1 and rank[i+1][j-1] > 6):
                    moveable[x]=[i, j]
                    x += 1
    return moveable, x

def can_move_black_pawn(rank, x, i, j):
    moveable = {}
    if rank[i-1][j] == 0 or (j < 8 and rank[i-1][j+1] < 7 and rank[i-1][j+1] > 0) \
                    or (j > 1 and rank[i-1][j-1] < 7 and rank[i-1][j-1] > 0):
                    moveable[x]=[i, j]
                    x += 1
    return moveable, x

