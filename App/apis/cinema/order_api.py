import random
from _datetime import datetime

from alipay import AliPay
from flask import request, g
from flask_restful import Resource, abort

from App.apis.cinema.decorator import login_required
from App.ext import alipay
from App.models.cinema.order_model import Order
from App.settings import APP_RSA_PRIVATE_KEY, ALIPAY_RSA_PUBLIC_KEY, ALIPAY_APP_ID


class OrdersResource(Resource):

    @login_required
    def post(self):

        movie_id = request.form.get("movie_id")

        order = Order()

        order.o_user = g.user.id
        order.o_movie = movie_id
        order.o_time = datetime.now()

        if not order.save():
            abort(400, msg="下单失败")

        subject = "%d核服务器你值得拥有" % random.randrange(500)

        order_string = alipay.api_alipay_trade_wap_pay(
            out_trade_no="order100%d" % order.id,
            total_amount=1,
            subject=subject,
            return_url="http://127.0.0.1:5000/cinema/orderstatus/",
            notify_url="http://127.0.0.1:5000/cinema/orderstatus/"  # 可选, 不填则使用默认notify url
        )

        data = {
            "msg": "ok",
            "status": 201,
            "pay_url": "https://openapi.alipaydev.com/gateway.do?" + order_string
        }

        return data

