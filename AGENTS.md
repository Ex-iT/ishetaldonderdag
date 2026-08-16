# AGENTS.md - Project Configuration for AI Agents

## Project Overview
**IsHetAlDonderdag.nl** - A minimal Flask application that tells you if it's Thursday in Amsterdam.
- **Language**: Python 3.14
- **Framework**: Flask 3.x
- **Deployment**: Vercel (Python builder)
- **Asset Pipeline**: Flask-Assets with content-hash cache busting

---

## Architecture

### Key Files
| File | Purpose |
|------|---------|
| `index.py` | Flask app factory, routes, asset bundles, security headers |
| `templates/index.html` | Main template with asset tags (critical CSS in bundle) |
| `static/js/main.js` | Client-side: theme toggle, GitHub link, dynamic nav injection |
| `static/css/main.css` | All styles (theme vars, base, nav) - bundled by Flask-Assets |
| `vercel.json` | Vercel deployment config (Python builder) |
| `Pipfile` | Python dependencies |

### Asset Pipeline (Flask-Assets)
- **JS Bundle**: `js/main.js` → `js/main.<hash>.js` (minified via `rjsmin`)
- **CSS Bundle**: `css/main.css` → `css/main.<hash>.css` (minified via `cssmin`)
- **Template Tag**: `{% assets "main_js" %}` / `{% assets "main_css" %}` generates correct hashed URL
- **Dev Mode** (`FLASK_DEBUG=1`): Serves source files with content-hash, auto-reload
- **Prod Mode** (`FLASK_DEBUG=0`): Serves minified, content-hashed files
- **No build step** - Flask-Assets compiles on-demand

---

## Development Workflow

### Start Dev Server
```bash
cd /home/ex-it/Development/ishetaldonderdag
./venv/bin/flask --app index.py --debug run
# Runs on http://localhost:5000
```

### Verify Cache Busting
```bash
# Dev mode - content-hashed (not unhashed)
curl http://localhost:5000/ | grep "script src"
# → /js/main.<hash>.js

# Prod mode - hashed, minified
FLASK_DEBUG=0 ./venv/bin/flask --app index.py run &
curl http://localhost:5000/ | grep "script src"
# → /js/main.<hash>.js (same hash if content unchanged)
```

### Modify Assets
1. Edit `static/js/main.js` or `static/css/main.css`
2. **Dev mode**: Refresh browser - changes load instantly, new hash generated
3. **Prod mode**: Hash changes automatically on next request

---

## Key Implementation Details

### Security Headers (index.py:46-63)
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
- Bundled via Flask-Assets, linked in template via `{% assets "main_css" %}`
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
- **No build command** - Flask-Assets compiles on first request
- **Note**: First request in production may have latency (bundle compilation)
- Consider pre-warming or adding build step if latency is an issue

### Environment Variables
- `FLASK_DEBUG=0` (default on Vercel)
- No other env vars required

---

## Dependency Management

### Pipfile (Production)
```toml
[packages]
Flask = ">=2.3.3"
Flask-Assets = ">=2.0.0,<3.0.0"
cssmin = ">=0.2.0"
rjsmin = ">=1.2.0"
requests = ">= 2.31.0"

[requires]
python_version = "3.14"
```

### Install/Update
```bash
pip install -r requirements.txt
```

---

## Common Tasks for Agents

### Add New JS/CSS Asset
1. Add file to `static/js/` or `static/css/`
2. Register new Bundle in `index.py`
3. Use `{% assets "bundle_name" %}` in template

### Modify Security Headers
Edit `after_request()` in `index.py` (lines 46-63)

### Update Python Version
1. Change `python_version` in `Pipfile`
2. Recreate venv: `rm -rf venv && python3.14 -m venv venv`
3. Reinstall dependencies

### Debug Asset Issues
```bash
# Check bundle registration
./venv/bin/python -c "from index import assets; print(assets._named_bundles)"

# Force rebuild (delete cached bundles)
rm -rf static/.webassets-cache
```

---

## Testing Checklist (Manual)

- [ ] Dev server starts: `./venv/bin/flask --app index.py --debug run`
- [ ] Page loads at `http://localhost:5000/`
- [ ] Theme toggle works (light ↔ dark)
- [ ] GitHub link present, opens in new tab
- [ ] Dev mode: JS loads as `/js/main.<hash>.js` (content-hashed)
- [ ] Prod mode: JS loads as `/js/main.<hash>.js` (minified, content-hashed)
- [ ] Modify `main.js` → hash changes in prod mode
- [ ] CSP headers present (check DevTools Network → Headers)
- [ ] Nonce rotates per request
- [ ] `Vary: Accept-Encoding` header present on all responses
- [ ] `Content-Type: text/html; charset=utf-8` on HTML responses
- [ ] `X-Frame-Options: DENY` on all responses
- [ ] `Referrer-Policy: strict-origin-when-cross-origin` on all responses
- [ ] localStorage errors don't break theme (private browsing test)
- [ ] Thursday detection works correctly (Amsterdam timezone)
- [ ] Vercel deploy succeeds (push to connected repo)