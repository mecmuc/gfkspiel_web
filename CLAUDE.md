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
- **Frontend**: jQuery Mobile 1.3.2 + Font Awesome 3.2.1 — no build system
- **CSS**: custom overrides in `gfkspiel.css` loaded after jQM stylesheet
- **German-language content**

## Key CSS facts

- `.bg-*` color classes (bg-green, bg-gray, etc.) are set by JS on the `<a>` tag inside listview `<li>` items
- jQM wraps list items: `<li class="ui-btn ui-li">` → `<a class="bg-gray ui-link-inherit">` → `<span class="ui-btn-inner">`
- To color list items: make `<li>` transparent + overflow:hidden, let `<a>`'s bg-* show through, make `<span>` transparent
- Use `.ui-shadow { box-shadow: none !important }` to kill jQM's drop shadows

## Off-limits

- Do not read `*.db` files (SQLite databases contain user data)
- Do not modify `web/static_prod/js/gfkspiel2.min.js` — game logic

## Notes

- Contact: gfkspiel@gmail.com
- Android app: Google Play; iOS app: App Store
