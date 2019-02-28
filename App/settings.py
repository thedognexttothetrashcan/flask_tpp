import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMIN_USERS = ("root", "admin")

ALIPAY_APP_ID = "2016091800537304"
ALIPAY_RSA_PUBLIC_KEY = open(os.path.join(BASE_DIR, "alipay/alipay_rsa_public_key.pem")).read()
APP_RSA_PRIVATE_KEY = open(os.path.join(BASE_DIR, "alipay/app_rsa_private_key.pem")).read()


def get_db_uri(dbinfo):

    backend = dbinfo.get("backend")
    driver = dbinfo.get("driver")
    user = dbinfo.get("user")
    password = dbinfo.get("password")
    host = dbinfo.get("host")
    port = dbinfo.get("port")
    name = dbinfo.get("name")

    return "{}+{}://{}:{}@{}:{}/{}".format(backend, driver, user, password, host, port, name)


class Config:

    DEBUG = False

    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRECT_KEY = "rock"


class DevelopConfig(Config):

    DEBUG = True

    dbinfo = {
        "backend": "mysql",
        "driver": "pymysql",
        "user": "root",
        "password": "rock1204",
        "host": "localhost",
        "port": "3306",
        "name": "FlaskTPP1809"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestingConfig(Config):

    TESTING = True

    dbinfo = {
        "backend": "mysql",
        "driver": "pymysql",
        "user": "root",
        "password": "rock1204",
        "host": "localhost",
        "port": "3306",
        "name": "FlaskTPP1809"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):

    dbinfo = {
        "backend": "mysql",
        "driver": "pymysql",
        "user": "root",
        "password": "rock1204",
        "host": "localhost",
        "port": "3306",
        "name": "FlaskTPP1809"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):

    DEBUG = True

    dbinfo = {
        "backend": "mysql",
        "driver": "pymysql",
        "user": "root",
        "password": "rock1204",
        "host": "localhost",
        "port": "3306",
        "name": "FlaskTPP1809"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}
