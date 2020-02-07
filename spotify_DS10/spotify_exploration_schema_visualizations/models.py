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

from __future__ import print_function
import base64
import json
import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn import preprocessing

try:
    import urllib.request
    import urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse


# Set up Spotify API base URL
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Set up authorization URL
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

# Client keys
CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']

"""
Server side parameters, which should be changed accordingly
in Spotify dev  account
 """
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8081
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


""""""""""""""""""""""""""""""""""
BREAK DOWN:
1. Classes of the five artist that match tempo 138.015
2.Add favorites
3.Search
4.Tracks
5. Delete a saved track
6. Spotify API 'Stretch Goal'
""""""""""""""""""""""""""""""""""


class artist_recs:

    """1. Classes of the five artist that match tempo 138.015"""


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


DB = SQLAlchemy()

df = pd.read_csv('SpotifyAudioFeaturesApril2019.csv')

conn = sqlite3.connect('spotify.db')

df.to_sql('track_name', conn, if_exists='replace')


@app.route('/go', methods=['GET', 'POST'])
def go():
    session.clear()
    session['num_tracks'] = '50'  # number of tracks to grab
    session['time_range'] = 'medium_term'  # time range of query:
# https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
    base_url = spotify.AUTH_URL
    response = make_response(redirect(base_url), 302)
    return response


 class Track(DB.Model):
    """Model for our track entry in our database"""
    id = DB.Column(DB.music(5))

"""
2. Add favorites
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
3. Search
"""

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Coldplay'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
result = sp.search(search_str)
pprint.pprint(result)

"""
4. Tracks
"""
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 1:
    artist_name = ' '.join(sys.argv[1:])
    results = sp.search(q=artist_name, limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])

""""
5. Delete a saved track
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

 @app.route('/track_name', methods=['POST'])
 def song():
    """Route for recommendations based on song selected."""

     track_id = request.get_json(force=True)

     get parameters:
     use track_id
     df = SELECT * FROM SpotifyAudioFeatures
     WHERE tempo > 138.015
     group by popularity

     df = SELECT * from artist_name WHERE track_name == track_id
     tempo = df['danceability']
     energy = df['energy']

     model
     model = "some pickled model"

     output
     should be 5 reccomendations
     recommendations = model.predict("parameters")
    return recommendations

 @app.route('/mood')
 def mood():
         """Route foor recommendations based on mood selected."""

     mood=request.get_json(force = True)

     # https://developer.spotify.com/web-api/authorization-guide/
     auth_query_parameters = {
         "response_type": "code",
         "redirect_uri": REDIRECT_URI,
         "scope": SCOPE,
         "client_id": CLIENT_ID
     }

     # Generate URL for Spotify API call
     URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                          for key, val in list(auth_query_parameters.items())])
     AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)


"""
6. Spotify API 'Stretch Goal'
This is code for our Spotify's API if we get there:
"""

     # Returns authorization header in URL, which allows request to API
     def authorize(auth_token):

         code_payload = {
             "grant_type": "authorization_code",
             "code": str(auth_token),
             "redirect_uri": REDIRECT_URI
         }

         base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
         headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

         post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

         # Return access token
         response_data = json.loads(post_request.text)
         access_token = response_data["access_token"]

         # use the access token to access Spotify API
         auth_header = {"Authorization": "Bearer {}".format(access_token)}
         return auth_header


     # https://developer.spotify.com/web-api/get-users-top-artists-and-tracks/
     def get_users_top(auth_header, t):
         if t not in ['artists', 'tracks']:
             print('invalid type')
             return None
         url = 'https://api.spotify.com/v1/me/top/tracks?limit=' + '50' + '&time_range=' + 'medium_term'
         r_tt = requests.get(url, headers=auth_header)
         tt_json = r_tt.json()
         track_list = []
         track_ids = []

         for x in range(0, tt_json['limit']):
             track_name = tt_json['items'][x]['name']
             track_id = tt_json['items'][x]['id']
             track_album = tt_json['items'][x]['album']['name']
             track_artist = tt_json['items'][x]['artists'][0]['name']

             track = {'name': track_name,
                      'artist': track_artist,
                      'album': track_album,
                      'id': track_id}

             track_list.append(track)
             track_ids.append(track_id)

         return track_list, track_ids


     # https://developer.spotify.com/web-api/track-endpoints/
     GET_TRACK_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'tracks')  # /<id>


     # https://developer.spotify.com/web-api/get-track/
     def get_track(track_id):
         url = "{}/{id}".format(GET_TRACK_ENDPOINT, id=track_id)
         resp = requests.get(url)
         return resp.json()


     # https://developer.spotify.com/web-api/get-several-tracks/
     def get_several_tracks(list_of_ids):
         url = "{}/?ids={ids}".format(GET_TRACK_ENDPOINT, ids=','.join(list_of_ids))
         resp = requests.get(url)
         return resp.json()


     # https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/
     # track_ids = list of track ids generated from 'get_users_top'
     def get_audio_features(auth_header, track_ids):

         GET_AUDIOFEAT_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'audio-features/?ids=')  # /<track id>

         url = GET_AUDIOFEAT_ENDPOINT  # generate URL to query track ids
         for id in track_ids:
             url = url + id + ','

         r_tt = requests.get(url, headers=auth_header)  # Get JSON of each track's audio features
         tt_json = r_tt.json()

         # Define which features you want to keep
         features = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                     'liveness', 'loudness', 'speechiness', 'tempo', 'mode',
                     'valence']

         # Convert results to dataframe
         df_trackfeat = pd.DataFrame(tt_json['audio_features'])
         df_trackfeat_matrix = df_trackfeat[features]

         # make weights, where ranking of most-played song receives higher weight
         # evenly spaced weights, 0-1; num = track limit given to Spotify
         weights = np.linspace(0.02, 1, num=50)
         weights = np.flip(weights, axis=0)  # change to descending order

         # Generate weighted average of audio features
         weighted_average = df_trackfeat_matrix.multiply(
             weights, axis=0).sum() * 10 / (len(df_trackfeat_matrix) / 2)

         # Connect to SQLite database & import as dataframe
         engine = create_engine('sqlite:///pitchfork_authors.db')
         connection = engine.connect()
         sql = "SELECT * FROM mytable"
         df = pd.read_sql(sql, connection)
         df = df.drop('index', axis=1)

         # 1. Make difference matrix
         df_difference = pd.DataFrame.copy(df.drop('author_fullname', axis=1))

         for feature in df_difference.columns:
             # absolute value of features
             df_difference[feature] = abs(df[feature] - weighted_average[feature])
             # 2. Scale features
             min_max_scaler = preprocessing.MinMaxScaler()
             df_difference[feature] = min_max_scaler.fit_transform(
                 df_difference[feature].values.reshape(-1, 1))
             # 3. Average each critic's feature differences from user's
         average_difference = df_difference.mean(axis=1)
         # 4. Take least-different critic ('best critic')
         best_critic = average_difference.idxmin()
         best_critic = df['author_fullname'].loc[best_critic]

         return best_critic
