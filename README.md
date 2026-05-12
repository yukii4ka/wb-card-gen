# wb-card-gen

generates product card images for wildberries listings. takes product data from a csv, overlays text and price on a template image, outputs ready-to-upload jpgs.

built this because manually editing cards in photoshop for 50+ products is not fun.

## what it does

- reads product list from `products.csv`
- loads a template image (configurable)
- draws product name, price, and optional badge using Pillow
- saves output to `out/` folder with SKU as filename

## usage

```bash
pip install -r requirements.txt
python gen.py --input products.csv --template templates/default.png
```

output goes to `out/` — one jpg per product.

## csv format

```
sku,name,price,badge
12345,Футболка оверсайз,1290,NEW
67890,Джинсы slim,2490,
```

`badge` is optional — leave empty to skip.

## config

edit `config.py` to change fonts, colors, image size (default 900x1200 for WB requirements), text positioning.

## stack

python · pillow · csv · pathlib
