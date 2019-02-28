from App.ext import db
from App.models import BaseModel
from App.models.cinema.cinema_model import Cinema

HALL_TYPE_COMMON = 0
HALL_TYPE_VIP = 1


class Hall(BaseModel):

    h_number = db.Column(db.String(32))
    h_type = db.Column(db.Integer, default=HALL_TYPE_COMMON)
    h_seats = db.Column(db.String(256))
    h_cinema = db.Column(db.Integer, db.ForeignKey(Cinema.id))