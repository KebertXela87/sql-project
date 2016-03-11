import psycopg2
import psycopg2.extras
import os, uuid
from flask import Flask, render_template, request, redirect, url_for, session, abort
import flask.ext.login as flask_login

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

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

@login_manager.user_loader
def user_loader(user_id):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT username FROM users WHERE username = %s;", (user_id,))
    username = cur.fetchone()
    if(len(username) > 0):
        user = User()
        user.id = username
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
    return render_template('timeline.html', currentpage='timeline')

@app.route('/search')
def search():
    return render_template('search.html', currentpage='search')
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    