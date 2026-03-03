from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Owner(db.Model):
    """Horse owner model"""
    __tablename__ = 'owners'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    horses = db.relationship('Horse', backref='owner', lazy=True)
    
    def __repr__(self):
        return f'<Owner {self.name}>'


class Horse(db.Model):
    """Horse model"""
    __tablename__ = 'horses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    rating = db.Column(db.Float, default=0.0, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    race_entries = db.relationship('RaceEntry', backref='horse', lazy=True)
    
    def __repr__(self):
        return f'<Horse {self.name}>'


class Jockey(db.Model):
    """Jockey model"""
    __tablename__ = 'jockeys'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    rating = db.Column(db.Float, default=0.0, nullable=False)
    race_entries = db.relationship('RaceEntry', backref='jockey', lazy=True)
    
    def __repr__(self):
        return f'<Jockey {self.name}>'


class Race(db.Model):
    """Race model"""
    __tablename__ = 'races'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    entries = db.relationship('RaceEntry', backref='race', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Race {self.date}>'


class RaceEntry(db.Model):
    """Many-to-many relationship: Race - Jockey - Horse with placement"""
    __tablename__ = 'race_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), nullable=False)
    jockey_id = db.Column(db.Integer, db.ForeignKey('jockeys.id'), nullable=False)
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'), nullable=False)
    place = db.Column(db.Integer, nullable=True)  # None if race not finished
    
    __table_args__ = (
        db.UniqueConstraint('race_id', 'jockey_id', 'horse_id', name='unique_race_entry'),
    )
    
    def __repr__(self):
        return f'<RaceEntry race:{self.race_id} jockey:{self.jockey_id} horse:{self.horse_id}>'
