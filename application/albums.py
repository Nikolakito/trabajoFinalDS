from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('albums', __name__, url_prefix='/album')

@bp.route('/')
def index():
    db = get_db()
    albums = db.execute(
        """SELECT AlbumId AS id, Title AS album 
         FROM albums
         ORDER BY Title DESC """
    ).fetchall()
    return render_template('albums/index.html', albums=albums)
@bp.route('/<int:id>/', methods=('GET', 'POST'))
def get_album(id):
    db = get_db()
    album = db.execute(
    """SELECT AlbumId AS id, Title AS album 
         FROM albums
          """
    ).fetchall()
    tracksi = get_db().execute(
        """SELECT t.Name AS nombre, g.Name AS genero, Composer, Milliseconds,
         Bytes, UnitPrice
         FROM tracks t 
         JOIN genres g ON t.GenreId=g.GenreId
         JOIN albums a ON t.AlbumId=a.AlbumId
         WHERE t.AlbumId = ?
         """,
        (id,)
    ).fetchall()

    if album is None:
        abort(404, f"Album id {id} doesn't exist.")

    return render_template('albums/detallito.html', album=album, tracksi=tracksi)