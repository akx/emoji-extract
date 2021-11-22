import os
import argparse
import sys
import unicodedata
from typing import Tuple, List

from fontTools.ttLib import TTFont  # type: ignore[import]


def get_chars_and_rest_from_glyph_name(orig_name: str) -> Tuple[List[str], str]:
    glyphs, _, rest = orig_name.partition(".")
    return [chr(int(g.lstrip("u"), 16)) for g in glyphs.split("_")], rest


def get_human_filename(glyphname: str) -> str:
    try:
        chars, rest = get_chars_and_rest_from_glyph_name(glyphname)
        uni_names = [unicodedata.name(char).replace(" ", "_") for char in chars]
        uni_name = "_".join(uni_names)
        if rest:
            uni_name += f"_{rest}"
        return uni_name.lower()
    except Exception:
        print(f"Failed to get human name for {glyphname}", file=sys.stderr)
    return glyphname


def do_extract(
    *,
    filename: str,
    out_root: str,
    font_number: int = 0,
    all_resolutions: bool = False,
    human_name: bool = False,
) -> None:
    font = TTFont(filename, fontNumber=font_number)
    sbix_table = font["sbix"]
    for resolution, strike in sorted(sbix_table.strikes.items(), reverse=True):
        for glyph in strike.glyphs.values():
            if glyph.graphicType == "png ":
                name = glyph.glyphName
                if human_name:
                    name = get_human_filename(name)
                filename = f"{out_root}/{resolution}/{name}.png"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "wb") as outf:
                    outf.write(glyph.imageData)
                    print(outf.name, outf.tell())
        if not all_resolutions:
            break


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--filename", default="/System/Library/Fonts/Apple Color Emoji.ttc")
    ap.add_argument("--font-number", "-n", default=0)
    ap.add_argument("--human-names", action="store_true", default=False)
    ap.add_argument("--out-root", default="images")
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
        human_name=args.human_names,
        out_root=args.out_root,
    )


if __name__ == "__main__":
    main()
