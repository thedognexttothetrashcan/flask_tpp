from App.ext import db
from App.models import BaseModel


class Movie(BaseModel):
    m_name = db.Column(db.String(128))
    m_name_en = db.Column(db.String(256))
    m_director = db.Column(db.String(64))
    m_leading_role = db.Column(db.String(256))
    m_duration = db.Column(db.Integer, default=90)
    m_country = db.Column(db.String(64))
    m_type = db.Column(db.String(64))
    m_screen_model = db.Column(db.String(32))
    m_open_day = db.Column(db.DateTime)
    m_introduce = db.Column(db.String(256))
    m_paidangs = db.relationship('PaiDang', backref="movie")