import click
from flask import current_app, g
from flask.cli import with_appcontext
import sqlite3
from scraper import Scraper
import random as r

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def fill_db(db):
    sc = Scraper()
    vocab_list = sc.iterate_endpoints()
    with current_app.open_resource('schema.sql') as f:
        for dictionary in vocab_list:
            try:
                params = [dictionary['JLPTlevel'], dictionary['furigana'], dictionary['kanji'], dictionary['pos'], dictionary['definition'], dictionary['usefulness']]
                query = "INSERT INTO JLPTVocab (level, furigana, kanji, pos, definition, usefulness) VALUES (?,?,?,?,?,?)"
                db.execute(query, params)
                db.commit()
            except Exception as e:
                print("{JLPTlevel}, {furigana}, {kanji}, {pos}, {definition}, {usefulness}".format(**dictionary))
                print(e)

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        fill_db(db)

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def db_size():
    cursor = get_db().cursor()
    res = cursor.execute('SELECT COUNT(*) AS size FROM JLPTVocab')
    return res.fetchone()['size']

def get_random_word():
    db = get_db()
    cursor = db.cursor()
    index = r.randint(1, db_size()+1)

    row = cursor.execute('SELECT * FROM JLPTVocab WHERE id IS {}'.format(index)).fetchone()
    res = {}
    for key in row.keys():
        res[key] = row[key]
    return res
