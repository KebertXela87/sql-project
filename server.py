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
    connectionString = 'dbname=thearchives user=jedimaster password=41PubBNmfQhmfCNy host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
        
@app.route('/')
def helloWorld():
    return render_template('index.html', currentpage = 'home')

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if request.method == 'POST':
        # check username
        print "Checking username...."
        cur.execute("SELECT username FROM users WHERE username = '%s';" % (request.form['username'],))
        if cur.fetchone():
            return render_template('account.html', currentpage='account', bad_account='badusername', account_created='false')
        
        # make sure passwords match
        print "Checking password...."
        password1 = request.form['password']
        password2 = request.form['retypepassword']
        if password1 != password2:
            return render_template('account.html', currentpage='account', bad_account='badpassword', account_created='false')
            
        # attempt to create user
        print "Attempting to create user...."
        print "username" + request.form['username'] + " Password: " + request.form['password']
        try:
            cur.execute("INSERT INTO users (username, password) VALUES ('%s', crypt('%s', gen_salt('bf')));" % (request.form['username'], request.form['password']))
        except:
            print("Error creating user...")
            db.rollback()
        db.commit()
        
        # check to see if user was created
        print "Checking success of user creation...."
        cur.execute("SELECT username FROM users WHERE username = '%s';" % (request.form['username'],))
        if cur.fetchone():
            # user was created
            print "User created"
            account_created = 'true'
        else:
            # user was NOT created
            print "User not created"
            account_created = 'false'
            
        return render_template('account.html', currentpage='account', bad_account='unknown', account_created=account_created)
            
    return render_template('account.html', currentpage = 'account')
    
@app.route('/account', methods=['GET', 'POST'])
def account():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if request.method == 'POST':
        
        if 'username' in session:
            oldUser = [session['username'], session['password']]
        else:
            oldUser = ['', '']
            
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        
        cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password);", (session['username'], session['password']))
        if cur.fetchone():
            return redirect(url_for('search'))
        else:
            return render_template('account.html', currentpage = 'account')
    
    return render_template('account.html', currentpage = 'account')
    
@app.route('/search')
def search():
    return render_template('search.html', currentpage = 'search')
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)