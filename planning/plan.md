## TODOS

### Step 1 ✓ Done

- Added two German lines with app store links above the menu in both:
  - `var/www/vhosts/default/htdocs/index.html` (static, when app is not running)
  - `var/local/gfkspiel.de/gfkspiel2/www/html/index_body.html` (app, when running)
- Links:
  - https://play.google.com/store/apps/details?id=de.benjanklaus.gfkspiel
  - https://apps.apple.com/de/app/gfk-spiel

### Step 2 ✓ Done

- Removed the Bedanken button from the main menu in `var/local/gfkspiel.de/gfkspiel2/www/html/index_body.html`
- Also removed the entire `#page-thanks` (bedanken) page section

### Step 3 ✓ Done

- Removed nested `.git` from `var/local/gfkspiel.de/gfkspiel2/` (was pointing to Bitbucket)
- All `gfkspiel2` files are now tracked directly in the `gfkspiel_web` GitHub repo
- Unpushed changes (Bedanken removal, audio/checkbox fixes) are preserved in the files
