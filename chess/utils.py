import string
from chess.models import Game, Rank, Defences, Attacks
from chess import db
from chess.routes import session

def get_moves(game_id, x, y, piece, blocklines, checklines):
    game = Game.query.filter_by(id=session['game_id']).first()
    if piece == 1:
        go, attack, _, z = get_white_pawn_moves(game_id, x, y, blocklines=blocklines, checklines=checklines)
        # Checking en passant conditions
        if x == 5 and game.white_en_passant and abs(game.white_en_passant_y - y) == 1:
            attack, z = add_white_en_passant(attack, z, game)
    elif piece == 2:
        go, attack, _, _ = get_white_knight_moves(game_id, x, y, blocklines=blocklines, checklines=checklines)
    elif piece == 3 or piece == 9:
        go, attack, _, _ = get_bishop_moves(game_id, x, y, blocklines=blocklines, checklines=checklines)
    elif piece == 4 or piece == 10:
        go, attack, _, _ = get_rook_moves(game_id, x, y, blocklines=blocklines, checklines=checklines)
    elif piece == 5 or piece == 11:
        go, attack, _, _ = get_queen_moves(game_id, x, y, blocklines=blocklines, checklines=checklines)
    elif piece == 6:
        go, attack, _, z = get_king_moves(game_id, x, y)
        go = remove_checks(game_id, go)
        attack = remove_checks(game_id, attack)
        if game.white_king_castling:
            go, z = add_white_king_castling(game_id, go, z)
        if game.white_queen_castling:
            go, z = add_white_queen_castling(game_id, go, z)
    elif piece == 7:
        go, attack, _, z = get_black_pawn_moves(game_id, x, y, blocklines=blocklines, checklines=checklines)
        # Checking en passant conditions
        if x == 4 and game.black_en_passant and abs(game.black_en_passant_y - y) == 1:
            attack, z = add_black_en_passant(attack, z, game)
    elif piece == 8:
        go, attack, _, _ = get_black_knight_moves(game_id, x, y, blocklines=blocklines, checklines=checklines)
    elif piece == 12:
        go, attack, _, z = get_king_moves(game_id, x, y)
        go = remove_checks(game_id, go)
        attack = remove_checks(game_id, attack)
        if game.black_king_castling:
            go, z = add_black_king_castling(game_id, go, z)
        if game.black_queen_castling:
            go, z = add_black_queen_castling(game_id, go, z)
    return go, attack

def get_board(game_id):
    rank = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
                                           Rank.f, Rank.g, Rank.h).filter_by(game_id=game_id, 
                                           number=i).first()
    return rank

def get_rank(game_id, i):
    rank = {}
    rank = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
                                           Rank.f, Rank.g, Rank.h).filter_by(game_id=game_id, 
                                           number=i).first()
    return rank

def get_defences(game_id):
    defences = {}
    for i in range (1, 9):
        defences[i] = Defences.query.with_entities(Defences.game_id, Defences.a, Defences.b, 
                                        Defences.c, Defences.d, Defences.e, 
                                        Defences.f, Defences.g, Defences.h).filter_by(game_id=game_id,
                                        number=i).first()
    return defences

def get_attacks(game_id):
    attacks = {}
    for i in range (1, 9):
        attacks[i] = Attacks.query.with_entities(Attacks.game_id, Attacks.a, Attacks.b, Attacks.c,
                                            Attacks.d, Attacks.e, Attacks.f, Attacks.g,
                                            Attacks.h).filter_by(game_id=game_id, number=i).first()
    return attacks

def get_king_coordinates(game_id, opp=True):
    rank = get_board(game_id)
    for x in range (1, 9): 
        for y in range (1, 9):
            if (((session['pieces'] == 1 and rank[x][y] == 6) or (session['pieces'] == 0 and rank[x][y] == 12)) and opp) or \
               (((session['pieces'] == 1 and rank[x][y] == 12) or (session['pieces'] == 0 and rank[x][y] == 6)) and not opp):
                return [x, y]

def get_white_pawn_moves(game_id, x, y, blocklines=[], checklines=[], z=0):
    go = {}
    attack = {}
    defence = {}
    rank = get_board(game_id)
    block = False
    for line in blocklines:
        if [x, y] in line.values():
            block = True
            if x < 8 and rank[x+1][y] == 0 and [x+1, y] in line.values():
                go[z] = [x+1, y]
                z += 1
            if x == 2 and rank[x+1][y] == 0 and rank[x+2][y] == 0 and [x+2, y] in line.values():
                go[z] = [x+2, y]
                z += 1
            if y > 1 and x < 8 and rank[x+1][y-1] > 6 and [x+1, y-1] in line.values() and len(line.values()) == 2:
                attack[z] = [x+1, y-1]
                z += 1
            if y < 8 and x < 8 and rank[x+1][y+1] > 6 and [x+1, y+1] in line.values() and len(line.values()) == 2:
                attack[z] = [x+1, y+1]
                z += 1
    if not block:
        for checkline in checklines:
            if x < 8 and rank[x+1][y] == 0 and [x+1, y] in checkline.values():
                go[z] = [x+1, y]
                z += 1
            if x == 2 and rank[x+1][y] == 0 and rank[x+2][y] == 0 and [x+2, y] in checkline.values():
                go[z] = [x+2, y]
                z += 1
            if y > 1 and x < 8 and rank[x+1][y-1] > 6 and [x+1, y-1] in checkline.values():
                attack[z] = [x+1, y-1]
                z += 1
            if y < 8 and x < 8 and rank[x+1][y+1] > 6 and [x+1, y+1] in checkline.values():
                attack[z] = [x+1, y+1]
                z += 1
        if not checklines:
            if x < 8 and rank[x+1][y] == 0:
                go[z] = [x+1, y]
                z += 1
            if x == 2 and rank[x+1][y] == 0 and rank[x+2][y] == 0:
                go[z] = [x+2, y]
                z += 1
            if y > 1 and x < 8 and rank[x+1][y-1] > 6:
                attack[z] = [x+1, y-1]
                z += 1
            if y < 8 and x < 8 and rank[x+1][y+1] > 6:
                attack[z] = [x+1, y+1]
                z += 1
    if y > 1 and x < 8 and rank[x+1][y-1] < 7:
        defence[z] = [x+1, y-1]
        z += 1
    if y < 8 and x < 8 and rank[x+1][y+1] < 7:
        defence[z] = [x+1, y+1]
        z += 1
    return go, attack, defence, z

def get_black_pawn_moves(game_id, x, y, blocklines=[], checklines = [], z=0):
    go = {}
    attack = {}
    defence = {}
    rank = get_board(game_id)
    block = False
    for line in blocklines:
        if [x, y] in line.values():
            block = True
            if x > 1 and rank[x-1][y] == 0 and [x-1, y] in line.values():
                go[z] = [x-1, y]
                z += 1
            if x == 7 and rank[x-1][y] == 0 and rank[x-2][y] == 0 and [x-2, y] in line.values():
                go[z] = [x-2, y]
                z += 1
            if y > 1 and x > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0 and [x-1, y-1] in line.values() and len(line.values()) == 2:
                attack[z] = [x-1, y-1]
                z += 1
            if y < 8 and x > 1 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0 and [x-1, y+1] in line.values() and len(line.values()) == 2:
                attack[z] = [x-1, y+1]
                z += 1
    if not block:
        for checkline in checklines:
            if x > 1 and rank[x-1][y] == 0 and [x-1, y] in checkline.values():
                go[z] = [x-1, y]
                z += 1
            if x == 7 and rank[x-1][y] == 0 and rank[x-2][y] == 0 and [x-2, y] in checkline.values():
                go[z] = [x-2, y]
                z += 1
            if y > 1 and x > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0 and [x-1, y-1] in checkline.values():
                attack[z] = [x-1, y-1]
                z += 1
            if y < 8 and x > 1 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0 and [x-1, y+1] in checkline.values():
                attack[z] = [x-1, y+1]
                z += 1
        if not checklines:
            if x > 1 and rank[x-1][y] == 0:
                go[z] = [x-1, y]
                z += 1
            if x == 7 and rank[x-1][y] == 0 and rank[x-2][y] == 0:
                go[z] = [x-2, y]
                z += 1
            if y > 1 and x > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0:
                attack[z] = [x-1, y-1]
                z += 1
            if y < 8 and x > 1 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0:
                attack[z] = [x-1, y+1]
                z += 1
    if  y > 1 and x > 1 and (rank[x-1][y-1] > 6 or rank[x-1][y-1] == 0):
        defence[z] = [x-1, y-1]
        z += 1
    if y < 8 and x > 1 and (rank[x-1][y+1] > 6 or rank[x-1][y+1] == 0):
        defence[z] = [x-1, y+1]
        z += 1
    return go, attack, defence, z

