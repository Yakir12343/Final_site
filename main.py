
from database import Database

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecret"
database = Database()


@app.route("/")
def index():
    database.create_table()
    return render_template('index.html')


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        database.create_table()
        username = request.form['username']
        password = request.form['password']
        hash_password = generate_password_hash(password)
        try:
            database.register(username, hash_password)
            return render_template("quiz.html")
        except sqlite3.IntegrityError:
            return render_template("occupiedname.html")
    return render_template("registration.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.login(username)
        try:
            if check_password_hash(user["password"], password):
                return render_template("quiz.html")
            else:
                return render_template("wrong_login.html")
        except:
            return render_template("wrong_login.html")

    return render_template("authorization.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route('/submit', methods=['POST'])    # НЕ ЗАБУДЬ ПРО него рассказать
def submit():
    score = 0
    capital = request.form.get('capital')
    planets = request.form.get('Planets')
    element = request.form.get('element')
    franzs_work = request.form.get('Franzs_work')
    gas = request.form.get('gas')
    chromosomes = request.form.get("chromosomes")
    answers = {
        capital: "Paris",
        planets: "eight",
        element: "aurum",
        franzs_work: "process",
        gas: "nitrogen",
        chromosomes: "48",
    }
    for key, value in answers.items():
        if key == value:
            score+=1
        else:
            score+=0
    score = str(score)   # из разметки снизу сделать html файл, вернуть через рендер темплаейт

    return render_template("end.html", score=score)








if __name__ == '__main__':
    app.run()
