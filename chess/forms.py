from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

class CreateGameForm(FlaskForm): 
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    pieces = SelectField('Pieces', choices=[('white', 'White'), ('black', 'Black'), ('random', 'Random')])
    cr_submit = SubmitField('Create a game')

class JoinGameForm(FlaskForm):
    game_id = StringField('Game ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    jn_submit = SubmitField('Join a game')

class ReturnGameForm(FlaskForm):
    game_id = StringField('Game ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pieces = SelectField('Pieces', choices=[('white', 'White'), ('black', 'Black')])
    rt_submit = SubmitField('Return to a game')