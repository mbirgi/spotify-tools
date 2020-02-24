import json
import matplotlib.pyplot as plt
import numpy as np
import pprint
import sys

import spotify
import utils


def get_genres(track):
    artist_id = track['artists'][0]['id']
    artist = sp.artist(artist_id)
    genres = artist['genres']
    return genres

def print_tracks(tracks, verbose=False):
    for index, item in enumerate(tracks['items'], start=1):
        track = item['track']
        genres = get_genres(track)
        print(str(index) + ". " + utils.track_info(track), genres)
        if verbose:
            track_audio_features = sp.audio_features(track['id'])[0]
            utils.print_track_audio_features(track_audio_features)

def print_playlist_audio_features(tracks):
    tracklist = list(item['track']['id'] for item in tracks['items'])
    featureslist = sp.audio_features(tracklist)
    features = [
        'acousticness',
        'danceability',
        'instrumentalness',
        'liveness',
        'speechiness',
        'valence',
    ]
    labels = []
    feature_data = []
    for feature in features:
        feature_data.append(list(data[feature] for data in featureslist))
        labels.append(feature)
    plt.boxplot(feature_data, labels=labels)
    plt.xticks(rotation=15)
    plt.show()

def print_tempo_track_list(tracks):
    for index, item in enumerate(tracks['items'], start=1):
        track = item['track']
        print(str(index) + ". " + utils.track_info(track))


sp = spotify.login(scope='playlist-modify-private')

user = sp.current_user()
username = user['id']
displayName = user['display_name']

while True:
    print()
    print(">>> UserID " + user['id'] + " logged in: " + displayName)
    print()
    playlist_id = input("Enter playlist ID or URI: ")
    if (playlist_id == ''):
        playlist_id = 'spotify:user:mbirgi:playlist:3i527oOgyP8p5XuX54yCww'
    playlist = sp.user_playlist(username, playlist_id, fields="name, tracks, next")
    playlist_name = playlist['name']

    while True:
        print()
        print("Playlist:", playlist_name)
        print()
        print("1 - Short track list")
        print("2 - Verbose track list")
        print("3 - Playlist audio features")
        print("4 - Track tempos")
        print()
        print("0 - Change playlist")
        print()
        choice = input("Your choice: ")
        print()

        if choice == '0':
            break

        tracks = playlist['tracks']

        if choice in ('1', '2'):
            print_tracks(tracks, verbose=(choice == '2'))
            while tracks['next']:
                tracks = sp.next(tracks)
                print_tracks(tracks, verbose=(choice == '2'))

        if choice == '3':
            print_playlist_audio_features(tracks)

        if choice == '4':
            print_tempo_track_list(tracks)

        print()
        print("=========================================")
