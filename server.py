import psycopg2
import psycopg2.extras

import os
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def connectToDB():
    connectionString = 'dbname=world user=worldsearch password=on3MHDBoijysi0wy host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
        
@app.route('/')
def helloWorld():
    return render_template('index.html', currentpage = 'home')
    
@app.route('/account')
def account():
    return render_template('account.html', currentpage = 'account')
    
@app.route('/search')
def search():
    return render_template('search.html', currentpage = 'search')
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)