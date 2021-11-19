from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from pytz import timezone

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    amsterdam = timezone('Europe/Amsterdam')
    now = amsterdam.localize(datetime.now())
    isThursday = now.isoweekday() == 4

    return render_template('index.html', isThursday=isThursday)

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
