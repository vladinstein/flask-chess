import string
from chess.models import Rank, Defences, Attacks
from chess import db
from chess.routes import session

def get_moves(game_id, x, y, figure, blocklines):
    if figure == 1:
        go, attack, _, _ = get_white_pawn_moves(game_id, x, y, blocklines=blocklines)
    elif figure == 2:
        go, attack, _, _ = get_white_knight_moves(game_id, x, y, blocklines=blocklines)
    elif figure == 3 or figure == 9:
        go, attack, _, _ = get_bishop_moves(game_id, x, y, blocklines=blocklines)
    elif figure == 4 or figure == 10:
        go, attack, _, _ = get_rook_moves(game_id, x, y, blocklines=blocklines)
    elif figure == 5 or figure == 11:
        go, attack, _, _ = get_queen_moves(game_id, x, y, blocklines=blocklines)
    elif figure == 6 or figure == 12:
        go, attack, _, _ = get_king_moves(game_id, x, y)
        go = remove_checks(game_id, go)
        attack = remove_checks(game_id, attack)
    elif figure == 7:
        go, attack, _, _ = get_black_pawn_moves(game_id, x, y, blocklines=blocklines)
    elif figure == 8:
        go, attack, _, _ = get_black_knight_moves(game_id, x, y, blocklines=blocklines)
    return go, attack

def get_board(game_id):
    rank = {}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, 
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
            if (((session['figures'] == 1 and rank[x][y] == 6) or (session['figures'] == 0 and rank[x][y] == 12)) and opp) or \
               (((session['figures'] == 1 and rank[x][y] == 12) or (session['figures'] == 0 and rank[x][y] == 6)) and not opp):
                return [x, y]

def get_white_pawn_moves(game_id, x, y, blocklines=[], z=0):
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
            if y > 1 and rank[x+1][y-1] > 6 and [x+1, y-1] in line.values() and len(line.values()) == 2:
                attack[z] = [x+1, y-1]
                z += 1
            if y < 8 and rank[x+1][y+1] > 6 and [x+1, y+1] in line.values() and len(line.values()) == 2:
                attack[z] = [x+1, y+1]
                z += 1
    if not block:
        if x < 8 and rank[x+1][y] == 0:
            go[z] = [x+1, y]
            z += 1
        if x == 2 and rank[x+1][y] == 0 and rank[x+2][y] == 0:
            go[z] = [x+2, y]
            z += 1
        if y > 1 and rank[x+1][y-1] > 6:
            attack[z] = [x+1, y-1]
            z += 1
        if y < 8 and rank[x+1][y+1] > 6:
            attack[z] = [x+1, y+1]
            z += 1
    if y > 1 and rank[x+1][y-1] < 7:
        defence[z] = [x+1, y-1]
        z += 1
    if y < 8 and rank[x+1][y+1] < 7:
        defence[z] = [x+1, y+1]
        z += 1
    return go, attack, defence, z

def get_black_pawn_moves(game_id, x, y, blocklines=[], z=0):
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
            if y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0 and [x-1, y-1] in line.values() and len(line.values()) == 2:
                attack[z] = [x-1, y-1]
                z += 1
            if y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0 and [x-1, y+1] in line.values() and len(line.values()) == 2:
                attack[z] = [x-1, y+1]
                z += 1
    if not block:
        if x > 1 and rank[x-1][y] == 0:
            go[z] = [x-1, y]
            z += 1
        if x == 7 and rank[x-1][y] == 0 and rank[x-2][y] == 0:
            go[z] = [x-2, y]
            z += 1
        if y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0:
            attack[z] = [x-1, y-1]
            z += 1
        if y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0:
            attack[z] = [x-1, y+1]
            z += 1
    if  y > 1 and (rank[x-1][y-1] > 6 or rank[x-1][y-1] == 0):
        defence[z] = [x-1, y-1]
        z += 1
    if y < 8 and (rank[x-1][y+1] > 6 or rank[x-1][y+1] == 0):
        defence[z] = [x-1, y+1]
        z += 1
    return go, attack, defence, z

