from flask import flash, redirect, render_template, request, url_for
from . import app, PATH
from .forms import MovementForm
from .models import DBManager
import datetime


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

    form = MovementForm(request.form)
    from_currency = request.values.get("from_currency")
    to_currency = request.values.get("to_currency")
    from_quantity = request.values.get("from_quantity")
    to_quantity = request.values.get("to_quantity")
    price_unit = request.values.get("price_unit")

    if request.values.get("submit_calcular"):
        if not form.validate():
            if from_quantity == "" or from_quantity == "0":
                flash(
                    "LAS CANTIDADES de venta DEBEN SER SUPERIOR A 0.00001",
                    category="Error",
                )
                return render_template("form_buy.html", form=form)
            if to_quantity == "" or to_quantity == "0":
                flash(
                    "LAS CANTIDADES de compra DEBEN SER SUPERIOR A 0.00001",
                    category="Error",
                )
                return render_template("form_buy.html", form=form)
            if price_unit == "" or price_unit == "0":
                flash(
                    "LAS CANTIDADES de unidades DEBEN SER SUPERIOR A 0.00001",
                    category="Error",
                )
                return render_template("form_buy.html", form=form)

        if from_currency == to_currency:
            flash(
                "OPERACIÓN INCORRECTA - DEBE ELEGIR DOS MONEDAS DISTINTAS",
                category="Error",
            )
            return render_template("form_buy.html", form=form)

    if request.method == "POST":
        form = MovementForm(data=request.form)
        db = DBManager(PATH)
        sql = "INSERT INTO movements(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?)"
        parameters = (
            datetime.datetime.now(datetime.timezone.utc).date(),
            datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S.%f"),
            form.from_currency.data,
            float(form.from_quantity.data),
            form.to_currency.data,
            float(form.to_quantity.data),
        )
        result = db.new_buy(sql, parameters)
        if result:
            flash("EL MOVIMIENTO SE HA GUARDADO CORRECTAMENTE", category="Exito")
            return redirect(url_for("home"))

        else:
            errors = []
            for key in form.errors:
                errors.append((key, form.errors[key]))
            return render_template("form_buy.html", form=form, errors=errors)


@app.route("/status")
def calculate_investment():
    return render_template("investments.html")
