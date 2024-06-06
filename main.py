from back.get_data import search_and_store_tracks
from  back.db import get_all_tracks


search_query = 'top hits'  # Vous pouvez changer cette requête pour rechercher par genre, artiste, etc.
search_and_store_tracks(search_query)
print("Les chansons ont été insérées dans la base de données MongoDB.")
get_all_tracks()

