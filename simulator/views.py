from flask import render_template
from . import app, PATH
from .models import DBManager


@app.route("/")
def home():
    db = DBManager(PATH)
    sql = "SELECT id, date, time, from_currency, from_quantity, to_currency, to_quantity FROM movements"
    movements = db.consultSQL(sql)
    return render_template("movements.html", movs=movements)


@app.route("/purchase")
def create_purchase():
    return render_template("buy.html")


@app.route("/status")
def calculate_investment():
    return render_template("investments.html")
