from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('artist', __name__, url_prefix='/artist')

@bp.route('/index')
def index():
    db = get_db()
    artistas = db.execute(
        """SELECT ar.ArtistId AS id, ar.Name AS artista 
         FROM artists ar 
         ORDER BY ar.Name DESC """
    ).fetchall()
    return render_template('artists/index.html', artistas=artistas)

def get_artist(id):
    post = get_db().execute(
        """SELECT Title AS album, ar.Name AS artista 
         FROM artists ar JOIN albums a ON a.ArtistId=ar.ArtistId
         WHERE t.ArtistId = ?""",
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post
@bp.route('/detallito/<int:id>/', methods=('GET', 'POST'))
def det_artist(id):
    post = get_artist(id)
    return render_template('artists/detallito.html', post=post)