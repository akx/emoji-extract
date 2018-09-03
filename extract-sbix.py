import os
import argparse

from fontTools.ttLib import TTFont


def do_extract(filename, font_number=0, all_resolutions=False):
    font = TTFont(filename, fontNumber=font_number)
    sbix_table = font["sbix"]
    for resolution, strike in sorted(sbix_table.strikes.items(), reverse=True):
        for glyph in strike.glyphs.values():
            if glyph.graphicType == "png ":
                filename = f"images/{resolution}/{glyph.glyphName}.png"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "wb") as outf:
                    outf.write(glyph.imageData)
                    print(outf.name, outf.tell())
        if not all_resolutions:
            break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--filename", default="/System/Library/Fonts/Apple Color Emoji.ttc")
    ap.add_argument("--font-number", "-n", default=0)
    ap.add_argument(
        "--all-resolutions",
        help="all resolutions or just the highest one?",
        action="store_true",
    )
    args = ap.parse_args()
    do_extract(
        filename=args.filename,
        font_number=args.font_number,
        all_resolutions=args.all_resolutions,
    )


if __name__ == "__main__":
    main()
