import os
import datetime
import json
import requests

from flask import Flask

app = Flask(__name__)


def save_content(content):
    file_name = datetime.datetime.now().strftime('egyptera.%Y-%m-%d-%H-%M-%S.html')
    file_name = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_name, 'w') as f:
        f.write(content)

def get_grid_status():
    url = 'http://loadmeter.egyptera.org/MiniCurrentLoadClock3.aspx'
    result = 'Unknown'



    r = requests.get(url)

    save_content(r.content)

    if 'Images/c1.gif' in r.text:
        result = 'Normal'

    if 'Images/c2.gif' in r.text:
        result = 'Warning'

    if 'Images/c3.gif' in r.text:
        result = 'Danger'

    return result

@app.route('/')
def hello_world():
    status_to_response = {
        'Danger': 'Power grid is now in the Danger Zone!',
        'Warning': 'Power grid is now in the Warning Zone!',
        'Normal': 'Power grid is now in the Normal Zone!',
    }
    status = get_grid_status()

    return status_to_response[status]



@app.route('/status')
def grid_status():
    status = get_grid_status()
    response = {}
    response['status'] = status
    return json.dumps(response)

if __name__ == '__main__':
    app.debug = True
    app.run()