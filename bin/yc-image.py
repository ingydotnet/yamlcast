import shutil
import sys

from chafa import Canvas, CanvasConfig
from chafa.loader import Loader

FONT_RATIO = 11 / 24


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: yc-image <path>")

    path = sys.argv[1]
    image = Loader(path)
    cols, rows = shutil.get_terminal_size((80, 24))

    config = CanvasConfig()
    config.width = cols
    config.height = rows
    config.calc_canvas_geometry(image.width, image.height, FONT_RATIO)

    canvas = Canvas(config)
    canvas.draw_all_pixels(
        image.pixel_type,
        image.get_pixels(),
        image.width,
        image.height,
        image.rowstride,
    )

    sys.stdout.buffer.write(canvas.print())
    sys.stdout.flush()


main()
