import datetime
import json
import os


def timestamp():
    timestamp = datetime.datetime.now().isoformat().split('.')[0].replace(':', '-').replace('T', '-')
    return timestamp


def show_tracks(tracks):
    for index, track in enumerate(tracks, start=1):
        line = str(index) + ". " + track['info']
        if 'pos' in track:
            line += " (pos: " + str(track['pos'] + 1) + ")"
        print(line)


def get_track(item):
    track = item['track']
    id = track['id']
    info = track_info(track)
    return {'id': id, 'info': info}


def print_track_list(tracks, verbose=False):
    for index, track in enumerate(tracks, start=1):
        print(str(index) + ". " + track_info(track))
        if verbose:
            print("\tid: " + track["id"])
            print("\tpopularity: " + str(track["popularity"]))
            print("\talbum: " + track["album"]["name"])


def print_track_audio_features(track_audio_features):
    interesting_features = (
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
    )
    track_audio_features_concentrated = {
        k: track_audio_features[k] for k in interesting_features
    }
    print(json.dumps(track_audio_features_concentrated,
                     sort_keys=False, indent=4))


def get_tracks_from_response(response):
    track_results = response['tracks']
    tracks = []
    for item in track_results['items']:
        track = item['track']
        tracks.append(track)
    return tracks


def get_track_ids(tracks):
    ids = []
    for track in tracks:
        ids.append(track['id'])
    return ids


def track_info(track):
    track_name = track['name']
    artists = track['artists']
    artist_names = (artist['name'] for artist in artists)
    return (track_name + "  //  "
            + ", ".join(artist_names))


def colprint(list_to_print):
    screen_width = int(os.popen('stty size', 'r').read().split()[1])
    col_width = len(max(list_to_print, key=len)) + 2
    num_cols = (screen_width - 4) // col_width
    num_lines = (len(list_to_print) // num_cols
                 + (len(list_to_print) % num_cols != 0))
    lines = []
    fmt_str = '{:<' + str(col_width) + '}'
    for line_index in range(num_lines):
        line = ""
        for col_index in range(num_cols):
            item_index = line_index * num_cols + col_index
            if item_index < len(list_to_print):
                item = list_to_print[item_index]
            else:
                break
            line += fmt_str.format(item)
        lines.append(line)
    print('\n'.join(lines))
