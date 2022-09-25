import string
from flask import render_template, request, redirect, url_for, flash
from flask import session
from flask_session import Session
from chess.forms import CreateGameForm, JoinGameForm
from chess.models import Game
from chess import app, bcrypt, db, socketio
from random import getrandbits

@socketio.on('connect')
def connect():
    session['sid'] = request.sid
    print(session['sid'])

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
    game = Game.query.get(game_id)
    files = string.ascii_lowercase[0:8]
    return render_template('game.html', game=game, files=files)



