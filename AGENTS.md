# AGENTS.md - Project Configuration for AI Agents

## Project Overview
**IsHetAlDonderdag.nl** - A minimal Flask application that tells you if it's Thursday in Amsterdam.
- **Language**: Python 3.14
- **Framework**: Flask 3.x
- **Deployment**: Vercel (Python builder)
- **Asset Pipeline**: CSS served directly; Flask-Minify for HTML/JS minification

---

## Architecture

### Key Files
| File | Purpose |
|------|---------|
| `index.py` | Flask app, routes, security headers |
| `templates/index.html` | Main template with inline CSS (critical), direct JS/CSS links |
| `static/js/main.js` | Client-side: theme toggle, GitHub link, dynamic nav injection |
| `static/css/main.css` | All styles (theme vars, base, nav) - served directly |
| `vercel.json` | Vercel deployment config (Python builder) |
| `requirements.txt` | Python dependencies |

### Asset Pipeline
- **JS**: `static/js/main.js` served directly at `/static/js/main.js` (Flask-Minify minifies on-the-fly)
- **CSS**: `static/css/main.css` served directly at `/static/css/main.css` (Flask-Minify minifies on-the-fly)
- **HTML**: Minified via `flask-minify` (htmlminf)
- **No Flask-Assets** - simple static serving avoids Vercel filesystem issues

---

## Development Workflow

### Start Dev Server
```bash
cd /home/ex-it/Development/ishetaldonderdag
./venv/bin/flask --app index.py --debug run
# Runs on http://localhost:5000
```

### Verify Assets
```bash
# Verify assets serve correctly
curl -I http://localhost:5000/static/js/main.js
curl -I http://localhost:5000/static/css/main.css
```

### Modify Assets
1. Edit `static/js/main.js` or `static/css/main.css`
2. **Restart dev server** - new hash generated for JS, CSS served fresh

---

## Key Implementation Details

### Security Headers (index.py:85-100)
- CSP with nonce-based script allowlisting
- `script-src 'self' 'nonce-{g.nonce}' 'strict-dynamic'`
- `style-src 'self' 'unsafe-inline' fonts.googleapis.com` (CSS bundle + Google Fonts)
- Nonce generated per-request via `secrets.token_urlsafe()` stored in Flask's `g` object
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Vary: Accept-Encoding` for proper CDN caching
- `Content-Type: text/html; charset=utf-8`

### Theme System
- CSS custom properties for light/dark themes (in `main.css` bundle)
- Persisted in `localStorage` + respects `prefers-color-scheme`
- Toggle button injected via JS, SVG icons inline
- localStorage access wrapped in try/catch for private browsing

### Navigation Menu (JS-injected)
- **GitHub link** (external, `target="_blank"`, `rel="noopener noreferrer"`)
- **Theme toggle** button (moon/sun icons)

### Critical CSS Strategy
- All CSS in `static/css/main.css` (theme vars, base styles, nav styles)
- Served directly at `/static/css/main.css`
- Fonts preloaded via `<link rel="preload">`
- No inline `<style>` block - HTML stays small for single-packet delivery

---

## Vercel Deployment

### Config (`vercel.json`)
```json
{
  "builds": [{"src": "*.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "/"}]
}
```
- **No build command** - `@vercel/python` installs deps from `requirements.txt`
- JS/CSS served directly from static folder

### Environment Variables
- `FLASK_DEBUG=0` (default on Vercel)
- No other env vars required

---

## Dependency Management

### requirements.txt (Production)
```txt
Flask>=2.3.3
flask-minify>=0.50
requests>=2.31.0
```

### Install/Update
```bash
pip install -r requirements.txt
```

---

## Common Tasks for Agents

### Add New JS/CSS Asset
1. Add file to `static/js/` or `static/css/`
2. Link in template (JS: `<script src="/static/js/...">`, CSS: `<link rel="stylesheet" href="/static/css/...">`)

### Modify Security Headers
Edit `after_request()` in `index.py`

### Update Python Version
1. Change `python_version` in `Pipfile`
2. Recreate venv: `rm -rf venv && python3.14 -m venv venv`
3. Reinstall dependencies

### Debug Asset Issues
```bash
# Verify assets serve correctly
curl -I http://localhost:5000/static/js/main.js
curl -I http://localhost:5000/static/css/main.css
```

---

## Testing Checklist (Manual)

- [ ] Dev server starts: `./venv/bin/flask --app index.py --debug run`
- [ ] Page loads at `http://localhost:5000/`
- [ ] Theme toggle works (light ↔ dark)
- [ ] GitHub link present, opens in new tab
- [ ] Dev mode: JS loads as `/static/js/main.js` (minified by flask-minify)
- [ ] Prod mode: JS loads as `/static/js/main.js` (minified by flask-minify)
- [ ] CSP headers present (check DevTools Network → Headers)
- [ ] Nonce rotates per request
- [ ] `Vary: Accept-Encoding` header present on all responses
- [ ] `Content-Type: text/html; charset=utf-8` on HTML responses
- [ ] `X-Frame-Options: DENY` on all responses
- [ ] `Referrer-Policy: strict-origin-when-cross-origin` on all responses
- [ ] localStorage errors don't break theme (private browsing test)
- [ ] Thursday detection works correctly (Amsterdam timezone)
- [ ] Vercel deploy succeeds (push to connected repo)