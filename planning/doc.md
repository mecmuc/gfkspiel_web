# GfkSpiel Web — Project Documentation

## Overview

GfkSpiel is an online educational game for learning Nonviolent Communication (Gewaltfreie Kommunikation / GFK), based on the board game by Klaus Karstädt. It teaches players to distinguish observations from judgments, identify feelings and needs, make effective requests, and practice empathetic responses.

**Available platforms:** Web (this repo), Android, iOS
**Contact:** gfkspiel@gmail.com
**Website:** gfk-spiel.de

---

## Repository Layout

```
gfkspiel_web/
├── planning/                          # Planning and documentation
└── var/                               # Snapshot of Plesk Ubuntu server filesystem
    ├── lib/                           # System libraries (apt, dpkg — not relevant)
    ├── local/
    │   └── gfkspiel.de/
    │       ├── gfkspiel2/             # Main application (Git repo)
    │       │   ├── web/               # Node.js web server
    │       │   ├── audio/             # Voice recordings
    │       │   ├── database/          # SQLite database
    │       │   └── .git/              # Git history (origin: git@bitbucket.org:Koblaid/gfkspiel2.git)
    │       └── nvm/                   # Node Version Manager installation
    └── www/
        └── vhosts/
            └── default/htdocs/        # Static fallback site (shown when server is down)
```

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Runtime | Node.js | 0.10.13 |
| Web framework | Express | ~3.2.6 |
| Database | SQLite3 | ~2.1.9 |
| Frontend framework | jQuery Mobile | 1.3.2 |
| Build tool | Grunt | ~0.4.1 |
| Process manager | Forever | - |
| Logging | Winston | ~0.7.2 |
| Icons | Font Awesome | 3.2.1 |
| Client storage | Store.js | 1.3.9 |
| Scrolling | Overthrow.js | 0.6.6 |

---

## Application Components

### `web/server.js` — Express Server

The main server. Handles routing and serves the game.

**Modes:**
- **Development** (default): port 3000, serves `static_devel/`, renders `index_devel.html`
- **Production** (`--production` flag): port 80, serves `static_prod/`, renders `index_prod.html`; drops privileges after binding

**Routes:**
- `GET /` — serves the game index page
- `GET /ajax/*` — maps directly to methods on the database adapter (`adapterNode.js`)

**Logging:**
- Winston logger writing to `/var/log/gfkspiel.de/game.log`
- In production, errors are also emailed to `gfkspiel@gmail.com` via Gmail SMTP

**Note:** The Gmail SMTP password is hardcoded in `server.js` line 98.

---

### `web/adapterNode.js` — Database Adapter

SQLite3 wrapper used server-side.

**Database path:** `../database/gfkspiel.db`

**Methods:**
- `select(stmt, args, callback)` — executes a SELECT query and returns rows via callback

AJAX requests from the frontend hit `/ajax/<methodName>` and are dispatched to the matching method on this adapter.

---

### `web/Gruntfile.js` — Build Configuration

Grunt tasks for building production assets:

| Task | Input | Output |
|---|---|---|
| `concat` | `../www/js/app.js` + `../www/js/adapterWeb.js` | `../tmp/gfkspiel2.js` |
| `uglify` | `../tmp/gfkspiel2.js` | `static_prod/js/gfkspiel2.min.js` |
| `cssmin` | `../www/css/gfkspiel.css` | `static_prod/css/gfkspiel2.min.css` |
| `jshint` | JS source files | (lint output) |
| `csslint` | CSS source files | (lint output) |

Default task runs in watch mode for development.

**Note:** The source files referenced by Grunt (`www/js/app.js`, `www/js/adapterWeb.js`, `www/css/gfkspiel.css`) are **not present** in the working directory — only the compiled outputs in `static_prod/` exist.

---

### `web/manage_server.sh` — Server Management Script

Shell script for managing the Node.js process via Forever.

| Command | Description |
|---|---|
| `start` | Start server with Forever |
| `stop` | Stop the server |
| `restart` | Restart the server |
| `list` | List running Forever processes |
| `update` | `git pull` + `npm install` + Grunt build |
| `setup` | Initial clone, install Forever, `npm install` |

**Config:**
- Log dir: `/var/log/gfkspiel.de/`
- NVM dir: `/var/local/gfkspiel.de/nvm/`
- Node version: 0.10

---

### `web/static_prod/` — Compiled Frontend Assets

