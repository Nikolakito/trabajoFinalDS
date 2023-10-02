from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from application.auth import login_required
from application.db import get_db

bp = Blueprint('musiquita', __name__)

@bp.route('/')
def index():
    db = get_db()
    cancion = db.execute(
        """SELECT t.Name AS nombre, Title AS album, ar.Name AS artista 
         FROM tracks t JOIN albums a ON a.AlbumId=t.AlbumId
         JOIN artists ar ON ar.ArtistId=a.ArtistId
         ORDER BY t.Name DESC """
    ).fetchall()
    return render_template('musiquita/index.html', cancion=cancion)
