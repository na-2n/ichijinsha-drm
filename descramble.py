import sys

from base64 import b64decode
from math import floor

from PIL import Image


def descramble(img: Image, drm_hash: str) -> Image:
    cp = img.copy()

    try:
        columns, rows, *tiles = b64decode(drm_hash)

        assert columns * rows == len(tiles)
    except:
        raise ValueError('drm_hash is not a valid hash') from None

    tile_width = floor((img.width - img.width % 8) / columns)
    tile_height = floor((img.height - img.height % 8) / rows)

    for idx, tile in enumerate(tiles):
        in_x = tile % columns
        in_y = floor(tile / columns)
        out_x = idx % columns 
        out_y = floor(idx / columns)

        sx = in_x * tile_width
        sy = in_y * tile_height

        dx = out_x * tile_width
        dy = out_y * tile_height

        with img.crop((sx, sy, sx + tile_width, sy + tile_height)) as tmp:
            cp.paste(tmp, (dx, dy, dx + tile_width, dy + tile_height))

    return cp


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'usage: {sys.argv[0]} <in> <drm hash> [out]')
        exit()

    with Image.open(sys.argv[1]) as img:
        with descramble(img, sys.argv[2]) as im:
            if len(sys.argv) > 3:
                im.save(sys.argv[3])
            else:
                im.show()

