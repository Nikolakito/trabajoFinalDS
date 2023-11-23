from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('artist', __name__, url_prefix='/artist')
bpapi = Blueprint('api_artist', __name__, url_prefix="/api/artist")

@bp.route('/')
def index():
    db = get_db()
    db.execute(
        """SELECT ar.ArtistId AS id, ar.Name AS artista 
         FROM artists ar 
         ORDER BY ar.Name DESC """
    )
    artistas = db.fetchall()
    return render_template('artists/index.html', artistas=artistas)


@bp.route('/<int:id>/', methods=('GET', 'POST'))
def get_artist(id):
    db = get_db
    db.execute(
        """SELECT ar.Name AS artista 
         FROM artists ar
         WHERE ar.ArtistId = %s""",
        (id,)
    )
    artist = db.fetchone()
    db = get_db
    db.execute(
        """SELECT a.Title AS disco FROM albums a
         WHERE a.ArtistId = %s""",
        (id,)
    )
    albums = db.fetchall()

    if artist is None:
        abort(404, f"Artist id {id} doesn't exist.")

    return render_template('artists/detallito.html', artist=artist, albums=albums)
#-----------------------------------------------------------json-----------------------------------------------------------------------

@bpapi.route('/')
def index():
    db = get_db()
    db.execute(
        """SELECT ar.ArtistId AS id, ar.Name AS artista 
         FROM artists ar 
         ORDER BY ar.Name DESC """
    )
    artistas = db.fetchall()
    return jsonify(artistas=artistas)


@bpapi.route('/<int:id>/', methods=('GET', 'POST'))
def get_artist(id):
    db=get_db()
    db.execute(
        """SELECT ar.Name AS artista 
         FROM artists ar
         WHERE ar.ArtistId = %s""",
        (id,)
    )
    artist = db.fetchall()

    if artist is None:
        abort(404, f"Artist id {id} doesn't exist.")

    db.execute(
        """SELECT a.Title AS disco FROM albums a
         WHERE a.ArtistId = %s""",
        (id,)
    )
    albums = db.fetchall()
    return jsonify(albums=albums, artist=artist)