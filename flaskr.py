import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing   #need this statement in our init_db() function

#Configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True   # Never leave this set to True on a production system since it will allow the user to execute code on the server
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#Create our application
app = Flask(__name__)                #creating a new flask object?
app.config.from_object(__name__)     #configuring it using the uppercase words above

#Connect to the database that we specify
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    #Goes to the DATABASE variable we set up in the config section

#Initialize the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
            #Opens schema.sql file and executes it on the db that we specified
        db.commit()

@app.before_request   #This means that the below function will be called before every request to the server
def before_request():
    g.db = connect_db()   #Open the database connection every time the user interacts with the server
    #We keep the connection open on 'g' which is a special object that works in threaded environments
    #g.db is not a variable name. G is the object and db is an attribute.    

@app.teardown_request  #This function gets executed whenever an exception occurs
def teardown_request(exception):
    g.db.close()   #If an exception occurs, close the database connection

#The functions below allow the users to interact with the site
@app.route('/')
def show_entries():
    cur = g.db.execute('SELECT title, text FROM entries ORDER BY id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
                [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid password"
        else:
            session['logged_in'] = True
            flash("You were logged in")
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


#This makes the server run
if __name__ == '__main__':
    app.run()











