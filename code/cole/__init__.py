# coding: utf-8

'''
Flask Application for serving `cole` REST API endpoints.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import os

from flask import Flask


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

def create_app(test_config=None):
    '''
    Flask application factory method.
    '''
    # ------------------------------
    # Create and configure the Flask app.
    # ------------------------------
    app = Flask(__name__,
                instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cole.sqlite3'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ------------------------------
    # Set up the Database.
    # ------------------------------
    from . import db
    db.init_app(app)

    # ------------------------------
    # Register Blueprints for Routes.
    # ------------------------------
    from . import collect
    app.register_blueprint(collect.blueprint)

    from . import uniques
    app.register_blueprint(uniques.blueprint)

    # ------------------------------
    # TODO: TEST ROUTE - delete!
    # ------------------------------
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
