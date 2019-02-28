from App.ext import db
from App.models import BaseModel
from App.models.cinema.paidang_model import PaiDang
from App.models.viewer.user_model import ViewerUser

SEAT_ORDER_STATUS_NOT_PAY = 0
SEAT_ORDER_STATUS_PAYED = 1


class SeatOrder(BaseModel):

    s_user = db.Column(db.Integer, db.ForeignKey(ViewerUser.id))
    s_paidang = db.Column(db.Integer, db.ForeignKey(PaiDang.id))
    s_price = db.Column(db.Float, default=1)
    s_seats = db.Column(db.String(128))
    s_status = db.Column(db.Integer, default=SEAT_ORDER_STATUS_NOT_PAY)
    s_expire = db.Column(db.DateTime)