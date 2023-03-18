from flask import Flask, jsonify

#create a sqlite database to store the data
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

#create a table with columns for county, state, year
c.execute('''CREATE TABLE data (county text, state text, year integer)''')

#load data from poweroutage.csv into the database
import csv
with open('poweroutage.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) #skip header
    for row in reader:
        c.execute("INSERT INTO data VALUES (?, ?, ?)", row)

#create a flask API to query the database
app = Flask(__name__)
@app.route('/api/<county>/<state>/<year>')
def api(county, state, year):
    c.execute("SELECT * FROM data WHERE county=? AND state=? AND year=?", (county, state, year))
    return jsonify(c.fetchall())