def get_knight_moves_part1(rank, x, y, z=0, checklines=[]):
    go = {}
    # change all that to "if not checklines"
    for checkline in checklines:
        if x < 7 and y < 8 and rank[x+2][y+1] == 0 and [x+2, y+1] in checkline.values():
            go[z] = [x+2, y+1]
            z += 1
        if x < 8 and y < 7 and rank[x+1][y+2] == 0 and [x+1, y+2] in checkline.values():
            go[z] = [x+1, y+2]
            z += 1
        if x > 1 and y < 7 and rank[x-1][y+2] == 0 and [x-1, y+2] in checkline.values():
            go[z] = [x-1, y+2]
            z += 1
        if x > 2 and y < 8 and rank[x-2][y+1] == 0 and [x-2, y+1] in checkline.values():
            go[z] = [x-2, y+1]
            z += 1
        if x > 2 and y > 1 and rank[x-2][y-1] == 0 and [x-2, y-1] in checkline.values():
            go[z] = [x-2, y-1]
            z += 1
        if x > 1 and y > 2 and rank[x-1][y-2] == 0 and [x-1, y-2] in checkline.values():
            go[z] = [x-1, y-2]
            z += 1
        if x < 8 and y > 2 and rank[x+1][y-2] == 0 and [x+1, y-2] in checkline.values():
            go[z] = [x+1, y-2]
            z += 1
        if x < 7 and y > 1 and rank[x+2][y-1] == 0 and [x+2, y-1] in checkline.values():
            go[z] = [x+2, y-1]
            z += 1
    if not checklines:      
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
    return go, z

def get_white_knight_moves(game_id, x, y, blocklines=[], checklines=[], z=0):
    attack = {}
    defence = {}
    rank = get_board(game_id)
    for line in blocklines:
        if [x, y] in line.values():
            go = {}
            return go, attack, defence, z
    # dictionary of possible moves
    go, z = get_knight_moves_part1(rank, x, y, z, checklines=checklines)
    for checkline in checklines:
        if x < 7 and y < 8 and rank[x+2][y+1] > 6 and [x+2, y+1] in checkline.values():
            attack[z] = [x+2, y+1]
            z += 1
        if x < 8 and y < 7 and rank[x+1][y+2] > 6 and [x+1, y+2] in checkline.values():
            attack[z] = [x+1, y+2]
            z += 1
        if x > 1 and y < 7 and rank[x-1][y+2] > 6 and [x-1, y+2] in checkline.values():
            attack[z] = [x-1, y+2]
            z += 1
        if x > 2 and y < 8 and rank[x-2][y+1] > 6 and [x-2, y+1] in checkline.values():
            attack[z] = [x-2, y+1]
            z += 1
        if x > 2 and y > 1 and rank[x-2][y-1] > 6 and [x-2, y-1] in checkline.values():
            attack[z] = [x-2, y-1]
            z += 1
        if x > 1 and y > 2 and rank[x-1][y-2] > 6 and [x-1, y-2] in checkline.values():
            attack[z] = [x-1, y-2]
            z += 1
        if x < 8 and y > 2 and rank[x+1][y-2] > 6 and [x+1, y-2] in checkline.values():
            attack[z] = [x+1, y-2]
            z += 1
        if x < 7 and y > 1 and rank[x+2][y-1] > 6 and [x+2, y-1] in checkline.values():
            attack[z] = [x+2, y-1]
            z += 1
    if not checklines:
        # dictionary of possible attacks
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
    if x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0:
        defence[z] = [x+2, y+1]
        z += 1
    if x < 8 and y < 7 and rank[x+1][y+2] < 7 and rank[x+1][y+2] > 0:
        defence[z] = [x+1, y+2]
        z += 1
    if x > 1 and y < 7 and rank[x-1][y+2] < 7 and rank[x-1][y+2] > 0:
        defence[z] = [x-1, y+2]
        z += 1
    if x > 2 and y < 8 and rank[x-2][y+1] < 7 and rank[x-2][y+1] > 0:
        defence[z] = [x-2, y+1]
        z += 1
    if x > 2 and y > 1 and rank[x-2][y-1] < 7 and rank[x-2][y-1] > 0:
        defence[z] = [x-2, y-1]
        z += 1
    if x > 1 and y > 2 and rank[x-1][y-2] and rank[x-1][y-2] > 0:
        defence[z] = [x-1, y-2]
        z += 1
    if x < 8 and y > 2 and rank[x+1][y-2] < 7 and rank[x+1][y-2] > 0:
        defence[z] = [x+1, y-2]
        z += 1
    if x < 7 and y > 1 and rank[x+2][y-1] < 7 and rank[x+2][y-1] > 0:
        defence[z] = [x+2, y-1]
        z += 1
    return go, attack, defence, z

def get_black_knight_moves(game_id, x, y, blocklines=[], checklines=[], z=0):
    attack = {}
    defence = {}
    rank = get_board(game_id)
    for line in blocklines:
        if [x, y] in line.values():
            go = {}
            return go, attack, defence, z
    # dictionary of possible moves
    go, z = get_knight_moves_part1(rank, x, y, z, checklines=checklines)
    for checkline in checklines:
        if x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0 and [x+2, y+1] in checkline.values():
            attack[z] = [x+2, y+1]
            z += 1
        if x < 8 and y < 7 and rank[x+1][y+2] < 7 and rank[x+1][y+2] > 0 and [x+1, y+2] in checkline.values():
            attack[z] = [x+1, y+2]
            z += 1
        if x > 1 and y < 7 and rank[x-1][y+2] < 7 and rank[x-1][y+2] > 0 and [x-1, y+2] in checkline.values():
            attack[z] = [x-1, y+2]
            z += 1
        if x > 2 and y < 8 and rank[x-2][y+1] < 7 and rank[x-2][y+1] > 0 and [x-2, y+1] in checkline.values():
            attack[z] = [x-2, y+1]
            z += 1
        if x > 2 and y > 1 and rank[x-2][y-1] < 7 and rank[x-2][y-1] > 0 and [x-2, y-1] in checkline.values():
            attack[z] = [x-2, y-1]
            z += 1
        if x > 1 and y > 2 and rank[x-1][y-2] < 7 and rank[x-1][y-2] > 0 and [x-1, y-2] in checkline.values():
            attack[z] = [x-1, y-2]
            z += 1
        if x < 8 and y > 2 and rank[x+1][y-2] < 7 and rank[x+1][y-2] > 0 and [x+1, y-2] in checkline.values():
            attack[z] = [x+1, y-2]
            z += 1
        if x < 7 and y > 1 and rank[x+2][y-1] < 7 and rank[x+2][y-1] > 0 and [x+2, y-1] in checkline.values():
            attack[z] = [x+2, y-1]
            z += 1     
    if not checklines:   
        # dictionary of possible attacks
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
    if x < 7 and y < 8 and rank[x+2][y+1] > 6:
        defence[z] = [x+2, y+1]
        z += 1
    if x < 8 and y < 7 and rank[x+1][y+2] > 6:
        defence[z] = [x+1, y+2]
        z += 1
    if x > 1 and y < 7 and rank[x-1][y+2] > 6:
        defence[z] = [x-1, y+2]
        z += 1
    if x > 2 and y < 8 and rank[x-2][y+1] > 6:
        defence[z] = [x-2, y+1]
        z += 1
    if x > 2 and y > 1 and rank[x-2][y-1] > 6:
        defence[z] = [x-2, y-1]
        z += 1
    if x > 1 and y > 2 and rank[x-1][y-2] > 6:
        defence[z] = [x-1, y-2]
        z += 1
    if x < 8 and y > 2 and rank[x+1][y-2] > 6:
        defence[z] = [x+1, y-2]
        z += 1
    if x < 7 and y > 1 and rank[x+2][y-1] > 6:
        defence[z] = [x+2, y-1]
        z += 1
    return go, attack, defence, z

