from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Brew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))  # e.g. "2025-06-20"
    name = db.Column(db.String(100))
    roast = db.Column(db.String(20))
    method = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Brew {self.name} ({self.date})>'