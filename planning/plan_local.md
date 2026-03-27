# Running GfkSpiel Locally — What Is Missing

This document describes what needs to be in place before the application can be run locally in development mode.

---

## 1. Missing Source Files (Blockers)

The development workflow requires source files that are **not present** in this repository snapshot. Only the compiled/minified output files (`static_prod/`) exist. Without these, you can run the production build but cannot develop or rebuild assets.

| Missing File | Referenced In | Purpose |
|---|---|---|
| `www/js/app.js` | `Gruntfile.js` (concat src) | Main game logic (source) |
| `www/js/adapterWeb.js` | `Gruntfile.js` (concat src) | Frontend DB adapter (source) |
| `www/js/dbAccess.js` | `index_devel.html` | DB access layer for development |
| `www/css/gfkspiel.css` | `Gruntfile.js` (cssmin src) | Game stylesheet (source) |
| `www/html/index_body.html` | `index_devel.html` (assumed) | HTML partial for the game UI |

**Action:** Retrieve these files from the Bitbucket repository (`git@bitbucket.org:Koblaid/gfkspiel2.git`). The `gfkspiel2/` directory already contains a `.git` folder pointing to this remote — check if there are untracked/gitignored paths or a separate branch with source files.

---

## 2. Node.js Version

The server requires **Node.js 0.10** (specifically 0.10.13 as installed via NVM on the server). Modern Node.js versions are incompatible with Express 3.x and the `sqlite3 ~2.1.9` binding.

**Action:** Install NVM locally and use it to install Node 0.10:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 0.10
nvm use 0.10
```

Alternatively, use Docker with a Node 0.10 image (see section 7).

---

## 3. npm Dependencies

`node_modules/` is present in the server snapshot (copied from the live server), but it should not be used directly — it was built on Linux for a different architecture. Dependencies must be reinstalled locally.

**Action:** From `var/local/gfkspiel.de/gfkspiel2/web/`:

```bash
npm install
```

Note: `sqlite3` compiles native bindings. You'll need build tools:
- macOS: Xcode Command Line Tools (`xcode-select --install`)
- Linux: `build-essential`, `python2`

---

## 4. SQLite Database

The game reads from `../database/gfkspiel.db` (relative to the `web/` directory), i.e. `var/local/gfkspiel.de/gfkspiel2/database/gfkspiel.db`.

**Check:** Verify this file exists and is not empty:

```bash
ls -lh var/local/gfkspiel.de/gfkspiel2/database/
```

If the file is missing or empty, the AJAX endpoints will fail. You would need either a database export from the live server or a seed/schema script (not currently present in the repo).

---

## 5. Log Directory

`server.js` writes logs to `/var/log/gfkspiel.de/game.log`. This path does not exist locally and the server will fail to start if it cannot create/write the log file.

**Action:** Create the directory before starting the server:

```bash
sudo mkdir -p /var/log/gfkspiel.de
sudo chown $(whoami) /var/log/gfkspiel.de
```

Or patch `server.js` to use a local path (e.g. `./logs/game.log`) for development.

---

## 6. Grunt Build Tool (for development mode only)

To rebuild assets or run the development watcher, Grunt CLI must be installed globally:

```bash
npm install -g grunt-cli
```

Then from `var/local/gfkspiel.de/gfkspiel2/web/`:

```bash
grunt  # runs watch mode (default task)
```

This is only needed if you want to modify and rebuild JS/CSS. The production build in `static_prod/` already exists and does not require this step to run the server.

---

## 7. Starting the Server

Once all the above is in place, start in development mode:

```bash
cd var/local/gfkspiel.de/gfkspiel2/web
node server.js
# server starts on http://localhost:3000
```

Or use the management script (requires Forever):

```bash
npm install -g forever
./manage_server.sh start
```

---

## 8. Optional: Docker Approach

Because of the very old Node.js version, Docker is the cleanest local setup:

```dockerfile
FROM node:0.10
WORKDIR /app
COPY var/local/gfkspiel.de/gfkspiel2/ .
RUN cd web && npm install
RUN mkdir -p /var/log/gfkspiel.de
WORKDIR /app/web
CMD ["node", "server.js"]
```

```bash
docker build -t gfkspiel .
docker run -p 3000:3000 gfkspiel
```

---

## Summary Checklist

- [ ] Retrieve missing source files from Bitbucket (`www/js/app.js`, `www/js/adapterWeb.js`, `www/js/dbAccess.js`, `www/css/gfkspiel.css`)
- [ ] Install Node.js 0.10 via NVM (or use Docker)
- [ ] Run `npm install` from `web/` with native build tools available
- [ ] Confirm `database/gfkspiel.db` exists and has content
- [ ] Create `/var/log/gfkspiel.de/` directory (or patch log path in `server.js`)
- [ ] (Optional) Install `grunt-cli` globally if rebuilding assets
- [ ] Start server: `node server.js` → open `http://localhost:3000`