def get_bishop_moves(game_id, x, y, blocklines=[], checklines=[], step=1, z=0):
    go = {}
    attack = {}
    defence = {}
    rank = get_board(game_id)
    #Checking if the piece is on the blockline. If it is it can only move down the blockline
    side_a = side_b = side_c = side_d = True
    block = False
    for line in blocklines:
        if [x, y] in line.values():
            block = True
            side_a = side_b = side_c = side_d = False
            if x < 8 and y < 8 and [x+1, y+1] in line.values():
                side_a = True
            if x < 8 and y > 1 and [x+1, y-1] in line.values():
                side_b = True
            if x > 1 and y > 1 and [x-1, y-1] in line.values():
                side_c = True
            if x > 1 and y < 8 and [x-1, y+1] in line.values():
                side_d = True         
    # we don't need a separate counter for attacks cause we don't really use keys anywhere
    #here we are going to add that extra if
    # if ([x, y] in blocklines and x+1 y+1 in blocklines) or [x, y] not in blocklines:
    if not block:
        go, attack, z = get_bishops_moves_with_checklines(rank, z, x, y, checklines=checklines)
    if not checklines:
        if x < 8 and y < 8 and side_a:
            if x > y:
                squares_num = 9 - x
            else:
                squares_num = 9 - y
            for i in range (1, squares_num, step):
                if rank[x+i][y+i] == 0:
                    go[z] = [x+i, y+i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x+i][y+i] == 12) or (rank[x][y] > 6 and rank[x+i][y+i] == 6):
                    attack[z] = [x+i, y+i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x+i][y+i] > 6 and rank[x+i][y+i] < 12) or \
                (rank[x][y] > 6  and rank[x+i][y+i] < 6):
                    attack[z] = [x+i, y+i]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x+i][y+i] < 7) or (rank[x][y] > 6  and rank[x+i][y+i] > 6):
                    defence[z] = [x+i, y+i]
                    z += 1
                    break
        if x < 8 and y > 1 and side_b:
            if x > (9 - y) :
                squares_num = 9 - x
            else:
                squares_num = y
            for i in range (1, squares_num, step):
                if rank[x+i][y-i] == 0:
                    go[z] = [x+i, y-i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x+i][y-i] == 12) or (rank[x][y] > 6 and rank[x+i][y-i] == 6):
                    attack[z] = [x+i, y-i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x+i][y-i] > 6 and rank[x+i][y-i] < 12) or \
                (rank[x][y] > 6 and rank[x+i][y-i] < 6):
                    attack[z] = [x+i, y-i]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x+i][y-i] < 7) or (rank[x][y] > 6 and rank[x+i][y-i] > 6):
                    defence[z] = [x+i, y-i]
                    z += 1
                    break
        if x > 1 and y > 1 and side_c:
            if x < y:
                squares_num = x
            else:
                squares_num = y
            for i in range (1, squares_num, step):
                if rank[x-i][y-i] == 0:
                    go[z] = [x-i, y-i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x-i][y-i] == 12) or (rank[x][y] > 6 and rank[x-i][y-i] == 6):
                    attack[z] = [x-i, y-i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x-i][y-i] > 6 and rank[x-i][y-i] < 12) or \
                    (rank[x][y] > 6 and rank[x-i][y-i] < 6):
                    attack[z] = [x-i, y-i]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x-i][y-i] < 7) or (rank[x][y] > 6 and rank[x-i][y-i] > 6):
                    defence[z] = [x-i, y-i]
                    z += 1
                    break
        if x > 1 and y < 8 and side_d:
            if (9 - x) > y:
                squares_num = x
            else:
                squares_num = 9 - y
            for i in range (1, squares_num, step):
                if rank[x-i][y+i] == 0:
                    go[z] = [x-i, y+i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x-i][y+i] == 12) or (rank[x][y] > 6 and rank[x-i][y+i] == 6):
                    attack[z] = [x-i, y+i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x-i][y+i] > 6 and rank[x-i][y+i] < 12) or \
                    (rank[x][y] > 6 and rank[x-i][y+i] < 6):
                    attack[z] = [x-i, y+i]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x-i][y+i] < 7) or (rank[x][y] > 6 and rank[x-i][y+i] > 6):
                    defence[z] = [x-i, y+i]
                    z += 1
                    break
    return go, attack, defence, z

def get_bishops_moves_with_checklines(rank, z, x, y, checklines=[]):
    go = {}
    attack = {}
    for checkline in checklines:
        checksquare = list(checkline.values())
        for count in range (len(checkline.values())):
            # Here check if each one of them is on bishops path, so we set variables inside the loop.
            side_a = side_b = side_c = side_d = False
            square_num = abs(x - checksquare[count][0])
            if checksquare[count][0] - x == checksquare[count][1] - y:
                if x < checksquare[count][0]:
                    side_a = True
                    for i in range(1, square_num):
                        if x < 8 and y < 8 and rank[x+i][y+i] != 0:
                            side_a = False
                else:
                    side_c = True
                    for i in range(1, square_num):
                        if x > 1 and y > 1 and rank[x-i][y-i] != 0:
                            side_c = False
            elif checksquare[count][0] + checksquare[count][1] == x + y:
                if x < checksquare[count][0]:
                    side_b = True
                    for i in range(1, square_num):
                        if x < 8 and y < 8 and rank[x+i][y-i] != 0:
                            side_b = False
                else:
                    side_d = True
                    for i in range(1, square_num):
                        if x > 1 and y > 1 and rank[x-i][y+i] != 0:
                            side_d = False
            if side_a or side_b or side_c or side_d:
                if rank[checksquare[count][0]][checksquare[count][1]] == 0:
                    go[z] = [checksquare[count][0], checksquare[count][1]]
                    z += 1
                else:
                    attack[z] = [checksquare[count][0], checksquare[count][1]]
                    z += 1
    return go, attack, z

def get_rook_moves(game_id, x, y, blocklines=[], checklines=[], step=1, z=0):
    go = {}
    attack = {}
    defence = {}
    rank = get_board(game_id)
    block = False
    side_a = side_b = side_c = side_d = 1
    for line in blocklines:
        if [x, y] in line.values():
            block = True
            side_a = side_b = side_c = side_d = 0
            if y < 8 and [x, y+1] in line.values():
                side_a = 1
            if x < 8 and [x+1, y] in line.values():
                side_b = 1
            if y > 1 and [x, y-1] in line.values():
                side_c = 1
            if x > 1 and [x-1, y] in line.values():
                side_d = 1 
    # we use 20 here, so that we can merge dicts later (indexes need to be different)
    if not block:
        go, attack, z = get_rooks_moves_with_checklines(rank, z, x, y, checklines=checklines)
    if not checklines:
        if y < 8 and side_a:
            squares_num = 9 - y
            for i in range (1, squares_num, step):
                if rank[x][y+i] == 0:
                    go[z] = [x, y+i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x][y+i] == 12) or (rank[x][y] > 6 and rank[x][y+i] == 6):
                    attack[z] = [x, y+i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x][y+i] > 6 and rank[x][y+i] < 12) or \
                (rank[x][y] > 6 and rank[x][y+i] < 6):
                    attack[z] = [x, y+i]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x][y+i] < 7) or (rank[x][y] > 6 and rank[x][y+i] > 6):
                    defence[z] = [x, y+i]
                    z += 1
                    break
        if x < 8 and side_b:
            squares_num = 9 - x
            for i in range (1, squares_num, step):
                if rank[x+i][y] == 0:
                    go[z] = [x+i, y]
                    z += 1
                elif (rank[x][y] < 7 and rank[x+i][y] == 12) or (rank[x][y] > 6 and rank[x+i][y] == 6):
                    attack[z] = [x+i, y]
                    z += 1
                elif (rank[x][y] < 7 and rank[x+i][y] > 6 and rank[x+i][y] < 12) or \
                    (rank[x][y] > 6 and rank[x+i][y] < 6):
                    attack[z] = [x+i, y]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x+i][y] < 7) or (rank[x][y] > 6 and rank[x+i][y] > 6):
                    defence[z] = [x+i, y]
                    z += 1
                    break
        if y > 1 and side_c:
            squares_num = y
            for i in range (1, squares_num, step):
                if rank[x][y-i] == 0:
                    go[z] = [x, y-i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x][y-i] == 12) or (rank[x][y] > 6 and rank[x][y-i] == 6):
                    attack[z] = [x, y-i]
                    z += 1
                elif (rank[x][y] < 7 and rank[x][y-i] > 6 and rank[x][y-i] < 12) or \
                    (rank[x][y] > 6 and rank[x][y-i] < 6):
                    attack[z] = [x, y-i]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x][y-i] < 7) or (rank[x][y] > 6 and rank[x][y-i] > 6):
                    defence[z] = [x, y-i]
                    z += 1
                    break
        if x > 1 and side_d:
            squares_num = x
            for i in range (1, squares_num, step):
                if rank[x-i][y] == 0:
                    go[z] = [x-i, y]
                    z += 1
                elif (rank[x][y] < 7 and rank[x-i][y] == 12) or (rank[x][y] > 6 and rank[x-i][y] == 6):
                    attack[z] = [x-i, y]
                    z += 1
                elif (rank[x][y] < 7 and rank[x-i][y] > 6 and rank[x-i][y] < 12) or \
                    (rank[x][y] > 6 and rank[x-i][y] < 6):
                    attack[z] = [x-i, y]
                    z += 1
                    break
                elif (rank[x][y] < 7 and rank[x-i][y] < 7) or (rank[x][y] > 6 and rank[x-i][y] > 6):
                    defence[z] = [x-i, y]
                    z += 1
                    break
    return go, attack, defence, z

