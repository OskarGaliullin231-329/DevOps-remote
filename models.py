from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# the models used by the application are now a direct reflection of the
# tables created by `db/init_db.sql`.  column names are chosen so that
# they match the SQL script exactly; helper properties are provided for
# backwards compatibility with some of the original code.

db = SQLAlchemy()


class Host(db.Model):
    """Application owner/host model corresponding to the ``hosts`` table.

    This table stores ``host_name`` and ``surname`` separately.  The
    ``name`` property returns the two concatenated with a space so the
    rest of the app can continue using ``host.name`` as before.
    """
    __tablename__ = 'hosts'
    
    id = db.Column(db.Integer, primary_key=True)
    host_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    
    horses = db.relationship('Horse', backref='host', lazy=True)
    
    @property
    def name(self):
        parts = [self.host_name or '']
        if self.surname:
            parts.append(self.surname)
        return ' '.join(p for p in parts if p).strip()
    
    def __repr__(self):
        return f'<Host {self.name}>'


class Horse(db.Model):
    """Horse model corresponding to the ``horses`` table."""
    __tablename__ = 'horses'
    
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'), nullable=False)
    horse_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer)
    
    results = db.relationship('RaceResult', backref='horse', lazy=True)
    
    @property
    def name(self):
        return self.horse_name
    
    def __repr__(self):
        return f'<Horse {self.horse_name}>'


class Jockey(db.Model):
    """Jockey model corresponding to the ``jockeys`` table."""
    __tablename__ = 'jockeys'
    
    id = db.Column(db.Integer, primary_key=True)
    jockey_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer)
    
    results = db.relationship('RaceResult', backref='jockey', lazy=True)
    
    @property
    def name(self):
        return self.jockey_name
    
    def __repr__(self):
        return f'<Jockey {self.jockey_name}>'


class Race(db.Model):
    """Race model corresponding to the ``races`` table."""
    __tablename__ = 'races'
    
    id = db.Column(db.Integer, primary_key=True)
    race_date = db.Column(db.Date, nullable=False)
    
    results = db.relationship('RaceResult', backref='race', lazy=True, cascade='all, delete-orphan')
    
    @property
    def date(self):
        # keep compatibility with existing templates that expect ``date``
        # to be a datetime-like object; convert the stored date to a
        # datetime at midnight.
        return datetime(self.race_date.year, self.race_date.month, self.race_date.day)
    
    def __repr__(self):
        return f'<Race {self.race_date}>'


class RaceResult(db.Model):
    """Mapping of horses and jockeys to races (``races_results`` table)."""
    __tablename__ = 'races_results'
    
    id = db.Column(db.Integer, primary_key=True)
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'), nullable=False)
    jockey_id = db.Column(db.Integer, db.ForeignKey('jockeys.id'), nullable=False)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), nullable=False)
    place = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f'<RaceResult race:{self.race_id} jockey:{self.jockey_id} horse:{self.horse_id}>'
