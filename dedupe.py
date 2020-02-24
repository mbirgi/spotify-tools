import os
import sys
import json
import pprint

import spotify
import utils


sp = spotify.login(scope='playlist-modify-private')

if sp:
    username = sp.me()['id']
    print("\n>>> User logged in: " + sp.me()['display_name'] + "\n")

while True:
    playlist_id = input("Enter playlist ID or URI to deduplicate: ")
    results = sp.user_playlist(username, playlist_id)
    snapshot_id = results['snapshot_id']
    paged_tracks = results['tracks']
    all_tracks = []
    for item in paged_tracks['items']:
        all_tracks.append(utils.get_track(item))
    while paged_tracks['next']:
        paged_tracks = sp.next(paged_tracks)
        for item in paged_tracks['items']:
            all_tracks.append(utils.get_track(item))
    print("These are the tracks of the selected playlist:\n")
    utils.show_tracks(all_tracks)

    unique_tracks = []
    duplicate_tracks = []
    index = 0
    for track in all_tracks:
        if track in unique_tracks:
            track['pos'] = index
            duplicate_tracks.append(track)
        else:
            unique_tracks.append(track)
        index += 1

    if len(duplicate_tracks) == 0:
        print("\n No duplicates found\n")
    else:
        print("\nThese tracks are duplicates and will be deleted:\n")
        utils.show_tracks(duplicate_tracks)
        doit = input("\nContinue? [y/N]: ")
        if doit.lower() == 'y':
            tracks_to_delete = []
            for track in duplicate_tracks:
                tracks_to_delete.append({
                    'uri': track['id'],
                    'positions': [track['pos']]
                })
            sp.user_playlist_remove_specific_occurrences_of_tracks(
                username,
                playlist_id,
                tracks_to_delete,
                snapshot_id
            )
            print("\nDuplicate tracks deleted\n")
