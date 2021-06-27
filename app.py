# Copyright (c) 2021 Veera Lupunen

from flask import Flask
import logging
from os import getenv

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes