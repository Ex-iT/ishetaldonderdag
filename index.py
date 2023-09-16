from datetime import datetime
from flask import Flask, render_template
from pytz import timezone
from flask_minify import minify
import secrets

app = Flask(__name__, static_folder='static', static_url_path='')
minify(app=app, html=True, js=True, cssless=True)

NONCE = ''

def is_thursday():
    amsterdam = timezone('Europe/Amsterdam')
    now = amsterdam.localize(datetime.now())
    return now.isoweekday() == 4

def set_nonce():
    global NONCE
    NONCE = secrets.token_urlsafe()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    set_nonce()
    return render_template('index.html', is_thursday=is_thursday(), nonce=NONCE)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html', is_thursday=is_thursday()), 404

@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    response.headers['Permissions-Policy'] = 'geolocation=(self), microphone=()'
    response.headers['Content-Security-Policy'] = f'default-src \'self\'; base-uri \'none\'; object-src \'none\'; style-src \'self\' \'unsafe-inline\' fonts.googleapis.com; font-src \'self\' fonts.gstatic.com; script-src \'self\' \'nonce-{NONCE}\' \'strict-dynamic\''

    return response
