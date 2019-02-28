from App.ext import db
from App.models import BaseModel
from App.models.cinema.hall_model import Hall
from App.models.common.movie_model import Movie


class PaiDang(BaseModel):
    p_movie = db.Column(db.Integer, db.ForeignKey(Movie.id))
    p_hall = db.Column(db.Integer, db.ForeignKey(Hall.id))
    p_time_start = db.Column(db.DateTime)
    p_time_end = db.Column(db.DateTime)
    p_price = db.Column(db.Float, default=1)
    seatorders = db.relationship('SeatOrder', backref="paidang", lazy=True)