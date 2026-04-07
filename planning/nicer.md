# Making the Game Nicer — Screen-by-Screen Plan

Current state: jQuery Mobile removed, clean CSS in place. The game works but looks functional rather than polished. This plan addresses each screen in priority order.

---

## Global / cross-cutting

### Page transitions
**Current**: instant show/hide (no animation)
**Proposed**: soft CSS fade-in (150ms opacity) when the router shows a page
```css
.page { animation: pageFadeIn 0.15s ease; }
@keyframes pageFadeIn { from { opacity: 0; } to { opacity: 1; } }
```

### Typography scale
**Current**: mostly 1em throughout, `font-weight: normal` everywhere
**Proposed**:
- Body text: 1em / line-height 1.7
- Page title (h1 in header): 1.1em, `font-weight: 500`
- Section headings (h2): 1.15em, slight left margin
- Small labels (settings, form): 0.95em

### Hover / tap feedback
**Current**: `opacity: 0.88` on hover
**Proposed**: add `transition: opacity 0.12s` and `active` scale-down effect for buttons
```css
a.menu-btn, a.nav-btn { transition: opacity 0.12s, transform 0.1s; }
a.menu-btn:active, a.nav-btn:active { transform: scale(0.97); }
```

---

## Screen 1 — Main Menu (`#page-main_menu`)

**Issues**:
- "Spielen" looks the same size as "Impressum" — hierarchy missing
- App store badge + Facebook badge row looks like an afterthought
- No breathing room above the first button

**Proposed**:
- Give "Spielen" a larger `font-size: 1.1em` and slightly more padding
- Add a small logo/title header above the buttons (just "GFK-Spiel" styled text, or a small icon)
- Move app store badges into a small `<footer>`-style row at the very bottom with reduced opacity
- Remove Facebook badge (platform largely dead)
- Add `padding-top: 8%` before first button

---

## Screen 2 — Task page (`#page-task`) ← most important

**Issues**:
- `#field-text` (NVC step description) and `#task-content` (the actual question) look identical
- No visual separation between the question area and the answer choices
- The Weiter/Erläuterung/Spielstand buttons appear suddenly after answering — no smooth reveal
- "Menü" button in header is small and the green color is the same as "Hilfe" — no visual distinction

**Proposed**:
- `#field-text`: smaller text (0.9em), dimmer opacity (0.85), acts as a category label
- `#task-content`: larger text (1.05em), stronger color, `padding: 14px 16px`, more prominent
- Add a subtle divider (`border-top: 1px solid rgba(255,255,255,0.15)`) between task and choice list
- Choice list items: increase `padding` to `13px 16px`, increase `margin-bottom` to `4px`
- `#button-div` reveal: add `transition: opacity 0.2s` + start hidden, fade in on answer
- Make "Menü" button `bg-gray` (less prominent) so "Hilfe" in green stands out more

---

## Screen 3 — Ask if new game (`#page-askifnewgame`)

**Issues**:
- Two buttons floating in the center of a plain blue page — looks unfinished

**Proposed**:
- Add a short welcome text above: "Willkommen beim GFK-Spiel"
- Center the buttons with more vertical spacing (`margin-top: 30%`)
- Give "Weiterspielen" a slightly different color from "Neues Spiel" when both are visible

---

## Screen 4 — New game (`#page-new_game`)

**Issues**:
- "Spielername eingeben:" is plain `<p>` text — looks like an instruction, not a label
- The `+` (add player) button sits awkwardly next to nothing
- The rounds selector row has a label but the select is unstyled for mobile
- "Spiel starten" button at the bottom isn't visually distinguished

**Proposed**:
- Style "Spielername eingeben:" as a section label (smaller, uppercase, letter-spacing)
- Move the `+` (add player) button inline with the last player row, or as a small `+` pill after the list
- Give the rounds `<select>` a custom arrow and better padding
- Make "Spiel starten" full-width (like a menu-btn) with `bg-green` — it's the primary CTA

---

## Screen 5 — Settings (`#page-settings`)

**Issues**:
- Native checkboxes with `accent-color: green` — look like system UI, not part of the game
- No grouping — 7 options listed without visual separation between categories

