from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('albums', __name__, url_prefix='/albums')

@bp.route('/index')
def index():
    db = get_db()
    albums = db.execute(
        """SELECT AlbumId AS id, Title AS album 
         FROM albums
         ORDER BY Title DESC """
    ).fetchall()
    return render_template('albums/index.html', albums=albums)

def get_album(id):
    post = get_db().execute(
        """SELECT *
         FROM (SELECT t.Name AS nombre, g.Name AS genero, Composer, Milliseconds,
         Bytes, UnitPrice
         FROM tracks t 
         JOIN genres g ON t.GenreId=g.GenreId
         WHERE AlbumId = ?) 
         """,
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post
@bp.route('/detallito/<int:id>/', methods=('GET', 'POST'))
def det_album(id):
    post = get_album(id)
    return render_template('albums/detallito.html', post=post)