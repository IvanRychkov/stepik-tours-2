from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def render_index():
    return render_template('index.html')


@app.route('/departure/<departure>/')
def render_departure(departure):
    return render_template('departure.html')


@app.route('/tours/<id>/')
def render_tours(id):
    return render_template('tour.html')