def get_knight_moves_part1(rank, x, y, z=0):
    go = {}
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

def get_white_knight_moves(game_id, x, y, blocklines=[], z=0):
    attack = {}
    defence = {}
    rank = get_board(game_id)
    for line in blocklines:
        if [x, y] in line.values():
            go = {}
            return go, attack, defence, z
    # dictionary of possible moves
    go, z = get_knight_moves_part1(rank, x, y, z)
    # dictionary of possible attacks
    if x < 7 and y < 8 and rank[x+2][y+1] > 6:
        attack[z] = [x+2, y+1]
        z += 1
    elif x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0:
        defence[z] = [x+2, y+1]
        z += 1
    if x < 8 and y < 7 and rank[x+1][y+2] > 6:
        attack[z] = [x+1, y+2]
        z += 1
    elif x < 8 and y < 7 and rank[x+1][y+2] < 7 and rank[x+1][y+2] > 0:
        defence[z] = [x+1, y+2]
        z += 1
    if x > 1 and y < 7 and rank[x-1][y+2] > 6:
        attack[z] = [x-1, y+2]
        z += 1
    elif x > 1 and y < 7 and rank[x-1][y+2] < 7 and rank[x-1][y+2] > 0:
        defence[z] = [x-1, y+2]
        z += 1
    if x > 2 and y < 8 and rank[x-2][y+1] > 6:
        attack[z] = [x-2, y+1]
        z += 1
    elif x > 2 and y < 8 and rank[x-2][y+1] < 7 and rank[x-2][y+1] > 0:
        defence[z] = [x-2, y+1]
        z += 1
    if x > 2 and y > 1 and rank[x-2][y-1] > 6:
        attack[z] = [x-2, y-1]
        z += 1
    elif x > 2 and y > 1 and rank[x-2][y-1] < 7 and rank[x-2][y-1] > 0:
        defence[z] = [x-2, y-1]
        z += 1
    if x > 1 and y > 2 and rank[x-1][y-2] > 6:
        attack[z] = [x-1, y-2]
        z += 1
    elif x > 1 and y > 2 and rank[x-1][y-2] and rank[x-1][y-2] > 0:
        defence[z] = [x-1, y-2]
        z += 1
    if x < 8 and y > 2 and rank[x+1][y-2] > 6:
        attack[z] = [x+1, y-2]
        z += 1
    elif x < 8 and y > 2 and rank[x+1][y-2] < 7 and rank[x+1][y-2] > 0:
        defence[z] = [x+1, y-2]
        z += 1
    if x < 7 and y > 1 and rank[x+2][y-1] > 6:
        attack[z] = [x+2, y-1]
        z += 1
    elif x < 7 and y > 1 and rank[x+2][y-1] < 7 and rank[x+2][y-1] > 0:
        defence[z] = [x+2, y-1]
        z += 1
    return go, attack, defence, z

