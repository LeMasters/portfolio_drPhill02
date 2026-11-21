# Instructions for Claude: maintaining DrPhill

You are helping Garrison LeMasters (ETBD, Miami University) maintain DrPhill, a Hugo portfolio theme and site template for undergraduate games students. Students edit through Pages CMS; GitHub Actions builds with Hugo; GitHub Pages publishes each student's site at `username.github.io/repo/`.

## Read first

1. `docs/DESIGN.md`: status, architecture, file map, content format, design rationale, standards, fallbacks, testing, open items.
2. If you are in the claude.ai Project "Portfolio reviews": also `Games_Portfolio_Project/portfolio-platform-working-practices.md` and `Games_Portfolio_Project/portfolio-platform-instructor-setup.md`. They take precedence over this file on working style.

## Working with Garrison

- Lead with the answer. Keep replies short. Lay out options with trade-offs; do not advocate. Be especially circumspect about pedagogy.
- When he is clicking through GitHub or Pages CMS, give **one step at a time** and wait; verify each step before the next.
- **Ask before pushing** to any repository, and before changing `.github/workflows/`, `.pages.yml`, or anything students will copy. A direct request ("fix X in the template") counts as the ask for the commits that do it.
- He judges how the theme looks. Your checks cover function, standards and accessibility.
- Label anything untested as untested, in replies and in docs, until a build or his check confirms it.

## The rules this theme follows

- **Most robust, most contemporary HTML/CSS; no libraries.** Plain CSS, no framework. JavaScript only for small enhancements the page works without. No requests to other sites (no Google Fonts, CDNs, analytics) — except the visitor-statistics script a student explicitly chooses in Profile (`partials/analytics.html`, off by default).
- **Content is portable Markdown/YAML** in `content/` and `data/`, in the format in DESIGN.md section 4. Never move content into templates, and never put presentation into content files (`data/style.yaml` is the one place for appearance).
- **Every key in a file Pages CMS edits has a field in `.pages.yml`** (hidden if need be), or a save will drop it.
- **Paths without a leading slash**; every student-typed link through `partials/url.html`; every image through `partials/img.html`.
- **Sections appear only with content**, decided in one place: `partials/sections.html`. Page and menu both read it. Every section, Gallery included, is a home-page section; the Gallery section links on to the full Gallery page.
- **Previous/next links** on project and gallery pages come from `partials/pager.html`; gallery entries that count are listed by `partials/gallery-items.html` (those with an image).
- **CSS**: every design value is a custom property in section 1 of `main.css`; class names follow the template file (BEM: `.block__element--variant`); logical properties; mobile first; container queries for component layout; each newer feature either ignored safely or preceded by a fallback with a `Fallback:` comment. Keep the numbered table of contents in sync.
- **Accessibility**: one `<h1>` per page, no skipped heading levels, alt text, visible focus, contrast ≥ 4.5:1, reduced motion respected.

## Building and testing

Claude's sandbox may not have Hugo installed. Download the pinned version from GitHub releases (the workflow pins 0.147.0 extended):

```
mkdir -p ~/bin && cd ~/bin
curl -sSL -o h.tgz https://github.com/gohugoio/hugo/releases/download/v0.147.0/hugo_extended_0.147.0_linux-amd64.tar.gz
tar xzf h.tgz hugo
```

Build at a **subfolder** address (as GitHub Pages does), serve, and run the checks:

```
~/bin/hugo --minify --baseURL "http://localhost:8765/TestRepo/" -d /tmp/srv/TestRepo
(cd /tmp/srv && python3 -m http.server 8765 &)
python3 -I dev/check_site.py http://localhost:8765/TestRepo/ --chrome /usr/bin/google-chrome
```

Also run `python3 -I dev/check_content.py` (`.pages.yml` and content parse; every key has a form field) and, after touching colours, `python3 -I dev/check_palettes.py`.

Also, after template changes:
- grep the built HTML for `src="/` or `href="/` paths that skip the subfolder;
- build once with sections emptied (no education files, empty `tools.yaml`, no About body, no `linkedin`) and confirm no trace of them, headings and menu included;
- if CSS changed, confirm every template class is styled, every styled class exists, and every `var(--…)` is defined (`--header-height` is set by script on purpose).

A local build is not the real test: the first GitHub build is, and Pages CMS behaviour can only be checked in Pages CMS. Say so.

**Clickable preview for Garrison** (optional): build with `relativeURLs = true` and `uglyURLs = true` (extra config file), change `href="./"`/`"../"` and `href="../#…"` to point at `index.html`, and publish the folder as a multi-file artifact. Never commit those settings.

## Common tasks

- **Add a section:** DESIGN.md section 10 lists the eight steps.
- **Swap or add a typeface:** `dev/build_fonts.py` (instructions at the top), then `main.css` sections 1–2, the `$fonts` map in `baseof.html`, and both select fields in `.pages.yml`.
- **Add or change a colour scheme:** DESIGN.md section 10; always run `python3 -I dev/check_palettes.py` after touching any colour.
- **Regenerate placeholder images:** `python3 -I dev/make_placeholders.py`.
- **Update the AI-training opt-out:** the crawler list and the `Content-Usage` / `Content-Signal` lines live in `themes/DrPhill/layouts/robots.txt`; the page tags in `baseof.html`. Check operators' current documentation and the IETF aipref drafts before changing them, and keep search crawlers open.

## After any change

Update `docs/DESIGN.md` (status, file map, history) and the README if students would notice. In the Project, update the instructor setup guide's current-state table rather than writing new docs.

## Do not

- Add a CSS framework, icon font, JavaScript library, or any outside request. (Analytics only as the student's opt-in choice in `analytics.html`; never on by default.)
- Edit generated output (`public/`, `resources/`).
- Use leading-slash paths, or `absURL` for in-site links (use `relURL` / `RelPermalink`).
- Push, change workflows, or change `.pages.yml` without Garrison's go-ahead.
- Present a local build or the artifact preview as proof that GitHub or Pages CMS works.
