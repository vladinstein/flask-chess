from dataclasses import dataclass
import string
from flask import render_template, request, redirect, url_for, flash
from flask import session
from flask import make_response
from flask_session import Session
from chess.forms import CreateGameForm, JoinGameForm, ReturnGameForm
from chess.models import Game, Rank
from chess.utils import get_moves, create_game, check_can_move, calculate_attacks, calculate_possible_checks, \
                        add_attacks_to_db, add_defences_to_db, check_if_check, get_king_coordinates, \
                        calculate_blocklines, calculate_checklines, disable_castling_white,\
                        disable_castling_black, switch_en_passant
from chess import app, bcrypt, db, socketio
from random import getrandbits

@app.after_request
def add_header(response):    
  response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  if ('Cache-Control' not in response.headers):
      response.headers['Cache-Control'] = 'public, max-age=600'
  return response

@app.route("/", methods=['GET', 'POST'])
def index():
    cr_form = CreateGameForm()
    jn_form = JoinGameForm()
    rt_form = ReturnGameForm()
    if cr_form.cr_submit.data and cr_form.validate():
        session['creator'] = 1
        session['join'] = 0
        session['return'] = 0
        hashed_password = bcrypt.generate_password_hash(cr_form.password.data).decode('utf-8')
        if cr_form.pieces.data == 'black':
            player_1 = True
            session['pieces'] = 1
        elif cr_form.pieces.data == 'random':
            player_1 = bool(getrandbits(1))
            if player_1:
                session['pieces'] = 1
            else:
                session['pieces'] = 0
        else:
            player_1 = False
            session['pieces'] = 0
        game = Game(password=hashed_password, player_1=player_1)
        db.session.add(game)
        db.session.commit()
        session['game_id'] = game.id
        create_game(game.id)
        flash('You have created a game. Send the ID of your game to your opponent and wait for him\
              to connect.', 'success')
        return redirect(url_for('game', game_id=game.id))
    elif jn_form.jn_submit.data and jn_form.validate():
        session['creator'] = 0
        session['join'] = 1
        session['return'] = 0
        game = Game.query.get(jn_form.game_id.data)
        if game and bcrypt.check_password_hash(game.password, jn_form.password.data) and not game.both_connected:
            if game.player_1:
                session['pieces'] = 0
            else:
                session['pieces'] = 1
            session['game_id'] = game.id
            flash('You have connected to the game.', 'success')
            return redirect(url_for('game', game_id=game.id))
        else:
            flash('Couldn\'t connect to the game. Check the game ID and the password.', 'danger')
    elif rt_form.rt_submit.data and rt_form.validate():
        session['creator'] = 0
        session['join'] = 0
        session['return'] = 1
        game = Game.query.get(rt_form.game_id.data)
        if game == None or not game.both_connected:
            flash('Cannot return to the game that hasn\'t started.', 'danger')
        else:
            if game and bcrypt.check_password_hash(game.password, rt_form.password.data):
                if rt_form.pieces.data == 'black':
                    session['pieces'] = 1
                    if game.white_disconnected == 1:
                        flash('You have connected to the game. Waiting for your opponent.', 'success')
                else:
                    session['pieces'] = 0
                    if game.black_disconnected == 1:
                        flash('You have connected to the game. Waiting for your opponent.', 'success')
                session['game_id'] = game.id
                flash('You have connected to the game.', 'success')
                return redirect(url_for('game', game_id=game.id))
            else:
                flash('Couldn\'t connect to the game. Check the game ID and the password.', 'danger')
    return render_template('index.html', cr_form=cr_form, jn_form=jn_form, rt_form=rt_form)

@socketio.on('disconnect')
def disconnect():
    game_id = session['game_id']
    game = Game.query.filter_by(id=game_id).first()
    if session['pieces'] == 0:
        game.white_disconnected = 1
    else:
        game.black_disconnected = 1
    db.session.commit()

