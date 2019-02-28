from flask import request, g
from flask_restful import abort

from App.ext import cache
from App.models.cinema.user_model import CinemaUser
from App.utils.token_utils import ADMIN, CINEMA


def login_required(fun):

    def wrapper(*args, **kwargs):

        token = request.args.get("token")

        if not token:
            abort(400, msg="请提供token")

        if not token.startswith(CINEMA):
            abort(400, msg="请提供有效token")

        user_id = cache.get(token)

        if not user_id:
            abort(400, msg="token 失效")

        user = CinemaUser.query.get(user_id)

        if not user:
            abort(400, msg="用户不存在")

        g.user = user

        return fun(*args, **kwargs)

    return wrapper

