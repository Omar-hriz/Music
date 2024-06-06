import spotipy
from spotipy.oauth2 import SpotifyOAuth
import back.config as config
import back.db as db

# Configuration de l'authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                               client_secret=config.client_secret,
                                               redirect_uri=config.redirect_uri,
                                               scope="user-library-read"))


def get_audio_features(track_ids):
    audio_features = sp.audio_features(tracks=track_ids)
    return audio_features


def search_and_store_tracks(query, limit=100):
    results = sp.search(q=query, limit=limit, type='track')
    tracks_info = []
    track_ids = [track['id'] for track in results['tracks']['items']]

    audio_features = get_audio_features(track_ids)
    for track, features in zip(results['tracks']['items'], audio_features):
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artist': ", ".join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'duration_ms': track['duration_ms'],
            'popularity': track['popularity'],
            'explicit': track['explicit'],
            'danceability': features['danceability'],
            'energy': features['energy'],
            'key': features['key'],
            'loudness': features['loudness'],
            'mode': features['mode'],
            'speechiness': features['speechiness'],
            'acousticness': features['acousticness'],
            'instrumentalness': features['instrumentalness'],
            'liveness': features['liveness'],
            'valence': features['valence'],
            'tempo': features['tempo']
        }
        tracks_info.append(track_info)

    db.store_tracks_in_db(tracks_info)
