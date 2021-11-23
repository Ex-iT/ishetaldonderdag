from datetime import datetime
from flask import Flask, render_template, redirect
from flask_minify import minify
from pytz import timezone

app = Flask(__name__, static_folder='static', static_url_path='')
minify(app=app, html=True, js=True, cssless=True)

def isThursday():
    amsterdam = timezone('Europe/Amsterdam')
    now = amsterdam.localize(datetime.now())
    return now.isoweekday() == 4

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template('index.html', isThursday=isThursday())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', isThursday=isThursday()), 404
