import os, json, sys
from flask import Flask, render_template
import sqlite3


port = sys.argv[1]
app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = sqlite3.connect('../db/emotes.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM emotes")
        data = {}
        try:
            for row in cur.fetchall():
                data[row[1]] = row[2]
        except IndexError:
            print(f'Index error on row: {row}')
        conn.close()
        keys = sorted(data.keys(), key = lambda x : data[x], reverse = True)
        out = ''
        i = 1
        for key in keys:
            if data[key] == 1:
                out += str(i) + '. ' + key.split(':')[1] + ' - ' + str(data[key]) + ' time <br>'
            else:
                out += str(i) + '. ' + key.split(':')[1] + ' - ' + str(data[key]) + ' times <br>'
            i += 1
        return render_template('index.html', content=out.split('<br>'))
  
    except Exception as e:
        print(f'Error: {e}')
        return "failed"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)