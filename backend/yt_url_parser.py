from urllib.parse import urlparse, parse_qs

def get_id_w_timestamp(url: str) -> str:
    query = urlparse(url)
    if query.hostname == 'youtu.be':
       v_id = query.path[1:]
       timecode = '&'+ query.query + 's'
       return v_id + timecode
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch':
            v_id = parse_qs(query.query)['v'][0]
            try:
                timecode = '&t=' + parse_qs(query.query)['t'][0]
            except KeyError as er:
                timecode = ''
            return v_id + timecode
    else:
        raise ValueError('Could not parse the link')

# test = [
#     'https://www.youtube.com/watch?v=_dFo0O4Mtz4',
#     'http://www.youtube.com/watch?v=xb3oMef3hnc',
#     'https://youtu.be/ytRWEdjf9lk?t=427',
#     'https://youtube.com/watch?v=9l878arGKgg&list=PLAioQnpWobqqCm54dT7e2ash3s40Al5-L&index=11&pp=iAQB8AUB',
#     'https://www.youtube.com/watch?v=RQC7JL4a6fc&t=1849s'
# ]
# for url in test:
#     print('https://www.youtube.com/watch?v=' + get_id_w_timestamp(url))