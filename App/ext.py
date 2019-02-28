from alipay import AliPay
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from App.settings import ALIPAY_APP_ID, APP_RSA_PRIVATE_KEY, ALIPAY_RSA_PUBLIC_KEY

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={
    "CACHE_TYPE": "redis"
})

alipay = AliPay(
            appid=ALIPAY_APP_ID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=APP_RSA_PRIVATE_KEY,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=ALIPAY_RSA_PUBLIC_KEY,
            sign_type="RSA", # RSA 或者 RSA2
            debug = True  # 默认False
        )


def init_ext(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    cache.init_app(app=app)