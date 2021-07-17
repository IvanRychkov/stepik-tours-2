import random

from flask import Flask, render_template, request
from data import title, subtitle, description, departures, tours
from operator import itemgetter
from pprint import pp

app = Flask(__name__)


def lower_first(s: str) -> str:
    """Делает первую букву в строке строчной."""
    return s[0].lower() + s[1:] if len(s) > 0 else ''


@app.route('/')
def render_index():
    # TODO: Максимум 6 туров на главной странице
    top_tours = (dict(sorted(tours.items(), key=lambda t: t[1]['stars'], reverse=True)[:6]))
    return render_template('index.html',
                           title=title,
                           subtitle=subtitle,
                           description=description,
                           departures=departures,
                           tours=top_tours)


@app.route('/departure/<departure_code>/')
def render_departure(departure_code):
    # Меняем регистр первой буквы
    departure_city = lower_first(departures[departure_code])

    # Оставляем отправления из релевантного города
    tours_available = {
        k: v for k, v in tours.items()
        if v['departure'] == departure_code
    }

    nights = map(itemgetter('nights'), tours_available.values())
    prices = map(itemgetter('price'), tours_available.values())
    print(request.path)
    return render_template('departure.html',
                           title=title,
                           departure_code=departure_code,
                           departure_city=departure_city,
                           departures=departures,
                           tours=tours_available,
                           min_price=min(map(itemgetter('price'), tours_available.values())),
                           max_price=max(map(itemgetter('price'), tours_available.values())),
                           nights=[*nights],
                           prices=[*prices])


@app.route('/tours/<int:tour_id>/')
def render_tours(tour_id):
    tour = tours[tour_id]
    departure_city = lower_first(departures[tour['departure']])
    return render_template('tour.html',
                           title=title,
                           tour=tour,
                           departure_city=departure_city,
                           departures=departures)


@app.errorhandler(404)
def render_error(error):
    return render_template('error.html',
                           departures=departures)


if __name__ == '__main__':
    app.run(host='localhost', port=5050, debug=True, use_reloader=True)