def get_rooks_moves_with_checklines(rank, z, x, y, checklines=[]):
    go = {}
    attack = {}
    for checkline in checklines:
        checksquare = list(checkline.values())
        for count in range (len(checkline.values())):
            side_a = side_b = side_c = side_d = False
            if checksquare[count][0] == x:
                square_num = abs(y - checksquare[count][1])
                if y < checksquare[count][1]:
                    side_a = True
                    for i in range(1, square_num):
                        if y < 8 and rank[x][y+i] != 0:
                            side_a = False
                else:
                    side_c = True
                    for i in range(1, square_num):
                        if y > 1 and rank[x][y-i] != 0:
                            side_c = False
            elif checksquare[count][1] == y:
                square_num = abs(x - checksquare[count][0])
                if x < checksquare[count][0]:
                    side_b = True
                    for i in range(1, square_num):
                        if x < 8 and rank[x+i][y] != 0:
                            side_b = False
                else:
                    side_d = True
                    for i in range(1, square_num):
                        if x > 1 and rank[x-i][y] != 0:
                            side_d = False
            if side_a or side_b or side_c or side_d:
                if rank[checksquare[count][0]][checksquare[count][1]] == 0:
                    go[z] = [checksquare[count][0], checksquare[count][1]]
                    z += 1
                else:
                    attack[z] = [checksquare[count][0], checksquare[count][1]]
                    z += 1
    return go, attack, z

def get_queen_moves(game_id, x, y, blocklines=[], checklines=[], z=0):
    go, attack, defence, z = get_bishop_moves(game_id, x, y, blocklines=blocklines, checklines=checklines,
                                              step=1, z=z)
    go_2, attack_2, defence_2, z = get_rook_moves(game_id, x, y, blocklines=blocklines, checklines=checklines, 
                                                  step=1, z=z)
    go.update(go_2)
    attack.update(attack_2)
    defence.update(defence_2)
    return go, attack, defence, z

def get_king_moves(game_id, x, y, z=0):
    #pass 10 so it's used as a step in the for loops, so that it can move only one square
    go, attack, defence, z = get_bishop_moves(game_id, x, y, step=10, z=z)
    go_2, attack_2, defence_2, z = get_rook_moves(game_id, x, y, step=10, z=z)
    go.update(go_2)
    attack.update(attack_2)
    defence.update(defence_2)
    return go, attack, defence, z

def calculate_attacks(game_id, opp=False, king_coordinates=[0, 0]):
    all_attacks = {}
    attack_king_coord = {}
    attack_king_pieces = []
    rank = get_board(game_id)
    z = 0
    king_idx = 0
    for x in range (1, 9):
        for y in range (1, 9):
            if (session['pieces'] == 0 and not opp) or (session['pieces'] == 1 and opp):
                if rank[x][y] == 1:
                    _, attack, _, z  = get_white_pawn_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 2:
                    _, attack, _, z = get_white_knight_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 3:
                    _, attack, _, z = get_bishop_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 4:
                    _, attack, _, z = get_rook_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 5:
                    _, attack, _, z = get_queen_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 6:
                    _, attack, _, z = get_king_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
            else:
                if rank[x][y] == 7:
                    _, attack, _, z = get_black_pawn_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 8:
                    _, attack, _, z = get_black_knight_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 9:
                    _, attack, _, z = get_bishop_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 10:
                    _, attack, _, z = get_rook_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 11:
                    _, attack, _, z = get_queen_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 12:
                    _, attack, _, z = get_king_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_pieces.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
    return all_attacks, attack_king_coord, attack_king_pieces

