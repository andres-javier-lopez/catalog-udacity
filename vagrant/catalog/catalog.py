#coding: utf-8
import random
import string

import flask

import database
import file_upload

def prepare_login():
    """Configures the state needed for login."""
    if 'state' not in flask.session:
        state = ''.join(random.choice(
            string.ascii_uppercase + string.digits
        ) for x in xrange(32))
        flask.session['state'] = state

def load_controllers(app):
    """Defines the controllers for the catalog module.

    The controllers definitions have to be called explicitly, and don't run
    when the module is imported. This allow us to use the app decorators to
    define the routes.
    """

    @app.route('/css/main.css')
    def load_css():
        """Loads the system css."""
        return flask.send_from_directory('css', 'main.css')

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
        prepare_login()
        categories = db_session.query(database.Category).all()

        last_items = db_session.query(database.Item).order_by(
            database.Item.datetime.desc()
        ).limit(8).all()

        return flask.render_template('recent.html', categories=categories,
                                     items=last_items)

    @app.route('/categories/new', methods=['GET', 'POST'])
    def new_category():
        """Creates a new category.

        Returns:
            An html form if its a GET request, or redirects to the main page if
            its a POST request.
        """
        if 'credentials' in flask.session:
            if not flask.session['credentials']:
                flask.abort(403)
        else:
            flask.abort(403)

        db_session = database.get_session()
        prepare_login()

        if flask.request.method == 'GET':
            return flask.render_template('new_category.html')
        elif flask.request.method == 'POST':
            try:
                category = database.Category(
                    name=flask.request.form['name']
                )
            except KeyError:
                flask.abort(400)
            db_session.add(category)
            db_session.commit()
            return flask.redirect(flask.url_for('show_catalog'))

    @app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
    def modify_category(category_id):
        """Modify the category.

        Args:
            category_id: Id of the category that will be modified.

        Returns:
            An html form if its a GET request, or redirects to the main page if
            its a POST request.
        """
        if 'credentials' in flask.session:
            if not flask.session['credentials']:
                flask.abort(403)
        else:
            flask.abort(403)

        db_session = database.get_session()
        prepare_login()
        category = db_session.query(database.Category).get(category_id)
        if category is None:
            flask.abort(404)

        if flask.request.method == 'GET':
            return flask.render_template('edit_category.html',
                                         category=category)
        elif flask.request.method == 'POST':
            try:
                category.name = flask.request.form['name']
            except KeyError:
                flask.abort(400)
            db_session.commit()
            return flask.redirect(flask.url_for('show_catalog'))

    @app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
    def delete_category(category_id):
        """Deletes the category if its empty.

        Args:
            category_id: Id of the category to be deleted.

        Returns:
            Return an html form if its a GET request, or redirects to the main
            page if its a POST request.
        """
        if 'credentials' in flask.session:
            if not flask.session['credentials']:
                flask.abort(403)
        else:
            flask.abort(403)

        db_session = database.get_session()
        prepare_login()
        category = db_session.query(database.Category).get(category_id)
        if category is None:
            flask.abort(404)

        if flask.request.method == 'GET':
            return flask.render_template('delete_category.html',
                                         category=category)
        elif flask.request.method == 'POST':
            if not category.items:
                db_session.delete(category)
                db_session.commit()
                return flask.redirect(flask.url_for('show_catalog'))
            else:
                flask.abort(500)

    @app.route('/catalog/<string:category_name>')
    def show_category_items(category_name):
        """Returns the item list for a specific category.

        Args:
            category_name: The name of the category that is being listed.

        Returns:
            Html template with the list of items.
        """
        db_session = database.get_session()
        prepare_login()
        categories = db_session.query(database.Category).all()
        category = db_session.query(database.Category).filter(
            database.Category.name == category_name
        ).one()

        return flask.render_template('catalog.html', category=category,
                                     categories=categories,
                                     catalog=category.items)

    @app.route('/catalog/<string:category_name>/<int:item_id>')
    def show_catalog_item(category_name, item_id):
        """Returns the html for a specific item in the catalog.

        Looks for the item in the catalog with the id provided in the url. Then
        returns the template with the item information.

        Args:
            category_name: Name of the current category.
            item_id: Id of the item that will be looked up in the catalog.

        Returns:
            Html with the item information.
        """
        db_session = database.get_session()
        prepare_login()
        categories = db_session.query(database.Category).all()
        item = db_session.query(database.Item).get(item_id)
        if item is not None:
            return flask.render_template('item.html',
                                         category_name=category_name,
                                         categories=categories,
                                         item=item)
        else:
            flask.abort(404)

    @app.route('/catalog/<string:category_name>/new', methods=['GET', 'POST'])
    def new_catalog_item(category_name):
        """Adds a new item to the chosen category.

        Shows a insert form if is a GET request, and inserts a new item to the
        database on a POST request.

        Args:
            category_name: Name of the category which the new item will belong.

        Returns:
            An html form if is a GET request, or redirects to the catalog if
            ifs a POST request.
        """

        if 'credentials' in flask.session:
            if not flask.session['credentials']:
                flask.abort(403)
        else:
            flask.abort(403)

        db_session = database.get_session()
        prepare_login()
        if flask.request.method == 'GET':
            categories = db_session.query(database.Category).all()
            return flask.render_template('new_item.html',
                                         categories=categories,
                                         category_name=category_name)
        elif flask.request.method == 'POST':
            categories = db_session.query(database.Category).all()
            category = db_session.query(database.Category).filter(
                database.Category.name == category_name
            ).one()
            try:
                item = database.Item(
                    name=flask.request.form['name'],
                    description=flask.request.form['description'],
                    image=file_upload.save_upload(),
                    gplus_id=flask.session['gplus_id'],
                    category_id=category.id
                )
            except KeyError:
                flask.abort(401)
            db_session.add(item)
            db_session.commit()
            return flask.redirect(flask.url_for('show_category_items',
                                                category_name=category_name))

    @app.route('/catalog/<string:category_name>/<int:item_id>/edit',
               methods=['GET', 'POST'])
    def edit_catalog_item(category_name, item_id):
        """Allows the edition of a catalog item.

        Shows an edit form if is a GET request, and changes the information of
        the item if is a POST request.

        Args:
            category_name: Name of the current category.
            item_id: Id of the item that will be edited.

        Returns:
            An html form if its a GET request, or redirects to the item if is a
            POST request.
        """

        if 'credentials' in flask.session:
            if not flask.session['credentials']:
                flask.abort(403)
        else:
            flask.abort(403)

        db_session = database.get_session()
        prepare_login()
        item = db_session.query(database.Item).get(item_id)
        if item is None:
            flask.abort(404)

        if flask.request.method == 'GET':
            try:
                if flask.session['gplus_id'] == item.gplus_id:
                    categories = db_session.query(database.Category).all()
                    return flask.render_template('edit_item.html',
                                                 category_name=category_name,
                                                 categories=categories,
                                                 item=item)
                else:
                    flask.abort(404)
            except KeyError:
                flask.abort(401)
        elif flask.request.method == 'POST':
            try:
                if flask.session['gplus_id'] == item.gplus_id:
                    item.name = flask.request.form['name']
                    item.description = flask.request.form['description']
                    filename = file_upload.save_upload()
                    if filename:
                        if item.image:
                            file_upload.delete_upload(item.image)
                        item.image = filename
                else:
                    flask.abort(403)
            except KeyError:
                flask.abort(401)
            db_session.commit()
            return flask.redirect(flask.url_for('show_catalog_item',
                                                category_name=category_name,
                                                item_id=item_id))

    @app.route('/catalog/<string:category_name>/<int:item_id>/delete',
               methods=['GET', 'POST'])
    def delete_catalog_item(category_name, item_id):
        """Allows the deletion of a catalog item.

        Shows a delete confirmation in a GET request, and deletes the item on a
        POST request.

        Args:
            category_name: Name of the current category.
            item_id: Id of the item that will be deleted.

        Returns:
            An html form if its a GET request, or redirects to the item if is a
            POST request.
        """

        try:
            if not flask.session['credentials']:
                flask.abort(403)
        except KeyError:
            flask.abort(403)

        db_session = database.get_session()
        prepare_login()
        item = db_session.query(database.Item).get(item_id)
        if item is None:
            flask.abort(404)

        if flask.request.method == 'GET':
            try:
                if flask.session['gplus_id'] == item.gplus_id:
                    categories = db_session.query(database.Category).all()
                    return flask.render_template('delete_item.html',
                                                 category_name=category_name,
                                                 categories=categories,
                                                 item=item)
                else:
                    flask.abort(403)
            except KeyError:
                flask.abort(401)
        elif  flask.request.method == 'POST':
            try:
                if flask.session['gplus_id'] == item.gplus_id:
                    if item.image:
                        file_upload.delete_upload(item.image)
                    db_session.delete(item)
                else:
                    flask.abort(403)
            except KeyError:
                flask.abort(401)
            db_session.commit()
            return flask.redirect(flask.url_for('show_category_items',
                                                category_name=category_name))
