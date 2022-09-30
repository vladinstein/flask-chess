import string
from flask import render_template, request, redirect, url_for, flash
from flask import session
from flask_session import Session
from chess.forms import CreateGameForm, JoinGameForm
from chess.models import Game, Rank
from chess import app, bcrypt, db, socketio
from random import getrandbits

@socketio.on('connect')
def connect():
    session['sid'] = request.sid
    print(session['sid'])

@socketio.on('take')
def moves(data):
    print(data)
    rank={}
    files = string.ascii_lowercase[0:8]
    y = files[int(data['y'])-1]
    x = int(data['x'])
    for i in range (1, 9):
        rank[i] = Rank.query.filter_by(game_id=data['id'], number=i).first().__dict__
    print(rank[x][y])
   
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
    files = string.ascii_lowercase[0:8]
    for i in range (1, 9):
        rank[i] = Rank.query.filter_by(game_id=game_id, number=i).first().__dict__
    for i in range (1, 9):
        for j in range (8):
            if rank[i][files[j]] == 1: 
                if rank[i+1][files[j]] == 0 or (j < 7 and rank[i+1][files[j+1]] > 6) \
                    or (j > 0 and rank[i+1][files[j-1]] > 6):
                        can_move.append([i, j+1])
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
            flash('You have connected to the game.', 'success')
            return redirect(url_for('game', game_id=game.id))
        else:
            flash('Couldn\'t connect to the game. Check the game ID and the password.', 'danger')
    return render_template('index.html', cr_form=cr_form, jn_form=jn_form)

@app.route("/game/<int:game_id>")
def game(game_id):
    rank={}
    for i in range (1, 9):
        rank[i] = Rank.query.filter_by(game_id=game_id, number=i).first()   
    files = string.ascii_lowercase[0:8]
    moving = white_check(game_id)
    print(moving)
    return render_template('game.html', files=files, rank=rank, moving=moving, game_id=game_id)



