#coding: utf-8

import flask

import catalog

if __name__ == '__main__':
    app = flask.Flask(__name__)
    catalog.load_controllers(app)
    app.run(host='0.0.0.0', port=8000)
