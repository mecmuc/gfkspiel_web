# Deploying GfkSpiel on a New Linux Server — What Is Missing

This document describes everything needed to deploy the application on a fresh Linux server (Ubuntu/Debian assumed, matching the original Plesk setup).

---

## 1. Missing Source Files (Same Blocker as Local)

The compiled production assets (`static_prod/`) are present, so the server can technically run without the source files. However, to do a clean deploy from source (recommended), the missing files must first be retrieved:

| Missing File | Purpose |
|---|---|
| `www/js/app.js` | Main game logic (source) |
| `www/js/adapterWeb.js` | Frontend DB adapter (source) |
| `www/js/dbAccess.js` | DB access layer (dev) |
| `www/css/gfkspiel.css` | Game stylesheet (source) |

**Action:** Clone or pull from Bitbucket:

```bash
git clone git@bitbucket.org:Koblaid/gfkspiel2.git /var/local/gfkspiel.de/gfkspiel2
```

---

## 2. System Packages

Install required build tools and runtime dependencies:

```bash
apt-get update
apt-get install -y \
  git \
  curl \
  build-essential \
  python2 \
  sqlite3
```

`build-essential` and `python2` are needed to compile the `sqlite3` native Node.js addon.

---

## 3. Node.js via NVM

The server uses Node.js 0.10 managed via NVM. Install NVM and the correct Node version:

```bash
# Install NVM to /var/local/gfkspiel.de/nvm (matching original setup)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
export NVM_DIR="/var/local/gfkspiel.de/nvm"

nvm install 0.10
nvm use 0.10
nvm alias default 0.10
```

> If upgrading Node.js is acceptable, Node 12 LTS is the newest version still compatible with Express 3.x and the `sqlite3` 2.x bindings. This would avoid the NVM 0.10 requirement. Anything above Node 12 requires updating Express and sqlite3.

---

## 4. npm Dependencies

From the `web/` directory:

```bash
cd /var/local/gfkspiel.de/gfkspiel2/web
npm install
```

This installs all dependencies listed in `package.json`, including native compilation of `sqlite3`.

---

## 5. Forever (Process Manager)

Forever is used to keep the server running and restart it on crashes:

```bash
npm install -g forever
```

---

## 6. Grunt CLI (for building production assets)

Required if deploying from source (not using pre-built `static_prod/`):

```bash
npm install -g grunt-cli
cd /var/local/gfkspiel.de/gfkspiel2/web
grunt build   # or the appropriate task — check Gruntfile.js
```

Skip this step if deploying the existing compiled `static_prod/` files directly.

---

## 7. SQLite Database

The game database must exist at `../database/gfkspiel.db` relative to `web/` (i.e. `/var/local/gfkspiel.de/gfkspiel2/database/gfkspiel.db`).

**Options:**
- Copy the database from the old server via `scp` or `rsync`
- Restore from a backup

There is no schema migration script or seed file in the repository, so there is no way to create the database from scratch without the original data.

**Action:** Transfer from old server:

```bash
scp old-server:/var/local/gfkspiel.de/gfkspiel2/database/gfkspiel.db \
    /var/local/gfkspiel.de/gfkspiel2/database/gfkspiel.db
```

---

## 8. Log Directory

`server.js` writes to `/var/log/gfkspiel.de/game.log`. Create the directory and set ownership:

```bash
mkdir -p /var/log/gfkspiel.de
chown <app-user>:<app-user> /var/log/gfkspiel.de
```

Replace `<app-user>` with the user that runs the Node process (see section 10).

---

## 9. Port 80 Access

`server.js` in production mode binds to port 80 and then drops privileges. This requires either:

- **Running the initial bind as root** (current approach — the process starts as root, binds port 80, then drops to a lower-privilege user)
- **Or using authbind / setcap** to allow a non-root user to bind port 80:

```bash
# Alternative: allow node to bind privileged ports without root
setcap 'cap_net_bind_service=+ep' $(which node)
```

The current `server.js` handles this by calling `process.setuid`/`process.setgid` after binding, so starting as root works as-is.

---

## 10. System User for the App

It is good practice to run the server under a dedicated non-root user. The original setup appears to do this (server drops privileges after binding). Create the user if it doesn't exist:

```bash
useradd --system --no-create-home gfkspiel
chown -R gfkspiel:gfkspiel /var/local/gfkspiel.de/gfkspiel2
chown -R gfkspiel:gfkspiel /var/log/gfkspiel.de
```

Then update `server.js` lines that call `process.setuid`/`process.setgid` to match this username.

---

## 11. Firewall

Open port 80 (and optionally 443 if HTTPS is added later):

```bash
ufw allow 80/tcp
ufw allow 443/tcp   # optional
ufw enable
```

---

## 12. HTTPS / TLS (Not Currently Configured)

The original setup has no HTTPS. For a new server, TLS should be added. The simplest approach is a reverse proxy using **nginx** + **Let's Encrypt**:

```bash
apt-get install -y nginx certbot python3-certbot-nginx
```

Change `server.js` production port from 80 to 3000 (local only), then configure nginx to proxy requests to it and handle TLS termination. This also avoids the port 80 privilege issue entirely.

---

## 13. Email Alerts (Production Logging)

`server.js` sends error emails via Gmail SMTP. The credentials are hardcoded in the source. For a new deploy:

- Verify the Gmail account (`gfkspiel@gmail.com`) is still active
- If using Gmail with 2FA, generate an **App Password** and update line 98 of `server.js`
- Alternatively, replace `winston-mail` with a different transport (e.g. SendGrid, SES)

---

## 14. Starting and Enabling on Boot

Start the server via the management script:

```bash
cd /var/local/gfkspiel.de/gfkspiel2/web
./manage_server.sh start
```

To start automatically on boot, create a systemd service (Forever does not register itself with systemd):

```ini
# /etc/systemd/system/gfkspiel.service
[Unit]
Description=GfkSpiel Node.js Server
After=network.target

[Service]
Type=forking
User=root
WorkingDirectory=/var/local/gfkspiel.de/gfkspiel2/web
ExecStart=/var/local/gfkspiel.de/nvm/versions/node/v0.10.13/bin/forever start server.js --production
ExecStop=/var/local/gfkspiel.de/nvm/versions/node/v0.10.13/bin/forever stop server.js
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable gfkspiel
systemctl start gfkspiel
```

---

## 15. Static Fallback Site

Copy the static fallback site to the default vhost root so visitors see the "server offline" page if the Node process is down:

```bash
cp -r var/www/vhosts/default/htdocs/* /var/www/html/
```

This only applies if nginx or Apache is also serving the vhost directly.

---

## Summary Checklist

- [ ] Clone repo from Bitbucket (includes missing source files)
- [ ] `apt-get install build-essential python2 git curl sqlite3`
- [ ] Install NVM and Node.js 0.10 (or Node 12 if upgrading)
- [ ] `npm install` from `web/`
- [ ] `npm install -g forever`
- [ ] Transfer `database/gfkspiel.db` from old server
- [ ] Create `/var/log/gfkspiel.de/` with correct ownership
- [ ] Create `gfkspiel` system user and set file ownership
- [ ] Open port 80 in firewall
- [ ] (Recommended) Set up nginx reverse proxy + Let's Encrypt for HTTPS
- [ ] Verify/update Gmail credentials in `server.js` line 98
- [ ] Create systemd service for auto-start on boot
- [ ] Start server: `./manage_server.sh start`
- [ ] Copy static fallback site to web root
