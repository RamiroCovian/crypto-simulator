from flask import render_template
from . import app


@app.route("/")
def home():
    return render_template("movements.html")


@app.route("/purchase")
def create_purchase():
    return "Se efectuara el cambio de monedas"


@app.route("/status")
def calculate_investment():
    return "Estado de inversion"
