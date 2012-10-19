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
    cursor = g.db.

#This makes the server run
if __name__ == '__main__':
    app.run()