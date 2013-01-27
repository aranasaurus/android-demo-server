import os
import time
import json
import requests
from requests.exceptions import ConnectionError

from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
def go():
    if os.path.exists('query.txt'):
        query = open('query.txt', 'r').read()

    if not query:
        query = "picard android"
    url = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={0}".format(query)
    app.logger.debug(url)

    r = requests.get(url.format(query))
    images = [(i, json.dumps(i)) for i in json.loads(r.text)['responseData']['results']]
    return render_template("index.html", images=images)

@app.route('/set/<query>')
def write_query(query):
    open('query.txt', 'w').write(query)
    return 'Query set to "{0}"'.format(query)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

