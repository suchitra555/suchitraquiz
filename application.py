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
def q6():
    return render_template('options.html')

@app.route('/q8')
def q8():
    return render_template('options1.html')


@app.route('/restrictedlat')
def restrictedlat():
    return render_template('lat.html')

@app.route('/list', methods = ['POST', 'GET'])
def list():
   con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
   cur = con.cursor()
   dep1 = float(request.form['dep1'])
   dep2 = float(request.form['dep2'])
   cur.execute("select StateName from voting_modified where TotalPop  between 2000 and 8000")
   rows = cur.fetchall()
   con.close()
   return render_template("list.html",rows = rows)

@app.route('/list1', methods = ['POST', 'GET'])
def list1():
   con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
   cur = con.cursor()
   dep1 = float(request.form['dep1'])
   dep2 = float(request.form['dep2'])
   cur.execute("select StateName from voting_modified where TotalPop  between 8000 and 40000")
   rows = cur.fetchall()
   con.close()
   return render_template("list3.html",rows = rows)

# @app.route('/options4', methods = ['POST', 'GET'])
# def options4():
#    con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
#    cur = con.cursor()
#    start_time = time.time()
#    num = int(request.form['num'])
#    for i in range(num):
#        val = round(random.uniform(10.0,12.5),1)
#        val2 = round(random.uniform(10.0,12.5),1)
#        cur.execute("select latitude,longitude,time,depthError from quake6 where depthError between ? and ?",(val,val2))
#        rows = cur.fetchall()
#        # print(rows)
#    con.close()
#    st = []
#    st.append(rows)
#    end_time = time.time()
#    elapsed_time = end_time - start_time
#    return render_template("lists1.html",rows = st,elapsedtime=elapsed_time)
#
# @app.route('/options5', methods=['POST', 'GET'])
# def options5():
#     cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
#     r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
#     start_time = time.time()
#     num = int(request.form['num'])
#     depth1 = float(request.form['depth1'])
#     depth2 = float(request.form['depth2'])
#     opt = request.form['opt']
#
#     rows = []
#     c = []
#     if (opt == 'n' or 'all'):
#         print("-- n ---")
#         for i in range(num):
#
#             val1 = random.uniform(depth1, depth2)
#             val2 = random.uniform(val1, depth2)
#             cur = cnxn.cursor()
#             a = "select latitude, longitude, time, depth from quake where depth between " + str(val1) + " and " + str(val2)
#
#             cur.execute("select latitude, longitude, time, depth from quake where depth between ? and  ?",
#                     (str(val1), str(val2),))
#             get = cur.fetchall()
#             rows.append(get)
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#
#     if (opt == 'im' or 'all'):
#         for i in range(num):
#             val1 = random.uniform(depth1, depth2)
#             val2 = random.uniform(val1, depth2)
#             cur = cnxn.cursor()
#             a = "select latitude, longitude, time, depth from quake where depth between " + str(val1) + " and " + str(
#                 val2)
#             if r.get(a):
#                 c.append('Cached')
#                 rows.append(r.get(a))
#             else:
#                 c.append('Not Cached')
#                 cur.execute("select latitude, longitude, time, depth from quake where depth between ? and  ?",
#                             (str(val1), str(val2),))
#                 get = cur.fetchall()
#                 rows.append(get)
#                 r.set(a, str(get))
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#
#     return render_template("list1.html", rows=rows, elapsed_time=elapsed_time)
#
# @app.route('/options6', methods=['POST', 'GET'])
# def options6():
#     cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
#     r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
#     start_time = time.time()
#     num = int(request.form['num'])
#     depth1 = float(request.form['depth1'])
#     depth2 = float(request.form['depth2'])
#
#     rows = []
#     c = []
#     for i in range(num):
#         val1 = random.uniform(depth1, depth2)
#         val2 = random.uniform(val1, depth2)
#         cur = cnxn.cursor()
#         a = "select latitude, longitude, time, depth from quake where depth between "+str(val1)+" and "+str(val2)
#         if r.get(a):
#             c.append('Cached')
#             rows.append(r.get(a))
#         else:
#             c.append('Not Cached')
#             cur.execute("select latitude, longitude, time, depth from quake where depth between ? and  ?",
#                 (str(val1), str(val2),))
#             get = cur.fetchall()
#             rows.append(get)
#             r.set(a, str(get))
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return render_template("list1.html", rows=rows, elapsed_time=elapsed_time)


if __name__ == '__main__':
    app.run(debug=True)
