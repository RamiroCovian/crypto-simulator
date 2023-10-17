import os
from flask import Flask

PATH = os.path.join("simulator", "data", "investments.db")
app = Flask(__name__)
app.config.from_prefixed_env()
