"""Minimal flask app"""

import sys
import pprint
import sqlite3
import spotipy
import pandas as pd
from flask import Flask
from .models import DB
import spotipy.util as util
from decouple import config
from dotenv import load_dotenv
from .predict import predict_user

""""""""""""""""""""""""""""""""""
BREAK DOWN:
1. Classes of the five artist that match tempo 138.015
2.Add favorites
3.Search
4.Tracks
5. Delete a saved track

""""""""""""""""""""""""""""""""""


class artist_recs:

    def __init__(self, first, track_id, track_name):
        self.first = first
        self.track_id = track_id
        self.track_name = track_name

    def artist_track(self):
        return '{}{}'.format(self.first, self.track_id.track_name)

    artist_1 = artist_track('Coldplay', '4Y9lVjRD82aJOQ2v13UIoF',
                            'Viva La Vida - Live In Buenos Aires')
    artist_2 = artist_track('Of Montreal', '5V8co6Vavse9sOwIksEprS',
                            'Soft Music/Juno Portraits Of The Jovian Sky')
    artist_3 = artist_track('The Dangerous Summer', '0SYo2aRh2MYfBoJAFOYtNs',
                            'Fire')
    artist_4 = artist_track('Tiny Fireflies', '26hWxPFxRqeBh6lFp3waLF', '2040')
    artist_5 = artist_track('Oatmello', '3MCvwmA6zeYml0q7kQLgLu', 'Kombucha')

    artist_1.first = 'Coldplay'
    artist_1.track_id = '4Y9lVjRD82aJOQ2v13UIoF'
    artist_1.track_name = 'Viva La Vida - Live In Buenos Aires'

    artist_2.first = 'Of Montreal'
    artist_2.track_id = '5V8co6Vavse9sOwIksEprS'
    artist_2.track_name = 'Soft Music/Juno Portraits Of The Jovian Sky'

    artist_3.first = 'The Dangerous Summer'
    artist_3.track_id = '0SYo2aRh2MYfBoJAFOYtNs'
    artist_3.track_name = 'Fire'

    artist_4.first = 'Tiny Fireflies'
    artist_4.track_id = '26hWxPFxRqeBh6lFp3waLF'
    artist_4.track_name = '2040'

    artist_5.first = 'Oatmello'
    artist_5.track_id = '3MCvwmA6zeYml0q7kQLgLu'
    artist_5.track_name = 'Kombucha'

    print(artist_1.artist)


"""
This is code for our Spotify's API if we get there:
"""
#DB = SQLAlchemy()

#df = pd.read_csv('SpotifyAudioFeaturesApril2019.csv')

#conn = sqlite3.connect('spotify.db')

#df.to_sql('track_name', conn, if_exists='replace')

# "'''STRETCH GOAL"""
# @app.route('/go', methods=['GET', 'POST'])
# def go():
#    session.clear()
#    session['num_tracks'] = '50'  # number of tracks to grab
#    session['time_range'] = 'medium_term'  # time range of query:
# https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
#    base_url = spotify.AUTH_URL
#    response = make_response(redirect(base_url), 302)
#    return response


# class Track(DB.Model):
#    """Model for our track entry in our database"""
#    id = DB.Column(DB.music(5))

"""
ADD FAV.
"""

scope = 'user-library'

if len(sys.argv) > 2:
    username = sys.argv[1]
    tids = sys.argv[2:]
else:
    print("Usage: %s username track-id ..." % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.current_user_saved_tracks_add(tracks=tids)
    pprint.pprint(results)
else:
    print("Can't access token for:", username)

"""
SEARCH
"""

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Coldplay'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
result = sp.search(search_str)
pprint.pprint(result)

"""
TRACKS
"""
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 1:
    artist_name = ' '.join(sys.argv[1:])
    results = sp.search(q=artist_name, limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])

""""
Delete a saved track
""""
scope = 'user-library-modify'

if len(sys.argv) > 2:
    username = sys.argv[1]
    tids = sys.argv[2:]
else:
    print("Usage: %s username track-id ..." % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.current_user_saved_tracks_delete(tracks=tids)
    pprint.pprint(results)
else:
    print("Can't get token for", username)

# @app.route('/track_name', methods=['POST'])
# def song():
#    """Route for recommendations based on song selected."""

    # track_id = request.get_json(force=True)

    # get parameters:
    # use track_id
    # df = SELECT * FROM SpotifyAudioFeatures
    # WHERE tempo > 138.015
    # group by popularity

    # df = SELECT * from artist_name WHERE track_name == track_id
    # tempo = df['danceability']
    # energy = df['energy']

    # model
    # model = "some pickled model"

    # output
    # should be 30 reccomendations
    # recommendations = model.predict("parameters")
    # return recommendations
# @app.route('/mood')
# def mood():
#    """Route foor recommendations based on mood selected."""

#     mood=request.get_json(force = True)
#     recommendations=
