import shutil
import sys

from chafa import (
    Canvas,
    CanvasConfig,
    CanvasMode,
    ColorExtractor,
    PixelMode,
    SymbolMap,
    SymbolTags,
)
from chafa.loader import Loader

FONT_RATIO = 11 / 24


def build_symbol_map():
    sm = SymbolMap()
    for tag in (
        SymbolTags.CHAFA_SYMBOL_TAG_SPACE,
        SymbolTags.CHAFA_SYMBOL_TAG_SOLID,
        SymbolTags.CHAFA_SYMBOL_TAG_BLOCK,
        SymbolTags.CHAFA_SYMBOL_TAG_HALF,
        SymbolTags.CHAFA_SYMBOL_TAG_HHALF,
        SymbolTags.CHAFA_SYMBOL_TAG_VHALF,
        SymbolTags.CHAFA_SYMBOL_TAG_QUAD,
    ):
        sm.add_by_tags(tag)
    return sm


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: yc-image <path>")

    path = sys.argv[1]
    image = Loader(path)
    cols, rows = shutil.get_terminal_size((80, 24))

    config = CanvasConfig()
    config.width = cols
    config.height = rows
    config.canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_TRUECOLOR
    config.pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SYMBOLS
    config.color_extractor = ColorExtractor.CHAFA_COLOR_EXTRACTOR_AVERAGE
    config.work_factor = 1.0
    config.set_symbol_map(build_symbol_map())
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
