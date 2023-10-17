from flask import redirect, render_template, request, url_for
from . import app, PATH
from .forms import MovementForm
from .models import DBManager


@app.route("/")
def home():
    db = DBManager(PATH)
    sql = "SELECT id, date, time, from_currency, from_quantity, to_currency, to_quantity FROM movements"
    movements = db.consultSQL(sql)
    return render_template("movements.html", movs=movements)


@app.route("/purchase/", methods=["GET", "POST"])
def create_purchase():
    if request.method == "GET":
        movements = {}
        form = MovementForm(data=movements)
        return render_template("form_buy.html", form=form)
    if request.method == "POST":
        form = MovementForm(data=request.form)
        db = DBManager(PATH)
        sql = "INSERT INTO movements(from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?)"
        # TODO: Debo cargar DATE y TIME a la db , da error por falta de esos datos!
        parameters = (
            form.from_currency.data,
            float(form.from_quantity.data),
            form.to_currency.data,
            float(form.to_quantity.data),
        )
        result = db.new_buy(sql, parameters)
        if result:
            return redirect(url_for("home"))
        else:
            errors = []
            for key in form.errors:
                errors.append((key, form.errors[key]))
            return render_template("form_buy.html", form=form, errors=errors)


@app.route("/status")
def calculate_investment():
    return render_template("investments.html")
