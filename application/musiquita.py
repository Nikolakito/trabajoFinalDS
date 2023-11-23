from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('tracks', __name__, url_prefix='/tracks')
bpapi = Blueprint('api_tracks', __name__, url_prefix="/api/tracks")


@bp.route('/')
def index():
    db = get_db()
    db.execute(
        """SELECT t.TrackId AS id, t.Name AS nombre
         FROM tracks t ORDER BY t.Name DESC """
    )
    cancion=db.fetchall()
    return render_template('tracks/index.html', cancion=cancion)

@bp.route('/detallito/<int:id>/', methods=('GET', 'POST'))
def get_track(id):
    db = get_db()
    db.execute(
        """SELECT t.Name AS nombre FROM tracks t 
         WHERE t.TrackId = %s""",
        (id,)
    )
    print(db.query)
    print(db.rowcount)
    print(db.rownumber)
    trackn = db.fetchone()
    print(trackn)
    print(id)
    print(type(id))
    db.close()
    db = get_db()
    db.execute
    (
        """SELECT g.Name AS genero, Composer, Milliseconds,
         Bytes, UnitPrice
         FROM tracks t 
         JOIN genres g ON t.GenreId=g.GenreId
         WHERE t.TrackId = %s""",
        (id,)
    )

    print(db.query)
    print(db.rowcount)
    print(db.rownumber)
    tracki = db.fetchone()
    print(tracki)

    if tracki is None:
        abort(404, f"track id {id} doesn't exist.")

    

    return render_template('tracks/detallito.html', trackn=trackn, tracki=tracki)

#-----------------------------------------------------------json-----------------------------------------------------------------------

@bpapi.route('')
def index_api():
    db = get_db()
    db.execute(
        """SELECT t.TrackId AS id, t.Name AS nombre
         FROM tracks t ORDER BY t.Name DESC """
    )
    cancion=db.fetchall()
    return jsonify(cancion=cancion)


@bpapi.route('/<int:id>/', methods=('GET', 'POST'))
def get_track_api(id):
    db = get_db()
    db.execute(
        """SELECT t.Name AS nombre FROM tracks t 
         WHERE t.TrackId = %s""",
        (id,)
    )
    trackn=db.fetchall()

    db=get_db()
    db.execute(
        """SELECT g.Name AS genero, Composer, Milliseconds,
         Bytes, UnitPrice
         FROM tracks t 
         JOIN genres g ON t.GenreId=g.GenreId
         WHERE t.TrackId = %s""",
        (id,)
    )
    tracki = db.fetchall()

    if tracki is None:
        abort(404, f"Post id {id} doesn't exist.")
    return jsonify(tracki=tracki, trackn=trackn)