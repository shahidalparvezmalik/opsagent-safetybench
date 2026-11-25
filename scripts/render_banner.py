"""Render the repository SVG to the linked-in ready JPEG (build-only dependencies)."""

from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "images" / "opsagent-safetybench-banner.svg"
OUT = ROOT / "docs" / "images" / "opsagent-safetybench-banner.JPG"
WIDTH, HEIGHT = 1920, 1080


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit("Missing SVG source: {}".format(SOURCE))
    png_data = cairosvg.svg2png(url=str(SOURCE), output_width=WIDTH, output_height=HEIGHT)
    with Image.open(BytesIO(png_data)) as rendered:
        if rendered.size != (WIDTH, HEIGHT):
            raise SystemExit("Unexpected SVG render size: {}".format(rendered.size))
        rendered.convert("RGB").save(OUT, format="JPEG", quality=92, optimize=True, progressive=True)
    with Image.open(OUT) as result:
        if result.format != "JPEG" or result.mode != "RGB" or result.size != (WIDTH, HEIGHT):
            raise SystemExit("JPEG validation failed: format={}, mode={}, size={}".format(result.format, result.mode, result.size))
    print("Saved {} ({}x{} JPEG RGB)".format(OUT, WIDTH, HEIGHT))


if __name__ == "__main__":
    main()
