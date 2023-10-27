import sqlite3
from flask import flash
import requests
from . import app
from config import HEADERS


class DBManager:
    def __init__(self, path):
        self.path = path

    def connect(self):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        return connection, cursor

    def disconnect(self, connection):
        connection.close()

    def consultSQL(self, consult):
        connection, cursor = self.connect()
        cursor.execute(consult)
        data = cursor.fetchall()

        self.records = []
        col_names = []
        for col in cursor.description:
            col_names.append(col[0])
        for fact in data:
            movement = {}
            index = 0
            for name in col_names:
                movement[name] = fact[index]
                index += 1
            self.records.append(movement)

        self.disconnect(connection)
        return self.records

    def get_info_parameters(self, consult, parameters):
        connection, cursor = self.connect()

        cursor.execute(consult, parameters)
        connection.commit()
        data = cursor.fetchall()
        if len(data) == 0:
            return data

        col_names = []
        for col in cursor.description:
            col_names.append(col[0])

        self.records = []
        for fact in data:
            f = {}
            for c, col in enumerate(col_names):
                f[col] = fact[c]
            self.records.append(f)
        self.disconnect(connection)
        return self.records

    def new_buy(self, consult, parameters):
        connection, cursor = self.connect()
        result = False
        try:
            cursor.execute(consult, parameters)
            connection.commit()
            result = True
        except Exception as ex:
            print(ex)
            connection.rollback()

        self.disconnect(connection)
        return result


def calculate_balance():  # Calcula cantidad de monedas
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
    calculation = {}
    for coin in coin_list:
        db = DBManager(app.config["PATH"])
        sql = "SELECT sum(case when to_currency = ? then to_quantity else 0 end) - sum(case when  from_currency = ? then from_quantity else 0 end) as wallet_balance FROM movements;"
        result = db.get_info_parameters(sql, (coin, coin))
        balance = result[0]["wallet_balance"]
        calculation[coin] = balance
    return calculation


def validate(amount, from_curren, to_current):  # validaciones de campos
    wallet = calculate_balance()
    try:
        if amount <= 0.00001:
            error = flash(
                "OPERACIÓN INCORRECTA - La cantidad debe ser superior a 0.00001",
                category="Error",
            )
            return error
    except Exception:
        error = flash(
            "OPERACIÓN INCORRECTA - Utiliza la ' , ' para separar decimales",
            category="Error",
        )
        return error

    if from_curren != "EUR" and wallet[from_curren] < float(amount):
        error = flash(
            "Usted dispone de {:.6f} {} para realizar transacciones.".format(
                wallet[from_curren], from_curren
            ),
            category="Error",
        )
        return error

    if from_curren == to_current:
        error = flash(
            "OPERACIÓN INCORRECTA - Debe elegir dos monedas distintas",
            category="Error",
        )
        return error


def api_request(url):  # Consulta de Api
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        api = response.json()
        return api
    else:
        raise Exception("Problema de consulta tipo {}".format(response.status_code))


def calculate_sum_from_quantity():  # Calcula la sumatoria de EUR invertidos
    db = DBManager(app.config["PATH"])
    sql = "SELECT sum(from_quantity) as from_curr_eur FROM movements WHERE from_currency = 'EUR';"
    result = db.consultSQL(sql)
    return result


def calculate_balance_eur_invested():  # Calcula el saldo de EUR en invertidos
    db = DBManager(app.config["PATH"])
    sql = "SELECT sum(case when to_currency = 'EUR' then to_quantity else 0 end) - sum(case when from_currency = 'EUR' then from_quantity else 0 end) as balance_eur FROM movements;"
    result = db.consultSQL(sql)
    return result
