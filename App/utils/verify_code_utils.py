import hashlib
import uuid

import requests
import time


def send_code(phone):
    url = "https://api.netease.im/sms/sendcode.action"

    app_key = "d2c6ee2d4213ef35362ba38038615c85"

    app_secret = "3947490de917"

    nonce = uuid.uuid4().hex

    curTime = str(int(time.time()))

    mix_str = app_secret + nonce + curTime

    checkSum = hashlib.new("sha1", mix_str.encode("utf-8")).hexdigest()

    data = {
        "mobile": phone
    }

    header = {
        "AppKey": app_key,
        "Nonce": nonce,
        "CurTime": curTime,
        "CheckSum": checkSum
    }

    resp = requests.post(url, data, headers=header)

    return resp.json()