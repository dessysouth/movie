from flask import Flask, render_template
from model import * 
from list import list
from auth import auth



@app.route("/")
def landing_page():
    return render_template("index.html")

@app.route('/home', method=['GET'])
def home():
    return render_template('home.html')


@app.route('/detail', method=['GET'])
def home():
    return render_template('home.html')



app.register_blueprint(list)
app.register_blueprint(auth)

