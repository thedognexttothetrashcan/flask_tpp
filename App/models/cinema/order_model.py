from App.ext import db
from App.models import BaseModel
from App.models.cinema.user_model import CinemaUser
from App.models.common.movie_model import Movie

ORDER_STATUS_NOT_PAY = 0
ORDER_STATUS_PAYED = 1


class Order(BaseModel):
    o_user = db.Column(db.Integer, db.ForeignKey(CinemaUser.id))
    o_status = db.Column(db.Integer, default=0)
    o_time = db.Column(db.DateTime)
    o_movie = db.Column(db.Integer, db.ForeignKey(Movie.id))