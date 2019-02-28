from App.ext import db
from App.models import BaseModel
from App.models.cinema.user_model import CinemaUser


class Cinema(BaseModel):

    c_name = db.Column(db.String(32), unique=True)
    c_address = db.Column(db.String(128))
    c_phone = db.Column(db.String(32))
    c_city = db.Column(db.String(32))
    c_user = db.Column(db.Integer, db.ForeignKey(CinemaUser.id))
    is_active = db.Column(db.Boolean, default=False)
    halls = db.relationship('Hall', backref="cinema", lazy=True)