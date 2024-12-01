import sqlite3
import click
import os #Navigation im Dateisystem
from flask import current_app, g

def get_db_con():
    if 'db_con' not in g:
        g.db_con = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db_con.row_factory = sqlite3.Row
    return g.db_con
#Standardvorgehensweise zum verbinden einer Datenbank

def close_db_con(e=None):
    db_con = g.pop('db_con', None)
    if db_con is not None:
        db_con.close()

@click.command('init-db')
def init_db():
    try:
        os.makedirs(current_app.instance_path) #verweist auf instances ordner
    except OSError:
        pass
    db_con = get_db_con()
    with current_app.open_resource('sql/create_table.sql') as f:
        db_con.executescript(f.read().decode('utf-8'))
    click.echo('Initialized the Database.')