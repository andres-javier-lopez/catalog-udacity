#coding: utf-8
import flask

import database

def load_controllers(app):
    '''Defines the controllers for the catalog module.

    The controllers definitions have to be called explicitly, and don't run
    when the module is imported. This allow us to use the app decorators to
    define the routes.
    '''

    @app.route('/')
    @app.route('/catalog')
    def show_catalog():
        '''Returns the html with the full catalog.

        Read the database and obtain the item catalog, then loads it into the
        catalog template.
        '''
        db_session = database.get_session()
        catalog = db_session.query(database.Item).all()

        return flask.render_template('catalog.html', catalog=catalog)

    @app.route('/catalog/<int:item_id>')
    def show_catalog_item(item_id):
        '''Returns the html for a specific item in the catalog.

        Looks for the item in the catalog with the id provided in the url. Then
        returns the template with the item information.

        Args:
            item_id: id of the item that will be looked up in the catalog.
        '''
        db_session = database.get_session()
        item = db_session.query(database.Item).get(item_id)
        if item is not None:
            return flask.render_template('item.html', item=item)
        else:
            flask.abort(404)
