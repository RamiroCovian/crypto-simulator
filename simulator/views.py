import datetime
from flask import flash, redirect, render_template, request, url_for
from . import app
from .forms import MovementForm
from .models import (
    DBManager,
    api_request,
    calculate_balance,
    calculate_balance_eur_invested,
    calculate_sum_from_quantity,
    validate,
)
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
        except Exception:
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
            except Exception:
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
            except Exception:
                flash("Error de conexion de URL", category="Error")
                return render_template(
                    "form_buy.html",
                    empty="yes",
                    form=form,
                    wallet=wallet,
                )


@app.route("/status")
def calculate_investment():
    try:
        consult = calculate_sum_from_quantity()  # euros invertidos
        total_euros_invested = consult[0]["from_curr_eur"]
        print(total_euros_invested)
        consult_2 = calculate_balance_eur_invested()  # saldo de euros invertidos
        balance_of_euros_invested = consult_2[0]["balance_eur"]
        print(balance_of_euros_invested)
        try:
            coin_list = [
                "EUR",
                "BTC",
                "ETH",
                "USDT",
                "ADA",
                "SOL",
                "XRP",
                "DOT",
                "DOGE",
                "SHIB",
            ]
            to = "EUR"
            coin_price_list = []
            i = 0
            if i <= 8:
                for coin in coin_list:
                    url = SERVER + ENDPOINT + coin + "/" + to
                    dicc = api_request(url)
                    rate = dicc["rate"]
                    coin_price_list.append(rate)
                    i += 1

            coin_with_rate = dict(
                zip(coin_list, coin_price_list)
            )  # precios actuales de las cryptos de coin_list

        except Exception as error:
            print(error)
            flash("Error de conexion de URL", category="Error")
            return render_template("investments.html")

        wallet = calculate_balance()  # monedas en la billetera
        values_cryptos_in_wallet = {}
        for rate in coin_with_rate:
            for rate in wallet:
                values_cryptos_in_wallet[rate] = (
                    coin_with_rate[rate] * wallet[rate]
                )  # Multiplico las monedas de mi billetera por el valor actual

        value_in_cryptos = 0
        first_value = True

        for value in values_cryptos_in_wallet.values():
            if first_value:
                first_value = False
            else:
                value_in_cryptos += value  # Valores de mis monedas sin los EUR

        current_value = (
            total_euros_invested + balance_of_euros_invested + value_in_cryptos
        )  # Valor actual

        difference_before = (
            balance_of_euros_invested + value_in_cryptos
        )  # Diferencia para saber si es ganancia/perdida

        if difference_before >= 0:
            status = "Positivo"
        else:
            status = "Negativo"

        return render_template(
            "investments.html",
            total_euros_invested=total_euros_invested,
            current_value=current_value,
            difference_before=difference_before,
            status=status,
        )
    except Exception:
        flash("Error en el acceso a la base de datos", category="Error")
        return render_template("investments.html")
