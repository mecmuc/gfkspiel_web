# Deploying GfkSpiel on a New Linux Server — Using Existing Static Assets

This plan deploys the application using the pre-built files already present in this repository snapshot — no Bitbucket clone, no Grunt build step required.

---

## 1. System Packages

```bash
apt-get update
apt-get install -y git curl build-essential python3 sqlite3
```

`build-essential` and `python3` are needed to compile the `sqlite3` native Node.js addon during `npm install`. (`python2` is no longer available on Ubuntu 22.04+.)

---

## 2. Node.js via NVM

```bash
mkdir -p /var/local/gfkspiel.de/nvm
export NVM_DIR="/var/local/gfkspiel.de/nvm"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source $NVM_DIR/nvm.sh
nvm install 12
nvm use 12
nvm alias default 12
```

> Node 12 LTS is required on modern Linux. Node 0.10 is incompatible with current build tools.

---

## 3. Copy Application Files to Server

Copy the following to the server (e.g. via FileZilla):

**`web/` → `/var/local/gfk-spiel.de/gfkspiel2/web/`**
```
web/
├── server.js
├── adapterNode.js
├── package.json
├── index_prod.html
├── manage_server.sh
└── static_prod/
    ├── js/gfkspiel2.min.js
    └── css/gfkspiel2.min.css
```

**`www/` → `/var/local/gfk-spiel.de/gfkspiel2/www/`** (required by server at runtime)
```
www/
├── js/dbAccess.js        ← required by server.js
└── html/index_body.html  ← required by server.js
```

**Additional assets into `static_prod/`:**
```
www/lib/  → static_prod/lib/   (jQuery Mobile, Font Awesome CSS, etc.)
www/font/ → static_prod/font/  (Font Awesome webfont files — required for icons/checkboxes!)
www/img/  → static_prod/img/   (game images, favicon)
```

**Audio files** (voice and ending music):
```
audio/    → /var/local/gfk-spiel.de/gfkspiel2/audio/
```
The server serves these via the `/audio` route in `server.js`.

---

## 4. Install npm Dependencies

On the server, from the `web/` directory:

```bash
cd /var/local/gfkspiel.de/gfkspiel2/web
npm install sqlite3@5 --save --production
npm install --production
```

`sqlite3` in `package.json` is version `~2.1.9` which is incompatible with Node 12. The first command upgrades it to v5 (compatible with Node 12 + Python 3) and updates `package.json`. The second installs the remaining dependencies.

---

## 5. Transfer the SQLite Database

There is no schema or seed script — the database must be copied from the old server:

```bash
scp old-server:/var/local/gfkspiel.de/gfkspiel2/database/gfkspiel.db \
    /var/local/gfkspiel.de/gfkspiel2/database/gfkspiel.db
```

---

## 6. Log Directory

```bash
mkdir -p /var/log/gfkspiel.de
chown <app-user>:<app-user> /var/log/gfkspiel.de
```

---

## 7. Install Forever and Start the Server

```bash
npm install -g forever@3
cd /var/local/gfkspiel.de/gfkspiel2/web
./manage_server.sh start
```

Use `forever@3` — newer versions pull in dependencies that require Node 15+ and fail with a syntax error on Node 12.

The server starts in production mode on port 3000 and serves `static_prod/` with `index_prod.html`.
nginx acts as reverse proxy in front of Node.js — see `plan_https_nginx.md`.

---

## 8. Firewall

```bash
ufw allow 80/tcp
ufw enable
```

---

## 9. Auto-start on Boot (systemd)

Use `Type=simple` and run node directly — do **not** use forever here, it conflicts with systemd.
The service file is in the repo as `gfkspiel.service`. Upload it to `/etc/systemd/system/gfkspiel.service`.

If a forever process is already running, kill it first before starting the service (forever's monitor
daemonizes with PID 1 as parent and respawns node on kill):

```bash
ps -ef | grep node   # find the forever monitor PID
kill -9 <monitor-pid> <node-pid>
```

Then enable and start:

```bash
systemctl daemon-reload
systemctl enable gfkspiel
systemctl start gfkspiel
```

```bash
systemctl daemon-reload
systemctl enable gfkspiel
systemctl start gfkspiel
```

---

## Summary Checklist

- [ ] `apt-get install build-essential python3 git curl sqlite3`
- [ ] Install NVM and Node.js 12
- [ ] Copy `web/`, `www/js/`, `www/html/`, `www/lib/` → `static_prod/lib/`, `www/font/` → `static_prod/font/`, `www/img/` → `static_prod/img/`
- [ ] Copy `audio/` → `/var/local/gfk-spiel.de/gfkspiel2/audio/`
- [ ] `npm install sqlite3@5 --save --production` then `npm install --production` from `web/`
- [ ] Transfer `database/gfkspiel.db` from old server
- [ ] Create `/var/log/gfkspiel.de/` with correct ownership
- [ ] Upload `gfkspiel.service` to `/etc/systemd/system/` and enable it
- [ ] Install nginx and configure HTTPS + HTTP→HTTPS redirect (see `plan_https_nginx.md`)
