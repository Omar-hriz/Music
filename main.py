from back.get_data import search_and_store_tracks
from back.db import get_all_tracks


search_query = 'top hits'  # Vous pouvez changer cette requête pour rechercher par genre, artiste, etc.
search_and_store_tracks(search_query)
print("Les chansons ont été insérées dans la base de données MongoDB.")
get_all_tracks()

# from back.db import create_users
# from back.db import assign_songs_to_users
# from back.db import get_all_users
#
# # Créer des utilisateurs
# create_users(10)  # Créez 10 utilisateurs
#
# # Assigner des chansons aux utilisateurs
# assign_songs_to_users(5)  # Assignez 5 chansons préférées à chaque utilisateur
#
# # Afficher tous les utilisateurs
# get_all_users()