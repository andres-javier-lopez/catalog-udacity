# coding: utf-8
"""Functions that help with the file upload process."""

import os

import flask
import werkzeug as wkz

import config


def is_allowed(filename):
    """Check if file extension is allowed.

    Args:
        filename: The name of the file.

    Returns:
        Return true if the name of the file is allowed.
    """
    return ('.' in filename and
            filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS)


def save_upload():
    """Save the uploaded file in the uploads directory.

    Returns:
        The route of the uploaded file
    """
    file_ = flask.request.files['file']
    if file_ and is_allowed(file_.filename):
        filename = wkz.secure_filename(file_.filename)
        here = os.path.dirname(__file__)
        file_.save(os.path.join(here, config.UPLOAD_FOLDER, filename))
        return flask.url_for('get_uploaded_file', filename=filename)
    else:
        return ''


def delete_upload(filename):
    """Deletes a file in the upload folder.

    Args:
        filename: name of the file to be delete.
    """
    here = os.path.dirname(__file__)
    os.remove(os.path.join(here, filename.strip('/')))


def load_controllers(app):
    """Defines the file routes for the application.

    Args:
        app: The flask application
    """

    @app.route('/uploads/<filename>')
    def get_uploaded_file(filename):
        """Gets a file that is stored on the uploads folder.

        Args:
            filename: The name of the file.

        Returns:
            The contents of the file.
        """
        return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)
