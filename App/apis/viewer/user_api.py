from flask import request
from flask_restful import Resource, abort, reqparse, fields, marshal

from App.ext import cache
from App.models.viewer.user_model import ViewerUser
from App.utils.token_utils import generate_viewer_token
from App.utils.verify_code_utils import send_code

parse = reqparse.RequestParser()
parse.add_argument("v_phone", required=True, help="请提供手机号")
parse.add_argument("v_password", required=True, help="请输入密码")
parse.add_argument("v_code", required=True, help="请输入验证码")

viewer_user_fields = {
    "v_phone": fields.String
}

single_user_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(viewer_user_fields)
}


def parse_args():
    args = parse.parse_args()
    v_name = args.get("v_phone")
    v_password = args.get("v_password")
    v_code = args.get("v_code")
    return v_name, v_password, v_code


class ViewerUsersResource(Resource):

    def get(self):

        return {"msg": "ok"}

    def post(self):

        action = request.args.get("action")

        if action == "register":
            v_phone, v_password, v_code = parse_args()

            verify_code = cache.get(v_phone)

            if verify_code != v_code:
                abort(400, msg="验证码错误")

            viewer_user = ViewerUser()
            viewer_user.v_phone = v_phone
            viewer_user.v_password = v_password

            if not viewer_user.save():
                abort(400, msg="注册失败")
            data = {
                "msg": "ok",
                "status": 201,
                "data": viewer_user
            }

            return marshal(data, single_user_fields)

        elif action == "login":
            v_phone = request.form.get("v_phone")
            v_password = request.form.get("v_password")
            v_code = request.form.get("v_code")

            users = ViewerUser.query.filter(ViewerUser.v_phone.__eq__(v_phone)).all()

            if not users:
                data = {
                    "msg": "user doesn't exist",
                    "status": 610,
                }
                return data

            user = users[0]

            if v_code:

                verify_code = cache.get(v_phone)

                if str(verify_code) != str(v_code):
                   abort(400, msg="验证码错误")
            elif not user.check_password(v_password):
                abort(401, msg="密码错误")

            token = generate_viewer_token()

            cache.set(token, user.id, timeout=60 * 60 * 7 * 24)

            data = {
                "msg": "ok",
                "status": 200,
                "token": token
            }

            return data

        elif action == "verifycode":

            phone = request.form.get("v_phone")

            result = send_code(phone)

            if result.get("code") == 200:
                verify_code = result.get("obj")
                cache.set(phone, verify_code, timeout=60*10)

                data = {
                    "msg": "发送成功",
                    "status": 200
                }

                return data
            data = {
                "msg": "发送失败",
                "status": 600
            }

            return data

        else:
            abort(400, msg="请提供正确的动作")
