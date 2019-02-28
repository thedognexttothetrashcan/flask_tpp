import uuid

from flask import request
from flask_restful import Resource, abort, reqparse, fields, marshal

from App.apis.admin.decorator import login_required as admin_login_required
from App.ext import cache
from App.models.cinema.user_model import CinemaUser
from App.utils.token_utils import generate_cinema_token

parse = reqparse.RequestParser()
parse.add_argument("c_name", required=True, help="请提供用户名")
parse.add_argument("c_password", required=True, help="请输入密码")

cinema_user_fields = {
    "c_name": fields.String
}

single_user_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(cinema_user_fields)
}


def parse_args():
    args = parse.parse_args()
    c_name = args.get("c_name")
    c_password = args.get("c_password")

    return c_name, c_password


class CinemaUsersResource(Resource):

    @admin_login_required
    def get(self):

        return {"msg": "ok"}

    def post(self):

        action = request.args.get("action")

        if action == "register":
            c_name, c_password = parse_args()

            cinema_user = CinemaUser()
            cinema_user.c_name = c_name
            cinema_user.c_password = c_password

            if not cinema_user.save():
                abort(400, msg="注册失败")
            data = {
                "msg": "ok",
                "status": 201,
                "data": cinema_user
            }

            return marshal(data, single_user_fields)

        elif action == "login":
            c_name, c_password = parse_args()

            users = CinemaUser.query.filter(CinemaUser.c_name.__eq__(c_name)).all()

            if not users:
                abort(404, msg="用户不存在")

            user = users[0]

            if not user.check_password(c_password):
                abort(400, msg="密码错误")

            if user.is_delete:
                abort(400, msg="账号已封停")

            token = generate_cinema_token()

            cache.set(token, user.id, timeout=60*60*7*24)

            data = {
                "msg": "ok",
                "status": 200,
                "token": token
            }

            return data

        else:
            abort(400, msg="请提供正确的动作")
