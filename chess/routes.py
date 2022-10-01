import string
from flask import render_template, request, redirect, url_for, flash
from flask import session
from flask_session import Session
from chess.forms import CreateGameForm, JoinGameForm
from chess.models import Game, Rank
from chess import app, bcrypt, db, socketio
from random import getrandbits
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('figures') is None:
            return redirect('/',code=302)
        return f(*args, **kwargs)
    return decorated_function

@socketio.on('connect')
def connect():
    session['sid'] = request.sid

@socketio.on('take')
def moves(data):
    figure = int(data['figure'])
    game_id = int(data['id'])
    y = int(data['y'])
    x = int(data['x'])
    go = []
    attack = []
    go, attack = check_moves(game_id, x, y, figure)
    go = dict(go)
    attack = dict(attack)
    socketio.emit('moves', data=(go, attack), room=session['sid'])

@socketio.on('go')
def moves(data):
    print(data)
    figure = int(data['figure'])
    game_id = int(data['id'])
    y = int(data['y'])
    x = int(data['x'])
    i = int(data['i'])
    y = int(data['y'])


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
    pass
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
    can_move = []
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, Rank.f,
                                           Rank.g, Rank.h).filter_by(game_id=game_id, number=i).first()
    for i in range (1, 9):
        for j in range (1, 9):
            if rank[i][j] == 1: 
                if rank[i+1][j] == 0 or (j < 8 and rank[i+1][j+1] > 6) \
                    or (j > 1 and rank[i+1][j-1] > 6):
                        can_move.append([i, j])
    return can_move

@app.route("/", methods=['GET', 'POST'])
def index():
    cr_form = CreateGameForm()
    jn_form = JoinGameForm()
    if cr_form.cr_submit.data and cr_form.validate():
        hashed_password = bcrypt.generate_password_hash(cr_form.password.data).decode('utf-8')
        if cr_form.figures.data == 'black':
            player_1 = True
            session['figures'] = 1
        elif cr_form.figures.data == 'random':
            player_1 = bool(getrandbits(1))
            if player_1:
                session['figures'] = 1
            else:
                session['figures'] = 0
        else:
            player_1 = False
            session['figures'] = 0
        game = Game(password=hashed_password, player_1=player_1)
        db.session.add(game)
        db.session.commit()
        session['game'] = game.id
        create_game(game.id)
        flash('You have created a game. Send the ID of your game to your opponent and wait for him\
              to connect.', 'success')
        return redirect(url_for('game', game_id=game.id))
    elif jn_form.jn_submit.data and jn_form.validate():
        game = Game.query.get(jn_form.game_id.data)
        if game and bcrypt.check_password_hash(game.password, jn_form.password.data):
            if game.player_1:
                session['figures'] = 0
            else:
                session['figures'] = 1
            session['game'] = game.id
            flash('You have connected to the game.', 'success')
            return redirect(url_for('game', game_id=game.id))
        else:
            flash('Couldn\'t connect to the game. Check the game ID and the password.', 'danger')
    return render_template('index.html', cr_form=cr_form, jn_form=jn_form)

@app.route("/game/<int:game_id>")
@login_required
def game(game_id):
    # is this solution ok?
    try: 
        session['game']
    except KeyError:
        return redirect(url_for('index'))
    if session['game'] != game_id:
        return redirect(url_for('index'))
    rank={}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, Rank.f,
                                        Rank.g, Rank.h).filter_by(game_id=game_id, number=i).first()   
    files = string.ascii_lowercase[0:8]
    moving = white_check(game_id)
    print(moving)
    return render_template('game.html', files=files, rank=rank, moving=moving, game_id=game_id)




