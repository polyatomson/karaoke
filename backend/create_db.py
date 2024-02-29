import mysql.connector
import json
from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class Song:
    song: str
    artist: str
    link: str
    origin: str
    in_use: bool
    voice: Optional[bool]
    views: int = 0


config = {'user': os.environ['DB_USER'],
  'password': os.environ['DB_PASSWORD'],
  'host': os.environ['DB_HOST'],
  'port': os.environ['DB_PORT'],
  'database': os.environ['DATABASE'],
  'raise_on_warnings': True
}


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

def create_schema():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
                    CREATE TABLE `Songs` (
                    `title` varchar(500) NOT NULL,
                    `song_id` int(11) NOT NULL AUTO_INCREMENT,
                    `artist` varchar(500) NOT NULL DEFAULT 'Unknown',
                    `vocals` tinyint(1) DEFAULT NULL,
                    `in_use` tinyint(1) NOT NULL DEFAULT '1',
                    `origin` varchar(20) NOT NULL,
                    `link` varchar(800) NOT NULL,
                    PRIMARY KEY (`song_id`),
                    UNIQUE KEY `Songs_UN_link` (`link`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                    """)
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
        print('created table Views')
    except Exception as ex:
        if ex.errno != 1050:
            raise(ex)
    conn.close()
    print()


def main():
    import_sheet()
    create_schema()

if __name__ == '__main__':
    main()