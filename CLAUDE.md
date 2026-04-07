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

1. Edit `www/css/gfkspiel.css`
2. Copy to production: `echo "/*! gfkspiel2 */" > web/static_prod/css/gfkspiel2.min.css && cat www/css/gfkspiel.css >> web/static_prod/css/gfkspiel2.min.css`
3. Upload `web/static_prod/css/gfkspiel2.min.css` to server
4. Hard-refresh browser (Cmd+Shift+R) — CSS is cached aggressively

## Stack

- **Server**: Node.js (port 3000) behind nginx, hosted on Ubuntu
- **Frontend**: jQuery 1.10.2 + Font Awesome 3.2.1 — no build system, no framework
- **Router**: custom `router.js` (~60 lines) handles hash-based page navigation
- **CSS**: `gfkspiel.css` — clean CSS using `.page`, `.page-header`, `.page-content`
- **German-language content**
- jQuery Mobile was removed (EOL 2021). See `planning/framework-migration.md`.

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
