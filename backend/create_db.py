import mysql.connector
import json
from dataclasses import dataclass, asdict
from typing import Optional
import os
import re

from yt_url_parser import get_id_w_timestamp
import operations_w_google_sheet

@dataclass
class Song:
    song: str
    artist: str
    link: str
    origin: str
    in_use: bool
    voice: Optional[bool]
    id: Optional[int]
    views: int = 0

    def to_tuple_no_id(self) -> tuple:
        # song_id, title, artist, vocals, in_use, origin, link
        return self.song, self.artist, self.voice, self.in_use, self.origin, self.link
    
    # def clean_link(self) -> None:
    #     if 'watch?v=' in self.link:
    #         video_id = re.search(r'watch\?v=(.+)').group()
    #     elif ''
        

config = {'user': os.environ['DB_USER'],
  'password': os.environ['DB_PASSWORD'],
  'host': os.environ['DB_HOST'],
  'port': os.environ['DB_PORT'],
  'database': os.environ['DATABASE'],
  'raise_on_warnings': True
}

def import_sheet_from_file(fp: str='google_sheet.tsv') -> list[list]:
    with open(fp, 'r', encoding='utf-8') as f:
        sheet = f.readlines()[1:]
    sheet = [[value.strip() for value in line.split('\t')] for line in sheet]
    return sheet
    
def process_sheet(sheet: list[list]) -> list[Song]:
    songs: list[Song]
    songs = list()
    for line in sheet:
        artist, song, link, origin, in_use, voice = line[1:7]
        link = get_id_w_timestamp(link)
        in_use = True if in_use == '' else False
        voice = voice.strip()
        if voice == 'w_voice':
            voice = True
        elif voice == 'no_voice':
            voice = False
        elif voice== '':
            voice = None
        songs.append(Song(song=song, artist=artist, link=link, origin=origin, in_use=in_use, voice=voice, id=None))
    return songs


def create_schema():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
                    CREATE TABLE `Songs` (
                    `song_id` int(11) NOT NULL AUTO_INCREMENT,
                    `title` varchar(500) NOT NULL,
                    `artist` varchar(500) NOT NULL DEFAULT 'Unknown',
                    `vocals` tinyint(1) DEFAULT NULL,
                    `in_use` tinyint(1) NOT NULL DEFAULT '1',
                    `origin` varchar(20) NOT NULL,
                    `link` varchar(800) NOT NULL,
                    PRIMARY KEY (`song_id`),
                    UNIQUE KEY `Songs_UN_link` (`link`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                    """)
        conn.commit()
        print('created table Songs')
    except Exception as ex:
        if ex.errno != 1050:
            raise(ex)
    conn.close()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS `Views` (
                    `song_id` int(11) NOT NULL,
                    `n_views` int(11) NOT NULL,
                    UNIQUE KEY `Views_UN` (`song_id`),
                    CONSTRAINT `Views_FK` FOREIGN KEY (`song_id`) REFERENCES `Songs` (`song_id`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                    """)
        conn.commit()
        print('created table Views')
    except Exception as ex:
        if ex.errno != 1050:
            raise(ex)
    conn.close()
    print()

def fill_db(data: list[Song]):
    # data = [asdict(song) for song in data]
    data = [song.to_tuple_no_id() for song in data]
    update_query = """
            UPDATE Songs SET title=%s, artist=%s, vocals=%s, in_use=%s, origin=%s
            WHERE link=%s
            """
    insert_query = """
    INSERT INTO Songs(title, artist, vocals, in_use, origin, link) 
    VALUES(%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE song_id=song_id;
    """
    #update
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.executemany(update_query, data)
    conn.commit()
    n_updated = cursor.rowcount
    conn.close()

    #insertion
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(song_id) as n FROM Songs")
    n_songs_before = cursor.fetchone()[0]
    
    cursor.executemany(insert_query, data)
    conn.commit()
    n_inserted = cursor.rowcount
    conn.close()

    emptybefore = 'Empty DB filled with' if n_songs_before==0 else 'Existing DB extended by'
    msg = f"""{emptybefore} {str(n_inserted)} songs.\n
                Total count is {str(n_songs_before+n_inserted)}.\n
                {str(n_updated)} rows were updated."""
    print(msg)
    return msg




def create_and_fill_from_file():
    sheet = import_sheet_from_file()
    data = process_sheet(sheet)
    create_schema()
    return fill_db(data)

def create_and_fill_from_google():
    sheet = operations_w_google_sheet.read('Karaoke seznam')
    data = process_sheet(sheet)
    create_schema()
    return fill_db(data)

if __name__ == '__main__':
    source = input('From file or google? (f/g) ')
    if source == 'f':
        create_and_fill_from_file()
    elif source == 'g':
        create_and_fill_from_google()