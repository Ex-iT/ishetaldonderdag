from datetime import datetime
from flask import Flask, render_template, request, Response
from pytz import timezone
from flask_minify import minify
import requests

app = Flask(__name__, static_folder='static', static_url_path='')
minify(app=app, html=True, js=True, cssless=True)

def is_thursday():
    amsterdam = timezone('Europe/Amsterdam')
    now = amsterdam.localize(datetime.now())
    return now.isoweekday() == 4

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template('index.html', is_thursday=is_thursday())

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html', is_thursday=is_thursday()), 404

@app.after_request
def after_request(response):
    if request.endpoint != 'proxy_thm':
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
        response.headers['Permissions-Policy'] = 'geolocation=(self), microphone=()'

    return response

# Adding a Content-Type and Cache-Control to the response from Try Hack Me's badge image
@app.route('/proxy/thm')
def proxy_thm():
    resp = requests.request(
        method=request.method,
        url='https://tryhackme-badges.s3.amazonaws.com/MrBlonde.png',
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    updated_headers = resp.raw.headers.items() + [
        ('Content-Type', 'image/png'),
        ('Cache-Control', 'max-age=3600, public'),
    ]

    return Response(resp.content, resp.status_code, updated_headers)
