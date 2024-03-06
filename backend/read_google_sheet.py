import gspread
import os
import json

def read(sheet_name: str) -> list[list]:
    
    credentials = json.loads(os.environ['GOOGLE_INFO'])
    gc = gspread.service_account_from_dict(credentials)

    sh = gc.open(sheet_name)
    worksheet = sh.worksheet('seznam')

    sheet = worksheet.get_all_values()
    return sheet[1:]

if __name__ == '__main__':
    read('Karaoke seznam')