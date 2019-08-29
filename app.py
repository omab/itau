import json
import datetime
import requests

from flask import Flask, request, redirect, render_template


API_URL = 'https://www.itaulink.com.uy/trx/cuentas/1/{account_hash}/{month}/{year}/consultaHistorica'

MONTHS = [
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre',
]

YEARS = list(reversed(range(2015, datetime.date.today().year + 1)))


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Render index template and process cURL url on POST"""

    if request.method == 'POST' and request.form.get('curl'):
        account_hash, session_cookie = parse_curl_line(request.form['curl'])
    else:
        account_hash = None
        session_cookie = None

    today = datetime.date.today()

    return render_template('index.html',
                           json=None,
                           account_hash=account_hash,
                           session_cookie=session_cookie,
                           current_year=today.year,
                           current_month=today.month - 1,
                           months=MONTHS,
                           years=YEARS)


@app.route('/report', methods=['POST'])
def report():
    """Fetch history from API and render"""

    month = request.form['month']
    year = request.form['year'][-2:]
    account_hash = request.form['account_hash']
    session_cookie = request.form['session_cookie']

    response = requests.get(
        API_URL.format(account_hash=account_hash, year=year, month=month),
        headers={'Cookie': session_cookie}
    )
    response.raise_for_status()

    today = datetime.date.today()
    json_response = response.json()

    return render_template('index.html',
                           json=json_response,
                           json_pretty=json.dumps(json_response, indent=4),
                           account_hash=account_hash,
                           session_cookie=session_cookie,
                           current_month=int(request.form.get('month') or today.month),
                           current_year=int(request.form.get('year') or today.year),
                           months=MONTHS,
                           years=YEARS,
                           str=str)


def parse_curl_line(line):
    """Parse curl line copied from browser and extract needed parameters"""
    items = line.replace('"', '').replace("'", '').split()
    cookies_index = items.index('Cookie:')
    data_index = items.index('--data')

    cookie = items[cookies_index + 1]
    account_hash = items[data_index + 1].split(':')[2]

    return (account_hash, cookie)