@socketio.on('connect')
def connect():
    session['sid'] = request.sid
    game_id = session['game_id']
    game = Game.query.filter_by(id=game_id).first()
    # If this is a creator of the game, simply copy the sid value to the db.
    if session['creator']:
        if session['pieces'] == 0:
            game.white_sid = session['sid']
            if game.both_connected:
                socketio.emit('change_flash_connected', room=game.white_sid)
                socketio.emit('change_flash_first', room=game.black_sid)          
        else:
            game.black_sid = session['sid']
            if game.both_connected:
                socketio.emit('change_flash_connected', room=game.black_sid)
                socketio.emit('change_flash_first', room=game.white_sid)
        db.session.commit()
    # If someone is joining a game, copy sid value and send messages.
    elif session['join']:
        if session['pieces'] == 0:
            game.white_sid = session['sid']
            if game.both_connected:
                socketio.emit('change_flash_connected', room=game.white_sid)
            # Send socket messages to change/remove flask flash messages.
            socketio.emit('change_flash_first', room=game.black_sid)
            socketio.emit('change_flash_second', room=game.white_sid)
        else:
            game.black_sid = session['sid']
            if game.both_connected:
                socketio.emit('change_flash_connected', room=game.black_sid)
            # Send socket messages to change/remove flask flash messages.
            socketio.emit('change_flash_first', room=game.white_sid)
            socketio.emit('change_flash_second', room=game.black_sid)
        if not game.both_connected:
            moving = check_can_move(game_id, game, pieces = 0)
            socketio.emit('connected', moving, room=game.white_sid)
            socketio.emit('wait_move_status', room=game.black_sid)
            game.both_connected = 1
        db.session.commit()
    # If someone is returning to a game, copy sid value and send a socket message.
    else:
        if session['pieces'] == 0:
            game.white_sid = session['sid']
            if game.white_disconnected == 1 and game.black_disconnected == 0:
                socketio.emit('change_flash_first', room=game.black_sid)
                socketio.emit('change_flash_second', room=game.white_sid)
        else:
            game.black_sid = session['sid']
            if game.black_disconnected == 1 and game.white_disconnected == 0:
                socketio.emit('change_flash_first', room=game.white_sid)
                socketio.emit('change_flash_second', room=game.black_sid)
        db.session.commit()
    if session['pieces'] == 0:
        game.white_disconnected = 0 
    else:
        game.black_disconnected = 0
    db.session.commit()

@socketio.on('touch')
def touch(data):
    game_id = session['game_id']
    piece = int(data['piece'])
    y = int(data['y'])
    x = int(data['x'])
    go = {}
    attack = {}
    blocklines = calculate_blocklines(game_id, opp=True)
    king_coordinates = get_king_coordinates(game_id, opp=False)
    _, attack_king_coord, attack_king_pieces = calculate_attacks(game_id, opp=True, king_coordinates=king_coordinates)
    checklines = calculate_checklines(game_id, attack_king_coord, attack_king_pieces, opp=True)
    go, attack = get_moves(game_id, x, y, piece, blocklines, checklines)
    socketio.emit('moves', data=(go, attack), room=session['sid'])

