import sqlite3
import os
import uuid
from contextlib import closing
from canary import config, app
from flask import g

__all__ = ['dbsetup', 'validate', 'getrecord', 'getiprecords',
           'getemailrecords', 'makenew', 'removekey', 'changerestricted']


@app.teardown_request
def teardown_request(exception):
    """Disconnect from the database."""
    if hasattr(g, '_keydb'):
        g._keydb.close()
    pass


def dbconnect():
    """Return a connection to the API keys database."""
    return sqlite3.connect(os.path.join(config['DB_DIR'], config['APIKEY_DB']))


def getconn():
    """Get the connection to the database, opening a new one if necessary."""
    db = getattr(g, '_keydb', None)
    if db is None:
        db = g._keydb = dbconnect()
    return db


def dbsetup():
    """Setup the DB if necessary."""
    with closing(dbconnect()) as db:
        with app.open_resource('keys.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def dbquery(query, args=(), one=False, commit=False):
    """Query the database with the specified query and arguments.

    Return a list of result dictionaries, or, if one=True, either a single result dict or None.
    Commit changes if commit=True.

    """
    db = getconn()
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    if commit:
        db.commit()
    return (rv[0] if rv else None) if one else rv


def validate(key, remote_addr):
    """Return whether the specified key is valid for the specified IP."""
    if not key:
        return False
    try:
        row = getrecord(key)
    except Exception:
        return False
    if not row:
        return False
    return row['restricted'] is 0 or row['ip'] == remote_addr


def getrecord(key):
    """Return the information for the API key or None if it doesn't exist."""
    return dbquery('select * from keys where apikey = ?', [key], one=True)


def getiprecords(ip):
    """Return the information for the API keys corresponding to the IP."""
    return dbquery('select * from keys where ip = ?', [ip])


def getemailrecords(email):
    """Return the information for the API keys corresponding to the email."""
    return dbquery('select * from keys where email = ?', [email])


def makenew(restricted, ip, email, key=None):
    """Return a new API key for the specified IP, email, and restriction level.

    Use key as the key if it is set.  Otherwise, create a new UUID.
    Throw an ExistingKeyError if unable to create a new UUID or if the specified key already exists.

    """
    tries = 2
    while tries > 0:
        tries -= 1
        key = key or uuid.uuid4()
        try:
            dbquery(
                "insert into keys (apikey, restricted, ip, email, created) values (?, ?, ?, ?, strftime('%s', 'now'))",
                [str(key), 1 if restricted else 0, ip, email], commit=True)
            return key
        except sqlite3.IntegrityError:
            # that UUID is already in the db
            pass
    # give up after hitting 2 existing UUIDs
    raise ExistingKeyError


def removekey(key):
    """Remove an API key from the database."""
    dbquery('delete from keys where apikey = ?', [key], commit=True)


def changerestricted(key, restricted):
    """Change the restriction level of an API key."""
    dbquery('update keys set restricted = ? where apikey = ?',
            [restricted, key], commit=True)


class ExistingKeyError(Exception):
    """Represents a key collision."""
    pass
