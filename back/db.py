import pymongo
import back.config as config
import random
from pymongo import MongoClient


# Connexion à MongoDB
client = pymongo.MongoClient(config.mongo_uri)
db = client.music_db  # Nom de la base de données
songs_collection = db.songs  # Nom de la collection
users_collection = db.users  # Nom de la collection des utilisateurs


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


def create_users(num_users):
    users = []
    for i in range(num_users):
        user = {
            'user_id': i,
            'name': f'User{i}',
            'favorite_songs': []
        }
        users.append(user)

    users_collection.insert_many(users)
    print(f"Created {num_users} users.")


def assign_songs_to_users(num_songs_per_user):
    users = list(users_collection.find())
    all_song_ids = [song['id'] for song in songs_collection.find()]

    for user in users:
        favorite_songs = random.sample(all_song_ids, num_songs_per_user)
        users_collection.update_one({'user_id': user['user_id']}, {'set': {'favorite_songs': favorite_songs}})

    print(f"Assigned {num_songs_per_user} songs to each user.")


def get_all_users():
    users = users_collection.find()
    for user in users:
        print(f"User ID: {user['user_id']}")
        print(f"Name: {user['name']}")
        print(f"Favorite Songs: {user['favorite_songs']}")
        print("---------------")





