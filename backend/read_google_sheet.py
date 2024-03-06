import gspread

def read(sheet_name: str) -> list[list]:
    gc = gspread.service_account('.config/gspread/service_account.json')

    sh = gc.open(sheet_name)
    worksheet = sh.worksheet('seznam')

    sheet = worksheet.get_all_values()
    return sheet[1:]

if __name__ == '__main__':
    read('Karaoke seznam')