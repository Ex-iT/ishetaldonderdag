from datetime import datetime
from flask import Flask, render_template, g, request
from flask_assets import Environment, Bundle
from zoneinfo import ZoneInfo
import secrets

app = Flask(__name__, static_folder="static", static_url_path="")

assets = Environment(app)
js_bundle = Bundle(
    "js/main.js",
    filters="rjsmin",
    output="js/main.%(version)s.js"
)
css_bundle = Bundle(
    "css/main.css",
    filters="cssmin",
    output="css/main.%(version)s.css"
)
assets.register("main_js", js_bundle)
assets.register("main_css", css_bundle)


def is_thursday():
    amsterdam = ZoneInfo("Europe/Amsterdam")
    now = datetime.now(amsterdam)
    return now.isoweekday() == 4


def set_nonce():
    g.nonce = secrets.token_urlsafe()


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

    if response.status_code == 200:
        path = request.path
        if (path.startswith("/js/main.") and path.endswith(".js")) or (
            path.startswith("/css/main.") and path.endswith(".css")
        ):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"

    return response
