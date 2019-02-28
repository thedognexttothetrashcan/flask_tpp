from flask import g, request
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.cinema.decorator import login_required
from App.models.cinema.cinema_model import Cinema
from App.models.cinema.hall_model import Hall

parse = reqparse.RequestParser()
parse.add_argument("cinema_id", required=True, help="请选择电影院")
parse.add_argument("h_num", required=True, help="请输入大厅编号")
parse.add_argument("h_type", required=True, help="请选择大厅类型")
parse.add_argument("h_seats", required=True, help="请录入大厅布局")

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

multi_hall_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(hall_fields))
}


class HallsResource(Resource):

    @login_required
    def get(self):
        cinema_id = request.args.get("cinema_id")

        cinema = Cinema.query.get(cinema_id)

        halls = cinema.halls

        data = {
            "msg": "ok",
            "status": 200,
            "data": halls
        }

        return marshal(data, multi_hall_fields)

    @login_required
    def post(self):

        args = parse.parse_args()

        cinema_id = args.get("cinema_id")
        h_num = args.get("h_num")
        h_type = args.get("h_type")
        h_seats = args.get("h_seats")

        cinema = Cinema.query.get(cinema_id)

        if not cinema:
            abort(404, msg="电影院不存在")

        if cinema.c_user != g.user.id:
            abort(403, msg="管好自己的")

        hall = Hall()

        hall.h_type = h_type
        hall.h_number = h_num
        hall.h_seats = h_seats
        hall.h_cinema = cinema_id

        if not hall.save():
            abort(400, msg="放映厅创建失败")

        data = {
            "msg": "ok",
            "status": 201,
            "data": hall
        }

        return marshal(data, single_hall_fields)
