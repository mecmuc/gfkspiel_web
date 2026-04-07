# Modernizing gfk-spiel.de

---

## Scope

Modernize the complete game UI — all jQuery Mobile pages in `index_body.html` — by updating the custom CSS (`gfkspiel.css`) and cleaning up the HTML. jQuery Mobile itself stays (replacing it would require rewriting all JS).

The earlier standalone info-page approach (htdocs `index.html`, `links.html`, `impressum.html`) was a mistake — those are not served by the live game server. Those files can be ignored.

---

## Architecture

```
www/css/gfkspiel.css          ← source CSS (edit here)
  ↓ (manual copy, no build)
web/static_prod/css/gfkspiel2.min.css   ← served in production

www/html/index_body.html      ← all jQuery Mobile pages (edit here)

web/index_prod.html           ← wrapper: loads jQuery Mobile CSS + gfkspiel2.min.css
```

`index_prod.html` loads:

1. `lib/jquery.mobile-1.3.2.min.css`
2. `lib/font-awesome.min-3.2.1.css`
3. `css/gfkspiel2.min.css` ← our custom overrides go last

---

## Color palette (refined, not replaced)

All NVC hues stay; shades are tightened from browser named-colors to proper hex values.

| Role                           | Current          | Proposed         |
| ------------------------------ | ---------------- | ---------------- |
| Page background gradient start | `#105694`        | `#1a5fa8`        |
| Page background gradient end   | `#4a74da`        | `#4d8fd4`        |
| Body/backdrop                  | `#111111`        | `#0d1b2a`        |
| `bg-green` (primary action)    | `#64c11b`        | `#5cb81c`        |
| `bg-gray` (secondary)          | `#565656`        | `#5a5a5a`        |
| `bg-bluegray` (settings)       | `#508279`        | `#4a7a72`        |
| `bg-contentblue` (list items)  | `#0e5593`        | `#0e5593` (keep) |
| `bg-red`                       | `#ff4141`        | `#e83030`        |
| `bg-yellow`                    | `#dd8700`        | `#d68200`        |
| `bg-green-result`              | `#008d3b`        | `#008d3b` (keep) |
| `bg-red-result`                | `#d80e00`        | `#cc0d00`        |
| Link color                     | `#ffffaa`        | `#f5c842`        |
| Link hover                     | `#ffffaa` (same) | `#ffd700`        |

---

## Typography

- Replace `"Lucida Grande",helvetica` with `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
- Line-height: `1.7` (up from `1.4em`)
- Applied via the existing font-family override in `gfkspiel.css`

---

## Buttons (pass 1 — flat colors, done)

- Stripped jQuery Mobile's built-in gradients, borders, box-shadows via `.ui-btn-up-c` overrides
- Flat solid colors for all `.bg-*` classes
- `border-radius: 8px` on menu buttons, `6px` on nav/list buttons

## Layout & shape (pass 2)

**Nav buttons** (`Menü`, `Hilfe`, `Weiter`, `Zurück`, etc.):

- Pill shape: `border-radius: 50px` on button + inner span (jQM wraps both)

**Menu buttons** (`Spielen`, `Info`, etc.):

- Rounder: `border-radius: 16px`
- Narrower margins: `margin: 3% 10%` with more vertical gap between buttons

**Choice list items** (answer options during game):

- Rounder: `border-radius: 12px`
- More padding inside each item

**Content areas**:

- Add `padding: 12px 0` to `.ui-content` so text doesn't hug the edges
- Consistent `8%` horizontal margin on content text

**Form elements** (new game page — player names, round selector, checkboxes):

- Inputs: semi-transparent white background (`rgba(255,255,255,0.15)`), white border, rounded
- Select dropdown: same treatment
- Checkboxes: transparent background, white border, rounded

**Header bar**:

- Already darkened; reduce vertical padding slightly for a tighter feel

---

## HTML cleanup (`index_body.html`)

- Remove deprecated `align="center"` / `align="justify"` attributes throughout
- Remove `width="100%"` on `<table>` tags
- Remove dead Google+ badge (`#googleplusbadge`) — platform shut down 2019
- Move inline `style=""` width/padding on content divs to CSS classes where practical
- Remove vendor-prefixed gradient comments (already in CSS, not needed in HTML)
- Remove `<p align="justify"> </p>` spacer hacks

---

## Files to change

| File                                    | Changes                                                                          | Done |
| --------------------------------------- | -------------------------------------------------------------------------------- | ---- |
| `www/css/gfkspiel.css`                  | Refined colors, better typography, flat buttons (pass 1) + layout/shape (pass 2) | ✓    |
| `web/static_prod/css/gfkspiel2.min.css` | Replace with updated CSS from above                                              | ✓    |
| `www/html/index_body.html`              | Remove deprecated attrs, dead badge, spacer hacks                                | ✓    |
| `CLAUDE.md`                             | Update to reflect real project structure (game server, not static pages)         | ✓    |

## Files NOT changed

- `web/index_prod.html` — wrapper is fine as-is
- `web/static_prod/js/gfkspiel2.min.js` — no JS changes
- `lib/` — jQuery Mobile and Font Awesome stay
- `var/www/vhosts/default/htdocs/` — not deployed by the game server

---

## What stays the same

- jQuery Mobile framework (upgrading would break JS)
- All game logic and page structure
- All NVC color hues
- All German text content
- The blue gradient page background feel
