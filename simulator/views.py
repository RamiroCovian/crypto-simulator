from flask import flash, render_template, request
from . import app, PATH
from .forms import MovementForm
from .models import DBManager, calculate_balance


@app.route("/")
def home():
    db = DBManager(PATH)
    sql = "SELECT id, date, time, from_currency, from_quantity, to_currency, to_quantity FROM movements"
    movements = db.consultSQL(sql)  # Consulto los movimientos realizados
    return render_template("movements.html", movs=movements)


@app.route("/purchase/", methods=["GET", "POST"])
def create_purchase():
    if request.method == "GET":
        movements = {}
        form = MovementForm(data=movements)
        try:
            wallet = calculate_balance()
        except Exception as e:
            flash("Error en el acceso a la base de datos", category="Error")
            return render_template("form_buy.html", form=form)

        crypto_from = [
            "EUR"
        ]  # Creo una lista de monedas disponibles para FROM: EUR + las que tenga con saldo

        try:
            for coin, amount in wallet.items():
                if amount > 0:
                    crypto_from.append(coin)
            form.from_currency.choices = crypto_from  # Restriccion de monedas FROM
        except:
            wallet = "vacio"
            form.from_currency.choices = crypto_from
        return render_template("form_buy.html", form=form, empty="yes", wallet=wallet)

    else:
        # request.method == "POST":
        pass


@app.route("/status")
def calculate_investment():
    return render_template("investments.html")
