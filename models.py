from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    group_name = db.Column(db.String(64), nullable=False, default="Cabritinhas")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    checkins = db.relationship('Checkin', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_description = db.Column(db.Text, nullable=True)
    checkin_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Checkin {self.id} by User {self.user_id}>'
    
    @property
    def formatted_date(self):
        return self.checkin_date.strftime('%d/%m/%Y')
    
    @property
    def formatted_time(self):
        return self.checkin_date.strftime('%H:%M')