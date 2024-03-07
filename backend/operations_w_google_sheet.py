import gspread
import os
import json
from operations_w_db import get_song_id, get_views

def read(sheet_name: str) -> list[list]:
    
    credentials = json.loads(os.environ['GOOGLE_INFO'])
    gc = gspread.service_account_from_dict(credentials)

    sh = gc.open(sheet_name)
    worksheet = sh.worksheet('seznam')

    sheet = worksheet.get_all_values()
    return sheet[1:]

def write_views(sheet_name: str) -> str:
    credentials = json.loads(os.environ['GOOGLE_INFO'])
    gc = gspread.service_account_from_dict(credentials)

    sh = gc.open(sheet_name)
    worksheet = sh.worksheet('seznam')
    ids = []
    views = []
    statuses = []
    links = worksheet.get('D:D')

    for link in links:
        link = link[0]
        if link != '' and link != 'Link':
            song_id = get_song_id(link)
            if song_id is None:
                statuses.append(['not_in_db'])
                song_id = ''
            else:
                statuses.append(['in_db'])
            n_views = get_views(song_id)
            ids.append([song_id])
            views.append([n_views])
    tb_length = str(len(links))
    worksheet.update(f'H2:H{tb_length}', views)
    worksheet.update(f'A2:A{tb_length}', ids)
    worksheet.update(f'I2:I{tb_length}', statuses)
    return 'info from db is now in google sheets'

if __name__ == '__main__':
    # read('Karaoke seznam')
    write_views('Karaoke seznam')