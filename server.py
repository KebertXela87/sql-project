import psycopg2
import psycopg2.extras
import os, uuid
from flask import Flask, render_template, request, redirect, url_for, session
# from flask.ext.socketio import SocketIO, emit
import flask.ext.login as flask_login


app = Flask(__name__, static_url_path='')
# app.config['SECRET_KEY'] = 'secret!'
app.secret_key = os.urandom(24).encode('hex')

# socketio = SocketIO(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

def connectToDB():
    connectionString = 'dbname=thearchives user=jedimaster password=41PubBNmfQhmfCNy host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

# setup all of the values from the users table for the current user
def setup_User(user, data):
    user.id = data['username']
    user.email = 'test'
    user.pic = ''

@login_manager.user_loader
def user_loader(user_id):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT * FROM users WHERE username = %s;", (user_id,))
    data = cur.fetchone()
    if(len(data) > 0):
        user = User()
        setup_User(user, data)
        return user
        
    return #no user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', login_failed = 'false', currentpage = 'login')
    
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
            
        return redirect(url_for('index'))
    
    #login failed
    return render_template('login.html', login_failed = 'true', currentpage = 'login')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

# the page to go to if a login is required and no one is loged in.
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html', login_failed = 'true', currentpage = 'login')
    
@app.route('/')
def index():
    return render_template('index.html', currentpage = 'home')

@app.route('/account')
@flask_login.login_required
def account():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return render_template('account.html', currentpage = 'account')

@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if request.method == 'GET':
        return render_template('create_account.html', currentpage = 'create_account')
    
    #POST
    # check username
    
    usernameinput = request.form['username']
    passwordinput = request.form['password']
    
    print "Checking username...."
    cur.execute("SELECT username FROM users WHERE username = %s;", (usernameinput,))
    if cur.fetchone():
        return render_template('create_account.html', currentpage='create_account', bad_account='badusername', account_created='false')
        
    # make sure passwords match
    print "Checking password...."
    password1 = request.form['password']
    password2 = request.form['retypepassword']
    if password1 != password2:
        return render_template('create_account.html', currentpage='create_account', bad_account='badpassword', account_created='false')
        
    # attempt to create user
    print "Attempting to create user...."
    print "username" + request.form['username'] + " Password: " + request.form['password']
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, crypt(%s, gen_salt('bf')));", (usernameinput, passwordinput))
    except:
        print("Error creating user...")
        db.rollback()
    db.commit()
        
    # check to see if user was created
    print "Checking success of user creation...."
    cur.execute("SELECT username FROM users WHERE username = %s;", (usernameinput,))
    if cur.fetchone():
        # user was created
        print "User created"
        account_created = 'true'
    else:
        # user was NOT created
        print "User not created"
        account_created = 'false'
            
    return render_template('account_created.html', currentpage='create_account', bad_account='unknown', account_created=account_created)

@app.route('/reviews')
def reviews():
    return render_template('reviews.html', currentpage='reviews')
    
@app.route('/timeline')
def timeline():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    movies = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM movies m NATURAL JOIN types t"
    novels = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM novels m NATURAL JOIN types t"
    yabooks = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM ya_books m NATURAL JOIN types t"
    shortstories = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM short_stories m NATURAL JOIN types t"
    comics = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM comics m NATURAL JOIN types t"
    tvshows = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM tv_shows m NATURAL JOIN types t"
    
    cur.execute(movies + " UNION " + novels + " UNION " + yabooks + " UNION " + shortstories + " UNION " + comics + " UNION " + tvshows + " ORDER BY timeline;")
    results = cur.fetchall()
    
    return render_template('timeline.html', currentpage='timeline', results=results)

# @socketio.on('connect', namespace='/timeline')
# def makeConnection(): 
#     print('connected')
    
@app.route('/search')
def search():
    return render_template('search.html', currentpage='search')
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    # socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    