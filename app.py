import os, json, sys
from flask import Flask
import psycopg2
postgres = 'postgres://lkqrjjtnsmdaor:ed80e278bbaf164b2f53b7f2c9173c448313ca793b7c57ec1bb0a9ec2d53bbc6@ec2-54-205-183-19.compute-1.amazonaws.com:5432/dc3lcj8g41q7p2'


port = sys.argv[1]
app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(postgres, sslmode='require')
        cur = conn.cursor()
        data = {}
        for row in cur.fetchall():
            data[row[0]] = data[row[1]]
        conn.close()
        return data
    except:
        return "failed"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)