#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import collections
import collections.abc
from re import search
collections.Callable = collections.abc.Callable
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from model import Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO-Done: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO-Done: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  city_states=db.session.query(Venue.state,Venue.city).distinct().all()
  venues=[]
  for cs in city_states:
    venue_coll=db.session.query(Venue.id,Venue.name).filter(Venue.state==cs.state,Venue.city==cs.city).all()
    venue_data=[]
    venues.append({
            'city': cs.city,
            'state': cs.state,
            'venues': venue_data
        })
    for venue in venue_coll:
      venue_data.append({
        'id':venue.id,
        'name':venue.name,
        'num_upcoming_shows':len(Show.query.filter_by(venue_id = venue.id).all())
      })
  return render_template('pages/venues.html', areas=venues);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO-Done: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchStr=request.form.get('search_term')
  venue_coll=db.session.query(Venue.id,Venue.name).filter(Venue.name.ilike("%"+searchStr+"%")).all()
  response={}
  venue_data=[]
  response['count']=len(venue_coll)
  for vc in venue_coll:
    venue_data.append({
      'id':vc.id,
      'name':vc.name,
      'num_upcoming_shows':len(Show.query.filter_by(id=vc.id).all())
    })
  response['data']=venue_data

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO-Done: replace with real venue data from the venues table, using venue_id
  
  data={}
  venues=Venue.query.filter_by(id=venue_id).first()
  data["id"]= venues.id
  data["name"]=  venues.name
  data["genres"]=  [venues.genres]
  data["address"]=  [venues.address] 
  data["city"]=  venues.city
  data["state"]=  venues.state
  data["phone"]=  venues.phone
  data["website"]=  venues.website_link
  data["facebook_link"]=  venues.facebook_link
  data["seeking_talent"]=  venues.seeking_talent
  data["seeking_seeking_description"]=  venues.seeking_description
  data["image_link"]=  venues.image_link
  past_shows_data=[]
  for artist,show in db.session.query(Artist, Show).filter(Artist.id == Show.artist_id,Show.venue_id == venue_id,Show.start_time < datetime.now()).all():
    past_shows_data.append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.start_time)
    })
  data["past_shows"]=  past_shows_data
  upcoming_shows_data=[]
  for artist,show in db.session.query(Venue, Show).filter(Artist.id == Show.artist_id,Show.venue_id == venue_id,Show.start_time > datetime.now()).all():
    upcoming_shows_data.append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.start_time)
    })
  data["upcoming_shows"]=upcoming_shows_data
  data["past_shows_count"]=len(past_shows_data)
  data["upcoming_shows_count"]=len(upcoming_shows_data) 

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:   
    form = VenueForm(request.form)
    venue = Venue(name=form.name.data,
                  city=form.city.data,
                  state=form.state.data,
                  address=form.address.data,
                  phone=form.phone.data,                  
                  genres=form.genres.data,
                  facebook_link=form.facebook_link.data,
                  image_link=form.image_link.data,
                  website_link=form.website_link.data,
                  seeking_talent=False if form.seeking_talent.data is None else True,
                  seeking_description=form.seeking_description.data)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + form.name.data + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()

  # TODO-Done: insert form data as a new Venue record in the db, instead
  # TODO-Done: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO-Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO-Pending: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists_coll=Artist.query.all()
  artists_data=[]
  for artist in artists_coll:
    artists_data.append({
      'id':artist.id,
      'name':artist.name
    })
  return render_template('pages/artists.html', artists=artists_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  searchStr=request.form.get('search_term')
  artists_coll=db.session.query(Artist.id,Artist.name).filter(Artist.name.ilike("%"+searchStr+"%")).all()
  response={}
  artist_data=[]
  response['count']=len(artists_coll)
  for ac in artists_coll:
    artist_data.append({
      'id':ac.id,
      'name':ac.name,
      'num_upcoming_shows':len(Show.query.filter_by(id=ac.id).all())
    })
  response['data']=artist_data
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO-Done: replace with real artist data from the artist table, using artist_id
  data={}
  artists=Artist.query.filter_by(id=artist_id).first()
  data["id"]= artists.id
  data["name"]=  artists.name
  data["genres"]=  [artists.genres]
  data["city"]=  artists.city
  data["state"]=  artists.state
  data["phone"]=  artists.phone
  data["website"]=  artists.website_link
  data["facebook_link"]=  artists.facebook_link
  data["seeking_venue"]=  artists.seeking_venue
  data["seeking_seeking_description"]=  artists.seeking_description
  data["image_link"]=  artists.image_link
  past_shows_data=[]
  for venue,show in db.session.query(Venue, Show).filter(Venue.id == Show.venue_id,Show.artist_id == artist_id,Show.start_time < datetime.now()).all():
    past_shows_data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time)
    })
  data["past_shows"]=  past_shows_data
  upcoming_shows_data=[]
  for venue,show in db.session.query(Venue, Show).filter(Venue.id == Show.venue_id,Show.artist_id == artist_id,Show.start_time > datetime.now()).all():
    upcoming_shows_data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time)
    })
  data["upcoming_shows"]=upcoming_shows_data
  data["past_shows_count"]=len(past_shows_data)
  data["upcoming_shows_count"]=len(upcoming_shows_data) 

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Venue.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO-Done: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get_or_404(artist_id)

  try:
    form = ArtistForm(request.form)
    artist.name=form.name.data
    artist.genres=form.genres.data
    artist.city=form.city.data
    artist.state=form.state.data
    artist.phone=form.phone.data
    artist.website_link=form.website_link.data
    artist.facebook_link=form.facebook_link.data
    artist.seeking_venue=False if form.seeking_venue.data is None else True
    artist.seeking_description=form.seeking_description.data
    artist.image_link=form.image_link.data
    db.session.commit()
    flash('artist ' + form.name.data + ' was successfully updated!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. artist ' + form.name.data + ' could not be updated.')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO-Done: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get_or_404(venue_id)
  try:
    form = VenueForm(request.form)
    venue.name=form.name.data
    venue.genres=form.genres.data
    venue.address=form.address.data
    venue.city=form.city.data
    venue.state=form.state.data
    venue.phone=form.phone.data
    venue.website_link=form.website_link.data
    venue.facebook_link=form.facebook_link.data
    venue.seeking_talent=False if form.seeking_talent.data is None else True
    venue.seeking_description=form.seeking_description.data
    venue.image_link=form.image_link.data
    db.session.commit()
    flash('Venue ' + form.name.data + ' was successfully updated!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + form.name.data + ' could not be updated.')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:  
    form = ArtistForm(request.form)
    artist = Artist(name=form.name.data,
                  city=form.city.data,
                  state=form.state.data,
                  phone=form.phone.data,
                  genres=form.genres.data,
                  facebook_link=form.facebook_link.data,
                  image_link=form.image_link.data,
                  website_link=form.website_link.data,
                  seeking_venue=False if form.seeking_venue.data is None else True,
                  seeking_description=form.seeking_description.data)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + form.name.data + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()

  # called upon submitting the new artist listing form
  # TODO-Done: insert form data as a new Venue record in the db, instead
  # TODO-Done: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO-Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO-Done: replace with real venues data.
  shows=db.session.query(Show,Venue,Artist).join(Artist, Artist.id == Show.artist_id).join(Venue,Venue.id==Show.venue_id,).all()
  data=[]
  for show in shows:
    l_shows=show[0]
    l_venue=show[1]
    l_artist=show[2]
    data.append({
      "venue_id": l_venue.id,
      "venue_name": l_venue.name,
      "artist_id": l_artist.id,
      "artist_name": l_artist.name,
      "artist_image_link": l_artist.image_link,
      "start_time": str(l_shows.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO-Done: insert form data as a new Show record in the db, instead
  try:  
    form = ShowForm(request.form)
    show = Show(start_time=form.start_time.data,
                  venue_id=form.venue_id.data,
                  artist_id=form.artist_id.data)
    db.session.add(show)
    db.session.commit()
    flash('Show ' + str(form.start_time.data) + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show ' + str(form.start_time.data) + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO-Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
