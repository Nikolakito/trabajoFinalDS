from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('artist', __name__, url_prefix='/artist')

@bp.route('/')
def index():
    db = get_db()
    artistas = db.execute(
        """SELECT ar.ArtistId AS id, ar.Name AS artista 
         FROM artists ar 
         ORDER BY ar.Name DESC """
    ).fetchall()
    return render_template('artists/index.html', artistas=artistas)


@bp.route('/<int:id>/', methods=('GET', 'POST'))
def get_artist(id):
    artist = get_db().execute(
        """SELECT ar.Name AS artista 
         FROM artists ar
         WHERE ar.ArtistId = ?""",
        (id,)
    ).fetchall()

    if artist is None:
        abort(404, f"Artist id {id} doesn't exist.")

    albums = get_db().execute(
        """SELECT a.Title AS disco FROM albums a
         WHERE a.ArtistId = ?""",
        (id,)
    ).fetchall()

    return render_template('artists/detallito.html', artist=artist, albums=albums)