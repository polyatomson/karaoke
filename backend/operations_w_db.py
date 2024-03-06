import mysql.connector
import os

config = {'user': os.environ['DB_USER'],
  'password': os.environ['DB_PASSWORD'],
  'host': os.environ['DB_HOST'],
  'port': os.environ['DB_PORT'],
  'database': os.environ['DATABASE'],
  'raise_on_warnings': True
}

def get_table() -> dict:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT * FROM Songs 
                   WHERE in_use=1 
                   ORDER BY artist, title ASC;
                   """)
    songs = cursor.fetchall()
    conn.close()
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""SELECT t.origin FROM (
                      SELECT origin, COUNT(song_id) as n_songs FROM Songs
                      WHERE in_use=1
                      GROUP BY origin) t
                      ORDER BY n_songs DESC;""")
    origins = cursor.fetchall()
    conn.close()
    origins = [orig[0] for orig in origins]
    return {'songs':songs, 'origins': origins}

def record_view(song_id: int) -> str:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Views(song_id, n_views) VALUES(%s, 1)
                   ON DUPLICATE KEY UPDATE n_views = n_views+1;""", (song_id,))
    conn.commit()
    cursor.execute("""SELECT n_views FROM Views WHERE song_id=%s;""", (song_id, ))
    n_views = cursor.fetchone()[0]
    conn.close()
    return f'view recorded, {n_views} total'
    
# res = get_table()
# print()
# {'song_id': 13, 'title': 'Ne moren bez nje', 'artist': 'Alen Vitasović', 'vocals': None, 'in_use': 1, 'origin': 'EX-YU', 'link': 'https://www.youtube....YPTH9IxqpY'}
# record_view(1)