def get_black_knight_moves(game_id, x, y, blocklines=[], z=0):
    attack = {}
    defence = {}
    rank = get_board(game_id)
    for line in blocklines:
        if [x, y] in line.values():
            go = {}
            return go, attack, defence, z
    # dictionary of possible moves
    go, z = get_knight_moves_part1(rank, x, y, z)
    # dictionary of possible attacks
    if x < 7 and y < 8 and rank[x+2][y+1] < 7 and rank[x+2][y+1] > 0:
        attack[z] = [x+2, y+1]
        z += 1
    elif x < 7 and y < 8 and rank[x+2][y+1] > 6:
        defence[z] = [x+2, y+1]
        z += 1
    if x < 8 and y < 7 and rank[x+1][y+2] < 7 and rank[x+1][y+2] > 0:
        attack[z] = [x+1, y+2]
        z += 1
    elif x < 8 and y < 7 and rank[x+1][y+2] > 6:
        defence[z] = [x+1, y+2]
        z += 1
    if x > 1 and y < 7 and rank[x-1][y+2] < 7 and rank[x-1][y+2] > 0:
        attack[z] = [x-1, y+2]
        z += 1
    elif x > 1 and y < 7 and rank[x-1][y+2] > 6:
        defence[z] = [x-1, y+2]
        z += 1
    if x > 2 and y < 8 and rank[x-2][y+1] < 7 and rank[x-2][y+1] > 0:
        attack[z] = [x-2, y+1]
        z += 1
    elif x > 2 and y < 8 and rank[x-2][y+1] > 6:
        defence[z] = [x-2, y+1]
        z += 1
    if x > 2 and y > 1 and rank[x-2][y-1] < 7 and rank[x-2][y-1] > 0:
        attack[z] = [x-2, y-1]
        z += 1
    elif x > 2 and y > 1 and rank[x-2][y-1] > 6:
        defence[z] = [x-2, y-1]
        z += 1
    if x > 1 and y > 2 and rank[x-1][y-2] < 7 and rank[x-1][y-2] > 0:
        attack[z] = [x-1, y-2]
        z += 1
    elif x > 1 and y > 2 and rank[x-1][y-2] > 6:
        defence[z] = [x-1, y-2]
        z += 1
    if x < 8 and y > 2 and rank[x+1][y-2] < 7 and rank[x+1][y-2] > 0:
        attack[z] = [x+1, y-2]
        z += 1
    elif x < 8 and y > 2 and rank[x+1][y-2] > 6:
        defence[z] = [x+1, y-2]
        z += 1
    if x < 7 and y > 1 and rank[x+2][y-1] < 7 and rank[x+2][y-1] > 0:
        attack[z] = [x+2, y-1]
        z += 1
    elif x < 7 and y > 1 and rank[x+2][y-1] > 6:
        defence[z] = [x+2, y-1]
        z += 1
    return go, attack, defence, z

def get_bishop_moves(game_id, x, y, blocklines=[], step=1, z=0):
    go = {}
    attack = {}
    defence = {}
    rank = get_board(game_id)
    #Checking if the figure is on the blockline. If it is it can only move down the blockline
    side_a = side_b = side_c = side_d = 1
    for line in blocklines:
        if [x, y] in line.values():
            side_a = side_b = side_c = side_d = 0
            if x < 8 and y < 8 and [x+1, y+1] in line.values():
                side_a = 1
            if x < 8 and y > 1 and [x+1, y-1] in line.values():
                side_b = 1
            if x > 1 and y > 1 and [x-1, y-1] in line.values():
                side_c = 1
            if x > 1 and y < 8 and [x-1, y+1] in line.values():
                side_d = 1         
    # we don't need a separate counter for attacks cause we don't really use keys anywhere
    #here we are going to add that extra if
    # if ([x, y] in blocklines and x+1 y+1 in blocklines) or [x, y] not in blocklines:
    if x < 8 and y < 8 and side_a:
        if x > y:
            squares_num = 9 - x
        else:
            squares_num = 9 - y
        for i in range (1, squares_num, step):
            if rank[x+i][y+i] == 0:
                go[z] = [x+i, y+i]
                z += 1
            elif (rank[x][y] < 7 and rank[x+i][y+i] > 6) or (rank[x][y] > 6  and rank[x+i][y+i] < 7):
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
            elif (rank[x][y] < 7 and rank[x+i][y-i] > 6) or (rank[x][y] > 6 and rank[x+i][y-i] < 7):
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
            elif (rank[x][y] < 7 and rank[x-i][y-i] > 6) or (rank[x][y] > 6 and rank[x-i][y-i] < 7):
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
            elif (rank[x][y] < 7 and rank[x-i][y+i] > 6) or (rank[x][y] > 6 and rank[x-i][y+i] < 7):
                attack[z] = [x-i, y+i]
                z += 1
                break
            elif (rank[x][y] < 7 and rank[x-i][y+i] < 7) or (rank[x][y] > 6 and rank[x-i][y+i] > 6):
                defence[z] = [x-i, y+i]
                z += 1
                break
    return go, attack, defence, z
 
