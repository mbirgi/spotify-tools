import os
import sys
import json
import pprint

import spotify
import utils


query = {
    'seed_genres': ['funk', 'soul'],
    'limit': 20,
    'country': 'CH',
}

track_attributes = {
    'target_tempo': 140.0,
    'min_danceability': 0.66,
    # 'max_liveness': 0.33,
    # 'max_speechiness': 0.33,
    # 'max_instrumentalness': 0.33,
    'max_acousticness': 0.33,
    # 'target_time_signature': 4,
    # 'min_valence': 0.5,
}

sp = spotify.login(scope='playlist-modify-private')

user = sp.current_user()
displayName = user['display_name']

while True:
    print('\n>>> Welcome, ' + displayName + '!')
    results = sp.recommendation_genre_seeds()
    print("\nThese are the available genre seeds:\n")
    utils.colprint(results['genres'])
    response = input("\nEnter up to 5 seed genres (default = "
            + ', '.join(query['seed_genres'])
            + "): ")
    if response:
        query['seed_genres'] = [genre.strip() for genre in response.split(',')]
    print("\n>>> Seed genres: " + str(query['seed_genres']))
    response = input("\nEnter target BPM (default = "
            + str(track_attributes['target_tempo']) + "): ")
    if response:
        track_attributes['target_tempo'] = float(response)
    print("\n>>> target BPM: " + str(track_attributes['target_tempo']))
    results = sp.recommendations(**query, **track_attributes)
    tracks = results['tracks']
    print()
    utils.print_track_list(tracks)
    response = input("\nSave playlist? (y/N): ")
    if response.lower() == 'y':
        playlist_name = (str(track_attributes['target_tempo'])
                + " BPM " + ', '.join(query['seed_genres']).title())
        response = input("\nEnter playlist name (default = " + playlist_name + "): ")
        if response:
            playlist_name = response
        description = "Created with BPMPlaylist.py"
        playlist = sp.user_playlist_create(user['id'], playlist_name,
            public=False, description=description)
        track_ids = utils.get_track_ids(tracks)
        sp.user_playlist_add_tracks(user['id'], playlist['id'], track_ids)
        print("\n>>> Playlist saved: " + playlist['name'])
    else:
        print("\n>>> Playlist NOT saved")
    print("\n=========================================")
