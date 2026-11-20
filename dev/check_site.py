#!/usr/bin/env python3
"""
Browser checks for a built DrPhill site (headless Chrome via Playwright).

Usage:
    hugo --minify --baseURL "http://localhost:8765/TestRepo/" -d /tmp/srv/TestRepo
    (cd /tmp/srv && python3 -m http.server 8765 &)
    python3 -I dev/check_site.py http://localhost:8765/TestRepo/ [--chrome /usr/bin/google-chrome]

Checks, at phone (390x844), tablet (700x900) and laptop (1440x820):
  - sticky header height and share of the screen; menu row vs Menu button
  - wide feature caption above the fold; number of columns in the first row of smaller projects
  - no sideways scrolling
  - each menu jump lands with the section heading just below the header
  - phone menu closes after a choice, on Escape, and on a tap elsewhere
And once: console errors, landmarks, heading order, images with alt and
width/height, empty links, duplicate ids, keyboard order, fonts downloaded.
Writes screenshots to ./shots/.
"""
import os, sys
from playwright.sync_api import sync_playwright

base = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "http://localhost:8765/TestRepo/"
chrome = sys.argv[sys.argv.index("--chrome") + 1] if "--chrome" in sys.argv else None
os.makedirs("shots", exist_ok=True)
problems = []

def note(ok, msg):
    print(("  ok   " if ok else "  FAIL ") + msg)
    if not ok:
        problems.append(msg)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome, args=["--no-sandbox"]) if chrome else p.chromium.launch()

    # Page structure, once.
    pg = b.new_page(viewport={"width": 1280, "height": 800})
    errors, fonts = [], []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("response", lambda r: fonts.append(r.url.rsplit("/", 1)[-1]) if r.url.endswith(".woff2") else None)
    print("Structure")
    for path in ["", "projects/"]:
        pg.goto(base + path); pg.wait_for_load_state("networkidle")
        r = pg.evaluate("""() => ({
          headings: [...document.querySelectorAll('h1,h2,h3')].map(h => +h.tagName[1]),
          noAlt: [...document.images].filter(i => !i.hasAttribute('alt')).length,
          noDims: [...document.images].filter(i => !i.getAttribute('width') && !i.src.endsWith('.gif') && !i.src.endsWith('.svg')).length,
          emptyLinks: [...document.querySelectorAll('a')].filter(a => !a.textContent.trim()).length,
          dupIds: (() => { const s = [...document.querySelectorAll('[id]')].map(e => e.id); return s.length - new Set(s).size })(),
          mains: document.querySelectorAll('main').length })""")
        jumps = any(b2 - a2 > 1 for a2, b2 in zip(r["headings"], r["headings"][1:]))
        note(r["headings"][:1] == [1] and not jumps, f"/{path}: one h1 first, no skipped heading levels {r['headings']}")
        note(r["noAlt"] == 0 and r["noDims"] == 0, f"/{path}: every image has alt and width/height")
        note(r["emptyLinks"] == 0 and r["dupIds"] == 0 and r["mains"] == 1, f"/{path}: no empty links, no duplicate ids, one <main>")
    note(not errors, f"no console errors {errors[:3]}")
    print("  fonts downloaded:", sorted(set(fonts)))
    pg.goto(base); seq = []
    for _ in range(3):
        pg.keyboard.press("Tab"); seq.append(pg.evaluate("document.activeElement.textContent.trim()"))
    note(seq[0] == "Skip to content", f"keyboard order starts with the skip link {seq}")
    pg.close()

    # Layout and menu, at three sizes.
    for w, h, label in [(390, 844, "phone"), (700, 900, "tablet"), (1440, 820, "laptop")]:
        print(f"{label} {w}x{h}")
        pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(base); pg.wait_for_load_state("networkidle")
        s = pg.evaluate("""() => { const q = s => document.querySelector(s);
          return { header: Math.round(q('.masthead').getBoundingClientRect().height),
            menuButton: getComputedStyle(q('.sitenav__menu') || document.body).display !== 'none' && !!q('.sitenav__menu'),
            cols: q('.projects__row') ? getComputedStyle(q('.projects__row')).gridTemplateColumns.split(' ').length : 0,
            caption: q('.card--wide .card__caption') ? Math.round(q('.card--wide .card__caption').getBoundingClientRect().bottom) : 0,
            overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
            sections: [...document.querySelectorAll('main section[id]')].map(e => e.id) } }""")
        print(f"  header {s['header']}px ({100*s['header']/h:.0f}%), Menu button: {s['menuButton']}, row columns: {s['cols']}, sections: {s['sections']}")
        note(not s["overflow"], "no sideways scrolling")
        note(s["caption"] <= h, f"wide feature caption above the fold ({s['caption']} <= {h})")
        pg.screenshot(path=f"shots/{label}.png", full_page=True)
        for sec in [x for x in s["sections"] if x != "projects"][:-1]:  # the last section may not scroll far enough
            if s["menuButton"]:
                pg.click(".sitenav__menu summary"); pg.click(f".sitenav__panel a[href$='#{sec}']")
                note(not pg.evaluate("document.querySelector('.sitenav__menu').open"), f"menu closes after choosing {sec}")
            else:
                pg.click(f".sitenav__row a[href$='#{sec}']")
            pg.wait_for_timeout(250)
            top = pg.evaluate(f"document.querySelector('#{sec} h2').getBoundingClientRect().top")
            bottom = pg.evaluate("document.querySelector('.masthead').getBoundingClientRect().bottom")
            note(bottom <= top <= bottom + 40, f"#{sec} heading lands just below the header ({top:.0f} vs {bottom:.0f})")
        if s["menuButton"]:
            pg.evaluate("window.scrollTo(0, 0)"); pg.click(".sitenav__menu summary"); pg.keyboard.press("Escape")
            note(not pg.evaluate("document.querySelector('.sitenav__menu').open"), "Escape closes the menu")
            pg.click(".sitenav__menu summary"); pg.mouse.click(3, h - 40)
            note(not pg.evaluate("document.querySelector('.sitenav__menu').open"), "a tap elsewhere closes the menu")
        pg.close()
    b.close()

print("\n" + ("All checks passed." if not problems else f"{len(problems)} problem(s)."))
sys.exit(1 if problems else 0)
