from datetime import datetime
from flask import Flask, render_template
from pytz import timezone
from flask_minify import minify

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
