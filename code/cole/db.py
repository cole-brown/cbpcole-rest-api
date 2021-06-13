# coding: utf-8

'''
Database Setup for Flask.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from flask import Flask

import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Flask DB Functions
# -----------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    '''
    Add our datbase to Flask's magic 'g'.
    '''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error: Optional[Exception] = None) -> None:
    '''
    Remove our datbase from Flask's magic 'g'.
    '''
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app: 'Flask') -> None:
    '''
    Connect our database functions to the Flask `app`.
    '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# ------------------------------------------------------------------------------
# Init DB from schema file.
# ------------------------------------------------------------------------------

def init_db() -> None:
    '''
    Initialize the database according to the schema.
    '''
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command() -> None:
    '''
    Command to clear the existing data and create new tables.
    '''
    init_db()
    click.echo('Initialized the database.')
