#coding: utf-8

import flask

import catalog
import login
import file_upload
import endpoints

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = 'those_are_my_secretz'
    app.debug = True
    catalog.load_controllers(app)
    login.load_controllers(app)
    file_upload.load_controllers(app)
    endpoints.load_controllers(app)
    app.run(host='0.0.0.0', port=8000)
