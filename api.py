import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup
import requests
import re
import time

from nltk.tokenize import sent_tokenize

print('Hi there! This script allows you to get the lyrics of the song you are currently playing on Spotify.\n:) \n')
time.sleep(2)
scope = 'user-read-currently-playing'
token = spotipy.util.prompt_for_user_token('31fh4k3mnjp7ikh4zzo6d5pacily',
                                                 'user-read-currently-playing',
                                                 '4d64ac6e2a274e38b601e7a4c1c7a1d2',
                                                 '46ae5d4d52cf4003a46f5316a68eef4b',
                                                 'http://127.0.0.1/callback')

if token:
    sp = spotipy.Spotify(auth=token)
    current_song = sp.currently_playing()
    duration = current_song['item']['duration_ms']*0.001
    print(f"Song Duration: {duration} seconds.")
    img = current_song['item']['album']['images'][1]['url']

    artist = current_song['item']['artists'][0]['name']
    artist = artist.capitalize()
    artist = artist.replace('&', 'and')
    name = current_song['item']['name']
    name = name.replace('Remastered', '')
    name = name.replace('-', '')
    name = name.strip()
    #print(name)
    name = name.replace('&', 'and')
    print(f'Artist: {artist}\nSong: {name}\n')
    time.sleep(2)
    name_song = ''
    for i in name:

        name_song_words = i.lower()
        name_song += name_song_words

else:
    print("There seems to be an issue.")


text_link = f'{artist} {name_song}'
text_link = re.sub('[^ A-Za-z0-9]+', '', text_link)
text_link = text_link.replace('  ', ' ')
text_link = text_link.replace(' ', '-')

#print(text_link)


try:
    link = f'https://genius.com/{text_link}-lyrics'
    #print(link)
    url = requests.get(link)
    soup = BeautifulSoup(url.content,'html.parser')
    match = soup.findAll(class_='lyrics')
    match = str(match)
    tags = re.compile(r'<[^>]+>')
    match = tags.sub('', match)
    match = match.replace('[', '')
    match = match.replace(']', '')
    length = match.count('\n')
    #print(length)
    if match == '':
        print('Lyrics not found!')
    else:
        print('Lyrics: ')
        print(match)
except Exception:
    print('There seems to be something wrong.')

