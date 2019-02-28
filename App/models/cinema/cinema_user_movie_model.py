from App.ext import db
from App.models import BaseModel
from App.models.cinema.user_model import CinemaUser
from App.models.common.movie_model import Movie


class CinemaUserMovie(BaseModel):
    c_cinema_user = db.Column(db.Integer, db.ForeignKey(CinemaUser.id))
    c_movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))