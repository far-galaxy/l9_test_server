# -*- coding: utf-8 -*-
from flask import *

app = Flask(__name__)

attempt = 0

@app.route('/styles/<path:path>')
def css(path):
    try:
        return send_file(f"{path}")
    except FileNotFoundError:
        abort(404)

@app.route('/rasp/', methods=['GET'])
def rasp():
    data = request.args.to_dict()
    if data == {}:
        return send_file("index.html")
    try:
        if 'selectedWeek' not in data:
            return send_file(f"shedules/{data['groupId']}/week_1.html")
        else:
            return send_file(f"shedules/{data['groupId']}/week_{data['selectedWeek']}.html")
    except FileNotFoundError:
        abort(404)
    except KeyError:
        abort(404)

@app.route('/rasp/search', methods=['POST'])
def search():
    global attempt
    data = request.values['text']
    print(data)
    attempt += 1
    if attempt == 1:
        abort(404)
    if attempt == 2:
        attempt = 0
        return "bruh"

        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
