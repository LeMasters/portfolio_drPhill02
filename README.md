# DrPhill — student portfolio

A plain, fast portfolio site. You edit it in **Pages CMS**; **GitHub** builds it with Hugo and publishes it at `https://your-username.github.io/your-repository/`.

You never need to install anything or touch code. Everything you write is kept in ordinary text files that you own and can take to any other site.

## Editing your site

Open [app.pagescms.org](https://app.pagescms.org), choose this repository, and use the six forms:

| Form | What it holds | Leave it empty and… |
|---|---|---|
| **Profile** | Your name, area of expertise, email, LinkedIn and GitHub addresses, other links, résumé (PDF), your About paragraph, and three settings: AI training (off unless you turn it on), an optional Google Search Console code, and visitor statistics (off unless you choose a service) | …the About section, Contact section, LinkedIn button or GitHub button disappears |
| **Projects** | One entry per project: title, caption, description, order, image, year, role, links, tags | …there are no projects on the page |
| **Gallery** | One entry per image: title, image, image description, order, caption | …the Gallery page and its menu link disappear |
| **Education** | One entry per degree or certificate: degree, school, year, order, optional detail | …the Education section disappears |
| **Tools** | The software and tools you use, each with an optional note | …the Tools section disappears |
| **Appearance** | Colour scheme (Ink or Dusk), typeface for text, typeface for titles | (defaults are used: Ink, Atkinson, Fraunces) |

Each save publishes the site again within a minute or two. The menu at the top lists only the sections that have something in them.

**Don't see your change?** Wait two minutes, then refresh the page (on a Mac, Cmd-Shift-R; on Windows, Ctrl-F5). Browsers often show a copy of a page they saved earlier. If it still hasn't changed, open your repository on GitHub and look at the **Actions** tab: a red ✗ means the site didn't rebuild, and your previous site is still online.

### What happens when you save

1. Pages CMS saves your words and images into your repository on GitHub (it records every version, so nothing is lost).
2. GitHub notices the change and runs **Hugo**, a program that turns your files into a finished website. Hugo makes smaller copies of your images for phones and laptops, builds a page for each project and gallery image, and adds the details search engines and link previews need.
3. GitHub Pages publishes the result.

Nothing runs on your site itself; it is plain web pages, which is why it's fast. The full details are in `docs/DESIGN.md`, section 2.

### Projects: how they are laid out

All your projects appear on the home page, in **Order** (1 first). The layout adjusts to how many you have:

| Projects | Layout |
|---|---|
| 1 | One wide project |
| 2 | Two side by side |
| 3 | One wide, then two side by side |
| 4 or more | One wide, then rows of three; a last row that isn't full lines up from the left |

On a phone, rows of three stack into one column; pairs stay side by side.

### Images

Upload images through the Projects form. Recommended: **1800 × 1200 px (3:2), under about 400 KB**. The site makes smaller copies for phones automatically, with tidy names: spaces and unusual characters become underscores (`My level 2.png` → `My_level_2-800w.webp`). Your original keeps its name in the repository. The wide feature crops the top and bottom of the image a little (the placeholder images show how much).

Gallery images can be any shape. The Gallery page shows a square crop of each; clicking one opens its own page with the whole image, its title and your caption, and links to the previous and next image. Up to 2000 px on the long side, under about 500 KB.

Always fill in **Image description**: it is read aloud to people who cannot see the image.

### Links

Type full addresses (`https://…`). If you forget the `https://`, the site adds it for you.

### AI training and search

By default your site asks AI companies not to use it to train their models. It does this in every page (a TDM-reservation tag, the opt-out recognised under EU copyright law, plus informal "noai" tags) and in a `robots.txt` file listing the main AI-training crawlers. Search engines, including AI search tools that link back to you, are still welcome. To allow AI training instead, switch on **Allow AI companies to train on this site** in Profile.

These are requests: reputable companies honour them, but nothing technical can force a crawler to comply. A `robots.txt` file only works when the site is at the top of its web address (`your-username.github.io` or your own domain), not in a subfolder; the page tags work everywhere.

To help people find you in search: write a clear area of expertise and project captions, describe every image, link to your portfolio from LinkedIn, itch.io and anywhere else you are, and (optionally) add your site to Google Search Console and paste its verification code into Profile.

### Visitor statistics (optional)

Your site can count its visitors using one of two free services. Neither uses cookies or collects visitors' personal details, so you don't need a cookie banner. The numbers are private: only you see them, in the service's dashboard; nothing appears on your site. Pick one:

**GoatCounter**: simplest; a small independent service.

1. Go to [goatcounter.com](https://www.goatcounter.com) and choose **Sign up**.
2. Pick a **code**: a short name such as `janedoe`. Your dashboard will be at `janedoe.goatcounter.com`. Add your email and a password.
3. In Pages CMS, open **Profile**. Set **Analytics** to **GoatCounter** and type your code (just `janedoe`) in **Analytics code**. Save.

**Cloudflare Web Analytics**: run by a large company; also shows how fast your pages load.

1. Create a free account at [cloudflare.com](https://www.cloudflare.com). You don't need to move your site or change any settings on GitHub.
2. In the Cloudflare dashboard, open **Web Analytics** and choose **Add a site**.
3. For the hostname, type your site's address without `https://` or any folder: `your-username.github.io` (or your own domain). Choose **Done**.
4. Cloudflare shows a short piece of code (a "JS snippet"). Copy all of it.
5. In Pages CMS, open **Profile**. Set **Analytics** to **Cloudflare Web Analytics** and paste the snippet into **Analytics code**. Save.

**Then check it works.** Wait for the site to publish (a minute or two), visit it from your phone, and look at your dashboard; your visit should appear within a few minutes. If nothing appears:

- Turn off any ad blocker for your site. Ad blockers often stop these services, which also means real visitor counts run a little low.
- Check the code you pasted. If the site can't recognise it, it leaves analytics out rather than breaking. The GitHub **Actions** tab then shows a yellow warning on that build starting "Analytics:".
- Visits are not counted while you preview your site on your own computer.

**To stop counting**, set **Analytics** back to **NONE**.

### Your web address

Your site starts at `https://your-username.github.io/your-repository/`. You can give it an address of your own (such as `janedoe.com`, about $11 a year): see the separate guide *How to Set Up Your Own Domain Name*. Nothing in your content changes; the site picks up its new address on the next publish.

## Where your content lives

| File | What it is |
|---|---|
| `content/_index.md` | Your profile; the text below the `---` lines is your About paragraph |
| `content/projects/*.md` | One file per project |
| `content/gallery/*.md` | One file per gallery image; the text below the `---` lines is its caption |
| `content/education/*.md` | One file per degree or certificate |
| `data/tools.yaml` | Your tools |
| `data/style.yaml` | Your colour scheme and typeface choices (appearance, not content) |
| `static/images/`, `static/files/` | Your uploaded images and files |

These are plain Markdown and YAML files. To move your portfolio somewhere else, download the repository (Code → Download ZIP): your words and images come with you.

## Everything else

| Path | What it is |
|---|---|
| `themes/DrPhill/` | The design (templates, styles, fonts). The same for every student. |
| `hugo.toml` | Site settings |
| `.pages.yml` | The Pages CMS forms |
| `.github/workflows/hugo.yml` | Builds and publishes the site on every save |
| `docs/DESIGN.md` | How the theme works and why (for instructors and maintainers) |
| `CLAUDE.md`, `dev/` | Instructions and test scripts for maintaining the theme |

## Typefaces

Four open-source typefaces are included and served from your own site (no requests to Google or any other company). Choose one for text and one for titles in **Appearance**:

| Choice | Designer | Kind |
|---|---|---|
| Atkinson Hyperlegible Next (default for text) | Braille Institute | Sans-serif, designed for legibility |
| Inter | Rasmus Andersson | Sans-serif, neutral |
| Source Serif 4 | Frank Grießhammer / Adobe | Serif, classic |
| Fraunces (default for titles) | Undercase Type | Serif, expressive |

All four are licensed under the SIL Open Font License 1.1; each licence is in its folder under `themes/DrPhill/static/fonts/`.

## Credits

DrPhill theme © 2026 Garrison LeMasters, Miami University (Department of Emerging Technology in Business and Design). MIT licence (`themes/DrPhill/LICENSE`). Built with [Hugo](https://gohugo.io) and [Pages CMS](https://pagescms.org); fonts via [Fontsource](https://fontsource.org).
