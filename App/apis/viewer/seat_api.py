import datetime
import time
from flask_restful import Resource, abort, fields, marshal
from sqlalchemy import or_, and_

from App.apis.viewer.decorator import login_required
from App.apis.viewer.seat_utils import get_avaliable_seats
from App.models.cinema.hall_model import Hall
from App.models.cinema.paidang_model import PaiDang
from App.models.viewer.seat_order_model import SeatOrder, SEAT_ORDER_STATUS_PAYED, SEAT_ORDER_STATUS_NOT_PAY

hall_fields = {
    "h_number": fields.String,
    "h_type": fields.Integer,
    "h_seats": fields.String,
    "h_cinema": fields.Integer
}

single_hall_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(hall_fields)
}


class SeatResource(Resource):

    @login_required
    def get(self, pk):
        """
            pk  排挡的id
        """
        paidang = PaiDang.query.get(pk)

        if not paidang:
            abort(400, msg="排挡不存在")

        if paidang.p_time_start < datetime.datetime.now():
            abort(400, msg="排挡已过期")

        hall_id = paidang.p_hall

        hall = Hall.query.get(hall_id)
        #
        # seatorders = SeatOrder.query.filter(SeatOrder.s_paidang.__eq__(pk))\
        #     .filter(or_(SeatOrder.s_status.__eq__(SEAT_ORDER_STATUS_PAYED)
        #                 , and_(SeatOrder.s_status.__eq__(SEAT_ORDER_STATUS_NOT_PAY), SeatOrder.s_expire.__ge__(datetime.datetime.now()))))
        #
        # sold_seats = set()
        #
        # for seatorder in seatorders:
        #     seat_list = seatorder.s_seats.split("#")
        #     print("seat_list", seat_list)
        #     sold_seats |= set(seat_list)
        #
        # all_seats = set(hall.h_seats.split("#"))
        #
        # print(sold_seats)
        #
        # print(all_seats)
        #
        # avaliable_seats = all_seats - sold_seats
        #
        # print(avaliable_seats)

        avaliable_seats = get_avaliable_seats(pk)

        avaliable = "#".join(list(avaliable_seats))
        hall.h_seats = avaliable

        data = {
            "msg": "ok",
            "status": 200,
            "data": hall
        }

        return marshal(data, single_hall_fields)