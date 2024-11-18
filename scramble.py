import sys

from typing import Tuple
from base64 import b64encode
from math import floor
from random import shuffle

from PIL import Image


def scramble(img: Image, cols: int, rows: int) -> Tuple:  # Tuple[Image, str]
    w = floor((img.width - img.width % 8) / cols)
    h = floor((img.height - img.height % 8) / rows)

    tiles = list(range(0, cols * rows))
    shuffle(tiles)

    cp = img.copy();

    for idx, tile in enumerate(tiles):
        in_x = idx % cols
        in_y = floor(idx / cols)
        out_x = tile % cols
        out_y = floor(tile / cols)

        sx = in_x * w 
        sy = in_y * h 

        dx = out_x * w
        dy = out_y * h

        with img.crop((sx, sy, sx + w, sy + h)) as tmp:
            cp.paste(tmp, (dx, dy, dx + w, dy + h))

    drm_hash = b64encode(bytes([cols, rows, *tiles])).decode('utf8')
    return cp, drm_hash


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(f'usage: {os.sys.argv[0]} <in> <columns> <rows> <out>')
        exit()

    with Image.open(sys.argv[1]) as img:
        im, drm_hash = scramble(img, int(sys.argv[2]), int(sys.argv[3]))

        im.save(sys.argv[4])
        print(drm_hash)

