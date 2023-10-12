from flask import render_template
from . import app


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/purchase")
def buy():
    return "Se efectuara el cambio de monedas"


@app.route("/status")
def investments():
    return "Estado de inversion"
