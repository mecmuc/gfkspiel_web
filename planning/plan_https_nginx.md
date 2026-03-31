# HTTPS mit nginx als Reverse Proxy

Eingerichtet auf dem Ubuntu-Server für gfk-spiel.de. nginx übernimmt SSL-Terminierung und HTTP→HTTPS-Redirect, Node.js läuft intern auf Port 3000.

---

## Architektur

```
Internet
  │
  ├── :80  → nginx → 301 Redirect auf https://
  └── :443 → nginx (SSL) → proxy_pass → Node.js :3000
```

---

## 1. nginx installieren

```bash
apt-get install -y nginx
rm /etc/nginx/sites-enabled/default
```

---

## 2. SSL-Zertifikat

Zertifikat und Key von Strato herunterladen und auf den Server legen:

```bash
mkdir -p /etc/ssl/gfk-spiel.de
# certificate.crt und private.key nach /etc/ssl/gfk-spiel.de/ kopieren
```

Das Zertifikat wird bei Strato beantragt über:
1. CSR + Key generieren (z.B. mit openssl)
2. CSR bei Strato einreichen
3. Ausgestelltes Zertifikat (`.crt`) herunterladen

---

## 3. nginx-Konfiguration

Datei: `/etc/nginx/sites-available/gfk-spiel.de`

```nginx
# HTTP → HTTPS Redirect
server {
    listen 80;
    server_name gfk-spiel.de www.gfk-spiel.de;
    return 301 https://$host$request_uri;
}

# HTTPS → Node.js
server {
    listen 443 ssl;
    server_name gfk-spiel.de www.gfk-spiel.de;

    ssl_certificate     /etc/ssl/gfk-spiel.de/certificate.crt;
    ssl_certificate_key /etc/ssl/gfk-spiel.de/private.key;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Aktivieren:

```bash
ln -s /etc/nginx/sites-available/gfk-spiel.de /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx
```

---

## 4. Node.js auf Port 3000

In `web/server.js` ist der prod-Port auf 3000 gesetzt (statt 80):

```js
} else if (config.mode == 'prod'){
    config.port = 3000;
    ...
}
```

Die `gfkspiel.service`-Datei bleibt unverändert (`--mode=prod`).

Nach Änderung an `server.js` auf dem Server neu einspielen und Dienst neu starten:

```bash
systemctl restart gfkspiel
```

---

## 5. Änderungen auf dem Server einspielen

Nach dem Ändern von `server.js` lokal: Datei auf den Server kopieren und Dienst neu starten:

```bash
scp web/server.js root@<server-ip>:/var/local/gfk-spiel.de/gfkspiel2/web/server.js
ssh root@<server-ip> "systemctl restart gfkspiel"
```

---

## Troubleshooting

**nginx startet nicht (`bind() failed: Address already in use` auf Port 80):**
Node.js und nginx können nicht gleichzeitig Port 80 belegen. Sicherstellen, dass Node.js auf Port 3000 läuft, dann nginx neu starten.

**nginx-Konfiguration testen:**
```bash
nginx -t
```

**Logs:**
```bash
journalctl -xeu nginx.service
tail -f /var/log/nginx/error.log
tail -f /var/log/gfkspiel.de/server.log
```
