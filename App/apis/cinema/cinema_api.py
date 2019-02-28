from flask import g, request
from flask_restful import Resource, fields, marshal, reqparse, abort

from App.apis.admin.decorator import super_user_required
from App.apis.cinema.decorator import login_required
from App.models.cinema.cinema_model import Cinema
from App.utils.user_utils import get_admin_user, get_cinema_user
from App.apis.admin.decorator import login_required as admin_user_login_required

cinema_fields = {
    "c_name": fields.String,
    "c_address": fields.String,
    "c_phone": fields.String,
    "is_active": fields.Boolean,
    "c_city": fields.String,
    "c_user": fields.Integer
}

single_cinema_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(cinema_fields)
}

multi_cinema_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(cinema_fields))
}

parse = reqparse.RequestParser()
parse.add_argument("c_name", required=True, help="请输入影院名")
parse.add_argument("c_phone", required=True, help="请输入电话号码")
parse.add_argument("c_address", required=True, help="请输入影院地址")
parse.add_argument("c_city", required=True, help="请选择城市")


class CinemasResource(Resource):

    def get(self):
        cinemas = Cinema.query.all()

        data = {
            "msg": "ok",
            "status": 200,
            "data": cinemas
        }

        return marshal(data, multi_cinema_fields)

    @login_required
    def post(self):
        args = parse.parse_args()

        c_name = args.get("c_name")
        c_phone = args.get("c_phone")
        c_address = args.get("c_address")
        c_city = args.get("c_city")

        cinema = Cinema()
        cinema.c_name = c_name
        cinema.c_city = c_city
        cinema.c_address = c_address
        cinema.c_phone = c_phone
        cinema.c_user = g.user.id

        if not cinema.save():
            abort(400, msg="影院创建失败")

        data = {
            "msg": "create ok",
            "status": 201,
            "data": cinema
        }

        return marshal(data, single_cinema_fields)


class CinemaResource(Resource):

    def get_object(self, pk):

        cinema = Cinema.query.get(pk)

        if not cinema:
            abort(404, msg="cinema doesn't exist")

        return cinema

    def get(self, pk):

        token = request.args.get("token")

        cinema = self.get_object(pk)

        data = {
            "msg": "ok",
            "status": 200,
            "data": cinema
        }

        if get_admin_user(token):
            return marshal(data, single_cinema_fields)

        if get_cinema_user(token):
            cinema_user_fields = {
                "c_name": fields.String,
                "c_address": fields.String,
                "c_phone": fields.String,
                "c_city": fields.String,
                "c_user": fields.Integer
            }
            #
            single_cinema_user_fields = {
                "msg": fields.String,
                "status": fields.Integer,
                "data": fields.Nested(cinema_user_fields)
            }

            return marshal(data, single_cinema_user_fields)

        cinema_anno_fields = {
            "c_name": fields.String,
            "c_address": fields.String,
            "c_phone": fields.String,
            "c_city": fields.String,
        }
        #
        single_cinema_anno_fields = {
            "msg": fields.String,
            "status": fields.Integer,
            "data": fields.Nested(cinema_anno_fields)
        }

        return marshal(data, single_cinema_anno_fields)

    @super_user_required
    def delete(self, pk):

        cinema = self.get_object(pk)

        if not cinema.delete_logic():
            abort(400, msg="delete fail")
        data = {
            "msg": "ok",
            "status": 204
        }
        return data

    # 供超级管理员使用，可以修改信息，可以激活账号
    @admin_user_login_required
    def patch(self, pk):
        cinema = self.get_object(pk)

        c_name = request.form.get("c_name")
        c_address = request.form.get("c_address")
        c_phone = request.form.get("c_phone")
        is_active = bool(request.form.get("is_active"))

        cinema.c_name = c_name or cinema.c_name
        cinema.c_address = c_address or cinema.c_address
        cinema.c_phone = c_phone or cinema.c_phone
        cinema.is_active = is_active or cinema.is_active

        if not cinema.save():
            abort(400, msg="信息修改失败")

        data = {
            "msg": "ok",
            "status": 201,
            "data": cinema
        }

        return marshal(data, single_cinema_fields)

    # 供影院用户使用，可以修改基本信息
    @login_required
    def put(self, pk):

        cinema = self.get_object(pk)

        if cinema.c_user != g.user.id:
            abort(403, msg="无权操作")

        c_phone = request.form.get("c_phone")

        cinema.c_phone = c_phone or cinema.c_phone

        if not cinema.save():
            abort(400, msg="信息修改失败")

        data = {
            "msg": "ok",
            "status": 201,
            "data": cinema
        }

        return marshal(data, single_cinema_fields)