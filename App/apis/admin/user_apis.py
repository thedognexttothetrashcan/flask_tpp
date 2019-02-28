import uuid

from flask import request, g
from flask_restful import Resource, fields, marshal, reqparse, abort

from App.apis.admin.decorator import super_user_required, login_required
from App.ext import cache
from App.models.admin import AdminUser
from App.settings import ADMIN_USERS
from App.utils.token_utils import generate_admin_token

user_fields = {
    "a_name": fields.String,
    "is_delete": fields.Boolean,
    "is_super": fields.Boolean
}

single_user_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(user_fields)
}

multi_user_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(user_fields))
}

parse = reqparse.RequestParser()
parse.add_argument("a_name", required=True, help="请提供用户名")
parse.add_argument("a_password", required=True, help="请提供密码")


def parse_args():
    args = parse.parse_args()
    a_name = args.get("a_name")
    a_password = args.get("a_password")
    return a_name, a_password


class AdminUsersResource(Resource):

    @super_user_required
    def get(self):

        users = AdminUser.query.all()

        data = {
            "msg": "ok",
            "status": 200,
            "data": users
        }

        return marshal(data, multi_user_fields)

    def post(self):

        action = request.args.get("action")

        if action == "register":
            a_name, a_password = parse_args()

            users = AdminUser.query.filter(AdminUser.a_name.__eq__(a_name)).all()

            if users:
                abort(400, msg="用户已存在")

            user = AdminUser()
            user.a_name = a_name
            user.a_password = a_password

            if a_name in ADMIN_USERS:
                user.is_super = True

            if not user.save():
                abort(400, msg="用户创建失败")

            data = {
                "msg": "ok",
                "status": 201,
                "data": user
            }

            return marshal(data, single_user_fields)

        elif action == "login":
            a_name, a_password = parse_args()

            users = AdminUser.query.filter(AdminUser.a_name.__eq__(a_name)).all()

            if not users:
                abort(400, msg="用户不存在")
            user = users[0]

            if not user.check_password(a_password):
                abort(400, msg="密码错误")

            token = generate_admin_token()

            cache.set(token, user.id, timeout=60*60*24*7)

            data = {
                "msg": "ok",
                "status": 200,
                "token": token
            }

            return data

        elif action == "qrcodelogin":
            token = request.args.get("token")
            cookie = request.args.get("cookie")

            if not token:
                abort(400, msg="请提供token")

            user_id = cache.get(token)

            if not user_id:
                abort(400, msg="token失效")

            user = AdminUser.query.get(user_id)

            if not user:
                abort(400, msg="用户不存在")

            cache.set(cookie, token, timeout=60)

            data = {
                "msg": "ok",
                "status": 200,
                "token": token
            }

            return data

        else:
            abort(400, msg="请提供正确动作")


class AdminUserResource(Resource):

    @login_required
    def get(self, pk):
        if g.user.is_super or g.user.id == pk:
            user = AdminUser.query.get(pk)

            if not user:
                abort(404, msg="user doesn't exist")

            data = {
                "msg": "ok",
                "status": 200,
                "data": user
            }
            return marshal(data, single_user_fields)

        else:
            abort(403, msg="error handle")

    @super_user_required
    def delete(self, pk):
        user = AdminUser.query.get(pk)

        if not user:
            abort(404, msg="user doesn't exist")

        if not user.delete_logic:
            abort(400, msg="删除失败")

        data = {
            "msg": "ok",
            "status": 204
        }

        return data

    @login_required
    def put(self, pk):
        if g.user.is_super or g.user.id == pk:
            user = AdminUser.query.get(pk)

            password = request.form.get("a_password")

            user.a_password = password

            if not user.save():
                abort(400, msg="信息修改失败")

            data = {
                "msg": "ok",
                "status": 201,
            }

            return data
        else:
            abort(403, msg="error handle")

    @login_required
    def patch(self, pk):
        if g.user.is_super or g.user.id == pk:
            user = AdminUser.query.get(pk)

            password = request.form.get("a_password")

            user.a_password = password

            if not user.save():
                abort(400, msg="信息修改失败")

            data = {
                "msg": "ok",
                "status": 201,
            }

            return data
        else:
            abort(403, msg="error handle")