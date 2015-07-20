# coding: utf-8
"""Defines the controllers for user login."""

import httplib2
import json
import random
import string

import flask
from flask import session as login_session
from oauth2client import client
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

def load_controllers(app):
    """Defines the module controllers."""

    @app.route('/login')
    def showLogin():
        """Shows the login screen."""
        state = ''.join(random.choice(
            string.ascii_uppercase + string.digits
        ) for x in xrange(32))
        login_session['state'] = state
        return flask.render_template('login.html', STATE=state)

    @app.route('/gconnect', methods=['POST'])
    def gconnect():
        """Process to login with google."""
        # Validate state token
        if flask.request.args.get('state') != login_session['state']:
            response = flask.make_response(
                json.dumps('Invalid state parameter.'), 401
            )
            response.headers['Content-Type'] = 'application/json'
            return response
        # Obtain authorization code
        code = flask.request.data

        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = client.flow_from_clientsecrets('client_secrets.json',
                                                        scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(code)
        except client.FlowExchangeError:
            response = flask.make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = flask.make_response(json.dumps(result.get('error')),
                                           500)
            response.headers['Content-Type'] = 'application/json'

        # Verify that the access token is used for the intended user.
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            response = flask.make_response(
                json.dumps("Token's user ID doesn't match given user ID."), 401
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is valid for this app.
        if result['issued_to'] != CLIENT_ID:
            response = flask.make_response(
                json.dumps("Token's client ID does not match app's."), 401
            )
            print "Token's client ID does not match app's."
            response.headers['Content-Type'] = 'application/json'
            return response

        stored_credentials = login_session.get('credentials')
        stored_gplus_id = login_session.get('gplus_id')
        if stored_credentials is not None and gplus_id == stored_gplus_id:
            response = flask.make_response(
                json.dumps('Current user is already connected.'), 200
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        # Store the access token in the session for later use.
        login_session['credentials'] = credentials.access_token
        login_session['gplus_id'] = gplus_id

        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']

        print "done!"
        return 'ok'

    @app.route('/gdisconnect')
    def gdisconnect():
        """Revokes the google token an deletes user information."""
        # Only disconnect a connected user.
        access_token = login_session.get('credentials')
        if access_token is None:
            response = flask.make_response(
                json.dumps('Current user not connected.'), 401
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
               % access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]

        if result['status'] == '200':
            # Reset the user's sesson.
            del login_session['credentials']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']

            return flask.redirect(flask.url_for('show_catalog'))
        else:
            # For whatever reason, the given token was invalid.
            del login_session['credentials']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']

            response = flask.make_response(
                json.dumps('Failed to revoke token for given user.'), 400
            )
            response.headers['Content-Type'] = 'application/json'
            return response