Pre-built production files:

- `js/gfkspiel2.min.js` — Compiled game logic (from `app.js` + `adapterWeb.js`)
- `css/gfkspiel2.min.css` — Compiled styles

**Key frontend objects (from minified source):**
- `AppStorage` — game state management (player names, scores, turns, settings)
- Task/field selection and progression logic
- Audio playback for positive/negative feedback
- Settings (sound on/off, voice selection, game mode)
- Video help system
- Game-over screen with quotes and images
- jQuery Mobile UI integration
- LocalStorage for persistent state via Store.js

---

### `web/index_devel.html` / `web/index_prod.html` — HTML Entry Points

Both files load the game SPA. Differences:
- `index_prod.html` loads minified assets and includes a cookie consent popup (via cdnjs.cloudflare.com)
- `index_devel.html` loads unminified source files for development

**External dependencies loaded:**
- jQuery Mobile 1.3.2 (JS + CSS)
- Font Awesome 3.2.1 (icons)
- Store.js 1.3.9 (localStorage wrapper)
- Overthrow.js 0.6.6 (scroll polyfill)

---

### `audio/` — Voice Recordings

All voice recordings are provided in both **OGG** and **MP3** formats.

**Voice actors:**
| ID | Name |
|---|---|
| 01 | Klaus |
| 02 | Sarina |
| 03 | Antonia |

**Feedback sound categories:**
- Positive: `sehr_erfreulich`, `saustark`, `stark`, `einwandfrei`, `wunderbar`, `hurra`, `holla_die_waldfee`, `hoert_hoert`, `ich_geh_mit_dir_konform_2`, `da_sind_wir_schon_zwei_die_das_so_sehen`, `der_hit`
- Negative: `geht_gar_nicht`, `konzentrier_dich`, `naa`, `naaa`, `ach_komm`, `lehn_ich_ab`, `kann_ja_mal_passieren`
- Game over: `end_1` through `end_8` (harp music by Heidi Pixner)

---

### `web/loganalyzer.py` — Analytics Script

Python script that parses `game.log` and generates usage statistics.

**Statistics tracked:**
- Method call frequency (which game features are used)
- Task completions per game field (20 learning fields, e.g. Tangram, Riskante Wörter, Empathische Vermutung)
- Video help views
- Voice actor usage per voice ID
- Correct vs. incorrect answer rates
- Sound format usage (MP3 vs. OGG)
- Session counts (IP-based)
- Timeline breakdowns (hourly, daily, weekly, monthly, yearly)

---

### `var/www/vhosts/default/htdocs/` — Static Fallback Site

Shown when the Node.js game server is not running.

**Pages:**
- `index.html` — Landing page with links to Android and iOS apps; shows "Der Server des GFK-Spiels läuft leider gerade nicht" when the game is offline. Google Analytics ID: `UA-40087022-1`
- `links.html` — External GFK resource links
- `impressum.html` — Legal/imprint page

**Credits (from impressum):**
| Role | Person |
|---|---|
| Content, Conception, Voice | Klaus Karstädt |
| Development, Conception | Jan Foshag |
| Development, Conception | Benjamin Arbogast |
| Design | Mario Metzger |
| Testing, Voice | Sarina Konrad |
| Voice | Antonia Kahlau |
| Content Review | Gerhard Lorenz |
| Harp Music | Heidi Pixner |

---

## Game Content

The game covers 20 NVC learning fields:

1. Tangram
2. Riskante Wörter
3. Sinnvolle Bitte?
4. Empathische Vermutung?
5. Bedürfnis passt hier?
6. Welche Strategie passt hier?
7. Um welches Bedürfnis geht es?
8. Bedürfnis oder nicht?
9. Im Wolfscafé
10–20. Various perception, feeling, and communication exercises

---

## Known Issues / Technical Debt

- **Missing source files:** `www/js/app.js`, `www/js/adapterWeb.js`, `www/js/dbAccess.js`, `www/css/gfkspiel.css`, `www/html/index_body.html` are referenced in `Gruntfile.js` and `index_devel.html` but not present in the repo snapshot
- **Hardcoded credentials:** Gmail SMTP password in `server.js` line 98
- **Outdated stack:** Node.js 0.10.13 (2013), Express 3.x (EOL), jQuery Mobile 1.3.2 (EOL)
- **No HTTPS:** No TLS configuration visible
- **Old dependencies:** All npm packages are several major versions behind
