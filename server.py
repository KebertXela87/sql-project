import psycopg2
import psycopg2.extras
import os, uuid, re
from flask import Flask, render_template, request, redirect, url_for, session, Markup
import flask.ext.login as flask_login
from flask_login import current_user
from flask.ext.socketio import SocketIO, emit
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.widgets import TextArea, Input
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

socketio = SocketIO(app)

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
    user.email = data['email']
    user.pic = data['profilepic']

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
        return render_template('login.html', login_failed='false', currentpage='login')
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
            
        return redirect(url_for('user_account'))

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
    useremailinput = request.form['email']
    profilepicinput = request.form['profilepic']
    
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
    
    
    # make sure email doesn't exist
    print "Checking email...."
    pattern = re.compile("\A\S+@\S+\.\S+\Z")
    cur.execute("SELECT email FROM users WHERE email = %s;", (useremailinput,))
    if cur.fetchone() or not pattern.match(useremailinput):
        return render_template('create_account.html', currentpage='create_account', bad_account='bademail', account_created='false')
        
    # attempt to create user
    print "Attempting to create user...."
    print "username" + request.form['username'] + " Password: " + request.form['password']
    try:
        cur.execute("INSERT INTO users (username, password, email, profilepic) VALUES (%s, crypt(%s, gen_salt('bf')), %s, %s);", (usernameinput, passwordinput, useremailinput, profilepicinput))
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
            
    return render_template('account_created.html', currentpage='create_account', bad_account='unknown', account_created=account_created, user=usernameinput)

@app.route('/useraccount', methods=('GET', 'POST'))
def user_account():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #print out the reviews
    cur.execute("SELECT r.id, r.review_text, r.review_item_id, r.review_rating FROM reviews r JOIN users u ON r.reviewer_id = u.id WHERE r.reviewer_id = (SELECT id FROM users WHERE username = %s) ORDER BY id DESC;", (current_user.id,))
    results = cur.fetchall()
    
    reviewResults = []
    
    if(len(results) > 0):
        for result in results:
            cur.execute("SELECT title FROM movies WHERE timeline_id = %s UNION SELECT title FROM novels WHERE timeline_id = %s UNION SELECT title FROM ya_books WHERE timeline_id = %s UNION SELECT title FROM short_stories WHERE timeline_id = %s UNION SELECT title FROM comics WHERE timeline_id = %s UNION SELECT title FROM tv_shows WHERE timeline_id = %s;", (result[2], result[2], result[2], result[2], result[2], result[2]))
            item_name = cur.fetchone()
            reviewText = Markup(result[1])
            tmp = {'username': current_user.id, 'review_text': reviewText, 'item_name': item_name[0], 'rating': result[3]}
            reviewResults.append(tmp)
    
    if request.method == 'GET':
        return render_template('user_account.html', currentpage='account', reviewResults=reviewResults)
    
    #POST
    
    newpassword = request.form['password']
    newpassword2 = request.form['retypepassword']
    if newpassword != newpassword2:
        return render_template('user_account.html', currentpage='account', bad_pass='true', reviewResults=reviewResults)
    
    try:
        cur.execute("SELECT password FROM users WHERE username = %s;", (current_user.id,))
        result = cur.fetchone()
        currentpass = result[0]
        currentUser = current_user.id
        cur.execute("UPDATE users SET password = crypt(%s, gen_salt('bf')) WHERE password = %s AND username = %s;", (newpassword, currentpass, currentUser))
    except:
        print("Error creating user...")
        db.rollback()
    db.commit()
    
    return render_template('user_account.html', currentpage='account', bad_pass='false', reviewResults=reviewResults)
    
    
    
