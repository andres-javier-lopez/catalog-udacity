#coding: utf-8
import flask

import database

def load_controllers(app):
    """Defines the controllers for the catalog module.

    The controllers definitions have to be called explicitly, and don't run
    when the module is imported. This allow us to use the app decorators to
    define the routes.
    """

    @app.route('/')
    @app.route('/catalog')
    def show_catalog():
        """Returns the html with the full catalog sorted in categories.

        Read the database and obtain the item catalog, then loads it into the
        catalog template.

        Returns:
            Html template with the list of categories.
        """
        db_session = database.get_session()
        catalog = db_session.query(database.Category).all()

        return flask.render_template('categories.html', catalog=catalog)

    @app.route('/catalog/<string:category_name>')
    def show_category_items(category_name):
        """Returns the item list for a specific category.

        Args:
            category_name: The name of the category that is being listed.

        Returns:
            Html template with the list of items.
        """
        db_session = database.get_session()
        category = db_session.query(database.Category).filter(
                database.Category.name == category_name
            ).one()

        return flask.render_template('catalog.html', category=category,
                                     catalog=category.items)

    @app.route('/catalog/<string:category_name>/<int:item_id>')
    def show_catalog_item(category_name, item_id):
        """Returns the html for a specific item in the catalog.

        Looks for the item in the catalog with the id provided in the url. Then
        returns the template with the item information.

        Args:
            category_name: Name of the current category. Its not used.
            item_id: Id of the item that will be looked up in the catalog.

        Returns:
            Html with the item information.
        """
        _ = category_name
        db_session = database.get_session()
        item = db_session.query(database.Item).get(item_id)
        if item is not None:
            return flask.render_template('item.html', item=item)
        else:
            flask.abort(404)
