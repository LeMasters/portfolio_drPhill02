# dev/ — maintainer tools

Not used by the Hugo build or by students. Python 3; run with `python3 -I`.

| Script | What it does | Needs |
|---|---|---|
| `check_site.py` | Browser checks of a built site at phone, tablet and laptop sizes (layout, menu, accessibility). See `docs/DESIGN.md` §9. | Playwright for Python, Chrome or Chromium |
| `check_palettes.py` | Contrast check (WCAG AA) of every colour scheme, read directly from `main.css`. Run after changing any colour. | Python only |
| `build_fonts.py` | Regenerates `themes/Alexander/static/fonts/` and `assets/css/fonts.css` from Fontsource files. Instructions at the top of the script. | A sparse clone of github.com/fontsource/font-files |
| `check_content.py` | Parses `.pages.yml` and every content file; reports any key that has no field in its Pages CMS form (a save would drop it). Run from the repository root. | PyYAML |
| `make_placeholders.py` | Regenerates the labelled sample images in `static/images/`: four project images (3:2) and six gallery images in mixed shapes. | Pillow |