def calculate_possible_checks(game_id, opp=False):
    into_check = {}
    rank = get_board(game_id)
    z = 0
    for x in range (1, 9):
        for y in range (1, 9):
            if (session['pieces'] == 0 and not opp) or (session['pieces'] == 1 and opp):
                if rank[x][y] == 1:
                    _, _, defence, z  = get_white_pawn_moves(game_id, x, y, z=z)
                    into_check.update(defence)
                if rank[x][y] == 2:
                    go, _, defence, z = get_white_knight_moves(game_id, x, y, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 3:
                    go, _, defence, z = get_bishop_moves(game_id, x, y, step=1, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 4:
                    go, _, defence, z = get_rook_moves(game_id, x, y, step=1, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 5:
                    go, _, defence, z = get_queen_moves(game_id, x, y, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 6:
                    go, _, defence, z = get_king_moves(game_id, x, y, z=z)
                    into_check.update(go)
                    into_check.update(defence)
            else:
                if rank[x][y] == 7:
                    _, _, defence, z = get_black_pawn_moves(game_id, x, y, z=z)
                    into_check.update(defence)
                if rank[x][y] == 8:
                    go, _, defence, z = get_black_knight_moves(game_id, x, y, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 9:
                    go, _, defence, z = get_bishop_moves(game_id, x, y, step=1, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 10:
                    go, _, defence, z = get_rook_moves(game_id, x, y, step=1, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 11:
                    go, _, defence, z = get_queen_moves(game_id, x, y, z=z)
                    into_check.update(go)
                    into_check.update(defence)
                if rank[x][y] == 12:
                    go, _, defence, z = get_king_moves(game_id, x, y, z=z)
                    into_check.update(go)
                    into_check.update(defence)
    return into_check

def add_attacks_to_db(game_id, all_attacks):
    files = string.ascii_lowercase[0:8] 
    for i in range(1, 9):
        attacks = Attacks.query.filter_by(game_id=game_id, number=i).first()
        for j in range(1, 9):
            if [i, j] in all_attacks.values():
                setattr(attacks, files[j-1], 1)
            else:
                setattr(attacks, files[j-1], 0)
        db.session.commit()

def add_defences_to_db(game_id, into_check):
    files = string.ascii_lowercase[0:8]
    for i in range(1, 9):
        defences = Defences.query.filter_by(game_id=game_id, number=i).first()
        for j in range(1, 9):
            if [i, j] in into_check.values():
                setattr(defences, files[j-1], 1)
            else:
                setattr(defences, files[j-1], 0)
        db.session.commit()

def remove_checks(game_id, moves):
    defences = get_defences(game_id)
    for key, value in list(moves.items()):
            if defences[value[0]][value[1]] == 1:
                del moves[key]
    return moves

def check_if_check(game_id, all_attacks, opp=False):
    rank = get_board(game_id)
    for x in range (1, 9):
        for y in range (1, 9):
            if rank[x][y] == 6 and ((session['pieces'] == 1 and not opp) or (session['pieces'] == 0 and opp)):
                if [x, y] in all_attacks.values():
                    return True
                else:
                    return False
            elif rank[x][y] == 12 and ((session['pieces'] == 0 and not opp) or (session['pieces'] == 1 and opp)):
                if [x, y] in all_attacks.values():
                    return True
                else:
                    return False
    return False

def create_game(game_id):
    rank = {}
    for i in range(1, 9):
        defence_white = Defences(game_id=game_id, number=i)
        db.session.add(defence_white)
        attacks = Attacks(game_id=game_id, number=i)
        db.session.add(attacks)
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

def calculate_checklines(game_id, attack_king_coord, attack_king_pieces, opp=False):
    #Calculate king coordinates of the other player
    king_coord = get_king_coordinates(game_id, opp=not opp)
    i = king_coord[0]
    j = king_coord[1]
    rank = get_board(game_id)
    checklines = []
    for count in range (len(attack_king_coord)):
        x = attack_king_coord[count][0]
        y = attack_king_coord[count][1]
        piece = attack_king_pieces[count]
        if (session['pieces'] == 1 and not opp) or (session['pieces'] == 0 and opp):
            pieces = 1
            if (x - y == i - j) and x - i > 0:
                calculate_block_check_lines_diagonal_1(checklines, rank, x, i, j, pieces, check=True)
            if (x - y == i - j) and i - x > 0:
                calculate_block_check_lines_diagonal_2(checklines, rank, x, y, i, pieces, check=True)
            if (x + y == i + j) and x - i > 0:
                calculate_block_check_lines_diagonal_3(checklines, rank, x, i, j, pieces, check=True)
            if (x + y == i + j) and i - x > 0:
                calculate_block_check_lines_diagonal_4(checklines, rank, x, y, i, pieces, check=True)
            if (x == i) and y - j > 0:
                calculate_block_check_lines_horizontal_1(checklines, rank, y, i, j, pieces, check=True)
            if (x == i) and j - y > 0:
                calculate_block_check_lines_horizontal_2(checklines, rank, x, y, j, pieces, check=True)
            if (y == j) and x - i > 0:
                calculate_block_check_lines_vertical_1(checklines, rank, x, i, j, pieces, check=True)
            if (y == j) and i - x > 0:
                calculate_block_check_lines_vertical_2(checklines, rank, x, y, i, pieces, check=True)
            if piece == 8:
                knight_attack = {}
                knight_attack[count] = [x, y]
                checklines.append(knight_attack)
        elif (session['pieces'] == 0 and not opp) or (session['pieces'] == 1 and opp):
            pieces = 0
            if (x - y == i - j) and x - i > 0:
                calculate_block_check_lines_diagonal_1(checklines, rank, x, i, j, pieces, check=True)
            if (x - y == i - j) and i - x > 0:
                calculate_block_check_lines_diagonal_2(checklines, rank, x, y, i, pieces, check=True)
            if (x + y == i + j) and x - i > 0:
                calculate_block_check_lines_diagonal_3(checklines, rank, x, i, j, pieces, check=True)
            if (x + y == i + j) and i - x > 0:
                calculate_block_check_lines_diagonal_4(checklines, rank, x, y, i, pieces, check=True)
            if (x == i) and y - j > 0:
                calculate_block_check_lines_horizontal_1(checklines, rank, y, i, j, pieces, check=True)
            if (x == i) and j - y > 0:
                calculate_block_check_lines_horizontal_2(checklines, rank, x, y, j, pieces, check=True)
            if (y == j) and x - i > 0:
                calculate_block_check_lines_vertical_1(checklines, rank, x, i, j, pieces, check=True)
            if (y == j) and i - x > 0:
                calculate_block_check_lines_vertical_2(checklines, rank, x, y, i, pieces, check=True)
            if piece == 2:
                knight_attack = {}
                knight_attack[count] = [x, y]
                checklines.append(knight_attack)
    return checklines

def calculate_blocklines(game_id, opp=False):
    #Calculate king coordinates of the other player
    king_coord = get_king_coordinates(game_id, opp=not opp)
    i = king_coord[0]
    j = king_coord[1]
    rank = get_board(game_id)
    blocklines = []
    for x in range (1, 9):
        for y in range (1, 9):
            if (session['pieces'] == 1 and not opp) or (session['pieces'] == 0 and opp):
                pieces = 1
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x - y == i - j) and x - i > 1:
                    calculate_block_check_lines_diagonal_1(blocklines, rank, x, i, j, pieces)
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x - y == i - j) and i - x > 1:
                    calculate_block_check_lines_diagonal_2(blocklines, rank, x, y, i, pieces)
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x + y == i + j) and x - i > 1:
                    calculate_block_check_lines_diagonal_3(blocklines, rank, x, i, j, pieces)
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x + y == i + j) and i - x > 1:
                    calculate_block_check_lines_diagonal_4(blocklines, rank, x, y, i, pieces)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (x == i) and y - j > 1:
                    calculate_block_check_lines_horizontal_1(blocklines, rank, y, i, j, pieces)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (x == i) and j - y > 1:
                    calculate_block_check_lines_horizontal_2(blocklines, rank, x, y, j, pieces)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (y == j) and x - i > 1:
                    calculate_block_check_lines_vertical_1(blocklines, rank, x, i, j, pieces)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (y == j) and i - x > 1:
                    calculate_block_check_lines_vertical_2(blocklines, rank, x, y, i, pieces)
            elif (session['pieces'] == 0 and not opp) or (session['pieces'] == 1 and opp):
                pieces = 0
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x - y == i - j) and x - i > 1:
                    calculate_block_check_lines_diagonal_1(blocklines, rank, x, i, j, pieces)
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x - y == i - j) and i - x > 1:
                    calculate_block_check_lines_diagonal_2(blocklines, rank, x, y, i, pieces)
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x + y == i + j) and x - i > 1:
                    calculate_block_check_lines_diagonal_3(blocklines, rank, x, i, j, pieces)
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x + y == i + j) and i - x > 1:
                    calculate_block_check_lines_diagonal_4(blocklines, rank, x, y, i, pieces)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (x == i) and y - j > 1:
                    calculate_block_check_lines_horizontal_1(blocklines, rank, y, i, j, pieces)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (x == i) and j - y > 1:
                    calculate_block_check_lines_horizontal_2(blocklines, rank, x, y, j, pieces)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (y == j) and x - i > 1:
                    calculate_block_check_lines_vertical_1(blocklines, rank, x, i, j, pieces)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (y == j) and i - x > 1:
                    calculate_block_check_lines_vertical_2(blocklines, rank, x, y, i, pieces)                  
    return blocklines

