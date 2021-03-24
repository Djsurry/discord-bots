import os, json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    with open('emotes.json') as f:
        return json.load(f)
    return 'Failed'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)