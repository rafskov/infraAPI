from flask import Flask, jsonify
import sqlite3

#check if the database exists
import os
if not os.path.exists('data.db'):
    #if not, create it

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

#create a flask API to query the data table in the sqlite database
app = Flask(__name__)
@app.route('/api/<county>/<state>/')
def api(county,state): #create docstring
    """Return the year of the last power outage in a county in a state"""
    #create conn for the database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data WHERE county=? AND state=?",(county, state))
    row = c.fetchone()
    if row:
        return jsonify({'county': row[0], 'state': row[1], 'year': row[2]})
    else:
        return jsonify({'error': 'not found'})
    