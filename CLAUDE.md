# gfkspiel_web

Website for **gfk-spiel.de** — a free learning game for Gewaltfreie Kommunikation (Nonviolent Communication / NVC), based on a board game by Klaus Karstädt.

## Project structure

```
var/www/vhosts/default/htdocs/   ← web root (deploy this to the server)
  index.html
  links.html
  impressum.html
  css/
    gfkspielde.css               ← main stylesheet
    style.css
  img/                           ← images and icon assets
planning/                        ← planning documents
var/lib/                         ← server infrastructure snapshot, not app code
```

## Stack

- Plain HTML (XHTML 1.0 Strict) + CSS — no build system, no framework
- German-language content
- Hosted on Ubuntu/Plesk

## Notes

- The live site currently shows a placeholder ("Server läuft leider gerade nicht")
- Links to Android (Google Play) and iOS (App Store) app versions
- Contact: gfkspiel@gmail.com
