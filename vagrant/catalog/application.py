#coding: utf-8
"""Main application."""

import flask
from flask.ext import seasurf

import catalog
import login
import file_upload
import endpoints
import config


app = flask.Flask(__name__)
csrf = seasurf.SeaSurf(app)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.secret_key = 'those_are_my_secretz'
catalog.load_controllers(app)
login.load_controllers(app, csrf)
file_upload.load_controllers(app)
endpoints.load_controllers(app)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