**Proposed**:
- Replace checkboxes with CSS toggle switches (pure CSS, no JS needed):
  - Hidden `<input type="checkbox">` + styled `<label>` with a sliding pill
  - Colors: off = `rgba(255,255,255,0.2)`, on = `#5cb81c`
- Group settings into two sections with a faint divider:
  - "Ton & Stimme": Sound, Klaus, Antonia, Sarina
  - "Spielverhalten": NVC-konform, Nur positiv, Dance Floor

---

## Screen 6 — Field list (`#page-field_list`)

**Issues**:
- Plain colored list — no indication of which NVC step each field belongs to

**Proposed**:
- Add a small colored left-border or dot indicator matching the NVC step color
- Slightly larger text, more padding per item

---

## Screen 7 — Score dialog (`#dialog-score`)

**Issues**:
- Plain text score, no visual hierarchy between players

**Proposed**:
- Style each player's score as a mini card:
  ```
  ┌────────────────────────────┐
  │  Anna      3 Punkte  (75%) │
  └────────────────────────────┘
  ```
- Highlight the current leader with a slightly brighter card

---

## Screen 8 — Game over (`#page-game_over`) ← needs the most work

**Issues**:
- Score text is just plain HTML `<br>` separated lines
- The quote image is shown but the quote text is only in `alt=""` — not readable
- "Nochmal spielen" / "Hauptmenü" buttons are just inline pills

**Proposed**:
- Score: render each player as a card row (same as screen 7)
- Quote: show the text from `endGameQuotes` below the image, styled as a `<blockquote>` with italic text and left border
- Image: center, rounded corners (`border-radius: 12px`), `max-width: 80%`
- Buttons: make them full-width menu-style buttons, not small pills
- Add a top celebration text: "Gut gespielt! 🎉" (or without emoji if preferred)

---

## Screen 9 — Explanation / Help dialogs

**Issues**:
- Plain `<p>` text with no visual container

**Proposed**:
- Wrap `#explanation_txt` and `#help_txt` in a styled card:
  ```css
  .info-card {
      background: rgba(255,255,255,0.1);
      border-radius: 10px;
      padding: 14px 16px;
      line-height: 1.8;
  }
  ```

---

## Screen 10 — Video pages (`#page-nvc_videos`, `#page-help`)

**Issues**:
- Table layout for videos feels outdated on mobile

**Proposed**:
- Replace `<table>` with flex rows: thumbnail left, title right, full-width tappable link
- Thumbnail: `border-radius: 6px`, `width: 80px`
- Title text: yellow link color, larger tap target

---

## Screen 11 — Info/text pages (game_info, nvc_info, links, impressum, datenschutz)

**Issues**:
- Very long pages (especially datenschutz/impressum) with no visual relief

**Proposed**:
- Add `max-width: 92%; margin: 0 auto;` to text blocks for readability
- Headings in these pages currently have `margin-left: 6%` — make them full-width and add a bottom border for section separation
- Links: already `color: #f5c842` — good

---

## Priority order for implementation

| Priority | Screen | Effort | Impact |
|---|---|---|---|
| 1 | Global: transitions + tap feedback | Small | High |
| 2 | Task page: hierarchy + button reveal | Medium | High |
| 3 | Game over: score cards + quote text | Medium | High |
| 4 | Settings: toggle switches | Medium | Medium |
| 5 | Main menu: Spielen prominence + badge cleanup | Small | Medium |
| 6 | New game: CTA button + player row layout | Small | Medium |
| 7 | Score dialog: player cards | Small | Medium |
| 8 | Explanation/Help: info card | Small | Low |
| 9 | Field list: left border indicator | Small | Low |
| 10 | Video pages: flex layout | Small | Low |
| 11 | Ask if new game: welcome text | Tiny | Low |

---

## Files to change

| File | Changes |
|---|---|
| `www/css/gfkspiel.css` | Transitions, toggle switches, card styles, button prominence |
| `www/html/index_body.html` | Game over quote text, section labels, toggle switch HTML |
| `www/js/app.js` | Pass quote text to game over screen; render player score cards |
