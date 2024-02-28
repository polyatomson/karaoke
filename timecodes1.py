import re
from dataclasses import dataclass

@dataclass
class Track:
    link: str
    song: str
    artist: str

    def to_tsv_line(self):
        return  self.artist + '\t' + self.song + '\t' + self.link


with open('karaoke1.txt', 'r', encoding='utf-8') as f:
    dat = f.readlines()
    common_link = dat[0].strip()
    dat = dat[1:]

def convert_minutes_to_seconds(minutes: str):
    splitted = minutes.split(':')
    if len(splitted) == 2:
        minutes, seconds = splitted
        return int(minutes)*60 + int(seconds)
    elif len(splitted) == 3:
        hours, minutes, seconds = splitted
        return int(hours)*3600 + int(minutes)*60 + int(seconds)
    else:
        print()

tracks = list()
for line in dat:
    parsed = re.search('(.+?) ([0-9\:]+)', line)
    time = parsed.group(2).strip()
    time_seconds = convert_minutes_to_seconds(time)
    name = parsed.group(1).strip()
    artist, song = name.rsplit('-', 1)
    artist = artist.strip()
    song = song.strip()
    link = common_link + str(time_seconds)
    tracks.append(Track(link, song, artist))

with open('catalogue1.tsv', 'a', encoding='utf-8') as f:
    for track in tracks:
        f.write(track.to_tsv_line() + '\n')

    
