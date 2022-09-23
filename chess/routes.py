from flask import render_template, redirect, url_for, flash
from chess.forms import CreateGameForm, JoinGameForm
from chess.models import Game
from chess import app, bcrypt, db

@app.route('/', methods=['GET', 'POST'])
def index():
    cr_form = CreateGameForm()
    jn_form = JoinGameForm()
    if cr_form.cr_submit.data and cr_form.validate():
        hashed_password = bcrypt.generate_password_hash(cr_form.password.data).decode('utf-8')
        game = Game(password=hashed_password)
        db.session.add(game)
        db.session.commit()
        flash('You have created a game. Send the ID of your game to your opponent and wait for him\
              to connect.', 'success')
        return redirect(url_for('game'))
    elif jn_form.jn_submit.data and jn_form.validate():
        flash('You have connected to the game.', 'success')
        return redirect(url_for('game'))        
    return render_template('index.html', cr_form=cr_form, jn_form=jn_form)

@app.route('/game')
def game():
    return render_template('game.html')


