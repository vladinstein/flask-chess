from dataclasses import dataclass
import string
from flask import render_template, request, redirect, url_for, flash
from flask import session
from flask import make_response
from flask_session import Session
from chess.forms import CreateGameForm, JoinGameForm
from chess.models import Game, Rank
from chess.utils import get_moves, create_game, check_can_move, calculate_attacks_possible_checks, add_defences_to_db
from chess import app, bcrypt, db, socketio
from random import getrandbits
from functools import wraps

@app.after_request
def add_header(response):    
  response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  if ('Cache-Control' not in response.headers):
      response.headers['Cache-Control'] = 'public, max-age=600'
  return response

#def login_required(f):
#    @wraps(f)
#    def decorated_function(*args, **kwargs):
#        if session.get('figures') is None:
#           return redirect('/',code=302)
#        return f(*args, **kwargs)
#   return decorated_function

@socketio.on('connect')
def connect():
    session['sid'] = request.sid

@socketio.on('info')
def info(data):
    game_id = int(data['id'])
    game = Game.query.filter_by(id=game_id).first()
    if session['creator']:
        if session['figures'] == 0:
            game.white_sid = session['sid']
        if session['figures'] == 1:
            game.black_sid = session['sid']
        db.session.commit()
    else:
        if not game.both_connected:
            if session['figures'] == 0:
                game.white_sid = session['sid'] 
                moving = check_can_move(game_id, figures = 0)
                socketio.emit('connected', moving, room=game.white_sid)
                socketio.emit('wait_move_status', room=game.black_sid)
                game.both_connected = 1
            else:
                game.black_sid = session['sid'] 
                moving = check_can_move(game_id, figures = 0)
                socketio.emit('connected', moving, room=game.white_sid)
                socketio.emit('wait_move_status', room=game.black_sid)
                game.both_connected = 1
            db.session.commit()
        else:
            if session['figures'] == 0:
                game.white_sid = session['sid'] 
            else:
                game.black_sid = session['sid']
            db.session.commit()


@socketio.on('take')
def take(data):
    figure = int(data['figure'])
    game_id = int(data['id'])
    y = int(data['y'])
    x = int(data['x'])
    go = {}
    attack = {}
    go, attack = get_moves(game_id, x, y, figure)
    socketio.emit('moves', data=(go, attack), room=session['sid'])

@socketio.on('go')
def go(data):
    figure = int(data['figure'])
    game_id = int(data['id'])
    y = int(data['y'])
    x = int(data['x'])
    i = int(data['i'])
    j = int(data['j'])
    files = string.ascii_lowercase[0:8]
    rank = Rank.query.filter_by(game_id=game_id, number=x).first()
    setattr(rank, files[y-1], figure)
    db.session.commit()
    rank = Rank.query.filter_by(game_id=game_id, number=i).first()
    setattr(rank, files[j-1], 0)
    db.session.commit()
    _, into_check = calculate_attacks_possible_checks(game_id)
    add_defences_to_db(game_id, into_check)
    game = Game.query.filter_by(id=game_id).first()
    if session['figures'] == 0:
        socketio.emit('opp_move', {'i': i, 'j': j, 'x': x, 'y': y}, room=game.black_sid)
    else:
        socketio.emit('opp_move', {'i': i, 'j': j, 'x': x, 'y': y}, room=game.white_sid)
    moving = {}
    if game.p1_move:
        game.p1_move = 0
    else:
        game.p1_move = 1
    db.session.commit()
    if figure < 7:
        moving = check_can_move(game_id, figures = 1)
        socketio.emit('next_move', moving, room=game.black_sid)
    else:
        moving = check_can_move(game_id, figures = 0)  
        socketio.emit('next_move', moving, room=game.white_sid)

@app.route("/", methods=['GET', 'POST'])
def index():
    cr_form = CreateGameForm()
    jn_form = JoinGameForm()
    if cr_form.cr_submit.data and cr_form.validate():
        session['creator'] = 1
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
        session['creator'] = 0
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
    moving = {}
    game = Game.query.filter_by(id=game_id).first()
    # game.white_sid can be removed 
    if game.black_sid and game.white_sid:
        if session ['figures'] == 0 and game.p1_move == 1:
            moving = check_can_move(game_id, figures = 0)
        elif session ['figures'] == 1 and game.p1_move == 0:
            moving = check_can_move(game_id, figures = 1)
    response = make_response(render_template('game.html', files=files, rank=rank, moving=moving, 
                                             game_id=game_id, both_connected = game.both_connected,
                                             p1_move = game.p1_move))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response