def get_rook_moves(game_id, x, y, blocklines=[], step=1, z=0):
    go = {}
    attack = {}
    defence = {}
    rank = get_board(game_id)
    side_a = side_b = side_c = side_d = 1
    for line in blocklines:
        if [x, y] in line.values():
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
    if y < 8 and side_a:
        squares_num = 9 - y
        for i in range (1, squares_num, step):
            if rank[x][y+i] == 0:
                go[z] = [x, y+i]
                z += 1
            elif (rank[x][y] < 7 and rank[x][y+i] > 6) or (rank[x][y] > 6 and rank[x][y+i] < 7):
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
            elif (rank[x][y] < 7 and rank[x+i][y] > 6) or (rank[x][y] > 6 and rank[x+i][y] < 7):
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
            elif (rank[x][y] < 7 and rank[x][y-i] > 6) or (rank[x][y] > 6 and rank[x][y-i] < 7):
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
            elif (rank[x][y] < 7 and rank[x-i][y] > 6) or (rank[x][y] > 6 and rank[x-i][y] < 7):
                attack[z] = [x-i, y]
                z += 1
                break
            elif (rank[x][y] < 7 and rank[x-i][y] < 7) or (rank[x][y] > 6 and rank[x-i][y] > 6):
                defence[z] = [x-i, y]
                z += 1
                break
    return go, attack, defence, z

