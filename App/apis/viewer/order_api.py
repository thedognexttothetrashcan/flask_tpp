
from datetime import timedelta, datetime

from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.viewer.decorator import login_required
from App.apis.viewer.seat_utils import get_avaliable_seats
from App.models.cinema.paidang_model import PaiDang
from App.models.viewer.seat_order_model import SeatOrder

parse = reqparse.RequestParser()
parse.add_argument("paidang_id", required=True, help="请提供排挡")
parse.add_argument("seats", required=True, help="请选择座位")

seat_order_fields = {
    "s_user": fields.Integer,
    "s_price": fields.Float,
    "s_seats": fields.String,
    "s_expire": fields.DateTime,
    "s_status": fields.Integer,
    "s_paidang": fields.Integer
}

single_seat_order_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(seat_order_fields)
}


class SeatOrdersResource(Resource):

    @login_required
    def post(self):
        now = datetime.now()
        expire = now + timedelta(minutes=15)

        args = parse.parse_args()

        paidang_id = args.get("paidang_id")
        seats = args.get("seats")

        seat_list = seats.split("#")

        paidang = PaiDang.query.get(paidang_id)

        price = paidang.p_price * len(seat_list)

        avaliable = get_avaliable_seats(paidang_id)

        if not avaliable.issuperset(set(seat_list)):
            abort(400, msg="锁单失败")

        seat_order = SeatOrder()

        seat_order.s_expire = expire
        seat_order.s_paidang = paidang_id
        seat_order.s_price = price
        seat_order.s_user = g.user.id
        seat_order.s_seats = seats

        if not seat_order.save():
            abort(400, msg="下单失败")

        # 验证座位状态
        seat_order_list = SeatOrder.query.fliter(SeatOrder.s_paidang.__eq__(paidang_id)).filter(SeatOrder.s_expire.__ge__(expire)).all()

        for seat_order_obj in seat_order_list:
            if seat_order.id != seat_order_obj.id:
                sold = set(seat_order_obj.s_seats.split("#"))
                want = set(seat_list)
                if sold & want:
                    if seat_order_obj.id < seat_order.id:
                        seat_order.delete()
                        abort(400, msg="锁单失败")

        data ={
            "msg": "ok",
            "status": 201,
            "data": seat_order
        }

        return marshal(data, single_seat_order_fields)