# gfkspiel_web

Website and game server for **gfk-spiel.de** — a free multiplayer learning game for Gewaltfreie Kommunikation (Nonviolent Communication / NVC), based on a board game by Klaus Karstädt.

## Real project structure

```
var/local/gfkspiel.de/gfkspiel2/   ← the actual game (Node.js server)
  web/
    index_prod.html                 ← HTML wrapper served to browser
    static_prod/
      css/
        gfkspiel2.min.css           ← ← production CSS (git-tracked, deploy this)
      js/
        gfkspiel2.min.js
      lib/
        jquery.mobile-1.3.2.min.css
        font-awesome.min-3.2.1.css
  www/
    css/
      gfkspiel.css                  ← source CSS (edit here, NOT git-tracked)
    html/
      index_body.html               ← all jQuery Mobile pages (edit here, NOT git-tracked)
    js/
      app.js                        ← game JS (do not touch)

var/www/vhosts/default/htdocs/      ← nginx static fallback (old info pages, not the game)
planning/                           ← planning documents
```

## Deployment workflow

After editing source files, rebuild and upload:

| Source (edit here) | Build command | Upload to server |
|---|---|---|
| `www/css/gfkspiel.css` | `npx clean-css-cli www/css/gfkspiel.css -o web/static_prod/css/gfkspiel2.min.css` | `web/static_prod/css/gfkspiel2.min.css` |
| `www/js/app.js` | `npx terser www/js/app.js www/js/adapterWeb.js --compress --mangle -o web/static_prod/js/gfkspiel2.min.js` | `web/static_prod/js/gfkspiel2.min.js` |
| `www/js/router.js` | `npx terser www/js/router.js --compress --mangle -o web/static_prod/js/router.js` | `web/static_prod/js/router.js` |
| `www/html/index_body.html` | (no build step) | `www/html/index_body.html` ← injected by Node.js server at runtime |
| `web/index_prod.html` | (no build step) | `web/index_prod.html` |

Hard-refresh browser after uploading (Cmd+Shift+R) — CSS/JS are cached aggressively.

## Stack

- **Server**: Node.js (port 3000) behind nginx, hosted on Ubuntu
- **Frontend**: vanilla JS + Font Awesome 3.2.1 — no framework, no jQuery
- **Router**: custom `router.js` (~60 lines) handles hash-based page navigation
- **CSS**: `gfkspiel.css` — clean CSS using `.page`, `.page-header`, `.page-content`
- **Build**: `terser` (JS minification) + `clean-css-cli` (CSS minification) via `npx`
- **German-language content**
- jQuery Mobile and jQuery core both removed. See `planning/framework-migration.md`.

## Key CSS / HTML facts

- Pages are `<div class="page" id="page-...">` — router shows/hides them
- `.bg-*` color classes (bg-green, bg-gray, etc.) are set by JS on the `<a>` tag inside list `<li>` items
- List items: `<ul id="choicelist"><li><a class="bg-gray ...">` — `<a>` carries the color, `<li>` is unstyled
- Font Awesome 3.x: icon classes are `icon-play-circle`, `icon-info-sign`, etc. (not `fa fa-*`)

## Off-limits

- Do not read `*.db` files (SQLite databases contain user data)
- Do not modify `web/static_prod/js/gfkspiel2.min.js` — game logic

## Notes

- Contact: gfkspiel@gmail.com
- Android app: Google Play; iOS app: App Store
