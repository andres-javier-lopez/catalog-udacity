#coding: utf-8

import flask

import catalog
import login

if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.secret_key = 'those_are_my_secretz'
    app.debug = True
    catalog.load_controllers(app)
    login.load_controllers(app)
    app.run(host='0.0.0.0', port=8000)
