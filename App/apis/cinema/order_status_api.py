import json

from flask import request
from flask_restful import Resource

from App.ext import alipay


class OrderStatusResource(Resource):

    def get(self):
        try:
            data = request.form.to_dict()
            # sign 不能参与签名验证
            signature = data.pop("sign")

            print(json.dumps(data))
            print(signature)

            # verify
            success = alipay.verify(data, signature)
            if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
                print("trade succeed")
        except Exception as e:
            print(e)

        return {"msg": "付款成功"}

    def post(self):
        data = request.form.to_dict()
        # sign 不能参与签名验证
        signature = data.pop("sign")

        print(json.dumps(data))
        print(signature)

        # verify
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            print("trade succeed")

        return {"msg": "receive ok"}