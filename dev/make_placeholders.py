#!/usr/bin/env python3
"""
Recreate the labelled placeholder images in static/images/ (needs Pillow).
Projects: four at 1800 x 1200 (3:2), with an outlined band showing what the 2:1 wide
feature shows. Gallery: six in mixed shapes (landscape, portrait, square, panorama),
to show that gallery pages display each image whole.
Usage: python3 -I dev/make_placeholders.py [output folder, default static/images]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1] if len(sys.argv) > 1 else "static/images"
def font(size, bold=False):
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
                 "/Library/Fonts/Arial%s.ttf" % (" Bold" if bold else "")]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

shades = [(176, 184, 194), (196, 188, 176), (182, 196, 186), (198, 186, 196)]
for i, colour in enumerate(shades, 1):
    W, H = 1800, 1200
    im = Image.new("RGB", (W, H), colour); d = ImageDraw.Draw(im)
    top = (H - W // 2) // 2
    d.rectangle([0, top, W - 1, top + W // 2 - 1], outline=(110, 110, 110), width=5)
    y = H // 2 - 120
    for text, f, step in [(f"Project image {i}", font(96, True), 140),
                          ("1800 × 1200 (3:2), under 400 KB", font(48), 70),
                          ("Outlined band: what a wide feature shows", font(44), 70)]:
        d.text(((W - d.textlength(text, font=f)) / 2, y), text, fill=(55, 55, 55), font=f); y += step
    im.save(os.path.join(out, f"project-{i}-placeholder.jpg"), quality=72, optimize=True)
gallery = [(1800, 1200), (1200, 1600), (1400, 1400), (2000, 1000), (1200, 1500), (1800, 1200)]
tints = [(186, 196, 210), (210, 196, 186), (190, 206, 196), (206, 192, 210), (204, 204, 190), (192, 202, 214)]
for i, ((W, H), colour) in enumerate(zip(gallery, tints), 1):
    im = Image.new("RGB", (W, H), colour); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(120, 120, 120), width=6)
    y = H // 2 - 80
    for text, f, step in [(f"Gallery image {i}", font(90, True), 120), (f"{W} × {H}", font(54), 70)]:
        d.text(((W - d.textlength(text, font=f)) / 2, y), text, fill=(55, 55, 55), font=f); y += step
    im.save(os.path.join(out, f"gallery-{i}-placeholder.jpg"), quality=72, optimize=True)
print("Wrote 4 project and 6 gallery placeholders to", out)
