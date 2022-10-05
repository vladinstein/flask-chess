from chess.models import Rank
from chess import db

def check_moves(game_id, x, y, figure):
    go = []
    attack = []
    if figure == 1:
        go, attack = white_pawn(game_id, x, y)
    elif figure == 2:
        go, attack = white_knight(game_id, x, y)
    elif figure == 3:
        go, attack = white_bishop(game_id, x, y)
    elif figure == 4:
        go, attack = white_rook(game_id, x, y)
    elif figure == 5:
        go, attack = white_queen(game_id, x, y)
    elif figure == 6:
        go, attack = white_king(game_id, x, y)
    elif figure == 7:
        go, attack = black_pawn(game_id, x, y)
    elif figure == 8:
        go, attack = black_knight(game_id, x, y)
    elif figure == 9:
        go, attack = black_bishop(game_id, x, y)
    elif figure == 10:
        go, attack = black_rook(game_id, x, y)
    elif figure == 11:
        go, attack = black_queen(game_id, x, y)
    else:
        go, attack = black_king(game_id, x, y)
    return go, attack

def white_pawn(game_id, x, y):
    rank={}
    can_go = []
    can_attack = []
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
                                           Rank.f, Rank.g, Rank.h).filter_by(game_id=game_id, 
                                           number=i).first()
    if rank[x+1][y] == 0:
        can_go.append([x+1, y])
    if x == 2 and rank[x+2][y] == 0:
        can_go.append([x+2, y])
    if y > 1 and rank[x+1][y-1] > 6:
        can_attack.append([x+1, y-1])
    if y < 8 and rank[x+1][y+1] > 6:
        can_attack.append([x+1, y+1])
    return can_go, can_attack


def white_knight(game_id, x, y):
    pass
def white_bishop(game_id, x, y):
    pass
def white_rook(game_id, x, y):
    pass
def white_queen(game_id, x, y):
    pass
def white_king(game_id, x, y):
    pass
def black_pawn(game_id, x, y):
    rank={}
    can_go = []
    can_attack = []
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
                                           Rank.f, Rank.g, Rank.h).filter_by(game_id=game_id, 
                                           number=i).first()
    if rank[x-1][y] == 0:
        can_go.append([x-1, y])
    if x == 7 and rank[x-2][y] == 0:
        can_go.append([x-2, y])
    if y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0:
        can_attack.append([x-1, y-1])
    if y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y-1] > 0:
        can_attack.append([x-1, y+1])
    return can_go, can_attack
def black_knight(game_id, x, y):
    pass
def black_bishop(game_id, x, y):
    pass
def black_rook(game_id, x, y):
    pass
def black_queen(game_id, x, y):
    pass
def black_king(game_id, x, y):
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

def white_check(game_id):
    rank={}
    can_move = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, Rank.f,
                                           Rank.g, Rank.h).filter_by(game_id=game_id, number=i).first()
    x = 0
    for i in range (1, 9):
        for j in range (1, 9):
            if rank[i][j] == 1: 
                if rank[i+1][j] == 0 or (j < 8 and rank[i+1][j+1] > 6) \
                    or (j > 1 and rank[i+1][j-1] > 6):
                    can_move[x]=[i, j]
                    x += 1
    return can_move

def black_check(game_id):
    rank={}
    can_move = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, Rank.f,
                                           Rank.g, Rank.h).filter_by(game_id=game_id, number=i).first()
    x = 0
    for i in range (1, 9):
        for j in range (1, 9):
            if rank[i][j] == 7: 
                if rank[i-1][j] == 0 or (j < 8 and rank[i-1][j+1] < 7 and rank[i-1][j+1] > 0) \
                    or (j > 1 and rank[i-1][j-1] < 7 and rank[i-1][j-1] > 0):
                    can_move[x]=[i, j]
                    x += 1
    return can_move