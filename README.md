# IsHetAlDonderdag.nl

A rebuild of the original `ishetaldonderdag.nl` based on Python 3.14 and [Flask 3.x](https://flask.palletsprojects.com/).

## Architecture

- **Language**: Python 3.14
- **Framework**: Flask 3.x
- **Asset Pipeline**: Flask-Minify (HTML/JS/CSS minification on-the-fly)
- **Static Files**: Served directly from `/static` folder
- **Deployment**: Vercel (Python builder)

## Development

Create a virtual environment:

```bash
python3.14 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

To start a local development server on port `5000` run:

```bash
flask --app index.py --debug run
```

## Asset Pipeline

- **HTML**: Minified via `flask-minify` (htmlminf)
- **JS**: `static/js/main.js` served at `/static/js/main.js` (minified on-the-fly)
- **CSS**: `static/css/main.css` served at `/static/css/main.css` (minified on-the-fly)
- **No build step** - all minification happens at runtime

## Security

- CSP with per-request nonce (`g.nonce`)
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Vary: Accept-Encoding`

## Attribution

Icons made by [Becris](https://www.flaticon.com/authors/becris) from [www.flaticon.com](https://www.flaticon.com/).