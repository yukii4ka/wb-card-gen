import argparse
import csv
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import config


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def draw_card(row, template_path, out_dir):
    sku = row["sku"].strip()
    name = row["name"].strip()
    price = row["price"].strip()
    badge = row.get("badge", "").strip()

    img = Image.open(template_path).convert("RGBA")
    img = img.resize((config.WIDTH, config.HEIGHT))

    draw = ImageDraw.Draw(img)

    name_font = load_font(config.FONT_PATH, config.FONT_SIZE_NAME)
    price_font = load_font(config.FONT_PATH, config.FONT_SIZE_PRICE)

    draw.text(config.NAME_POS, name, font=name_font, fill=config.TEXT_COLOR)
    draw.text(config.PRICE_POS, f"{price} ₽", font=price_font, fill=config.PRICE_COLOR)

    if badge:
        badge_font = load_font(config.FONT_PATH, config.FONT_SIZE_BADGE)
        bx, by = config.BADGE_POS
        bw, bh = config.BADGE_SIZE
        draw.rectangle([bx, by, bx + bw, by + bh], fill=config.BADGE_BG)
        draw.text((bx + 8, by + 4), badge, font=badge_font, fill=config.BADGE_TEXT_COLOR)

    out_path = out_dir / f"{sku}.jpg"
    img.convert("RGB").save(out_path, "JPEG", quality=95)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="generate wb product card images")
    parser.add_argument("--input", required=True, help="path to products.csv")
    parser.add_argument("--template", default="templates/default.png", help="template image")
    parser.add_argument("--out", default="out", help="output directory")
    args = parser.parse_args()

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    ok = 0
    for row in rows:
        try:
            out_path = draw_card(row, template_path, out_dir)
            print(f"  {row['sku']} -> {out_path}")
            ok += 1
        except Exception as e:
            print(f"  {row['sku']} failed: {e}", file=sys.stderr)

    print(f"\ndone: {ok}/{len(rows)}")


if __name__ == "__main__":
    main()