def get_queen_moves(game_id, x, y, blocklines=[], z=0):
    go, attack, defence, z = get_bishop_moves(game_id, x, y, blocklines=blocklines, step=1, z=z)
    go_2, attack_2, defence_2, z = get_rook_moves(game_id, x, y, blocklines=blocklines, step=1, z=z)
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
    attack_king_figures = []
    rank = get_board(game_id)
    z = 0
    king_idx = 0
    for x in range (1, 9):
        for y in range (1, 9):
            if (session['figures'] == 0 and not opp) or (session['figures'] == 1 and opp):
                if rank[x][y] == 1:
                    _, attack, _, z  = get_white_pawn_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 2:
                    _, attack, _, z = get_white_knight_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 3:
                    _, attack, _, z = get_bishop_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 4:
                    _, attack, _, z = get_rook_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 5:
                    _, attack, _, z = get_queen_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 6:
                    _, attack, _, z = get_king_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
            else:
                if rank[x][y] == 7:
                    _, attack, _, z = get_black_pawn_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 8:
                    _, attack, _, z = get_black_knight_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 9:
                    _, attack, _, z = get_bishop_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 10:
                    _, attack, _, z = get_rook_moves(game_id, x, y, step=1, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 11:
                    _, attack, _, z = get_queen_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
                if rank[x][y] == 12:
                    _, attack, _, z = get_king_moves(game_id, x, y, z=z)
                    if king_coordinates in attack.values():
                        attack_king_coord[king_idx] = [x, y]
                        attack_king_figures.append(rank[x][y])
                        king_idx += 1
                    all_attacks.update(attack)
    return all_attacks, attack_king_coord, attack_king_figures

def calculate_possible_checks(game_id, opp=False):
    into_check = {}
    rank = get_board(game_id)
    z = 0
    for x in range (1, 9):
        for y in range (1, 9):
            if (session['figures'] == 0 and not opp) or (session['figures'] == 1 and opp):
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
            if rank[x][y] == 6 and ((session['figures'] == 1 and not opp) or (session['figures'] == 0 and opp)):
                if [x, y] in all_attacks.values():
                    return True
                else:
                    return False
            elif rank[x][y] == 12 and ((session['figures'] == 0 and not opp) or (session['figures'] == 1 and opp)):
                if [x, y] in all_attacks.values():
                    return True
                else:
                    return False
    return False

def check_checkmate(game_id, king_coordinates, attack_king_coord, attack_king_figures, all_attacks):
    rank = get_board(game_id)
    x = king_coordinates[0]
    y = king_coordinates[1]
    z = 0
    if session['figures'] == 1:
        king_moveable, _ = check_white_king_can_move(game_id, rank, z, x, y)
    if session['figures'] == 0:
        king_moveable, _ = check_black_king_can_move(game_id, rank, z, x, y)
    #when doublecheck
    if len(attack_king_coord) == 2 and not king_moveable:
        return True
    #when check is from adjasent square:
    if len(attack_king_coord) == 1:
        i = attack_king_coord[0][0]
        j = attack_king_coord[0][1]
        if ((i == x - 1 and j == y - 1) or (i == x - 1 and j == y) or (i == x - 1 and j == y + 1) or (i == x and j == y + 1) or
            (i == x + 1 and j == y + 1) or (i == x + 1 and j == y) or (i == x + 1 and j == y - 1) or
            (i == x and j == y - 1)) and not king_moveable and not [i, j] in all_attacks.values():
            return True
        if attack_king_figures[0] == 2 and not king_moveable and not [i, j] in all_attacks.values():
            return True
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

def calculate_checklines(game_id, attack_king_coord, attack_king_figures, opp=False):
    #Calculate king coordinates of the other player
    king_coord = get_king_coordinates(game_id, opp=not opp)
    i = king_coord[0]
    j = king_coord[1]
    rank = get_board(game_id)
    checklines = []
    for count in range (len(attack_king_coord)):
        x = attack_king_coord[count][0]
        y = attack_king_coord[count][1]
        figure = attack_king_figures[count]
        if (session['figures'] == 1 and not opp) or (session['figures'] == 0 and opp):
            figures = 1
            if (x - y == i - j) and x - i > 0:
                calculate_block_check_lines_diagonal_1(checklines, rank, x, i, j, figures, check=True)
            if (x - y == i - j) and i - x > 0:
                calculate_block_check_lines_diagonal_2(checklines, rank, x, y, i, figures, check=True)
            if (x + y == i + j) and x - i > 0:
                calculate_block_check_lines_diagonal_3(checklines, rank, x, i, j, figures, check=True)
            if (x + y == i + j) and i - x > 0:
                calculate_block_check_lines_diagonal_4(checklines, rank, x, y, i, figures, check=True)
            if (x == i) and y - j > 0:
                calculate_block_check_lines_horizontal_1(checklines, rank, y, i, j, figures, check=True)
            if (x == i) and j - y > 0:
                calculate_block_check_lines_horizontal_2(checklines, rank, x, y, j, figures, check=True)
            if (y == j) and x - i > 0:
                calculate_block_check_lines_vertical_1(checklines, rank, x, i, j, figures, check=True)
            if (y == j) and i - x > 0:
                calculate_block_check_lines_vertical_2(checklines, rank, x, y, i, figures, check=True)
            if figure == 8:
                knight_attack = {}
                knight_attack[count] = [x, y]
                checklines.append(knight_attack)
        elif (session['figures'] == 0 and not opp) or (session['figures'] == 1 and opp):
            figures = 0
            if (x - y == i - j) and x - i > 0:
                calculate_block_check_lines_diagonal_1(checklines, rank, x, i, j, figures, check=True)
            if (x - y == i - j) and i - x > 0:
                calculate_block_check_lines_diagonal_2(checklines, rank, x, y, i, figures, check=True)
            if (x + y == i + j) and x - i > 0:
                calculate_block_check_lines_diagonal_3(checklines, rank, x, i, j, figures, check=True)
            if (x + y == i + j) and i - x > 0:
                calculate_block_check_lines_diagonal_4(checklines, rank, x, y, i, figures, check=True)
            if (x == i) and y - j > 0:
                calculate_block_check_lines_horizontal_1(checklines, rank, y, i, j, figures, check=True)
            if (x == i) and j - y > 0:
                calculate_block_check_lines_horizontal_2(checklines, rank, x, y, j, figures, check=True)
            if (y == j) and x - i > 0:
                calculate_block_check_lines_vertical_1(checklines, rank, x, i, j, figures, check=True)
            if (y == j) and i - x > 0:
                calculate_block_check_lines_vertical_2(checklines, rank, x, y, i, figures, check=True)
            if figure == 2:
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
            if (session['figures'] == 1 and not opp) or (session['figures'] == 0 and opp):
                figures = 1
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x - y == i - j) and x - i > 1:
                    calculate_block_check_lines_diagonal_1(blocklines, rank, x, i, j, figures)
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x - y == i - j) and i - x > 1:
                    calculate_block_check_lines_diagonal_2(blocklines, rank, x, y, i, figures)
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x + y == i + j) and x - i > 1:
                    calculate_block_check_lines_diagonal_3(blocklines, rank, x, i, j, figures)
                if (rank[x][y] == 9 or rank[x][y] == 11) and (x + y == i + j) and i - x > 1:
                    calculate_block_check_lines_diagonal_4(blocklines, rank, x, y, i, figures)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (x == i) and y - j > 1:
                    calculate_block_check_lines_horizontal_1(blocklines, rank, y, i, j, figures)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (x == i) and j - y > 1:
                    calculate_block_check_lines_horizontal_2(blocklines, rank, x, y, j, figures)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (y == j) and x - i > 1:
                    calculate_block_check_lines_vertical_1(blocklines, rank, x, i, j, figures)
                if (rank[x][y] == 10 or rank[x][y] == 11) and (y == j) and i - x > 1:
                    calculate_block_check_lines_vertical_2(blocklines, rank, x, y, i, figures)
            elif (session['figures'] == 0 and not opp) or (session['figures'] == 1 and opp):
                figures = 0
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x - y == i - j) and x - i > 1:
                    calculate_block_check_lines_diagonal_1(blocklines, rank, x, i, j, figures)
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x - y == i - j) and i - x > 1:
                    calculate_block_check_lines_diagonal_2(blocklines, rank, x, y, i, figures)
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x + y == i + j) and x - i > 1:
                    calculate_block_check_lines_diagonal_3(blocklines, rank, x, i, j, figures)
                if (rank[x][y] == 3 or rank[x][y] == 5) and (x + y == i + j) and i - x > 1:
                    calculate_block_check_lines_diagonal_4(blocklines, rank, x, y, i, figures)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (x == i) and y - j > 1:
                    calculate_block_check_lines_horizontal_1(blocklines, rank, y, i, j, figures)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (x == i) and j - y > 1:
                    calculate_block_check_lines_horizontal_2(blocklines, rank, x, y, j, figures)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (y == j) and x - i > 1:
                    calculate_block_check_lines_vertical_1(blocklines, rank, x, i, j, figures)
                if (rank[x][y] == 4 or rank[x][y] == 5) and (y == j) and i - x > 1:
                    calculate_block_check_lines_vertical_2(blocklines, rank, x, y, i, figures)                  
    return blocklines

