from flask import render_template
from . import app


@app.route("/")
def home():
    return render_template("movements.html")


@app.route("/purchase")
def create_purchase():
    return render_template("buy.html")


@app.route("/status")
def calculate_investment():
    return render_template("investments.html")
