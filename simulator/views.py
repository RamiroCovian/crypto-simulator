import datetime
from flask import flash, redirect, render_template, request, url_for
from . import app
from .forms import MovementForm
from .models import DBManager, api_request, validate, calculate_balance
from config import ENDPOINT, SERVER


@app.route("/")
def home():
    db = DBManager(app.config["PATH"])
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

    else:  # request.method == "POST":
        form = MovementForm(data=request.form)
        form.from_currency.choices = [
            form.from_currency.data
        ]  # Bloqueo listas una vez elegida
        form.to_currency.choices = [form.to_currency.data]
        wallet = calculate_balance()

        if request.form.get("submit_accept") == "save" and form.validate():
            try:
                db = DBManager(app.config["PATH"])
                sql = "INSERT INTO movements(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?)"
                parameters = (
                    datetime.datetime.now(datetime.timezone.utc).date(),
                    datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"),
                    form.from_currency.data,
                    float(form.from_quantity.data),
                    form.to_currency.data,
                    form.to_quantity.data,
                )
                result = db.new_buy(
                    sql, parameters
                )  # Ejecuta la compra y guarda los datos de la compra
                if result:
                    flash(
                        "EL MOVIMIENTO SE HA GUARDADO CORRECTAMENTE", category="Exito"
                    )
                    return redirect(url_for("home"))
                else:
                    flash(
                        "OPERACIÓN INCORRECTA - Debes presionar el boton 'Calcular' antes de confirmar la compra",
                        category="Error",
                    )
                    return render_template(
                        "form_buy.html", form=form, empty="yes", wallet=wallet
                    )
            except Exception as e:
                flash(
                    "Error de conexion de URL",
                    category="Error",
                )
                return render_template(
                    "form_buy.html", form=form, empty="yes", wallet=wallet
                )
        else:
            amount = form.from_quantity.data
            from_curren = form.from_currency.data
            to_current = form.to_currency.data

            error = validate(amount, from_curren, to_current)
            if error != None:
                return render_template(
                    "form_buy.html", form=form, empty="yes", wallet=wallet
                )

            try:
                url = SERVER + ENDPOINT + from_curren + "/" + to_current
                dicc = api_request(url)
                rate = dicc["rate"]  # Precio de la crypto
                if amount != 0:
                    to_quanti = rate * amount  # Cantidad de compra
                    price_u = amount / to_quanti  # Precio Unitario
                    date_buy = datetime.datetime.now(
                        datetime.timezone.utc
                    ).date()  # fecha y hora del momento de la consulta API
                    time_buy = datetime.datetime.now(datetime.timezone.utc).strftime(
                        "%H:%M:%S"
                    )
                    return render_template(
                        "form_buy.html",
                        empty="no",
                        form=form,
                        to_quanti=to_quanti,
                        price_u=price_u,
                        time_buy=time_buy,
                        date_buy=date_buy,
                        wallet=wallet,
                        amount=amount,
                    )
                else:
                    flash(
                        "OPERACIÓN INCORRECTA - La cantidad debe ser distinta de 0",
                        category="Error",
                    )
                    return render_template("form_buy.html", form=form, empty="yes")
            except Exception as error:
                print(error)
                flash("Error de conexion de URL", category="Error")
                return render_template(
                    "form_buy.html",
                    empty="yes",
                    form=form,
                    wallet=wallet,
                )


@app.route("/status")
def calculate_investment():
    return render_template("investments.html")
