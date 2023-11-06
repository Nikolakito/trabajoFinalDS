from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('tracks', __name__, url_prefix='/tracks')



@bp.route('/')
def index():
    db = get_db()
    cancion = db.execute(
        """SELECT t.TrackId AS id, t.Name AS nombre
         FROM tracks t ORDER BY t.Name DESC """
    ).fetchall()
    return render_template('tracks/index.html', cancion=cancion)

@bp.route('/detallito/<int:id>/', methods=('GET', 'POST'))
def get_track(id):
    trackn = get_db().execute(
        """SELECT t.Name AS nombre FROM tracks t 
         WHERE t.TrackId = ?""",
        (id,)
    ).fetchall()

    tracki = get_db().execute(
        """SELECT g.Name AS genero, Composer, Milliseconds,
         Bytes, UnitPrice
         FROM tracks t 
         JOIN genres g ON t.GenreId=g.GenreId
         WHERE t.TrackId = ?""",
        (id,)
    ).fetchall()

    if tracki is None:
        abort(404, f"Post id {id} doesn't exist.")

    

    return render_template('tracks/detallito.html', trackn=trackn, tracki=tracki)