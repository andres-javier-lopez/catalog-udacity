# coding: utf-8
"""Defines the API endpoints of the system."""

import json

import flask
import sqlalchemy as sqla
from werkzeug.contrib import atom

import database

def load_controllers(app):
    """Defines the controlleres on the Flask app."""

    @app.route('/catalog.json')
    def json_api():
        """Shows the entire catalog as a JSON file."""
        db_session = database.get_session()
        catalog = db_session.query(database.Category).all()
        return json.dumps(catalog, default=database.parseJSON)

    @app.route('/feed.atom')
    def atom_feed():
        """Returns an atom feed with the latest items.

        Based on http://flask.pocoo.org/snippets/10/
        """
        db_session = database.get_session()
        feed = atom.AtomFeed('Recently added items',
                             feed_url=flask.request.url,
                             url=flask.request.url_root)
        items = db_session.query(database.Item).order_by(
            database.Item.datetime.desc()
        ).limit(20).all()

        for item in items:
            feed.add(item.name, unicode(item.description),
                     content_type='html',
                     url='%scatalog/%s/%d' % (
                        flask.request.url_root,
                        item.category.name,
                        item.id
                     ),
                     updated=item.datetime,
                     published=item.datetime)
        return feed.get_response()

