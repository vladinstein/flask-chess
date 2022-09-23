from chess import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    white_sid = db.Column(db.String(120))
    black_sid = db.Column(db.String(120))

    def __repr__(self):
        return f"Game('{self.id}')"