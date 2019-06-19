from flask import Flask
import os
import random
import time

import pyodbc
import pandas as pd
import redis as redis
from flask import Flask, render_template, request
import sqlite3 as sql

from math import radians, sin, cos, sqrt, atan2

myHostname = "azureassignment3.redis.cache.windows.net"
myPassword = "xw5S6heXPfqGZL4PfzatH+d7nnCawcY5dSMNTyWC+qQ="
server = 'mysqlserversuchitra.database.windows.net'
database = 'assignment3'
username = 'azureuser'
password = 'Geetha1963@'
driver= '{ODBC Driver 17 for SQL Server}'

app = Flask(__name__)
port = os.getenv('VCAP_APP_PORT','5000')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/q6')
def q7():
    return render_template('options.html')

@app.route('/q8')
def q8():
    return render_template('options1.html')


@app.route('/restrictedlat')
def restrictedlat():
    return render_template('lat.html')

@app.route('/list',methods=['POST', 'GET'])
def list():
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    cursor = cnxn.cursor()
    d1 = request.form['d1']
    d2 = request.form['d2']
    lon = request.form['lon']
    cursor.execute("SELECT latitude,longitude,time,depthError FROM quake6 where depthError between ? and ? and longitude > ?",(d1,d2,lon),)
    row = cursor.fetchall()
    return render_template("list.html", data1=row)

@app.route('/options4', methods=['POST', 'GET'])
def options4():
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    l1 = float(request.form['l1'])
    l2 = float(request.form['l2'])
    lon = request.form['lon']
    rows = []
    randval = []
    num = int(request.form['num'])
    elapsed_time = []
    for i in range(num):
        start_time = time.time()
        val = str(round(random.uniform(l1, l2), 1))
        cur = cnxn.cursor()
        cur.execute("select count(*) from quake6 WHERE depthError =? and longitude = ?", (val,lon))
        get = cur.fetchall();
        rows.append(get)
        end_time = time.time()
        e_time=end_time - start_time
        elapsed_time.append(e_time)
        randval.append(val)
    return render_template("list3.html", rows=[rows,randval,elapsed_time])

@app.route('/options5', methods=['POST', 'GET'])
def options5():
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    l1 = float(request.form['l1'])
    l2 = float(request.form['l2'])
    lon = request.form['lon']
    c = request.form['c']
    rows = []
    num = int(request.form['num'])
    if c == 'Cache':
        start_time = time.time()
        for i in range(num):
            val = str(round(random.uniform(l1, l2), 1))
            cur = cnxn.cursor()
            c = "select count(*) from quake6 WHERE depthError =" + val +"and longitude = "+lon
            # cur.execute("select * from all_month WHERE place LIKE ?", ('%'+loc+'%',))
            if r.get(c):
                print('Cached')
                rows.append(r.get(c))
            else:
                print('Not Cached')
                cur.execute("select count(*) from quake6 WHERE depthError =? and longitude = ?", (val,lon))
                get = cur.fetchall();
                rows.append(get)
                r.set(c, str(get))
        end_time = time.time()
        elapsed_time = end_time - start_time
    elif c == "None":
        start_time = time.time()
        for i in range(num):
            val = str(round(random.uniform(l1, l2), 1))
            cur = cnxn.cursor()
            # cur.execute("select * from all_month WHERE place LIKE ?", ('%'+loc+'%',))
            if r.get(c):
                print('Cached')
                rows.append(r.get(c))
            else:
                print('Not Cached')
                cur.execute("select count(*) from quake6 WHERE depthError =? and longitude = ?", (val, lon))
                get = cur.fetchall();
                rows.append(get)
                r.set(c, str(get))
        end_time = time.time()
        elapsed_time = end_time - start_time
    return render_template("list3.html", rows=[rows, elapsed_time])

@app.route('/options6', methods=['POST', 'GET'])
def options6():
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    l1 = float(request.form['l1'])
    l2 = float(request.form['l2'])
    lon = request.form['lon']
    rows = []
    randval = []
    num = int(request.form['num'])
    elapsed_time = []
    for i in range(num):
        start_time = time.time()
        val = str(round(random.uniform(l1, l2), 1))
        cur = cnxn.cursor()
        c = "select count(*) from quake6 WHERE depthError =" + val +"and longitude = "+lon
        if r.get(c):
            print('Cached')
            rows.append(r.get(c))
        else:
            print('Not Cached')
            cur.execute("select count(*) from quake6 WHERE depthError =? and longitude=?", (val,lon))
            get = cur.fetchall();
            rows.append(get)
            r.set(c, str(get))
        end_time = time.time()
        e_time=end_time - start_time
        elapsed_time.append(e_time)
        randval.append(val)
    return render_template("list3.html", rows=[rows,randval,elapsed_time])


if __name__ == '__main__':
    app.run(debug=True)
