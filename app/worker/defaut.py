"""This project has an example of how I write my codes."""
import datetime
import requests

from flask import render_template

from app import app
from app.utils import db_simulation


@app.route('/')
def index():
    """
    Call an information from utils and return in a simple html

    :return: html text.
    """
    user = db_simulation.info
    current_time = datetime.datetime.now()
    year = current_time.year

    name = user.get('name')
    age = user.get('born')
    age = year - age
    age = str(age)
    experience = user.get('experience')

    return '''<!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>My page</title>
                    </head>
                    <body>
                        <h1>My name is ''' + name + '''</h1>
                        <h2>I'm ''' + age + ''' years old</h2>
                        <h2>and I work in ''' + experience[0] + ''' and '''+experience[1]+'''</h2>
                         <button><a href="/index">Redirect</a></button>
                         <form method="POST" action="/asn_info">
                          <button>Query</button>
                         </form>
                    </body>
                </html>'''


@app.route('/index')
def example():
    """
    Here I use render template to display the information.

    :return: With render template.
    """
    user = db_simulation.info

    name = user.get('name')
    return render_template('index.html', name=name)


@app.route('/asn_info', methods=["POST"])
def asn_info():
    """
    In this function we use an external API to query data.

    :return: Query from bgp view.
    """
    query = requests.get('https://api.bgpview.io/asn/61138')

    query = query.json()

    data = query.get('data')

    status = query.get('status')
    asn_number = data.get('asn')
    lg = data.get('looking_glass')

    return render_template('asn_info.html',
                           asn_info=query,
                           status=status,
                           asn_number=asn_number,
                           lg=lg
                           )
