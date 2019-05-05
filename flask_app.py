
# from app import app
# from db_setup import init_db, db_session
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from forms import SearchForm
from tables import Results
import pandas as pd

import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = SECRET_KEY

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="bcschiffler",
    password="6bo@XGXyO8Y3eJpkF8ym",
    hostname="bcschiffler.mysql.eu.pythonanywhere-services.com",
    databasename="bcschiffler$letterboxd",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'Movie'
    index = db.Column(db.Integer)
    user = db.Column(db.String(40), nullable=False)
    movie_id = db.Column(db.String(10), nullable=False, primary_key=True)
    info = db.relationship('Info', lazy=True)

class Info(db.Model):
    __tablename__ = 'Info'
    index = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(10), db.ForeignKey('Movie.movie_id'), nullable=False)
    image_src = db.Column(db.String(100))
    name = db.Column(db.String(50))
    path = db.Column(db.String(50))

class User(db.Model):
    __tablename__ = 'User'
    index = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(40), nullable=False)
    rec_users = db.Column(db.String(100))

@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        if request.form['action'] == 'Search':
            return search_results(search)
        elif request.form['action'] == 'Random':
            return search_results('random')
    return render_template('index.html', form=search)

@app.route('/')
def search_results(search):
    results = []

    if search == 'random':

        random_user = db.session.query(Movie.user).order_by(func.rand()).offset(20).limit(1).all()[0][0]

        qry = db.session.query(Info).join(Movie).filter(
            Movie.user == random_user)
        results = qry.all()

        user_qry = db.session.query(User).filter(
            User.user == random_user).limit(5)
        user_results = user_qry.all()

        search = SearchForm(request.form)

    else:

        search_string = search.data['search'].strip()

        if search_string:

            qry = db.session.query(Info).join(Movie).filter(
                Movie.user == search_string)
            results = qry.all()

            user_qry = db.session.query(User).filter(
                User.user == search_string).limit(5)
            user_results = user_qry.all()

    if not results:
        flash('No recommendations found for this user!')
        return redirect('/')
    else:
        # display results
        #table = Results(results)
        #table.border = True
        return render_template('index.html', results=results, user_results=user_results, form=search)

if __name__ == '__main__':
    app.run()