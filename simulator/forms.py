from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class MovementForm(FlaskForm):
    from_currency = SelectField(
        "De:",
        choices=[
            ("EUR", "Euro"),
            ("BTC", "Bitcoin"),
            ("ETH", "Ethereum"),
            ("USDT", "Tether UDSt"),
            ("ADA", "Cardano"),
            ("SOL", "Solana"),
            ("XRP", "XRP"),
            ("DOT", "Polkadot"),
            ("DOGE", "Dogecoin"),
            ("SHIB", "Shiba Inu"),
        ],
    )
    to_currency = SelectField(
        "Para:",
        choices=[
            ("EUR", "Euro"),
            ("BTC", "Bitcoin"),
            ("ETH", "Ethereum"),
            ("USDT", "Tether UDSt"),
            ("ADA", "Cardano"),
            ("SOL", "Solana"),
            ("XRP", "XRP"),
            ("DOT", "Polkadot"),
            ("DOGE", "Dogecoin"),
            ("SHIB", "Shiba Inu"),
        ],
    )
    from_quantity = DecimalField(
        "Cantidad:",
        places=6,
        validators=[
            DataRequired(message="No puede haber un movimiento sin cantidad"),
            NumberRange(min=0.00001, max=99999999),
        ],
    )
    to_quantity = DecimalField(
        "Cantidad:",
        places=6,
        validators=[
            DataRequired(message="No puede haber un movimiento sin cantidad"),
            NumberRange(min=0.00001, max=99999999),
        ],
    )
    price_unit = DecimalField(
        "Precio Unitario:",
        places=6,
        validators=[
            DataRequired(message="No puede haber un movimiento sin cantidad"),
            NumberRange(min=0.00001, max=99999999),
        ],
    )

    submit_calcular = SubmitField("Calcular")
    submit_aceptar = SubmitField("Aceptar")
