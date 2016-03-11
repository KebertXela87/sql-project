import psycopg2
import psycopg2.extras
import os, uuid
from flask import Flask, render_template, request, redirect, url_for, session, next_is_valid, abort
import flask.ext.login as flask_login

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT username FROM users WHERE username = %s;", (user_id,))
    if cur.fetchone():
        user = User()
        user.id = user_id #change this?
        return user
        
    return #no user

def connectToDB():
    connectionString = 'dbname=thearchives user=jedimaster password=41PubBNmfQhmfCNy host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    #attempt login
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    usernameinput = request.form['username']
    passwordinput = request.form['password']
    
    cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password);", (usernameinput, passwordinput))
    if cur.fetchone():
        user = User()
        user.id = usernameinput
        flask_login.login_user(user)
        
        next = request.args.get('next')
        if not next_is_valid(next):
            return abort(400)
            
        return redirect(next or url_for('account'))
    
    #login failed
    return 'bad login' #change this
    
@app.route('/')
def helloWorld():
    
    if 'username' in session:
        currentUser = session['username']
    else:
        currentUser = ''
        
    return render_template('index.html', currentpage = 'home', user=currentUser)

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if request.method == 'POST':
        # check username
        print "Checking username...."
        cur.execute("SELECT username FROM users WHERE username = '%s';" % (request.form['username'],))
        if cur.fetchone():
            return render_template('account.html', currentpage='account', bad_account='badusername', account_created='false', user=currentUser)
        
        # make sure passwords match
        print "Checking password...."
        password1 = request.form['password']
        password2 = request.form['retypepassword']
        if password1 != password2:
            return render_template('account.html', currentpage='account', bad_account='badpassword', account_created='false', user=currentUser)
            
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
            
        return render_template('account.html', currentpage='account', bad_account='unknown', account_created=account_created, user=currentUser)
    
    if 'username' in session:
        currentUser = session['username']
    else:
        currentUser = ''
        
    return render_template('account.html', currentpage = 'account', user=currentUser)
    
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
            return render_template('account.html', currentpage = 'account', user=currentUser)
    
    if 'username' in session:
        currentUser = session['username']
    else:
        currentUser = ''
    
    return render_template('account.html', currentpage = 'account', user=currentUser)
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    global currentUser
    if request.method == 'POST':
        searchTerm = ''
        
        print request.form['titleSearch']
        print request.form['yearSearch']
        print request.form['timeSearch']
        
        if request.form['titleSearch']:
            print "in titlesearch"
            searchTerm = request.form['titleSearch']
            print "searchTerm: " + searchTerm
            cur.execute("SELECT * FROM movies WHERE UPPER(title) LIKE UPPER(%s);", ("%%" + searchTerm + "%%",))
        elif request.form['yearSearch']:
            print "in year search"
            searchTerm = request.form['yearSearch']
            print "searchTerm: " + searchTerm
            cur.execute("SELECT * FROM movies WHERE bby_aby_year LIKE %s;", ("%%" + searchTerm + "%%",))
        elif request.form['timeSearch']:
            print "in time search"
            searchTerm = request.form['timeSearch']
            print "searchTerm: " + searchTerm
            cur.execute("SELECT * FROM movies WHERE running_time LIKE %s;", ("%" + searchTerm + "%",))
            
        results = cur.fetchall()
        print "Printing results: "
        print results
        if(len(results) > 0):
            return render_template('search.html', currentPage='search', results=results,  nosearch='false', user=currentUser)
        
        return render_template('search.html', currentPage='search', results='',  nosearch='false', user=currentUser)
    
    cur.execute("SELECT * FROM movies;")
    results = cur.fetchall()
    
    if 'username' in session:
        currentUser = session['username']
    else:
        currentUser = ''
        
    return render_template('search.html', currentpage='search', results=results, nosearch='true', user=currentUser)
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)