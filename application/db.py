
import psycopg2
import psycopg2.extras
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        conn = psycopg2.connect(host="127.0.0.1",
            database="chinook",
            user="postgres",
            password="postgres",
            port=5432)
        g.conn = conn
        g.db = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    conn = g.pop('conn', None)

    if db is not None:
        db.close()

    if conn is not None:
        conn.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.execute(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Se inició la db.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