def calculate_block_check_lines_diagonal_1(lines, rank, x, i, j, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    #For lines that start with a king we add one extra field to include attacking piece
    #and start the count from 1 to exclude the king.
    for count in range(1, x - i + 1):
        line[count-1] = [i+count, j+count]
        if rank[i+count][j+count]:
            all_count += 1
        if (pieces == 1 and rank[i+count][j+count] and rank[i+count][j+count] < 7) or \
           (pieces == 0 and rank[i+count][j+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_diagonal_2(lines, rank, x, y, i, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    #For lines that start with an attacker, we start the count from 0 to include the attacker
    for count in range(i - x):
        line[count] = [x+count, y+count]
        if rank[x+count][y+count]:
            all_count += 1
        if (pieces == 1 and rank[x+count][y+count] and rank[x+count][y+count] < 7) or \
           (pieces == 0 and rank[x+count][y+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_diagonal_3(lines, rank, x, i, j, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(1, x - i + 1):
        line[count-1] = [i+count, j-count]
        if rank[i+count][j-count]:
            all_count += 1
        if (pieces == 1 and rank[i+count][j-count] and rank[i+count][j-count] < 7) or \
           (pieces == 0 and rank[i+count][j-count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_diagonal_4(lines, rank, x, y, i, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(i - x):
        line[count] = [x+count, y-count]
        if rank[x+count][y-count]:
            all_count += 1
        if (pieces == 1 and rank[x+count][y-count] and rank[x+count][y-count] < 7) or \
           (pieces == 0 and rank[x+count][y-count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_horizontal_1(lines, rank, y, i, j, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(1, y - j + 1):
        line[count-1] = [i, j+count]
        if rank[i][j+count]:
            all_count += 1
        if (pieces == 1 and rank[i][j+count] and rank[i][j+count] < 7) or \
           (pieces == 0 and rank[i][j+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_horizontal_2(lines, rank, x, y, j, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(j - y):
        line[count] = [x, y+count]
        if rank[x][y+count]:
            all_count += 1
        if (pieces == 1 and rank[x][y+count] and rank[x][y+count] < 7) or \
           (pieces == 0 and rank[x][y+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_vertical_1(lines, rank, x, i, j, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(1, x - i + 1):
        line[count-1] = [i+count, j]
        if rank[i+count][j]:
            all_count += 1
        if (pieces == 1 and rank[i+count][j] and rank[i+count][j] < 7) or \
           (pieces == 0 and rank[i+count][j] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_vertical_2(lines, rank, x, y, i, pieces, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(i - x):
        line[count] = [x+count, y]
        if rank[x+count][y]:
            all_count += 1
        if (pieces == 1 and rank[x+count][y] and rank[x+count][y] < 7) or \
           (pieces == 0 and rank[x+count][y] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def check_can_move(game_id, game, blocklines=[], checklines = [], pieces=None):
    rank = get_board(game_id)
    moveable = {}
    z = 0
    for x in range (1, 9):
        for y in range (1, 9):
            if pieces == 0:
                if len(checklines) < 2:
                    if rank[x][y] == 1:
                        add_moveable, z = check_white_pawn_can_move(rank, game, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 2:
                        add_moveable, z = check_white_knight_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 3:
                        add_moveable, z = check_white_bishop_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 4:
                        add_moveable, z = check_white_rook_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 5:
                        add_moveable, z = check_white_queen_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                if rank[x][y] == 6:
                    add_moveable, z = check_white_king_can_move(game_id, rank, z, x, y)
                    moveable.update(add_moveable)
            else:
                if len(checklines) < 2:
                    if rank[x][y] == 7:
                        add_moveable, z = check_black_pawn_can_move(rank, game, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 8:
                        add_moveable, z = check_black_knight_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 9:
                        add_moveable, z = check_black_bishop_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 10:
                        add_moveable, z = check_black_rook_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                    if rank[x][y] == 11:
                        add_moveable, z = check_black_queen_can_move(rank, z, x, y, blocklines, checklines)
                        moveable.update(add_moveable)
                if rank[x][y] == 12:
                    add_moveable, z = check_black_king_can_move(game_id, rank, z, x, y)
                    moveable.update(add_moveable)
    return moveable
                
def check_white_pawn_can_move(rank, game, z, x, y, blocklines, checklines):
    moveable = {}
    #This check is for when that piece is on the blockline
    for line in blocklines:
        # This is when there's both a checkline and a blockline
        if [x, y] in line.values() and checklines:
             return moveable, z
        # Next two cases for when there's only a blockline
        # len(line.values()) == 2) can be removed
        if x < 8 and [x, y] in line.values():
            if ((rank[x+1][y] == 0 and [x+1, y] in line.values()) or
            (y < 8 and rank[x+1][y+1] > 6 and [x+1, y+1] in line.values()) or 
            (y > 1 and rank[x+1][y-1] > 6 and [x+1, y-1] in line.values()) or
            (game.white_en_passant and (y < 8 and rank[x+1][y+1] == 0 and [x+1, y+1] in line.values() and game.white_en_passant_y == y + 1 or
            y > 1 and rank[x+1][y-1] == 0 and [x+1, y-1] in line.values() and game.white_en_passant_y == y - 1))):
                moveable[z]=[x, y]
                z += 1
                return moveable, z
            else:
                return moveable, z
    # This is when there's only a checkline
    for checkline in checklines:
        # Check if any possible moves or attacks (including en passant) can remove the check.
        if x < 8 and (rank[x+1][y] == 0 and [x+1, y] in checkline.values() or 
        (x == 2 and rank[x+1][y] == 0 and rank[x+2][y] == 0 and [x+2, y] in checkline.values()) or
        (y < 8 and rank[x+1][y+1] > 6 and [x+1, y+1] in checkline.values()) or
        (y > 1 and rank[x+1][y-1] > 6 and [x+1, y-1] in checkline.values()) or 
        (game.white_en_passant and  
        (y > 1 and rank[x][y-1] == 7 and [x, y-1] in checkline.values() and game.white_en_passant_y == y - 1 or 
        y < 8 and rank[x][y+1] == 7 and [x, y+1] in checkline.values() and game.white_en_passant_y == y + 1))):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z
    # This check is for when the piece is niether on a blockline nor on a checkline.
    if x < 8 and (rank[x+1][y] == 0 or (y < 8 and rank[x+1][y+1] > 6) or (y > 1 and rank[x+1][y-1] > 6) or 
    (game.white_en_passant and (y < 8 and rank[x+1][y+1] == 0 and game.white_en_passant_y == y + 1 or 
    y > 1 and rank[x+1][y-1] == 0 and game.white_en_passant_y == y - 1))):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_pawn_can_move(rank, game, z, x, y, blocklines, checklines):
    moveable = {}
    #This check is for when that piece is on the blockline
    for line in blocklines:
        if [x, y] in line.values() and checklines:
             return moveable, z
        if x > 1 and [x, y] in line.values():
            if ((rank[x-1][y] == 0 and [x-1, y] in line.values()) or 
            (y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0 and [x-1, y+1] in line.values()) or 
            (y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0 and [x-1, y-1] in line.values()) or
            (game.black_en_passant and (y < 8 and rank[x-1][y+1] == 0 and [x-1, y+1] in line.values() and game.black_en_passant_y == y + 1 or
            y > 1 and rank[x-1][y-1] == 0 and [x-1, y-1] in line.values() and game.black_en_passant_y == y - 1))):
                moveable[z]=[x, y]
                z += 1
                return moveable, z
            else:
                return moveable, z
    for checkline in checklines:
        if x > 1 and ((rank[x-1][y] == 0 and [x-1, y] in checkline.values()) or 
        (x == 7 and rank[x-1][y] == 0 and rank[x-2][y] == 0 and [x-2, y] in checkline.values()) or
        (y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0 and [x-1, y+1] in checkline.values()) or
        (y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0) and [x-1, y-1] in checkline.values() or
        (game.black_en_passant and  
        (y > 1 and rank[x][y-1] == 1 and [x, y-1] in checkline.values() and game.black_en_passant_y == y - 1 or 
        y < 8 and rank[x][y+1] == 1 and [x, y+1] in checkline.values() and game.black_en_passant_y == y + 1))):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z
    #This check is for when the piece is not on the blockline and not on the checkline
    if x > 1 and (rank[x-1][y] == 0 or (y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0) 
    or (y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0) or 
    (game.black_en_passant and (y < 8 and rank[x-1][y+1] == 0 and game.black_en_passant_y == y + 1 or 
    y > 1 and rank[x-1][y-1] == 0 and game.black_en_passant_y == y - 1))):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_knight_can_move_part1(rank, x, y, checklines):
    # If there's a checkline, return true or false depending on if any moves lead into checkline
    for checkline in checklines:
        if ((x < 7 and y < 8 and rank[x+2][y+1] == 0 and [x+2, y+1] in checkline.values()) or 
        (x < 8 and y < 7 and rank[x+1][y+2] == 0 and [x+1, y+2] in checkline.values()) or 
        (x > 1 and y < 7 and rank[x-1][y+2] == 0 and [x-1, y+2] in checkline.values()) or 
        (x > 2 and y < 8 and rank[x-2][y+1] == 0 and [x-2, y+1] in checkline.values()) or
        (x > 2 and y > 1 and rank[x-2][y-1] == 0 and [x-2, y-1] in checkline.values()) or 
        (x > 1 and y > 2 and rank[x-1][y-2] == 0 and [x-1, y-2] in checkline.values()) or 
        (x < 8 and y > 2 and rank[x+1][y-2] == 0 and [x+1, y-2] in checkline.values()) or 
        (x < 7 and y > 1 and rank[x+2][y-1] == 0 and [x+2, y-1] in checkline.values())):
            return True
        else:
            return False
    # If there's no checkline, do regular check
    if (x < 7 and y < 8 and rank[x+2][y+1] == 0) or (x < 8 and y < 7 and rank[x+1][y+2] == 0) or \
    (x > 1 and y < 7 and rank[x-1][y+2] == 0) or (x > 2 and y < 8 and rank[x-2][y+1] == 0) or \
    (x > 2 and y > 1 and rank[x-2][y-1] == 0) or (x > 1 and y > 2 and rank[x-1][y-2] == 0) or \
    (x < 8 and y > 2 and rank[x+1][y-2] == 0) or (x < 7 and y > 1 and rank[x+2][y-1] == 0):
        return True
    else:
        return False

def check_white_knight_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    for line in blocklines:
        if [x, y] in line.values():
            return moveable, z
    part_1 = check_knight_can_move_part1(rank, x, y, checklines)
    for checkline in checklines:
            if (part_1 or (x < 7 and y < 8 and rank[x+2][y+1] > 6 and [x+2, y+1] in checkline.values()) or
            (x < 8 and y < 7 and rank[x+1][y+2] > 6 and [x+1, y+2] in checkline.values()) or
            (x > 1 and y < 7 and rank[x-1][y+2] > 6 and [x-1, y+2] in checkline.values()) or
            (x > 2 and y < 8 and rank[x-2][y+1] > 6 and [x-2, y+1] in checkline.values()) or
            (x > 2 and y > 1 and rank[x-2][y-1] > 6 and [x-2, y-1] in checkline.values()) or
            (x > 1 and y > 2 and rank[x-1][y-2] > 6 and [x-1, y-2] in checkline.values()) or
            (x < 8 and y > 2 and rank[x+1][y-2] > 6 and [x+1, y-2] in checkline.values()) or
            (x < 7 and y > 1 and rank[x+2][y-1] > 6 and [x+2, y-1] in checkline.values())):
                moveable[z]=[x, y]
                z += 1
                return moveable, z
            else:
                return moveable, z
    if part_1 or (x < 7 and y < 8 and rank[x+2][y+1] > 6) or \
    (x < 8 and y < 7 and rank[x+1][y+2] > 6) or (x > 1 and y < 7 and rank[x-1][y+2] > 6) or \
    (x > 2 and y < 8 and rank[x-2][y+1] > 6) or (x > 2 and y > 1 and rank[x-2][y-1] > 6) or \
    (x > 1 and y > 2 and rank[x-1][y-2] > 6) or (x < 8 and y > 2 and rank[x+1][y-2] > 6) or \
    (x < 7 and y > 1 and rank[x+2][y-1] > 6):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_knight_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    for line in blocklines:
        if [x, y] in line.values():
            return moveable, z
    part_1 = check_knight_can_move_part1(rank, x, y, checklines)
    for checkline in checklines:
        # Need to finish this
        if (part_1 or 
        (x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0 and [x+2, y+1] in checkline.values()) or
        (x < 8 and y < 7 and rank[x+1][y+2] < 7 and rank[x+1][y+2] > 0 and [x+1, y+2] in checkline.values()) or
        (x > 1 and y < 7 and rank[x-1][y+2] < 7 and rank[x-1][y+2] > 0 and [x-1, y+2] in checkline.values()) or
        (x > 2 and y < 8 and rank[x-2][y+1] < 7 and rank[x-2][y+1] > 0 and [x-2, y+1] in checkline.values()) or
        (x > 2 and y > 1 and rank[x-2][y-1] < 7 and rank[x-2][y-1] > 0 and [x-2, y-1] in checkline.values()) or
        (x > 1 and y > 2 and rank[x-1][y-2] < 7 and rank[x-1][y-2] > 0 and [x-1, y-2] in checkline.values()) or
        (x < 8 and y > 2 and rank[x+1][y-2] < 7 and rank[x+1][y-2] > 0 and [x+1, y-2] in checkline.values()) or
        (x < 7 and y > 1 and rank[x+2][y-1] < 7 and rank[x+2][y-1] > 0 and [x+2, y-1] in checkline.values())):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z
    if part_1 or (x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0) or \
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

def check_white_bishop_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    for line in blocklines:
        if [x, y] in line.values() and checklines:
             return moveable, z
        if ([x, y] in line.values() and (x < 8 and y < 8 and [x+1, y+1] in line.values() and
        (rank[x+1][y+1] == 0 or rank[x+1][y+1] > 6)) or (x < 8 and y > 1 and [x+1, y-1] in line.values() and 
        (rank[x+1][y-1] == 0 or rank[x+1][y-1] > 6)) or (x > 1 and y > 1 and [x-1, y-1] in line.values() and 
        (rank[x-1][y-1] == 0 or rank[x-1][y-1] > 6)) or (x > 1 and y < 8 and [x-1, y+1] in line.values() and
        (rank[x-1][y+1] == 0 or rank[x-1][y+1] > 6))):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        if ([x, y] in line.values() and ([x+1, y+1] not in line.values() and [x+1, y-1] not in line.values()
        and [x-1, y-1] not in line.values() and [x-1, y+1] not in line.values())):
            return moveable, z
    if checklines:
        moveable, z = check_bishops_with_checklines(rank, z, x, y, checklines)
        return moveable, z
    if (x < 8 and y < 8 and (rank[x+1][y+1] == 0 or rank[x+1][y+1] > 6)) or \
    (x < 8 and y > 1 and (rank[x+1][y-1] == 0 or rank[x+1][y-1] > 6)) or \
    (x > 1 and y > 1 and (rank[x-1][y-1] == 0 or rank[x-1][y-1] > 6)) or \
    (x > 1 and y < 8 and (rank[x-1][y+1] == 0 or rank[x-1][y+1] > 6)):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_bishop_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    for line in blocklines:
        if [x, y] in line.values() and checklines:
             return moveable, z
        if ([x, y] in line.values() and (x < 8 and y < 8 and [x+1, y+1] in line.values() and
        rank[x+1][y+1] < 7) or (x < 8 and y > 1 and [x+1, y-1] in line.values() and
        rank[x+1][y-1] < 7) or (x > 1 and y > 1 and [x-1, y-1] in line.values() and 
        rank[x-1][y-1] < 7) or (x > 1 and y < 8 and [x-1, y+1] in line.values() and
        rank[x-1][y+1] < 7)):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        if ([x, y] in line.values() and ([x+1, y+1] not in line.values() and [x+1, y-1] not in line.values()
        and [x-1, y-1] not in line.values() and [x-1, y+1] not in line.values())):
            return moveable, z
    if checklines:
        moveable, z = check_bishops_with_checklines(rank, z, x, y, checklines)
        return moveable, z
    if (x < 8 and y < 8 and rank[x+1][y+1] < 7) or (x < 8 and y > 1 and rank[x+1][y-1] < 7) or \
    (x > 1 and y > 1 and rank[x-1][y-1] < 7) or (x > 1 and y < 8 and rank[x-1][y+1] < 7):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_bishops_with_checklines(rank, z, x, y, checklines):
    moveable = {}
    for checkline in checklines:
        checksquare = list(checkline.values())
        # Here we need to check if at least one will become true, so we set variables before the loop.
        side_a = side_b = side_c = side_d = False
        for count in range (len(checkline.values())):
            square_num = abs(x - checksquare[count][0])
            if checksquare[count][0] - x == checksquare[count][1] - y:
                if x < checksquare[count][0]:
                    side_a = True
                    for i in range(1, square_num):
                        if x < 8 and y < 8 and rank[x+i][y+i] != 0:
                            side_a = False
                else:
                    side_c = True
                    for i in range(1, square_num):
                        if x > 1 and y > 1 and rank[x-i][y-i] != 0:
                            side_c = False
            elif checksquare[count][0] + checksquare[count][1] == x + y:
                if x < checksquare[count][0]:
                    side_b = True
                    for i in range(1, square_num):
                        if x < 8 and y < 8 and rank[x+i][y-i] != 0:
                            side_b = False
                else:
                    side_d = True
                    for i in range(1, square_num):
                        if x > 1 and y > 1 and rank[x-i][y+i] != 0:
                            side_d = False
        if side_a or side_b or side_c or side_d:
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z

def check_white_rook_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    for line in blocklines:
        if [x, y] in line.values() and checklines:
             return moveable, z
        if ([x, y] in line.values() and (y < 8 and [x, y+1] in line.values() and
        (rank[x][y+1] == 0 or rank[x][y+1] > 6)) or (x < 8 and [x+1, y] in line.values() and 
        (rank[x+1][y] == 0 or rank[x+1][y] > 6)) or (y > 1 and [x, y-1] in line.values() and 
        (rank[x][y-1] == 0 or rank[x][y-1] > 6)) or (x > 1 and [x-1, y] in line.values() and
        (rank[x-1][y] == 0 or rank[x-1][y] > 6))):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        if ([x, y] in line.values() and ([x, y+1] not in line.values() and [x+1, y] not in line.values()
        and [x, y-1] not in line.values() and [x-1, y] not in line.values())):
            return moveable, z
    if checklines:
        moveable, z = check_rooks_with_checklines(rank, z, x, y, checklines)
        return moveable, z
    if (y < 8 and (rank[x][y+1] == 0 or rank[x][y+1] > 6)) or \
    (x < 8 and (rank[x+1][y] == 0 or rank[x+1][y] > 6)) or \
    (y > 1 and (rank[x][y-1] == 0 or rank[x][y-1] > 6)) or \
    (x > 1 and (rank[x-1][y] == 0 or rank[x-1][y] > 6)):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_rook_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    for line in blocklines:
        if [x, y] in line.values() and checklines:
             return moveable, z
        if ([x, y] in line.values() and (y < 8 and [x, y+1] in line.values() and rank[x][y+1] < 7) or 
        (x < 8 and [x+1, y] in line.values() and rank[x+1][y] < 7) or 
        (y > 1 and [x, y-1] in line.values() and rank[x][y-1] < 7) or 
        (x > 1 and [x-1, y] in line.values() and rank[x-1][y] < 7)):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        if ([x, y] in line.values() and ([x, y+1] not in line.values() and [x+1, y] not in line.values()
        and [x, y-1] not in line.values() and [x-1, y] not in line.values())):
            return moveable, z
    if checklines:
        moveable, z = check_rooks_with_checklines(rank, z, x, y, checklines)
        return moveable, z
    if (y < 8 and rank[x][y+1] < 7) or (x < 8 and rank[x+1][y] < 7) or \
    (y > 1 and rank[x][y-1] < 7) or (x > 1 and rank[x-1][y] < 7):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_rooks_with_checklines(rank, z, x, y, checklines):
    moveable = {}
    for checkline in checklines:
        checksquare = list(checkline.values())
        side_a = side_b = side_c = side_d = False
        for count in range (len(checkline.values())):
            if checksquare[count][0] == x:
                square_num = abs(y - checksquare[count][1])
                if y < checksquare[count][1]:
                    side_a = True
                    for i in range(1, square_num):
                        if y < 8 and rank[x][y+i] != 0:
                            side_a = False
                else:
                    side_c = True
                    for i in range(1, square_num):
                        if y > 1 and rank[x][y-i] != 0:
                            side_c = False
            elif checksquare[count][1] == y:
                square_num = abs(x - checksquare[count][0])
                if x < checksquare[count][0]:
                    side_b = True
                    for i in range(1, square_num):
                        if x < 8 and rank[x+i][y] != 0:
                            side_b = False
                else:
                    side_d = True
                    for i in range(1, square_num):
                        if x > 1 and rank[x-i][y] != 0:
                            side_d = False
        if side_a or side_b or side_c or side_d:
        # if ((x < 8 and y < 8 and rank[x+1][y+1] == 0 and side_a) or
        # (x < 8 and y > 1 and rank[x+1][y-1] == 0 and side_b) or
        # (x > 1 and y > 1 and rank[x-1][y-1] == 0 and side_c) or
        # (x > 1 and y < 8 and rank[x-1][y+1] == 0 and side_d)):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z

def check_white_queen_can_move(rank, z, x, y, blocklines, checklines):
    moveable, z = check_white_bishop_can_move(rank, z, x, y, blocklines, checklines)
    moveable_2, z = check_white_rook_can_move(rank, z, x, y, blocklines, checklines)
    moveable.update(moveable_2)
    return moveable, z

def check_white_king_can_move(game_id, rank, z, x, y):   
    moveable = {}
    defences = get_defences(game_id)
    if (x < 8 and y < 8 and not defences[x+1][y+1] and (rank[x+1][y+1] == 0 or rank[x+1][y+1] > 6)) or \
    (x < 8 and y > 1 and not defences[x+1][y-1] and (rank[x+1][y-1] == 0 or rank[x+1][y-1] > 6)) or \
    (x > 1 and y > 1 and not defences[x-1][y-1] and (rank[x-1][y-1] == 0 or rank[x-1][y-1] > 6)) or \
    (x > 1 and y < 8 and not defences[x-1][y+1] and (rank[x-1][y+1] == 0 or rank[x-1][y+1] > 6)) or \
    (y < 8 and not defences[x][y+1] and (rank[x][y+1] == 0 or rank[x][y+1] > 6)) or \
    (x < 8 and not defences[x+1][y] and (rank[x+1][y] == 0 or rank[x+1][y] > 6)) or \
    (y > 1 and not defences[x][y-1] and (rank[x][y-1] == 0 or rank[x][y-1] > 6)) or \
    (x > 1 and not defences[x-1][y] and (rank[x-1][y] == 0 or rank[x-1][y] > 6)):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_queen_can_move(rank, z, x, y, blocklines, checklines):
    moveable, z = check_black_bishop_can_move(rank, z, x, y, blocklines, checklines)
    moveable_2, z = check_black_rook_can_move(rank, z, x, y, blocklines, checklines)
    moveable.update(moveable_2)
    return moveable, z

def check_black_king_can_move(game_id, rank, z, x, y):
    moveable = {}
    defences = get_defences(game_id)
    if (x < 8 and y < 8 and not defences[x+1][y+1] and rank[x+1][y+1] < 7) or \
    (x < 8 and y > 1 and not defences[x+1][y-1] and rank[x+1][y-1] < 7) or \
    (x > 1 and y > 1 and not defences[x-1][y-1] and rank[x-1][y-1] < 7) or \
    (x > 1 and y < 8 and not defences[x-1][y+1] and rank[x-1][y+1] < 7) or\
    (y < 8 and not defences[x][y+1] and rank[x][y+1] < 7) or (x < 8 and not defences[x+1][y] and rank[x+1][y] < 7) or \
    (y > 1 and not defences[x][y-1] and rank[x][y-1] < 7) or (x > 1 and not defences[x-1][y] and rank[x-1][y] < 7):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def disable_castling_white(i, j, game):
    # Add values to the DB and refresh session values.
    if (i == 1 and j == 1 and game.white_queen_castling):
        game.white_queen_castling = False
    elif (i == 1 and j == 5 and (game.white_queen_castling or game.white_king_castling)):
        game.white_queen_castling = False
        game.white_king_castling = False
    elif (i == 1 and j == 8 and game.white_king_castling):
        game.white_king_castling = False

def disable_castling_black(i, j, game):
    if (i == 8 and j == 1 and game.black_queen_castling):
        game.black_queen_castling = False
    elif (i == 8 and j == 5 and (game.black_queen_castling or game.black_king_castling)):
        game.black_queen_castling = False
        game.black_king_castling = False
    elif (i == 8 and j == 8 and game.black_king_castling):
        game.black_king_castling = False

def add_white_king_castling(game_id, moves, z):
    defences = get_defences(game_id)
    rank = get_board(game_id)
    attacks = get_attacks(game_id)
    white_king_castling = 1
    if attacks[1][5] == 1:
        white_king_castling = 0
    elif rank[1][6] != 0 or rank[1][7] != 0:
        white_king_castling = 0
    elif defences[1][6] == 1 or defences[1][7] == 1:
        white_king_castling = 0
    if white_king_castling:
        moves[z] = [1, 8]
        moves[z+1] = [1, 7]
        z += 2
    return moves, z

def add_white_queen_castling(game_id, moves, z):
    defences = get_defences(game_id)
    rank = get_board(game_id)
    attacks = get_attacks(game_id)
    white_queen_castling = 1
    if attacks[1][5] == 1:
        white_queen_castling = 0
    elif rank[1][2] != 0 or rank[1][3] != 0 or rank[1][4] != 0:
        white_queen_castling = 0
    elif defences[1][3] == 1 or defences[1][4] == 1:
        white_queen_castling = 0
    if white_queen_castling:
        moves[z] = [1, 1]
        moves[z+1] = [1, 3]
        z += 2
    return moves, z

def add_black_king_castling(game_id, moves, z):
    defences = get_defences(game_id)
    rank = get_board(game_id)
    attacks = get_attacks(game_id)
    black_king_castling = 1
    if attacks[8][5] == 1:
        black_king_castling = 0
    elif rank[8][6] != 0 or rank[8][7] != 0:
        black_king_castling = 0
    elif defences[8][6] == 1 or defences[8][7] == 1:
        black_king_castling = 0
    if black_king_castling:
        moves[z] = [8, 8]
        moves[z+1] = [8, 7]
        z += 2
    return moves, z

def add_black_queen_castling(game_id, moves, z):
    defences = get_defences(game_id)
    rank = get_board(game_id)
    attacks = get_attacks(game_id)
    black_queen_castling = 1
    if attacks[8][5] == 1:
        black_queen_castling = 0
    elif rank[8][2] != 0 or rank[8][3] != 0 or rank[8][4] != 0:
        black_queen_castling = 0
    elif defences[8][3] == 1 or defences[8][4] == 1:
        black_queen_castling = 0
    if black_queen_castling:
        moves[z] = [8, 1]
        moves[z+1] = [8, 3]
        z += 2
    return moves, z

def switch_en_passant(piece, i, x, y, game, game_id):
    rank = get_rank(game_id, x)
    if piece == 1 and x - i == 2 and ((y > 1 and rank[y-1] == 7) or (y < 8 and rank[y+1] == 7)):
        game.black_en_passant = True
        game.black_en_passant_y = y
    else:
        game.black_en_passant = False
    if piece == 7 and i - x == 2 and ((y > 1 and rank[y-1] == 1) or (y < 8 and rank[y+1] == 1)):
        game.white_en_passant = True
        game.white_en_passant_y = y
    else:
        game.white_en_passant = False
    
def add_white_en_passant(moves, z, game):    
    moves[z] = [6, game.white_en_passant_y]
    z += 1
    return moves, z

def add_black_en_passant(moves, z, game):
    moves[z] = [3, game.black_en_passant_y]
    z += 1
    return moves, z