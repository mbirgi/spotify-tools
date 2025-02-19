import logging
import os

import spotipy
import spotipy.util

from dotenv import load_dotenv
load_dotenv()


def login(username='mbirgi', scope='user-library-read'):
    spotify_auth_params = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'scope': scope
    }
    try:
        token = spotipy.util.prompt_for_user_token(username, **spotify_auth_params)
    except:
        os.remove(f'.cache-{username}')
        token = spotipy.util.prompt_for_user_token(username, **spotify_auth_params)
    return spotipy.Spotify(auth=token)


def get_saved_albums(sp):
    album_results = sp.current_user_saved_albums()
    albums = album_results['items']
    while album_results['next']:
        album_results = sp.next(album_results)
        albums.extend(album_results['items'])
    return albums


def get_saved_tracks(sp):
    track_results = sp.current_user_saved_tracks()
    tracks = track_results['items']
    while track_results['next']:
        track_results = sp.next(track_results)
        tracks.extend(track_results['items'])
    return tracks


def get_playlists(sp):
    playlist_results = sp.current_user_playlists()
    playlists = playlist_results['items']
    while playlist_results['next']:
        playlist_results = sp.next(playlist_results)
        playlists.extend(playlist_results['items'])
    return playlists


def get_genres(track, spotipy_instance):
    artist_id = track['artists'][0]['id']
    artist = spotipy_instance.artist(artist_id)
    genres = artist['genres']
    return genres


def get_playlist_by_name(spotipy_instance, playlist_name, create_if_none=False):
    user_id = spotipy_instance.current_user()['id']
    results = spotipy_instance.user_playlists(user_id)
    user_playlists = results['items']
    while results['next']:
        results = spotipy_instance.next(results)
        user_playlists.extend(results['items'])
    playlist_id, is_new = None, None
    for list in user_playlists:
        if playlist_name == list['name']:
            playlist_id = list['id']
            is_new = False
            break
    if not playlist_id and create_if_none == True:
        new_playlist = spotipy_instance.user_playlist_create(user_id, name=playlist_name, public=False)
        playlist_id = new_playlist['id']
        is_new = True
    return playlist_id, is_new


def populate_playlist(sp, playlist_id, track_ids):
    # update playlist to the supplied tracks
    exit

def add_tracks(spotipy_instance, playlist_id, track_ids, skip_duplicates=True):
    # get existing tracks:
    results = spotipy_instance.playlist_tracks(playlist_id)  # TODO: get only IDs ('fields' filter)
    existing_tracks = results['items']
    while results['next']:
        results = spotipy_instance.next(results)
        existing_tracks.extend(results['items'])
    existing_track_ids = [item['track']['id'] for item in existing_tracks]
    logging.info(f"Playlist has {len(existing_track_ids)} existing tracks")
    logging.info(f"Skipping duplicates: {skip_duplicates}")
    if skip_duplicates:
        new_track_ids = [track_id for track_id in track_ids if track_id not in existing_track_ids]
    else:
        new_track_ids = track_ids
    logging.info(f"{len(new_track_ids)} tracks to be added")
    user_id = spotipy_instance.current_user()['id']
    if new_track_ids:
        limit = 100
        for i in range(0, len(new_track_ids), limit):
            ids = new_track_ids[i:(i + limit)]
            spotipy_instance.user_playlist_add_tracks(user_id, playlist_id, ids)
            logging.info(f"{len(ids)} tracks added")
        logging.info("OK")
        return
    logging.info("No tracks added")


def get_tracks_in_playlists(spotipy_instance, playlist_ids):
    tracks = set()    # TODO: make set for no dupes? CHECK!
    for pl_id in playlist_ids:
        # print(f"Getting tracks for playlist {pl_id}")
        results = spotipy_instance.playlist_tracks(pl_id)     # TODO: get only IDs ('fields' filter)
        pl_tracks = results['items']
        while results['next']:
            results = spotipy_instance.next(results)
            pl_tracks.extend(results['items'])
        tracks.update(pl_tracks)
    return tracks


def get_audio_features_for_tracks(spotipy_instance, track_ids):
    batch_size = 50
    # features = []
    # for i in range(0, len(track_ids), batch_size):
    #     results = spotipy_instance.audio_features(track_ids[i:i+batch_size])
    #     features.extend(results)
    # return features
    audio_features = []
    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i+batch_size]
        audio_features.extend(spotipy_instance.audio_features(batch))
    return audio_features

def get_audio_features(sp, track_ids):
    """
    Get audio features for a list of track IDs using Spotipy
    
    Args:
        sp: Authenticated Spotipy client
        track_ids (list): List of Spotify track IDs
    """
    # Spotipy automatically handles batching for us
    try:
        return sp.audio_features(track_ids)
    except spotipy.SpotifyException as e:
        print(f"Error: {str(e)}")
        return None
