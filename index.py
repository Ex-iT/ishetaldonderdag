from datetime import datetime
from flask import Flask, render_template, g, request, send_from_directory, Response
from zoneinfo import ZoneInfo
from flask_minify import minify
import secrets

app = Flask(__name__, static_folder="static", static_url_path="/static")
minify(app=app, html=True, js=True, cssless=True)


def is_thursday():
    amsterdam = ZoneInfo("Europe/Amsterdam")
    now = datetime.now(amsterdam)
    return now.isoweekday() == 4


def generate_rss():
    """Generate RSS 2.0 feed for IsHetAlDonderdag - daily entries."""
    amsterdam = ZoneInfo("Europe/Amsterdam")
    now = datetime.now(amsterdam)
    from datetime import timedelta
    
    # Build items for the last 10 days
    items = []
    for i in range(10):
        day = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
        is_thu = day.weekday() == 3
        title = "Ja, het is donderdag!" if is_thu else "Nee, het is nog geen donderdag."
        
        items.append({
            "title": title,
            "description": f"Is het al donderdag op {day.strftime('%d %B %Y')}? {title}",
            "link": "https://ishetaldonderdag.nl/",
            "guid": f"https://ishetaldonderdag.nl/{day.strftime('%Y-%m-%d')}",
            "pubDate": day.strftime("%a, %d %b %Y %H:%M:%S %z"),
        })
    
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Is Het Al Donderdag?</title>
    <link>https://ishetaldonderdag.nl/</link>
    <description>Wil je weten of het al donderdag is? De RSS feed voor donderdag-status.</description>
    <language>nl-NL</language>
    <lastBuildDate>{now.strftime("%a, %d %b %Y %H:%M:%S %z")}</lastBuildDate>
    <atom:link href="https://ishetaldonderdag.nl/rss" rel="self" type="application/rss+xml"/>
    <generator>IsHetAlDonderdag.nl</generator>
    <ttl>60</ttl>
"""
    for item in items:
        rss += f"""    <item>
      <title>{item['title']}</title>
      <description>{item['description']}</description>
      <link>{item['link']}</link>
      <guid isPermaLink="false">{item['guid']}</guid>
      <pubDate>{item['pubDate']}</pubDate>
    </item>
"""
    rss += """  </channel>
</rss>"""
    return rss


def set_nonce():
    g.nonce = secrets.token_urlsafe()


@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory("static/images", filename)


@app.route("/manifest.json")
@app.route("/robots.txt")
@app.route("/browserconfig.xml")
@app.route("/favicon.ico")
def static_root_files():
    filename = request.path.lstrip("/")
    return send_from_directory("static", filename)


@app.route("/rss")
def rss_feed():
    rss_content = generate_rss()
    return Response(rss_content, mimetype="application/rss+xml; charset=utf-8")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def home(path):
    set_nonce()
    return render_template("index.html", is_thursday=is_thursday(), nonce=g.nonce)


@app.errorhandler(404)
def page_not_found(error):
    set_nonce()
    return render_template("index.html", is_thursday=is_thursday(), nonce=g.nonce), 404


@app.after_request
def after_request(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(self), microphone=()"
    if hasattr(g, "nonce"):
        response.headers["Content-Security-Policy"] = (
            f"default-src 'self'; base-uri 'none'; object-src 'none'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src 'self' fonts.gstatic.com; script-src 'self' 'nonce-{g.nonce}' 'strict-dynamic'"
        )
    response.headers["Vary"] = "Accept-Encoding"
    if response.content_type and "text/html" in response.content_type:
        response.charset = "utf-8"

    return response