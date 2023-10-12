from . import app


@app.route("/")
def home():
    return "Mostrara una tabla con moviminetos"


@app.route("/purchase")
def buy():
    return "Se efectuara el cambio de monedas"


@app.route("/status")
def investments():
    return "Estado de inversion"