@socketio.on('go')
def go(data):
    game = Game.query.filter_by(id=session['game_id']).first()
    # Do this first, so that if the page is reaload, the move has alredy been switched
    # (better solution?)
    game.p1_move = not game.p1_move
    db.session.commit()
    game_id = session['game_id']
    piece = int(data['piece'])
    piece2 = int(data['piece2'])
    y = int(data['y'])
    x = int(data['x'])
    i = int(data['i'])
    j = int(data['j'])
    checklines = []
    castling = False
    en_passant = False
    promotion = False
    files = string.ascii_lowercase[0:8]
    rank = Rank.query.filter_by(game_id=game_id, number=i).first()
    if (piece > 7 and piece2 == 7) or (piece > 1 and piece < 6 and piece2 == 1):
        promotion = True
    if piece == 6 and piece2 == 4 and y == 8:
        castling = True
        rank.e = 0
        rank.g = 6
        rank.f = 4
        rank.h = 0
    elif piece == 6 and piece2 == 4 and y == 1:
        castling = True
        rank.a = 0
        rank.c = 6
        rank.d = 4
        rank.e = 0
    elif piece == 12 and piece2 == 10 and y == 8:
        castling = True
        rank.e = 0
        rank.g = 12
        rank.f = 10
        rank.h = 0
    elif piece == 12 and piece2 == 10 and y == 1:
        castling = True
        rank.a = 0
        rank.c = 12
        rank.d = 10
        rank.e = 0
    elif (piece == 1 or piece == 7) and piece2 == 0 and abs(j - y) == 1:
        en_passant = True
        setattr(rank, files[j-1], 0)
        setattr(rank, files[y-1], 0)
        rank_2 = Rank.query.filter_by(game_id=game_id, number=x).first()
        setattr(rank_2, files[y-1], piece)
    else:
        setattr(rank, files[j-1], 0)
        rank_2 = Rank.query.filter_by(game_id=game_id, number=x).first()
        setattr(rank_2, files[y-1], piece)
    db.session.commit()
    switch_en_passant(piece, i, x, y, game, game_id)
    #calculate this players attacks, defences and see if there is a check for the opponent
    king_coordinates = get_king_coordinates(game_id)
    all_attacks, attack_king_coord, attack_king_pieces = calculate_attacks(game_id, king_coordinates=king_coordinates)
    into_check = calculate_possible_checks(game_id)
    add_attacks_to_db(game_id, all_attacks)
    add_defences_to_db(game_id, into_check)
    check = check_if_check(game_id, all_attacks)
    if session['pieces'] == 0:
        socketio.emit('opp_move', {'i': i, 'j': j, 'x': x, 'y': y, 
                      'castling': castling, 'en_passant': en_passant, 'promotion': promotion, 'piece': piece,
                      'piece2': piece2}, room=game.black_sid)
    else:
        socketio.emit('opp_move', {'i': i, 'j': j, 'x': x, 'y': y,
                      'castling': castling, 'en_passant': en_passant, 'promotion': promotion, 'piece': piece,
                      'piece2': piece2}, room=game.white_sid)
    if check:
        checklines = calculate_checklines(game_id, attack_king_coord, attack_king_pieces)
    blocklines = calculate_blocklines(game_id)
    if session['pieces'] == 0:
        moving = check_can_move(game_id, game, blocklines=blocklines, checklines=checklines, pieces = 1)
        if not moving:
            # If not moving and check, emit checkmate and victory.
            if check:
                socketio.emit('checkmate', room=game.black_sid)
                socketio.emit('victory', room=game.white_sid)
                game.p2_checkmate = True
            # Else emit stalemate.
            else:
                socketio.emit('stalemate', room=game.black_sid)
                socketio.emit('stalemate', room=game.white_sid)
                game.stalemate = True
        else:
            socketio.emit('next_move', {'moving': moving, 'check': check}, room=game.black_sid)
            socketio.emit('switch_move', room=game.white_sid)
        if game.p2_check != check:
            game.p2_check = check
    else:
        moving = check_can_move(game_id, game, blocklines=blocklines, checklines=checklines, pieces = 0)
        if not moving:
            if check:
                socketio.emit('checkmate', room=game.white_sid)
                socketio.emit('victory', room=game.black_sid)
                game.p1_checkmate = True
            else:
                socketio.emit('stalemate', room=game.white_sid)
                socketio.emit('stalemate', room=game.black_sid)
                game.stalemate = True
        else:
            socketio.emit('next_move', {'moving': moving, 'check': check}, room=game.white_sid)
            socketio.emit('switch_move', room=game.black_sid)
        if game.p1_check != check:
            game.p1_check = check 
    if session['pieces'] == 0:
        disable_castling_white(i, j, game)
    else:
        disable_castling_black(i, j, game)
    db.session.commit()

@app.route("/game/<int:game_id>")
def game(game_id):
    # is this solution ok?
    try: 
        session['game_id']
    except KeyError:
        return redirect(url_for('index'))
    if session['game_id'] != game_id:
        return redirect(url_for('index'))
    rank={}
    for i in range (1, 9):
        rank[i] = Rank.query.with_entities(Rank.game_id, Rank.a, Rank.b, Rank.c, Rank.d, Rank.e, Rank.f,
                                        Rank.g, Rank.h).filter_by(game_id=game_id, number=i).first()   
    files = string.ascii_lowercase[0:8]
    moving = {}
    game = Game.query.filter_by(id=game_id).first()
    # game.white_sid can be removed
    king_coordinates = get_king_coordinates(game_id, opp=False)
    _, attack_king_coord, attack_king_pieces = calculate_attacks(game_id, opp=True, king_coordinates=king_coordinates)
    checklines = calculate_checklines(game_id, attack_king_coord, attack_king_pieces, opp=True)
    blocklines = calculate_blocklines(game_id, opp=True)
    if game.black_sid and game.white_sid:
        if session ['pieces'] == 0 and game.p1_move == 1:
            moving = check_can_move(game_id, game, blocklines=blocklines, checklines=checklines, pieces = 0)
        elif session ['pieces'] == 1 and game.p1_move == 0:
            moving = check_can_move(game_id, game, blocklines=blocklines, checklines=checklines, pieces = 1)
    response = make_response(render_template('game.html', files=files, rank=rank, moving=moving, 
                                             game_id=game_id, both_connected = game.both_connected,
                                             p1_move = game.p1_move, p1_check = game.p1_check,
                                             p2_check = game.p2_check, p1_checkmate = game.p1_checkmate,
                                             p2_checkmate = game.p2_checkmate, stalemate = game.stalemate))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route("/links")
def links():
    return render_template('links.html')




