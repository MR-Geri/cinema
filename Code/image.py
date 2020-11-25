import datetime
import locale
from PIL import Image, ImageDraw, ImageFont

from settings import path_temp, path_ticket, path_font


image = Image.open(path_ticket)
locale.setlocale(locale.LC_ALL, '')
font_70 = ImageFont.truetype(path_font, size=70)
font_100 = ImageFont.truetype(path_font, size=100)


def ticket(row: int, place: int, hall: str, price: int, date: str) -> None:
    im = image.copy()
    text = ImageDraw.Draw(im)
    date = datetime.datetime(*reversed(list(map(int, date.split('.'))))).strftime('%d %B %Y')
    if 'ь' in date:
        day, month, year = date.replace('ь', 'я').split()
    elif 'й' in date:
        day, month, year = date.replace('й', 'я').split()
    else:
        day, month, year = date.split()
        month += 'а'
    lines = [f'Ряд: {row}', f'Место: {place}', f'{hall}']
    for ind, line in enumerate(lines):
        text.text(
            (470, 630 + 85 * ind),
            line,
            font=font_70,
            fill='#0B0B0B'
        )
    text.text(
        (900, 700),
        f'{price}Р',
        font=font_100,
        fill='#0B0B0B'
    )
    lines = [f'{" " * (9 - len(day))}{day}', f'{" " * (9 - len(month))}{month}', f'{" " * (9 - len(year))}{year}']
    for ind, line in enumerate(lines):
        text.text(
            (1200, 630 + 85 * ind),
            line,
            font=font_70,
            fill='#0B0B0B'
        )
    im.save(f'{path_temp}/{row}_{place}_{hall}_{price}_{date}.jpg')
