# -*- coding: utf-8 -*-
from flask import *
from ssau_downloader import download

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
        p, week = path(data)
        return send_file(f"{p}/week_{week}.html")
        
    except FileNotFoundError:
        ID = data['groupId'] if 'groupId' in data else data['staffId']
        p, week = path(data)
        
        download('groupId' in data, ID, week)
        try:
            return send_file(f"{p}/week_{week}.html")
        except FileNotFoundError:
            abort(404)
    except KeyError:
        abort(404)

def path(data):
    if 'groupId' in data:
        p = f"groups/{data['groupId']}"
    elif 'staffId' in data:
        p = f"teachers/{data['staffId']}"
            
    if 'selectedWeek' not in data:
        week = 1
    else:
        week = data['selectedWeek']
    return p, week

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
