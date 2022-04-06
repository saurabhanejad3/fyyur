from app import db
#----------------------------------------------------------------------------#
# Venue Model.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    show = db.relationship('Show', backref=db.backref('Venue',lazy=True))
    
    def __repr__(self):
      return f'Venue {self.id}: {self.name}'

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    show = db.relationship('Show', backref=db.backref('Artist',lazy=True))
   
    def __repr__(self): return f'Artist {self.id}: {self.name}'

class Show(db.Model):
    __tablename__ = 'shows'

    id=db.Column(db.Integer, primary_key=True)
    start_time=db.Column(db.DateTime, nullable=False)
    artist_id=db.Column(db.Integer, db.ForeignKey('artists.id'))
    venue_id=db.Column(db.Integer, db.ForeignKey('venues.id'))

    def __repr__(self):
      return f'shows {self.id}: {self.start_time}'