from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SubmitField


class MovementForm(FlaskForm):
    from_currency = SelectField(
        "De:",
        choices=[("Euro", "EUR"), ("Bitcoin", "BTC"), ("Ethereum", "ETH")],
    )
    to_currency = SelectField(
        "Para:",
        choices=[("Euro", "EUR"), ("Bitcoin", "BTC"), ("Ethereum", "ETH")],
    )
    from_quantity = DecimalField("Cantidad:", places=6)
    to_quantity = DecimalField("Cantidad:", places=6)
    price_unit = DecimalField("Precio Unitario:", places=6)

    submit = SubmitField("Guardar")


"""
#TODO: FALTA VALIDAR CAMPOS
"""
