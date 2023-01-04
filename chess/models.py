from email.policy import default
from chess import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    white_sid = db.Column(db.String(120))
    black_sid = db.Column(db.String(120))
    player_1 = db.Column(db.Boolean, default = False, nullable=False)
    p1_move = db.Column(db.Boolean, default = True, nullable=False)
    p1_check = db.Column(db.Boolean, default = False, nullable=False)
    p2_check = db.Column(db.Boolean, default = False, nullable=False)
    p1_checkmate = db.Column(db.Boolean, default = False, nullable=False)
    p2_checkmate = db.Column(db.Boolean, default = False, nullable=False)
    stalemate = db.Column(db.Boolean, default = False, nullable=False)
    white_king_castling = db.Column(db.Boolean, default = True, nullable=False)
    white_queen_castling = db.Column(db.Boolean, default = True, nullable=False)
    black_king_castling = db.Column(db.Boolean, default = True, nullable=False)
    black_queen_castling = db.Column(db.Boolean, default = True, nullable=False)
    white_en_passant = db.Column(db.Boolean, default = False, nullable=False)
    white_en_passant_y = db.Column(db.Integer)
    black_en_passant = db.Column(db.Boolean, default = False, nullable=False)
    black_en_passant_y = db.Column(db.Integer)
    both_connected = db.Column(db.Boolean, default = False, nullable=False)
    ranks = db.relationship('Rank', backref='game', lazy=True)

    def __repr__(self):
        return f"Game('{self.id}')"

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    a = db.Column(db.Integer, nullable=False)
    b = db.Column(db.Integer, nullable=False)
    c = db.Column(db.Integer, nullable=False)
    d = db.Column(db.Integer, nullable=False)
    e = db.Column(db.Integer, nullable=False)
    f = db.Column(db.Integer, nullable=False)
    g = db.Column(db.Integer, nullable=False)
    h = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Rank('Game {self.game_id}, number {self.number}:\
 {self.a}, {self.b}, {self.c}, {self.d}, {self.e}, {self.f}, {self.g}, {self.h}')"

class Defences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    a = db.Column(db.Boolean, default=False, nullable=False)
    b = db.Column(db.Boolean, default=False, nullable=False)
    c = db.Column(db.Boolean, default=False, nullable=False)
    d = db.Column(db.Boolean, default=False, nullable=False)
    e = db.Column(db.Boolean, default=False, nullable=False)
    f = db.Column(db.Boolean, default=False, nullable=False)
    g = db.Column(db.Boolean, default=False, nullable=False)
    h = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Defence White('Game {self.game_id}, number {self.number}:\
 {self.a}, {self.b}, {self.c}, {self.d}, {self.e}, {self.f}, {self.g}, {self.h}')"

class Attacks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    a = db.Column(db.Boolean, default=False, nullable=False)
    b = db.Column(db.Boolean, default=False, nullable=False)
    c = db.Column(db.Boolean, default=False, nullable=False)
    d = db.Column(db.Boolean, default=False, nullable=False)
    e = db.Column(db.Boolean, default=False, nullable=False)
    f = db.Column(db.Boolean, default=False, nullable=False)
    g = db.Column(db.Boolean, default=False, nullable=False)
    h = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Attacks('Game {self.game_id}, number {self.number}:\
 {self.a}, {self.b}, {self.c}, {self.d}, {self.e}, {self.f}, {self.g}, {self.h}')"