from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('musiquita', __name__, url_prefix='/musiquita')



@bp.route('/')
def index():
    db = get_db()
    cancion = db.execute(
        """SELECT t.TrackId AS id, t.Name AS nombre, Title AS album, ar.Name AS artista 
         FROM tracks t JOIN albums a ON a.AlbumId=t.AlbumId
         JOIN artists ar ON ar.ArtistId=a.ArtistId
         ORDER BY t.Name DESC """
    ).fetchall()
    return render_template('musiquita/index.html', cancion=cancion)

def get_track(id):
    post = get_db().execute(
        """SELECT t.Name AS nombre, g.Name AS genero, Composer, Milliseconds,
         Bytes, UnitPrice
         FROM tracks t 
         JOIN genres g ON t.GenreId=g.GenreId
         WHERE t.TrackId = ?""",
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post

@bp.route('/detallito/<int:id>/', methods=('GET', 'POST'))
def det_track(id):
    post = get_track(id)
    return render_template('musiquita/detallito.html', post=post)