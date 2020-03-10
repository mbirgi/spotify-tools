import spotify
import utils
import json
import os

sp = spotify.login(scope='playlist-modify-private')
results = sp.current_user_playlists()
playlists = results['items']
while results['next']:
    results = sp.next(results)
    playlists.extend(results['items'])
folder = 'data'
filename = f'playlists_{utils.timestamp()}.json'
if not os.path.exists(folder):
    os.mkdir(folder)
with open(os.path.join(folder, filename), 'w', encoding='utf-8') as f:
    json.dump(playlists, f, ensure_ascii=False, indent=4)
