import spotipy.util as util
import pickle
import json
import spec
import requests


#These do not have calls
class spotify:
    def __init__(self):
        self.token = ''
        self.__username = ''
        self.__scope = 'playlist-modify-private user-modify-playback-state user-library-modify user-read-currently-playing user-read-playback-state app-remote-control user-library-read'
        self.head = {
            'Accept' : 'application/json',
            'Content-Type':'application/json',
            'Authroization':'Bearer {}'.format(self.token)
        }
        self.__playlists = []

    def get_token(self):
        self.__token = util.prompt_for_user_token(self.__username, self.__scope,client_id='7c7b8350ae144e2c8baa92f61150acda',client_secret='88f140e2bab74353b6337b976b3eeb52',redirect_uri='http://localhost:8888/callback')

    
    def add_username(self):
        while True:
            try:
                self.__username = str(input("Input you spotify username: "))
                self.__token = util.prompt_for_user_token(self.__username, self.__scope,client_id='7c7b8350ae144e2c8baa92f61150acda',client_secret='88f140e2bab74353b6337b976b3eeb52',redirect_uri='http://localhost:8888/callback')
                return
            except:
                print ("Wrong username")
    
    def get_head(self):
        self.head = {
            'Accept' : 'application/json',
            'Content-Type':'application/json',
            'Authroization':'Bearer {}'.format(self.token)
        }
        return self.head


def get_token(location):
    try:
        location = "{}/spotify.DAT".format(location)
        with open(location, 'rb') as fh:
            spotify_handle = pickle.load(fh)
            spotify_handle.get_token()
            return spotify_handle
    except:
        location = "{}/spotify.DAT".format(location)
        with open(location, 'wb') as fh:
            spotify_handle = spotify()
            spotify_handle.add_username()
            return spotify_handle

#These have a call
def skip_track(location, text):
    spotify_handle = get_token(location)
    head = spotify_handle.get_head()
    url = 'https://api.spotify.com/v1/me/player/next'
    requests.post(url, headers=head)

def previous_track(location, text):
    spotify_handle = get_token(location)
    head = spotify_handle.get_head()
    url = 'https://api.spotify.com/v1/me/player/previous'
    requests.post(url, headers=head)
    
def set_volume(location, text):
    spotify_handle = get_token(location)
    head = spotify_handle.get_head()
    if 'lower' in text:
        volume = '30'
    if 'higher' in text:
        volume = '75'
    if 'medium' in text:
        volume = '50'
    if 'full' in text:
        volume = '100'
    if 'off' in text:
        volume = '0'
    url = 'https://api.spotify.com/v1/me/player/volume?volume_percent={}'.format(volume)
    requests.post(url, headers=head)

def get_playlists(location, text):
    url = 'https://api.spotify.com/v1/me/playlists'
    spotify_handle = get_token(location)
    head = {
        'Authorization' : 'Bearer {}'.format(spotify_handle.token)
    }
    playlists = requests.get(url, headers=head)
    info = playlists.json()
    playlists = []
    for i in range(len(info['items'])):
        name = info['items'][i]['name']
        uri = info['items'][i]['uri']
        playlists.append([name, uri])
    return playlists

def get_album(location, text):
    artist = str(input("Input Artist: "))
    url = 'https://api.spotify.com/v1/search?q={}&type=album'.format(artist)
    spotify_handle = get_token(location)
    head = {
        'Authroization':'Bearer {}'.format(spotify_handle.token)
    }
    albums = requests.get(url, headers=head)
    info = albums.json()
    albums = []
    for i in range(len(info['albums'])):
        artist = info['albums']['items'][i]['artists'][0]['name']
        album_name = info['albums']['items'][i]['name']
        album_uri = info['albums']['items'][i]['uri']
        albums.append([artist, album_name, album_uri]) 
    return albums  

def pause_play(location, text):
    spotify_handle = get_token(location)
    head = spotify_handle.get_head()
    url = 'https://api.spotify.com/v1/me/player/play'
    requests.post(url, headers=head)


#Not used directly
def start_playback(location, device, context):
    spotify_handle = get_token(location)
    head = spotify_handle.get_head()
    url = ' https://api.spotify.com/v1/me/player/play'
    data = {'context_uri':['{}'.format(context)], 'device_ids':['{}'.format(device)]}
    requests.put(url, data=json.dumps(data), headers=head)

def change_device(location, device):
    spotify_handle = get_token(location)
    head = spotify_handle.get_head()
    url =  'https://api.spotify.com/v1/me/player'
    data = { "device_ids": ["{}".format(device)] }
    requests.put(url, data=json.dumps(data), headers=head)

def devices(location, text):
    spotify_handle = get_token(location)
    url = 'https://api.spotify.com/v1/me/player/devices'
    head = {
        'Authorization' : 'Bearer {}'.format(spotify_handle.token)
    }
    devices = requests.get(url, headers=head)
    info = devices.json()
    devices_info = []
    for i in range(len(info['devices'])):
        device_id = info['devices'][i]['id']
        name = info['devices'][i]['name']
        devices_info.append([name, device_id])
    return devices_info
        
       




