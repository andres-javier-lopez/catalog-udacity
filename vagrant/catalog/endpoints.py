# coding: utf-8
"""Defines the API endpoints of the system."""

import json

import database

def load_controllers(app):
    """Defines the controlleres on the Flask app."""

    @app.route('/catalog.json')
    def json_api():
        """Shows the entire catalog as a JSON file."""
        db_session = database.get_session()
        catalog = db_session.query(database.Category).all()
        return json.dumps(catalog, default=database.parseJSON)
