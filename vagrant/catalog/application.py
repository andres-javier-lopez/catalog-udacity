#coding: utf-8
"""Main application."""

import flask

import catalog
import login
import file_upload
import endpoints
import config

if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.secret_key = 'those_are_my_secretz'
    app.debug = True
    catalog.load_controllers(app)
    login.load_controllers(app)
    file_upload.load_controllers(app)
    endpoints.load_controllers(app)
    app.run(host='0.0.0.0', port=8000)
