import psycopg2
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class Song:
    song: str
    artist: str
    link: str
    origin: str
    in_use: bool
    voice: Optional[bool]
    views: int = 0

def import_sheet(fp: str='backend/google_sheet.tsv') -> list[Song]:
    with open(fp, 'r', encoding='utf-8') as f:
        sheet = f.readlines()[1:]
    songs: list[Song]
    songs = list()
    for line in sheet:
        
        artist, song, link, origin, in_use, voice = line.split('\t')[1:]
        in_use = True if in_use == '' else False
        if voice == 'w_voice':
            voice = True
        elif voice == 'no_voice':
            voice = False
        else:
            voice = None
        songs.append(Song(song=song, artist=artist, link=link, origin=origin, in_use=in_use, voice=voice))
    return songs




def main():
    import_sheet()

if __name__ == '__main__':
    main()