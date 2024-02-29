from bs4 import BeautifulSoup
from dataclasses import dataclass
import re

@dataclass
class PlaylistTrack:
    artist: str
    title: str
    link: str

    def to_tsv_line(self):
        return self.artist + '\t' + self.title + '\t' + self.link + '\n'

with open('karafan_playlist.html', 'r') as f:
    page = BeautifulSoup(f, 'html.parser')

playlist: list[PlaylistTrack]
playlist = []

items = page.find_all('ytd-playlist-panel-video-renderer')
for item in items:
    a = item.find_next('a')
    link = 'https://youtube.com' + a.attrs['href']
    title = item.css.select('#video-title')
    title = title[0].attrs['title']
    artist, title = title.split('-')
    artist, title = artist.strip(), title.strip()
    playlist.append(PlaylistTrack(artist, title, link))

with open('karafan_playlist.txt', 'a', encoding='utf-8') as f:
    f.writelines([line.to_tsv_line() for line in playlist])



print()