def calculate_block_check_lines_diagonal_1(lines, rank, x, i, j, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    #For lines that start with a king we add one extra field to include attacking figure
    #and start the count from 1 to exclude the king.
    for count in range(1, x - i + 1):
        line[count-1] = [i+count, j+count]
        if rank[i+count][j+count]:
            all_count += 1
        if (figures == 1 and rank[i+count][j+count] and rank[i+count][j+count] < 7) or \
           (figures == 0 and rank[i+count][j+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_diagonal_2(lines, rank, x, y, i, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    #For lines that start with an attacker, we start the count from 0 to include the attacker
    for count in range(i - x):
        line[count] = [x+count, y+count]
        if rank[x+count][y+count]:
            all_count += 1
        if (figures == 1 and rank[x+count][y+count] and rank[x+count][y+count] < 7) or \
           (figures == 0 and rank[x+count][y+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_diagonal_3(lines, rank, x, i, j, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(1, x - i + 1):
        line[count-1] = [i+count, j-count]
        if rank[i+count][j-count]:
            all_count += 1
        if (figures == 1 and rank[i+count][j-count] and rank[i+count][j-count] < 7) or \
           (figures == 0 and rank[i+count][j-count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_diagonal_4(lines, rank, x, y, i, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(i - x):
        line[count] = [x+count, y-count]
        if rank[x+count][y-count]:
            all_count += 1
        if (figures == 1 and rank[x+count][y-count] and rank[x+count][y-count] < 7) or \
           (figures == 0 and rank[x+count][y-count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_horizontal_1(lines, rank, y, i, j, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(1, y - j + 1):
        line[count-1] = [i, j+count]
        if rank[i][j+count]:
            all_count += 1
        if (figures == 1 and rank[i][j+count] and rank[i][j+count] < 7) or \
           (figures == 0 and rank[i][j+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_horizontal_2(lines, rank, x, y, j, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(j - y):
        line[count] = [x, y+count]
        if rank[x][y+count]:
            all_count += 1
        if (figures == 1 and rank[x][y+count] and rank[x][y+count] < 7) or \
           (figures == 0 and rank[x][y+count] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_vertical_1(lines, rank, x, i, j, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(1, x - i + 1):
        line[count-1] = [i+count, j]
        if rank[i+count][j]:
            all_count += 1
        if (figures == 1 and rank[i+count][j] and rank[i+count][j] < 7) or \
           (figures == 0 and rank[i+count][j] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def calculate_block_check_lines_vertical_2(lines, rank, x, y, i, figures, check=False):
    line = {}
    all_count = 0
    block_count = 0
    for count in range(i - x):
        line[count] = [x+count, y]
        if rank[x+count][y]:
            all_count += 1
        if (figures == 1 and rank[x+count][y] and rank[x+count][y] < 7) or \
           (figures == 0 and rank[x+count][y] > 6):
            block_count += 1
    if block_count == 1 and all_count == 2 and not check:
        lines.append(line)
    elif block_count == 0 and all_count == 1 and check:
        lines.append(line)

def check_can_move(game_id, blocklines=[], checklines = [], figures=None):
    rank = get_board(game_id)
    moveable = {}
    z = 0
    for x in range (1, 9):
        for y in range (1, 9):
            if figures == 0:
                if rank[x][y] == 1:
                    add_moveable, z = check_white_pawn_can_move(rank, z, x, y, blocklines, checklines)
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
                if rank[x][y] == 7:
                    add_moveable, z = check_black_pawn_can_move(rank, z, x, y, blocklines, checklines)
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
                
def check_white_pawn_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    #This check is for when that figure is on the blockline
    for line in blocklines:
        # This is when there's both a checkline and a blockline
        if [x, y] in line.values() and checklines:
             return moveable, z
        # Next two cases for when there's only a blockline
        if x < 8 and [x, y] in line.values() and ((rank[x+1][y] == 0 and [x+1, y] in line.values()) or
                                                 (y < 8 and rank[x+1][y+1] > 6 and [x+1, y+1] in line.values() 
                                                 and len(line.values()) == 2) or 
                                                 (y > 1 and rank[x+1][y-1] > 6 and [x+1, y-1] in line.values() 
                                                 and len(line.values()) == 2)):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        if x < 8 and [x, y] in line.values() and ([x+1, y] not in line.values() and
                                                 ([x+1, y+1] not in line.values() or len(line.values()) > 2) and 
                                                 ([x+1, y-1] not in line.values() or len(line.values()) > 2)):
            return moveable, z
    # This is when there's only a checkline
    for checkline in checklines:
        if x < 8 and (rank[x+1][y] == 0 and [x+1, y] in checkline.values() or 
        (y < 8 and rank[x+1][y+1] > 6 and [x+1, y+1] in checkline.values())
        or (y > 1 and rank[x+1][y-1] > 6 and [x+1, y-1] in checkline.values())):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z
    #This check is for when the figure is not on the blockline
    if x < 8 and (rank[x+1][y] == 0 or (y < 8 and rank[x+1][y+1] > 6)
        or (y > 1 and rank[x+1][y-1] > 6)):
        moveable[z]=[x, y]
        z += 1
    return moveable, z

def check_black_pawn_can_move(rank, z, x, y, blocklines, checklines):
    moveable = {}
    #This check is for when that figure is on the blockline
    for line in blocklines:
        if [x, y] in line.values() and checklines:
             return moveable, z
        if x > 1 and [x, y] in line.values() and ((rank[x-1][y] == 0 and [x-1, y] in line.values()) or
                                                 (y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0 and 
                                                 [x-1, y+1] in line.values() and len(line.values()) == 2) or
                                                 (y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0 and 
                                                 [x-1, y-1] in line.values() and len(line.values()) == 2)):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        if x > 1 and [x, y] in line.values() and ([x-1, y] not in line.values() and
                                                 ([x-1, y+1] not in line.values() or len(line.values()) > 2) and 
                                                 ([x-1, y-1] not in line.values() or len(line.values()) > 2)):
            return moveable, z
    for checkline in checklines:
        if x > 1 and ((rank[x-1][y] == 0 and [x-1, y] in checkline.values()) or 
        (y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0 and [x-1, y+1] in checkline.values()) or
        (y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0) and [x-1, y-1] in checkline.values()):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z
    #This check is for when the figure is not on the blockline and not on the checkline
    if x > 1 and (rank[x-1][y] == 0 or (y < 8 and rank[x-1][y+1] < 7 and rank[x-1][y+1] > 0) 
    or (y > 1 and rank[x-1][y-1] < 7 and rank[x-1][y-1] > 0)):
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
    for checkline in checklines:
        if ((x < 8 and y < 8 and ((rank[x+1][y+1] == 0 or rank[x+1][y+1] > 6) and [x+1, y+1] in checkline.values())) or
        (x < 8 and y > 1 and ((rank[x+1][y-1] == 0 or rank[x+1][y-1] > 6) and [x+1, y-1] in checkline.values())) or
        (x > 1 and y > 1 and ((rank[x-1][y-1] == 0 or rank[x-1][y-1] > 6) and [x-1, y-1] in checkline.values())) or
        (x > 1 and y < 8 and ((rank[x-1][y+1] == 0 or rank[x-1][y+1] > 6) and [x-1, y+1] in checkline.values()))):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
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
    for checkline in checklines:
        if ((x < 8 and y < 8 and rank[x+1][y+1] < 7 and [x+1, y+1] in checkline.values()) or 
        (x < 8 and y > 1 and rank[x+1][y-1] < 7 and [x+1, y-1] in checkline.values()) or
        (x > 1 and y > 1 and rank[x-1][y-1] < 7 and [x-1, y-1] in checkline.values()) or 
        (x > 1 and y < 8 and rank[x-1][y+1] < 7 and [x-1, y+1] in checkline.values())):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z
    if (x < 8 and y < 8 and rank[x+1][y+1] < 7) or (x < 8 and y > 1 and rank[x+1][y-1] < 7) or \
    (x > 1 and y > 1 and rank[x-1][y-1] < 7) or (x > 1 and y < 8 and rank[x-1][y+1] < 7):
        moveable[z]=[x, y]
        z += 1
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
    for checkline in checklines:
        if ((y < 8 and ((rank[x][y+1] == 0 or rank[x][y+1] > 6) and [x, y+1] in checkline.values())) or
        (x < 8 and ((rank[x+1][y] == 0 or rank[x+1][y] > 6) and [x+1, y] in checkline.values())) or
        (y > 1 and ((rank[x][y-1] == 0 or rank[x][y-1] > 6) and [x, y-1] in checkline.values())) or
        (x > 1 and ((rank[x-1][y] == 0 or rank[x-1][y] > 6) and [x-1, y] in checkline.values()))):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
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
    for checkline in checklines:
        if ((y < 8 and rank[x][y+1] < 7 and [x, y+1] in checkline.values()) or 
        (x < 8 and rank[x+1][y] < 7 and [x+1, y] in checkline.values()) or
        (y > 1 and rank[x][y-1] < 7 and [x, y-1] in checkline.values()) or
        (x > 1 and rank[x-1][y] < 7 and [x-1, y] in checkline.values())):
            moveable[z]=[x, y]
            z += 1
            return moveable, z
        else:
            return moveable, z
    if (y < 8 and rank[x][y+1] < 7) or (x < 8 and rank[x+1][y] < 7) or \
    (y > 1 and rank[x][y-1] < 7) or (x > 1 and rank[x-1][y] < 7):
        moveable[z]=[x, y]
        z += 1
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