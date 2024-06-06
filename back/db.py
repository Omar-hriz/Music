import pymongo
import back.config as config

# Connexion à MongoDB
client = pymongo.MongoClient(config.mongo_uri)
db = client.music_db  # Nom de la base de données
songs_collection = db.songs  # Nom de la collection


def store_tracks_in_db(tracks_info):
    if tracks_info:
        result = songs_collection.insert_many(tracks_info)
        print(f"Inserted {len(result.inserted_ids)} tracks into MongoDB")
    else:
        print("No tracks to insert.")


def get_all_tracks():
    tracks = songs_collection.find()
    for track in tracks:
        print(f"Name: {track['name']}")
        print(f"Artist: {track['artist']}")
        print(f"Album: {track['album']}")
        print(f"Release Date: {track['release_date']}")
        print(f"Duration (ms): {track['duration_ms']}")
        print(f"Popularity: {track['popularity']}")
        print(f"Explicit: {track['explicit']}")
        print("---------------")