@app.route('/reviews', methods=('GET', 'POST'))
def reviews():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    form = ReviewForm()
    
    if request.method == 'POST':
        item = form.items.data
        thereview = form.review_text.data
        therating = request.form['rating']
        theuser = current_user.id
        
        # get item id
        cur.execute("SELECT timeline_id FROM movies WHERE title = %s UNION SELECT timeline_id FROM novels WHERE title = %s UNION SELECT timeline_id FROM ya_books WHERE title = %s UNION SELECT timeline_id FROM short_stories WHERE title = %s UNION SELECT timeline_id FROM comics WHERE title = %s UNION SELECT timeline_id FROM tv_shows WHERE title = %s;", (item, item, item, item, item, item))
        item_id = cur.fetchone()
        
        # get user id
        cur.execute("SELECT id FROM users WHERE username = %s;", (theuser,))
        user_id = cur.fetchone()
        
        # insert review into review database
        try:
            cur.execute("INSERT INTO reviews (reviewer_id, review_text, review_item_id, review_rating) VALUES (%s, %s, %s, %s);", (user_id[0], thereview, item_id[0], therating))
        except:
            print("Error inserting review...")
            db.rollback()
        db.commit()
    
    q = "SELECT title FROM movies UNION SELECT title FROM novels UNION SELECT title FROM ya_books UNION SELECT title FROM short_stories UNION SELECT title FROM comics UNION SELECT title FROM tv_shows ORDER BY title;"
    cur.execute(q)
    results = cur.fetchall()
    form.items.choices = [(result['title'], result['title']) for result in results]
    
    #print out the reviews
    cur.execute("SELECT id, reviewer_id, review_text, review_item_id, review_rating FROM reviews ORDER BY id DESC;")
    results = cur.fetchall()
    
    reviewResults = []
    
    if(len(results) > 0):
        for result in results:
            cur.execute("SELECT username FROM users WHERE id = %s;", (result[1],))
            user_name = cur.fetchone()
            cur.execute("SELECT title FROM movies WHERE timeline_id = %s UNION SELECT title FROM novels WHERE timeline_id = %s UNION SELECT title FROM ya_books WHERE timeline_id = %s UNION SELECT title FROM short_stories WHERE timeline_id = %s UNION SELECT title FROM comics WHERE timeline_id = %s UNION SELECT title FROM tv_shows WHERE timeline_id = %s;", (result[3], result[3], result[3], result[3], result[3], result[3]))
            item_name = cur.fetchone()
            reviewText = Markup(result[2])
            tmp = {'username': user_name[0], 'review_text': reviewText, 'item_name': item_name[0], 'rating': result[4]}
            reviewResults.append(tmp)
        
    return render_template('reviews.html', currentpage='reviews', form=form, reviewResults=reviewResults)
    
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
    
@app.route('/search')
def search():
    return render_template('search.html', currentpage='search')
    
@socketio.on('connect', namespace='/archives')
def makeConnection(): 
    print('connected')

@socketio.on('search', namespace='/archives')
def new_search(sTerm):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    print("In socketio 'search'")
    searchResults = []
    
    movies = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM movies m NATURAL JOIN types t WHERE (UPPER(m.year) LIKE UPPER(%s) OR UPPER(m.title) LIKE UPPER(%s) OR UPPER(t.type_name) LIKE UPPER(%s) OR UPPER(to_char(m.released, 'Month DD YYYY')) LIKE UPPER(%s))"
    novels = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM novels m NATURAL JOIN types t WHERE (UPPER(m.year) LIKE UPPER(%s) OR UPPER(m.title) LIKE UPPER(%s) OR UPPER(t.type_name) LIKE UPPER(%s) OR UPPER(to_char(m.released, 'Month DD YYYY')) LIKE UPPER(%s))"
    yabooks = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM ya_books m NATURAL JOIN types t WHERE (UPPER(m.year) LIKE UPPER(%s) OR UPPER(m.title) LIKE UPPER(%s) OR UPPER(t.type_name) LIKE UPPER(%s) OR UPPER(to_char(m.released, 'Month DD YYYY')) LIKE UPPER(%s))"
    shortstories = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM short_stories m NATURAL JOIN types t WHERE (UPPER(m.year) LIKE UPPER(%s) OR UPPER(m.title) LIKE UPPER(%s) OR UPPER(t.type_name) LIKE UPPER(%s) OR UPPER(to_char(m.released, 'Month DD YYYY')) LIKE UPPER(%s))"
    comics = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM comics m NATURAL JOIN types t WHERE (UPPER(m.year) LIKE UPPER(%s) OR UPPER(m.title) LIKE UPPER(%s) OR UPPER(t.type_name) LIKE UPPER(%s) OR UPPER(to_char(m.released, 'Month DD YYYY')) LIKE UPPER(%s))"
    tvshows = "SELECT m.timeline_id AS timeline, m.year, m.title, t.type_name, to_char(m.released, 'Month DD YYYY') AS date FROM tv_shows m NATURAL JOIN types t WHERE (UPPER(m.year) LIKE UPPER(%s) OR UPPER(m.title) LIKE UPPER(%s) OR UPPER(t.type_name) LIKE UPPER(%s) OR UPPER(to_char(m.released, 'Month DD YYYY')) LIKE UPPER(%s))"
    
    unionquery = movies + " UNION " + novels + " UNION " + yabooks + " UNION " + shortstories + " UNION " + comics + " UNION " + tvshows + " ORDER BY timeline;"
    print(unionquery % ("%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%"))
    cur.execute(unionquery, ("%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%", "%%" + sTerm + "%%"))
    results = cur.fetchall()
    
    if(len(results) > 0):
        for result in results:
            tmp = {'year': result[1], 'title': result[2], 'type_name': result[3], 'date': result[4]}
            searchResults.append(tmp)
    
        for searchResult in searchResults:
            print(searchResult)
            emit('searchResult', searchResult)
        emit('showResults')
    else:
        emit('showNoResults')


#form classes
class ReviewForm(Form):
    items = SelectField(u'Pick an item', validators=[DataRequired()])
    review_text = StringField(u'name', widget=TextArea(), validators=[DataRequired()])

if __name__ == '__main__':
    #app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    