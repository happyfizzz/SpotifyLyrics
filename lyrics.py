import re
import time

import requests
import spotipy
from bs4 import BeautifulSoup
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

# print('Hi there! This script allows you to get the lyrics of the song you are currently playing on Spotify.\n:) \n')

time.sleep(1)
scope = 'user-read-currently-playing'
# SPOTIFY TOKEN
token = spotipy.util.prompt_for_user_token('SPOTIFY USERNAME',
                                           'user-read-currently-playing',
                                           'CLIENT ID',
                                           'CLIENT SECRET',
                                           'REDIRECT URI')

try:
    if token:
        sp = spotipy.Spotify(auth=token)
        current_song = sp.currently_playing()
        duration = current_song['item']['duration_ms'] * 0.001
        # print(f"Song Duration: {duration} seconds.")
        img = current_song['item']['album']['images'][1]['url']

        artist = current_song['item']['artists'][0]['name']
        artist = artist.capitalize()
        artist = artist.replace('&', 'and')
        name = current_song['item']['name']
        name = name.replace('Remastered', '')
        name = name.replace('-', '')
        name = name.strip()
        # print(name)
        name = name.replace('&', 'and')
        # print(f'Artist: {artist}\nSong: {name}\n')
        time.sleep(1)
        name_song = ''
        for i in name:
            name_song_words = i.lower()
            name_song += name_song_words

except:
    print('There seems to be an issue to get that song.')

text_link = f'{artist} {name_song}'
text_link = re.sub('[^ A-Za-z0-9]+', '', text_link)
text_link = text_link.replace('  ', ' ')
text_link = text_link.replace(' ', '-')

# print(text_link)

# SEARCH FOR THE LYRICS ON GENIUS.
try:
    link = f'https://genius.com/{text_link}-lyrics'
    # print(link)
    url = requests.get(link)
    soup = BeautifulSoup(url.content, 'html.parser')
    match = soup.findAll(class_='lyrics')
    match = str(match)
    tags = re.compile(r'<[^>]+>')
    match = tags.sub('', match)
    match = match.replace('[', '')
    match = match.replace(']', '')
    length = match.count('\n')
    # print(length)
    words_to_print = duration // length
    # print(words_to_print)
    if match == '':
        print('Lyrics not found!')
    else:
        print('Lyrics: ')
        # thumbnail = io.show()
        '''for letter in match:
            sys.stdout.write(letter)
            time.sleep(0.035*words_to_print)
            sys.stdout.flush()
            time.sleep(0.005)'''

except Exception:
    print('There seems to be something wrong.')

# PRINT OUT THE LYRICS USING KIVY APP 
class TestScreen(Label):

    def __init__(self, string, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.font_size = 25
        self.font_name = 'C:\\Users\\BB\\Desktop\\light.ttf'
        self.string = string
        self.typewriter = Clock.create_trigger(self.typeit, 0.035 * words_to_print)
        time.sleep(0.005)
        self.typewriter()

    def typeit(self, dt):
        self.text += self.string[0]
        self.string = self.string[1:]
        if len(self.string) > 0:
            self.typewriter()


# ARTIST NAME AND OTHER INFO IN THE APP
class LyricsApp(App):
    def build(self):
        try:

            self.root = FloatLayout()
            self.song_info = Label(text=f'[color=DB7093]Artist: [/color] {artist}\n[color=DB7093]Song: [/color]{name}',
                                   markup=True, font_size='20sp',
                                   font_name='C:\\Users\\BB\\Desktop\\light.ttf', size_hint=(1.0, 1.0), halign="left",
                                   valign="top")
            self.song_info.bind(size=self.song_info.setter('text_size'))
            self.anim_song = Animation(t='in_sine', opacity=0, duration=duration)
            self.anim_song.start(self.song_info)
            self.root.add_widget(self.song_info)

            self.text = Label(text='[size=45]Spotify[/size][u][b][color=C71585]Lyrics[/color][/b][/u]', halign="right",
                              valign="bottom",
                              markup=True, font_size='40sp',
                              font_name='C:\\Users\\BB\\Desktop\\light.ttf')
            self.text.bind(size=self.text.setter('text_size'))
            self.anim = Animation(t='in_sine', opacity=0, duration=10)
            self.anim.start(self.text)
            self.root.add_widget(self.text)
            self.root.add_widget(TestScreen(match))
            return self.root
        except:
            self.root = FloatLayout()
            self.text = Label(text="Couldn't get the lyrics. Please try some other song. ")
            self.root.add_widget(self.text)


if __name__ == '__main__':
    LyricsApp().run()

