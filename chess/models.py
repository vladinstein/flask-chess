from chess import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    white_sid = db.Column(db.String(120))
    black_sid = db.Column(db.String(120))
    player_1 = db.Column(db.Boolean, default = False, nullable=False)

    def __repr__(self):
        return f"Game('{self.id}')"