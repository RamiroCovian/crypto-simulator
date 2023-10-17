from flask import render_template, request
from . import app, PATH
from .forms import MovementForm
from .models import DBManager


@app.route("/")
def home():
    db = DBManager(PATH)
    sql = "SELECT id, date, time, from_currency, from_quantity, to_currency, to_quantity FROM movements"
    movements = db.consultSQL(sql)
    return render_template("movements.html", movs=movements)


@app.route("/purchase", methods=["GET", "POST"])
def create_purchase():
    if request.method == "GET":
        movements = {}
        form = MovementForm(data=movements)
    return render_template("form_buy.html", form=form)


@app.route("/status")
def calculate_investment():
    return render_template("investments.html")
