from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class MovementForm(FlaskForm):
    from_currency = SelectField(
        "De:",
        choices=[],
    )
    to_currency = SelectField(
        "Para:",
        choices=[
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
        ],
    )
    from_quantity = FloatField(
        "Cantidad:",
        validators=[
            DataRequired(message="No puede haber un movimiento sin cantidad"),
            NumberRange(min=0.00001, max=99999999),
        ],
        render_kw={"readonly": False},
    )
    to_quantity = FloatField(
        "Cantidad:",
        render_kw={"readonly": True},
    )
    price_unit = FloatField(
        "Precio Unitario:",
        render_kw={"readonly": True},
    )

    submit_calculate = SubmitField("Calcular")
    submit_accept = SubmitField("Aceptar")
