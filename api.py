import spotipy
from bs4 import BeautifulSoup
import requests
import re
import time
from skimage import io
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock


#print('Hi there! This script allows you to get the lyrics of the song you are currently playing on Spotify.\n:) \n')
time.sleep(1)
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
    #print(f"Song Duration: {duration} seconds.")
    img = current_song['item']['album']['images'][1]['url']

    io.imshow(io.imread(str(img)))

    artist = current_song['item']['artists'][0]['name']
    artist = artist.capitalize()
    artist = artist.replace('&', 'and')
    name = current_song['item']['name']
    name = name.replace('Remastered', '')
    name = name.replace('-', '')
    name = name.strip()
    #print(name)
    name = name.replace('&', 'and')
    #print(f'Artist: {artist}\nSong: {name}\n')
    time.sleep(1)
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
    soup = BeautifulSoup(url.content, 'html.parser')
    match = soup.findAll(class_='lyrics')
    match = str(match)
    tags = re.compile(r'<[^>]+>')
    match = tags.sub('', match)
    match = match.replace('[', '')
    match = match.replace(']', '')
    length = match.count('\n')
    #print(length)
    words_to_print = duration//length
    #print(words_to_print)
    if match == '':
        print('Lyrics not found!')
    else:
        print('Lyrics: ')
        #thumbnail = io.show()
        '''for letter in match:
            sys.stdout.write(letter)
            time.sleep(0.035*words_to_print)
            sys.stdout.flush()
            time.sleep(0.005)'''

except Exception:
    print('There seems to be something wrong.')

class TestScreen(Label):

    def __init__(self, string, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.font_size = 25
        self.font_name = 'C:\\Users\\BB\\Desktop\\font_new.ttf'
        self.string = string
        self.typewriter = Clock.create_trigger(self.typeit, 0.035*words_to_print)
        time.sleep(0.005)
        self.typewriter()

    def typeit(self, dt):
        self.text += self.string[0]
        self.string = self.string[1:]
        if len(self.string) > 0:
            self.typewriter()

class LyricsApp(App):
    def build(self):

        self.root = FloatLayout()
        self.song_info = Label(text=f'[color=DB7093]Artist: [/color] {artist}\n[color=DB7093]Song: [/color]{name}',
                     markup=True, font_size='20sp',
                     font_name='C:\\Users\\BB\\Desktop\\font_new.ttf', size_hint=(1.0, 1.0), halign="left", valign="top")
        self.song_info.bind(size=self.song_info.setter('text_size'))
        self.anim_song = Animation(t='in_sine', opacity=0, duration=duration)
        self.anim_song.start(self.song_info)
        self.root.add_widget(self.song_info)

        self.text = Label(text='[size=45]Spotify[/size][u][b][color=C71585]Lyrics[/color][/b][/u]', halign="right", valign="bottom",
                     markup=True, font_size='40sp',
                     font_name='C:\\Users\\BB\\Desktop\\font_new.ttf')
        self.text.bind(size=self.text.setter('text_size'))
        self.anim = Animation(t='in_sine', opacity=0, duration=10)
        self.anim.start(self.text)
        self.root.add_widget(self.text)

        self.root.add_widget(TestScreen(match))

        return self.root

if __name__ == '__main__':
    LyricsApp().run()
