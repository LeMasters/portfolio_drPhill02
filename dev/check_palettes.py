#!/usr/bin/env python3
"""
Check every colour scheme in themes/DrPhill/assets/css/main.css against WCAG contrast.

Reads the colours straight from the stylesheet: the default scheme ("ink") from the
--color-* custom properties in :root, the others from the [data-palette="…"] blocks.
Run after changing any colour:  python3 -I dev/check_palettes.py
Exit status 1 if any pairing falls short.
"""
import re, sys

CSS = "themes/DrPhill/assets/css/main.css"
css = re.sub(r"/\*.*?\*/", "", open(CSS, encoding="utf-8").read(), flags=re.S)

def colours(block):
    return {m.group(1): m.group(2).lower() for m in re.finditer(r"--color-([\w-]+):\s*(#[0-9a-fA-F]{6})", block)}

root = colours(re.search(r":root\s*\{(.*?)\n\}", css, re.S).group(1))
schemes = {"ink": root}
for name, block in re.findall(r'\[data-palette="([\w-]+)"\]\s*\{(.*?)\}', css, re.S):
    schemes[name] = {**root, **colours(block)}

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

# (foreground, background, minimum, where it is used)
PAIRS = [
    ("text", "bg", 4.5, "body text"),
    ("text-muted", "bg", 4.5, "captions, labels, menu"),
    ("accent", "bg", 4.5, "links, button text"),
    ("bg", "accent", 4.5, "text on accent: button hover, open Menu, skip link"),
    ("text-muted", "placeholder", 4.5, "title in an empty image frame"),
    ("text", "placeholder", 4.5, "phone-menu item on hover"),
    ("block-text", "block-bg", 4.5, "bottom block text"),
    ("block-muted", "block-bg", 4.5, "bottom block small text"),
    ("accent", "bg", 3.0, "focus ring (non-text, WCAG 1.4.11)"),
]

failures = 0
for name, c in schemes.items():
    worst = min(ratio(c[f], c[b]) for f, b, need, _ in PAIRS if need == 4.5)
    print(f"{name}: lowest text pairing {worst:.1f}:1")
    for f, b, need, where in PAIRS:
        r = ratio(c[f], c[b])
        if r < need:
            failures += 1
            print(f"  FAIL {f} on {b}: {r:.2f}:1 (needs {need}) — {where}")
print("All schemes pass." if not failures else f"{failures} failure(s).")
sys.exit(1 if failures else 0)
