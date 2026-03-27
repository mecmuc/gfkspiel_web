# Deploying GfkSpiel on a New Linux Server — Using Existing Static Assets

This plan deploys the application using the pre-built files already present in this repository snapshot — no Bitbucket clone, no Grunt build step required.

---

## 1. System Packages

```bash
apt-get update
apt-get install -y git curl build-essential python2 sqlite3
```

`build-essential` and `python2` are needed to compile the `sqlite3` native Node.js addon during `npm install`.

---

## 2. Node.js via NVM

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
export NVM_DIR="/var/local/gfkspiel.de/nvm"
nvm install 0.10
nvm use 0.10
nvm alias default 0.10
```

> Node 12 LTS is the highest version still compatible with Express 3.x and `sqlite3 ~2.1.9` if you want to avoid Node 0.10.

---

## 3. Copy Application Files to Server

Copy the relevant parts of this repo snapshot to the server. You do **not** need the `www/` source directories — only the server code and pre-built assets:

```bash
rsync -av \
  var/local/gfkspiel.de/gfkspiel2/web/ \
  new-server:/var/local/gfkspiel.de/gfkspiel2/web/
```

The key files being deployed:

```
web/
├── server.js
├── adapterNode.js
├── package.json
├── index_prod.html
├── static_prod/
│   ├── js/gfkspiel2.min.js
│   └── css/gfkspiel2.min.css
└── manage_server.sh
```

---

## 4. Install npm Dependencies

On the server, from the `web/` directory:

```bash
cd /var/local/gfkspiel.de/gfkspiel2/web
npm install --production
```

The `--production` flag skips Grunt and other dev dependencies.

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
npm install -g forever
cd /var/local/gfkspiel.de/gfkspiel2/web
./manage_server.sh start
```

The server starts in production mode on port 80 and serves `static_prod/` with `index_prod.html`.

---

## 8. Firewall

```bash
ufw allow 80/tcp
ufw enable
```

---

## 9. Auto-start on Boot (systemd)

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

## Summary Checklist

- [ ] `apt-get install build-essential python2 git curl sqlite3`
- [ ] Install NVM and Node.js 0.10 (or Node 12)
- [ ] `rsync` `web/` directory to server
- [ ] `npm install --production` from `web/`
- [ ] Transfer `database/gfkspiel.db` from old server
- [ ] Create `/var/log/gfkspiel.de/` with correct ownership
- [ ] `npm install -g forever`
- [ ] `./manage_server.sh start`
- [ ] Open port 80 in firewall
- [ ] Create systemd service for auto-start on boot
