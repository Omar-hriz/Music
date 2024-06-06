import spotipy
from spotipy.oauth2 import SpotifyOAuth
import back.config as config
import back.db as db

# Configuration de l'authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                               client_secret=config.client_secret,
                                               redirect_uri=config.redirect_uri,
                                               scope="user-library-read"))


def search_and_store_tracks(query, limit=50):
    results = sp.search(q=query, limit=limit, type='track')
    tracks_info = []
    for track in results['tracks']['items']:
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artist': ", ".join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'duration_ms': track['duration_ms'],
            'popularity': track['popularity'],
            'explicit': track['explicit']
        }
        tracks_info.append(track_info)

    db.store_tracks_in_db(tracks_info)