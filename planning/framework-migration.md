# Framework Migration Plan: jQuery Mobile → Modern Stack

## Why migrate?

jQuery Mobile reached end-of-life in 2021. It works but:
- Security vulnerabilities won't be patched
- No mobile browser optimizations beyond 2014-era assumptions
- CSS overrides are a constant fight against jQM's own styles
- Hard to add new features (animations, offline support, push notifications)

---

## What the app actually does

Understanding this scopes the migration effort:

- **Multi-page SPA**: ~15 "pages" (`data-role="page"`) with jQM transitions between them
- **Game state in JS**: `app.js` manages player turns, scores, question/answer flow, round tracking
- **Dynamic UI**: JS appends list items (`choiceList.append(...)`), updates button classes (bg-gray → bg-green-result), shows/hides elements
- **Audio**: Speech audio clips per question/answer
- **Networked**: Node.js backend serves game data (questions, sessions); frontend talks to it via AJAX/WebSocket
- **No user accounts**: Session-based, ephemeral game rooms

---

## Option A: React (Vite + React)

**Best fit for this project.**

### Why React
- Component model maps cleanly to the page/widget structure (MenuPage, GamePage, ChoiceList, NavButtons)
- Huge ecosystem, easy to find help
- State management (useState/useReducer) replaces the scattered JS global state in app.js
- React Router replaces jQM page transitions

### Migration approach
1. Keep Node.js backend as-is — only the frontend changes
2. Scaffold with Vite: `npm create vite@latest gfkspiel-ui -- --template react`
3. Port each jQM `data-role="page"` → React component
4. Replace jQM listview → plain `<ul>` with CSS
5. Replace jQM button widgets → `<button>` with CSS classes
6. Port `app.js` game logic → React state + hooks
7. Keep the NVC color CSS classes (bg-green, bg-gray, etc.) — they're framework-agnostic

### Effort estimate
- **Large**: app.js is ~1000+ lines of tightly coupled jQM event handling
- The hardest part is untangling `pageinit`/`pageshow` lifecycle events → `useEffect`
- Audio handling needs care (autoplay restrictions in modern browsers)

---

## Option B: Next.js

**Possible, but not the natural fit.**

### What Next.js adds
- Server-side rendering (SSR) and static generation
- File-based routing
- API routes (could replace the Node.js backend)
- Built-in image optimization, etc.

### Why it's a mismatch here
- The game is a **real-time, session-based multiplayer app** — SSR buys nothing; there's nothing to pre-render
- The existing Node.js server already handles the backend; Next.js API routes would duplicate it
- Next.js adds complexity (build pipeline, server/client component split) without benefit for this use case
- Deployment becomes heavier (needs Node.js process for SSR, not just static files)

### When Next.js would make sense
- If you wanted to add a public-facing marketing/info site (SEO matters there)
- If you wanted to consolidate frontend + backend into one codebase using Next.js API routes

**Verdict**: Use plain React (Vite) for the game. If you ever want a proper landing page at gfk-spiel.de with SEO, Next.js could serve that separately.

---

## Option C: Vue 3 + Vite

Functionally equivalent to React for this project. Slightly gentler learning curve if starting fresh. Less ecosystem breadth. No strong reason to prefer it over React here.

---

## Option D: Incremental — no framework ✓ DONE

Replace only the jQuery Mobile dependency with plain HTML/CSS/vanilla JS.

**Implemented in commit after 2026-04-07:**

| File | Change |
|---|---|
| `www/js/router.js` + `static_prod/js/router.js` | New ~60-line hash router firing `pagecreate`/`pageshow`/`pagehide`/`pagebeforehide` jQuery events, `$.mobile.changePage` stub |
| `www/js/app.js` + `static_prod/js/gfkspiel2.min.js` | Removed: `listview('refresh')`, `.checkboxradio("refresh")`, `.button()`, `trigger('create')`, `data-role` in dynamic HTML |
| `www/html/index_body.html` | Replaced all `data-role="page/header/content/listview/button/fieldcontain"` with semantic CSS classes; added Font Awesome `<i>` icons |
| `web/index_prod.html` | Removed `jquery.mobile-1.3.2.min.css`, `jquery.mobile-1.3.2.min.js`, `overthrow.js`; added `router.js` |
| `www/css/gfkspiel.css` + `static_prod/css/gfkspiel2.min.css` | Complete rewrite — clean CSS without `!important` fighting, using `.page`, `.page-header`, `.page-content` |

**jQuery core also removed (2026-04-07):** `app.js` and `adapterWeb.js` fully rewritten in vanilla JS (`fetch`, `querySelector`, `addEventListener`, `CustomEvent`, `classList`, `dataset`). jQuery script tag removed from `index_prod.html`. `$(initApp)` → `document.addEventListener('DOMContentLoaded', initApp)`.

**Deployment note**: `www/html/index_body.html` must also be uploaded to the server — it is read by Node.js at runtime (not served as a static file), so it's easy to miss when deploying.

**Result**: No dead jQM dependency. CSS is clean and maintainable. Same visual appearance and game logic.

---

## Recommended path

1. **Done**: CSS modernization + Option D (jQM removed) ✓
2. **Done**: jQuery core removed — pure vanilla JS throughout ✓
3. **Later**: If new features are needed (user accounts, leaderboard, PWA), migrate to React/Vite at that point when the effort is justified.

---

## Files that would change in a full React migration

| Current                              | React equivalent                          |
| ------------------------------------ | ----------------------------------------- |
| `www/html/index_body.html`           | `src/pages/` — one component per page     |
| `www/js/app.js`                      | `src/hooks/useGame.js` + component state  |
| `www/css/gfkspiel.css`               | `src/styles/game.css` (largely reusable)  |
| `web/index_prod.html`                | `index.html` (Vite entry)                 |
| `web/static_prod/`                   | `dist/` (Vite build output)               |
| Node.js backend                      | Unchanged — just update CORS/static serving |
